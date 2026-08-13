"""
D3.js force-directed network visualization.

_paper_connections.json + _papers_index.json → network.html
- Category colors, score-based node size, hover (essence), click (review link)
- Category toggle, relation type filter, search, ego network

Usage:
  PYTHONUTF8=1 python pipeline/generate_network.py --topic my-topic
  PYTHONUTF8=1 python pipeline/generate_network.py --topic my-topic
"""

import argparse
import json
import os
from collections import defaultdict
from datetime import datetime

from config_loader import PAPERS_DIR as _PAPERS_DIR, get_topic_dir
from paper_curation.rendering.network.template import render_network_template
from paper_curation.rendering.network.view_model import build_network_view_model

PAPERS_DIR = str(_PAPERS_DIR)

RELATION_COLORS = {
    "alternative": "#3B82F6",
    "extension": "#10B981",
    "foundation": "#8B5CF6",
    "counterpoint": "#F59E0B",
    "application": "#EF4444",
}


def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def build_network_data(topic):
    with open(os.path.join(PAPERS_DIR, "_papers_index.json"), "r", encoding="utf-8") as f:
        all_papers = json.load(f)

    topic_dir = str(get_topic_dir(topic))
    with open(os.path.join(topic_dir, "_paper_connections.json"), "r", encoding="utf-8") as f:
        connections = json.load(f)

    # Load UMAP coordinates if available
    umap_path = os.path.join(topic_dir, "_umap_coords.json")
    umap_coords = {}
    if os.path.exists(umap_path):
        with open(umap_path, "r", encoding="utf-8") as f:
            umap_coords = json.load(f)

    topic_papers = [p for p in all_papers if topic in p.get("topics", [])]

    # Tab10 base colors + shade function for sub-categories
    TAB10 = [
        (31, 119, 180), (255, 127, 14), (44, 160, 44), (214, 39, 40),
        (148, 103, 189), (140, 86, 75), (227, 119, 194), (127, 127, 127),
        (188, 189, 34), (23, 190, 207),
    ]

    def _shade(rgb, factor):
        """Lighten (>1) or darken (<1) a color."""
        r, g, b = rgb
        if factor > 1:
            r = min(255, int(r + (255 - r) * (factor - 1)))
            g = min(255, int(g + (255 - g) * (factor - 1)))
            b = min(255, int(b + (255 - b) * (factor - 1)))
        else:
            r = int(r * factor)
            g = int(g * factor)
            b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    all_cat_names = sorted(set(
        p.get("classifications", {}).get(topic, {}).get("primary_category", "Other")
        for p in topic_papers
    ))
    SHAPES = ["circle", "square", "triangle", "diamond"]
    cat_colors = {}
    cat_shapes = {}
    for i, c in enumerate(all_cat_names):
        if c == "Other":
            cat_colors[c] = "#999999"
            cat_shapes[c] = "circle"
        else:
            base = TAB10[i % len(TAB10)]
            shade_level = 1.0 + 0.3 * (i // len(TAB10))
            cat_colors[c] = _shade(base, shade_level)
            cat_shapes[c] = SHAPES[(i // len(TAB10)) % len(SHAPES)]

    nodes = []
    slug_set = set()
    for p in topic_papers:
        slug = p["slug"]
        cls = p.get("classifications", {}).get(topic, {})
        cat = cls.get("primary_category", "Other")
        sub = cls.get("sub_category", "")
        score = p.get("score", 0) or 0
        year = str(p.get("date", ""))[:4]
        num = slug.split("_")[0] if "_" in slug else ""
        all_cats = cls.get("all_categories", [cat])
        is_multi = len(all_cats) > 1
        coord = umap_coords.get(slug, {})
        nodes.append({
            "id": slug, "num": num, "title": p.get("title", ""),
            "category": cat, "all_categories": all_cats,
            "sub_category": sub, "score": score,
            "year": year, "essence": (p.get("essence", "") or "")[:200],
            "color": cat_colors.get(cat, "#999999"),
            "shape": cat_shapes.get(cat, "circle"),
            "multi": is_multi,
            "ux": coord.get("x"), "uy": coord.get("y"),
            "ux3": coord.get("x3"), "uy3": coord.get("y3"), "uz3": coord.get("z3"),
        })
        slug_set.add(slug)

    # Connections are bidirectional (A→B and B→A both exist in the data), so we
    # collapse each unordered pair to a single undirected edge. The displayed
    # relation/reason is taken from the higher-priority direction.
    _REL_ORDER = {"foundation": 0, "alternative": 1, "extension": 2,
                  "application": 3, "counterpoint": 4}
    links = []
    _pair_idx = {}
    for slug, conns in connections.items():
        if slug not in slug_set:
            continue
        for c in conns:
            target = c.get("slug", "")
            if target not in slug_set or target == slug:
                continue
            rel = c.get("relation", "alternative")
            key = frozenset((slug, target))
            if key in _pair_idx:
                existing = links[_pair_idx[key]]
                if _REL_ORDER.get(rel, 9) < _REL_ORDER.get(existing["relation"], 9):
                    existing["relation"] = rel
                    existing["reason"] = c.get("reason", "")
                    existing["color"] = RELATION_COLORS.get(rel, "#ccc")
                continue
            _pair_idx[key] = len(links)
            links.append({
                "source": slug, "target": target,
                "relation": rel,
                "reason": c.get("reason", ""),
                "color": RELATION_COLORS.get(rel, "#ccc"),
            })

    # Per-node connection list for the info panel: grouped BY PAPER (one entry per
    # neighbour) with every relation+reason, from this node's own perspective —
    # mirrors the per-paper "같이 보면 좋은 논문" card. Edges above stay undirected
    # for drawing; this keeps the correct directional reasons for the panel.
    node_conns = {}
    for slug in slug_set:
        lst = []
        for c in connections.get(slug, []):
            t = c.get("slug", "")
            if t not in slug_set:
                continue
            reasons = c.get("reasons") or [{"relation": c.get("relation", "alternative"),
                                            "reason": c.get("reason", "")}]
            lst.append({
                "o": t,
                "r": [[rr.get("relation", "alternative"), rr.get("reason", "")]
                      for rr in reasons],
            })
        if lst:
            lst.sort(key=lambda e: _REL_ORDER.get(e["r"][0][0], 9))
            node_conns[slug] = lst

    cats = sorted(set(n["category"] for n in nodes))
    years = sorted(set(n["year"] for n in nodes if n["year"] and n["year"].isdigit() and 1900 <= int(n["year"]) <= 2100))

    # Sub-category colors: shade of parent category color
    # Build cat → sub mapping
    cat_subs = defaultdict(set)
    for n in nodes:
        cat_subs[n["category"]].add(n.get("sub_category", "General"))

    # Find parent tab10 index for each category
    cat_to_tab_idx = {}
    for i, c in enumerate(all_cat_names):
        if c != "Other":
            cat_to_tab_idx[c] = i % len(TAB10)

    sub_colors = {}
    for cat, subs in cat_subs.items():
        tab_idx = cat_to_tab_idx.get(cat, 7)  # default gray
        base = TAB10[tab_idx]
        sorted_subs = sorted(subs)
        for j, s in enumerate(sorted_subs):
            # Vary shade: 0.6 (dark) → 1.4 (light) across sub-categories
            n_subs = len(sorted_subs)
            factor = 0.6 + 0.8 * j / max(1, n_subs - 1) if n_subs > 1 else 1.0
            sub_colors[s] = _shade(base, factor)

    has3D = any(n.get("ux3") is not None for n in nodes)
    return nodes, links, cat_colors, cat_shapes, sub_colors, years, has3D, node_conns


def _escape_html(text):
    """Escape HTML special characters."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#x27;")


def _script_json(value):
    """Serialize JSON without allowing HTML parser script termination."""
    return (
        json.dumps(value, ensure_ascii=False)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def generate_html(nodes, links, cat_colors, cat_shapes, sub_colors, years, topic, has3D=False, node_conns=None):
    # The package view-model boundary is the production schema/safety gate.
    # Presentation-specific coordinates/colors remain in the source mappings.
    build_network_view_model(topic, nodes, links)
    nodes_json = _script_json(nodes)
    links_json = _script_json(links)
    node_conns_json = _script_json(node_conns or {})
    cat_colors_json = _script_json(cat_colors)

    year_min = years[0] if years else "2020"
    year_max = years[-1] if years else "2026"

    # Pre-compute category counts
    cat_counts = {}
    for n in nodes:
        cat_counts[n["category"]] = cat_counts.get(n["category"], 0) + 1
    cat_shapes_json = _script_json(cat_shapes)
    cat_counts_json = _script_json(cat_counts)
    sub_colors_json = _script_json(sub_colors)
    sub_counts = {}
    for n in nodes:
        sc = n.get("sub_category", "")
        if sc:
            sub_counts[sc] = sub_counts.get(sc, 0) + 1
    sub_counts_json = _script_json(sub_counts)
    # cat → subs hierarchy
    cat_subs_map = defaultdict(list)
    for n in nodes:
        sc = n.get("sub_category", "General")
        if sc not in cat_subs_map[n["category"]]:
            cat_subs_map[n["category"]].append(sc)
    for k in cat_subs_map:
        cat_subs_map[k].sort()
    cat_subs_json = _script_json(dict(cat_subs_map))

    escaped_topic = _escape_html(topic)
    return render_network_template({
        "TITLE_TOPIC": escaped_topic,
        "HEADING_TOPIC": escaped_topic,
        "YEAR_MIN_RANGE_MIN": str(year_min),
        "YEAR_MAX_RANGE_MIN": str(year_max),
        "YEAR_MIN_RANGE_VALUE": str(year_min),
        "YEAR_MIN_MAX_MIN": str(year_min),
        "YEAR_MAX_RANGE_MAX": str(year_max),
        "YEAR_MAX_RANGE_VALUE": str(year_max),
        "YEAR_MIN_LABEL": str(year_min),
        "YEAR_MAX_LABEL": str(year_max),
        "THREE_D_CONTROL": '<span class="hl-btn" id="layout-3d">UMAP 3D</span>' if has3D else "",
        "NODES_JSON": nodes_json,
        "LINKS_JSON": links_json,
        "NODE_CONNECTIONS_JSON": node_conns_json,
        "CATEGORY_COLORS_JSON": cat_colors_json,
        "CATEGORY_SHAPES_JSON": cat_shapes_json,
        "CATEGORY_COUNTS_JSON": cat_counts_json,
        "SUBCATEGORY_COLORS_JSON": sub_colors_json,
        "SUBCATEGORY_COUNTS_JSON": sub_counts_json,
        "CATEGORY_SUBCATEGORIES_JSON": cat_subs_json,
        "RELATION_COLORS_JSON": _script_json(RELATION_COLORS),
        "YEAR_MIN_INITIAL": str(year_min),
        "YEAR_MAX_INITIAL": str(year_max),
        "HAS_3D": "true" if has3D else "false",
    })


def _run_network(topic):
    """Programmatic entrypoint for generate_network."""
    topic_dir = str(get_topic_dir(topic))

    log(f"Building network for {topic}...")
    nodes, links, cat_colors, cat_shapes, sub_colors, years, has3D, node_conns = build_network_data(topic)
    log(f"  {len(nodes)} nodes, {len(links)} links, has3D={has3D}")

    html = generate_html(nodes, links, cat_colors, cat_shapes, sub_colors, years, topic, has3D=has3D, node_conns=node_conns)

    out_path = os.path.join(topic_dir, "network.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    log(f"  Written: {out_path} ({len(html):,} chars)")
    log("Done!")
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Generate d3.js paper network")
    parser.add_argument("--topic", default="", help="대상 토픽 (생략 시 설정된 토픽이 하나면 그것)")
    args = parser.parse_args()
    from config_loader import resolve_topic
    args.topic = resolve_topic(args.topic, script="generate_network")
    _run_network(topic=args.topic)


if __name__ == "__main__":
    main()
