"""
Global paper connections management.

All topics share a single global connections file (docs/papers/_global_connections.json).
Topic-specific _paper_connections.json files are derived from global by filtering.

This ensures cross-topic connections are preserved regardless of execution order.

The global file stores the *raw, directional* edges exactly as generated (one
``source_topic``-tagged entry per A→B). The per-topic ``_paper_connections.json``
files — which every renderer consumes — are derived as a **bidirectional,
per-target-deduped** view: each A→B edge implies B→A (relation flipped), and a
paper connected for several reasons appears once with all reasons listed. See
:func:`make_bidirectional_deduped`.
"""

import json
import os
from collections import OrderedDict

PAPERS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "docs", "papers")
GLOBAL_CONN_PATH = os.path.join(PAPERS_DIR, "_global_connections.json")

# When we synthesize the reverse edge B→A from a stored edge A→B, the relation
# must be re-expressed from B's point of view. The stored relation describes how
# the *target* relates to the *source* (A→B "foundation" means "B is a
# foundation for A"). Flipping the direction therefore flips the relation:
#   A→B foundation  ⇒  B→A extension   (A builds on / extends B)
#   A→B extension   ⇒  B→A foundation  (B is the basis A extends)
#   A→B application ⇒  B→A foundation  (B is the method A applies)
#   alternative / counterpoint are mutual ⇒ unchanged.
REVERSE_RELATION = {
    "foundation": "extension",
    "extension": "foundation",
    "application": "foundation",
    "alternative": "alternative",
    "counterpoint": "counterpoint",
}

# Canonical display/sort priority for relations (also used to pick the "primary"
# relation when one paper is connected for several reasons).
REL_ORDER = {"foundation": 0, "alternative": 1, "extension": 2,
             "application": 3, "counterpoint": 4}


def _entry_reasons(entry):
    """Normalize a connection entry to a list of (relation, reason) pairs.

    Accepts both the new multi-reason schema (``reasons: [{relation, reason}]``)
    and the legacy single ``relation``/``reason`` fields.
    """
    rs = entry.get("reasons")
    if isinstance(rs, list) and rs:
        return [((r.get("relation") or "alternative"), r.get("reason", ""))
                for r in rs]
    return [((entry.get("relation") or "alternative"), entry.get("reason", ""))]


def make_bidirectional_deduped(conns_by_slug):
    """Return a bidirectional, per-target-deduped connections dict.

    For every directed edge A→B we also synthesize the reverse edge B→A (relation
    flipped via :data:`REVERSE_RELATION`). For each ordered pair we keep **one
    reason per relation** — so a paper connected several times under the *same*
    relation (e.g. a forward "foundation" edge plus a reverse "application" edge
    that flips back to "foundation") shows a single "기반 연구" line, while genuinely
    distinct relations (foundation + alternative) each get their own. Forward
    reasons (written from this paper's own perspective) win over reverse-derived
    ones. The top-level ``relation``/``reason`` mirror the highest-priority reason
    for consumers that read a single relation.
    """
    # buckets[src][tgt] = {relation: (reason, is_forward)} — one reason / relation
    buckets = {}

    def _add(src, tgt, rel, reason, is_forward):
        if not src or not tgt or src == tgt:
            return
        relmap = buckets.setdefault(src, OrderedDict()).setdefault(tgt, OrderedDict())
        cur = relmap.get(rel)
        # Keep one reason per relation: prefer a forward reason; otherwise keep
        # the first one seen (stable).
        if cur is None or (is_forward and not cur[1]):
            relmap[rel] = (reason, is_forward)

    for src, conns in conns_by_slug.items():
        for entry in conns or []:
            tgt = entry.get("slug")
            for rel, reason in _entry_reasons(entry):
                _add(src, tgt, rel, reason, True)
                _add(tgt, src, REVERSE_RELATION.get(rel, rel), reason, False)

    result = {}
    for src, tgts in buckets.items():
        items = []
        for tgt, relmap in tgts.items():
            reasons = [{"relation": rel, "reason": rr[0]}
                       for rel, rr in relmap.items()]
            reasons.sort(key=lambda r: REL_ORDER.get(r["relation"], 9))
            primary = reasons[0]
            items.append({
                "slug": tgt,
                "relation": primary["relation"],
                "reason": primary["reason"],
                "reasons": reasons,
            })
        items.sort(key=lambda c: (REL_ORDER.get(c["relation"], 9), c["slug"]))
        result[src] = items
    return result


def load_global_connections():
    """Load global connections file. Returns empty dict if not found."""
    if os.path.exists(GLOBAL_CONN_PATH):
        with open(GLOBAL_CONN_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_global_connections(connections):
    """Save global connections file."""
    with open(GLOBAL_CONN_PATH, "w", encoding="utf-8") as f:
        json.dump(connections, f, ensure_ascii=False, indent=2)


def merge_to_global(new_connections, source_topic=None):
    """Merge new connections into global file. Returns merged global connections.

    For each slug, new connections are added alongside existing ones (dedup by target slug).
    If source_topic is given, existing connections from the SAME topic are replaced
    (prevents stale entries from prior runs of the same topic).
    """
    global_conns = load_global_connections()

    if source_topic:
        # Remove prior connections from this topic for slugs being updated
        for slug in new_connections:
            if slug in global_conns:
                global_conns[slug] = [
                    c for c in global_conns[slug]
                    if c.get("source_topic") != source_topic
                ]

    # Merge new connections
    for slug, conns in new_connections.items():
        existing = global_conns.get(slug, [])
        seen_targets = {c["slug"] for c in existing}
        for c in conns:
            if c["slug"] not in seen_targets:
                entry = dict(c)
                if source_topic:
                    entry["source_topic"] = source_topic
                existing.append(entry)
                seen_targets.add(c["slug"])
        global_conns[slug] = existing

    save_global_connections(global_conns)
    return global_conns


def filter_for_topic(global_conns, topic_slugs):
    """Filter global connections to those where source is in topic_slugs.

    Returns connections dict suitable for topic's _paper_connections.json.
    Connections to targets outside the topic are kept (generate_network filters them).
    """
    topic_set = set(topic_slugs)
    filtered = {}
    for slug, conns in global_conns.items():
        if slug in topic_set:
            # Strip source_topic from output (internal field)
            filtered[slug] = [
                {k: v for k, v in c.items() if k != "source_topic"}
                for c in conns
            ]
    return filtered


def sync_topic_connections(new_connections, topic, topic_slugs, topic_dir, log=print):
    """Full workflow: merge to global → filter for topic → save topic file.

    Args:
        new_connections: newly computed connections dict {slug: [{slug, relation, reason}]}
        topic: topic name (e.g. "ai4s", "scisci")
        topic_slugs: list of slugs belonging to this topic
        topic_dir: path to topic directory (e.g. docs/ai4s/)
        log: logging function
    """
    # Merge into global (raw directional store)
    global_conns = merge_to_global(new_connections, source_topic=topic)
    global_total = sum(len(v) for v in global_conns.values())
    log(f"  Global connections: {len(global_conns)} papers, {global_total} total links")

    # Derive the bidirectional + per-target-deduped view, then filter for topic.
    bidi_conns = make_bidirectional_deduped(global_conns)
    topic_conns = filter_for_topic(bidi_conns, topic_slugs)
    topic_total = sum(len(v) for v in topic_conns.values())

    # Save topic file
    conn_path = os.path.join(topic_dir, "_paper_connections.json")
    with open(conn_path, "w", encoding="utf-8") as f:
        json.dump(topic_conns, f, ensure_ascii=False, indent=2)
    log(f"  Topic connections: {len(topic_conns)} papers, {topic_total} links → {conn_path}")

    return topic_conns
