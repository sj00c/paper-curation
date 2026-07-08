#!/usr/bin/env python3
"""전체 커리큘럼 연구 지도 — 1~N강에 등장한 모든 논문을 한 캔버스에.

- Dashun Wang 그룹 논문 = 주황색, 그 외 그룹 = 같은 명도의 회색.
- 발표 연도 gradation: 오래될수록 밝게(the older, the brighter).
- 위치는 lecture_map.compute_layout 의 constellation(강별 centroid) 재사용.
- 등장 논문 = 각 강 gather_evidence 의 core(그룹) + 관련(top10) 합집합.

사용: python curriculum_map.py [out.png]
"""
import os, sys, colorsys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import agent_lecture_digest as ald
import lecture_map as lm

ORANGE_H = 26.0 / 360.0          # 주황 hue
L_HI, L_LO = 0.86, 0.32          # 오래된(밝음) .. 최신(어두움)


def _iyear(v):
    try:
        return int(str(v)[:4])
    except Exception:
        return None



def wang_rgb(L):
    return colorsys.hls_to_rgb(ORANGE_H, L, 0.90)


def gray_rgb(L):
    return colorsys.hls_to_rgb(0.0, L, 0.0)


def is_wang(slug, coreset, idx):
    if slug in coreset:
        return True
    auth = idx.get(slug, {}).get("authors") or []
    return any("dashun wang" in (a or "").lower() for a in auth)


def build_curriculum_map(out_path):
    lm.set_korean_font()
    L = lm.compute_layout(1)                    # constellation-wide fields
    ppos, hub, nums, idx, edges = L["ppos"], L["hub"], L["nums"], L["idx"], L["edges"]
    led = ald.load_ledger()
    course = led.get("course", "Dashun Wang 커리큘럼")

    # featured papers = union over lectures of (core + related top10)
    coreset, featured, year = set(), set(), {}
    for lec in led["lectures"]:
        _ev, core, related = ald.gather_evidence(lec)
        for c in core:
            coreset.add(c["slug"]); featured.add(c["slug"])
            if c.get("year"):
                year[c["slug"]] = _iyear(c["year"])
        for r in related:
            featured.add(r["slug"])
            if r.get("year") and r["slug"] not in year:
                year[r["slug"]] = _iyear(r["year"])
    # fill missing years from index
    for s in featured:
        if year.get(s) is None:
            year[s] = _iyear(lm._year(idx.get(s, {})))

    featured = [s for s in featured if s in ppos]
    wang = [s for s in featured if is_wang(s, coreset, idx)]
    other = [s for s in featured if s not in set(wang)]
    yvals = [year[s] for s in featured if year.get(s)]
    ymin, ymax = min(yvals), max(yvals)
    # gradation by publication ORDER (distinct-year rank), evenly spread so a
    # single old outlier doesn't compress the scale. older -> brighter.
    distinct = sorted(set(yvals))
    _rank = {y: i for i, y in enumerate(distinct)}

    def Lof(y):
        if y is None or len(distinct) <= 1:
            return (L_HI + L_LO) / 2
        return L_HI - (_rank[y] / (len(distinct) - 1)) * (L_HI - L_LO)

    fig, ax = plt.subplots(figsize=(16.2, 9.6), dpi=160)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, facecolor="white", zorder=0))

    wangset, otherset = set(wang), set(other)
    # (1) 기타 그룹 논문 -> 연관 있다고 판단된 Wang 그룹 논문 연결선
    #     (회색, 기타 논문 연도로 gradation: 오래될수록 밝게)
    g_segs, g_cols = [], []
    for a, b in edges:
        if a in wangset and b in otherset:
            g, w = b, a
        elif a in otherset and b in wangset:
            g, w = a, b
        else:
            continue
        g_segs.append([ppos[g], ppos[w]]); g_cols.append(gray_rgb(Lof(year[g])))
    ax.add_collection(LineCollection(g_segs, colors=g_cols, linewidths=0.5,
                                     alpha=0.35, zorder=1))
    # (2) Wang 그룹 논문 시간순(오래된->새로운) 연결선 (주황 spine, 연도 gradation)
    wsorted = sorted([w for w in wang if year.get(w)], key=lambda w: (year[w], w))
    s_segs = [[ppos[wsorted[i]], ppos[wsorted[i + 1]]] for i in range(len(wsorted) - 1)]
    s_cols = [wang_rgb(Lof(year[wsorted[i]])) for i in range(len(wsorted) - 1)]
    ax.add_collection(LineCollection(s_segs, colors=s_cols, linewidths=1.3,
                                     alpha=0.75, zorder=2, capstyle="round"))

    # faint lecture-number hubs for spatial context
    for n in nums:
        h = hub[n]
        ax.text(h[0], h[1], str(n), fontsize=17, color="#EAEDF0",
                fontweight="bold", ha="center", va="center", zorder=2)

    # nodes: gray (other) behind, orange (Wang) in front
    for s in other:
        c = gray_rgb(Lof(year[s])); pp = ppos[s]
        ax.scatter([pp[0]], [pp[1]], s=52, facecolor=[c], edgecolors="#FFFFFF",
                   linewidths=0.5, alpha=0.96, zorder=3)
    for s in wang:
        Lv = Lof(year[s])
        c = wang_rgb(Lv); ec = wang_rgb(max(0.16, Lv - 0.22)); pp = ppos[s]
        ax.scatter([pp[0]], [pp[1]], s=104, facecolor=[c], edgecolors=[ec],
                   linewidths=0.9, zorder=5)

    # ---- title ----
    ax.text(0.015, 0.985, "%s — 전체 연구 지도" % course, fontsize=17,
            fontweight="bold", color="#212529", va="top")
    ax.text(0.015, 0.945,
            "논문 %d편 (Wang 그룹 %d · 타 그룹 %d) · %d–%d"
            % (len(featured), len(wang), len(other), ymin, ymax),
            fontsize=10.5, color="#868E96", va="top")

    # ---- legend: group swatches ----
    lx, ly = 0.70, 0.955
    ax.scatter([lx], [ly], s=150, facecolor=[wang_rgb(0.55)],
               edgecolors=[wang_rgb(0.33)], linewidths=1.0,
               transform=ax.transAxes, clip_on=False, zorder=10)
    ax.text(lx + 0.018, ly, "Dashun Wang 그룹", fontsize=11, color="#212529",
            va="center", transform=ax.transAxes)
    ax.scatter([lx], [ly - 0.045], s=110, facecolor=[gray_rgb(0.55)],
               edgecolors="#FFFFFF", linewidths=0.6,
               transform=ax.transAxes, clip_on=False, zorder=10)
    ax.text(lx + 0.018, ly - 0.045, "다른 그룹", fontsize=11, color="#212529",
            va="center", transform=ax.transAxes)
    ax.plot([lx - 0.007, lx + 0.007], [ly - 0.092, ly - 0.092], color=wang_rgb(0.5),
            lw=2.4, solid_capstyle="round", transform=ax.transAxes, clip_on=False, zorder=10)
    ax.text(lx + 0.018, ly - 0.092, "Wang 그룹 시간순 연결", fontsize=10,
            color="#212529", va="center", transform=ax.transAxes)
    ax.plot([lx - 0.007, lx + 0.007], [ly - 0.132, ly - 0.132], color=gray_rgb(0.5),
            lw=1.3, transform=ax.transAxes, clip_on=False, zorder=10)
    ax.text(lx + 0.018, ly - 0.132, "기타 → 연관 Wang 논문", fontsize=10,
            color="#212529", va="center", transform=ax.transAxes)

    # ---- year gradient bars (older = brighter) ----
    bx, bw = 0.72, 0.05
    by0, by1 = 0.25, 0.68           # bottom(new/dark) .. top(old/bright)
    steps = 64
    for i in range(steps):
        t = i / (steps - 1)                       # 0 bottom .. 1 top
        yy = by0 + (by1 - by0) * t
        Lv = L_LO + (L_HI - L_LO) * t             # top brightest
        ax.add_patch(Rectangle((bx, yy), bw, (by1 - by0) / steps + 0.001,
                               facecolor=wang_rgb(Lv), edgecolor="none",
                               transform=ax.transAxes, zorder=9))
        ax.add_patch(Rectangle((bx + bw + 0.012, yy), bw, (by1 - by0) / steps + 0.001,
                               facecolor=gray_rgb(Lv), edgecolor="none",
                               transform=ax.transAxes, zorder=9))
    ax.text(bx, by1 + 0.02, "연도별 명암 (오래될수록 밝게)", fontsize=10.5,
            fontweight="bold", color="#212529", transform=ax.transAxes)
    ax.text(bx - 0.005, by1, "  %d (oldest)" % ymin, fontsize=9, color="#495057",
            ha="right", va="center", transform=ax.transAxes)
    ax.text(bx - 0.005, by0, "  %d (newest)" % ymax, fontsize=9, color="#495057",
            ha="right", va="center", transform=ax.transAxes)
    ax.text(bx - 0.005, (by0 + by1) / 2, "  ↑ 오래된 논문", fontsize=8.2,
            color="#868E96", ha="right", va="center", transform=ax.transAxes)
    ax.text(bx, by0 - 0.03, "Wang", fontsize=8.5, color="#B34700",
            ha="center", transform=ax.transAxes)
    ax.text(bx + bw + 0.012 + bw / 2, by0 - 0.03, "기타", fontsize=8.5,
            color="#868E96", ha="center", transform=ax.transAxes)

    fig.savefig(out_path, bbox_inches="tight", facecolor="white")
    print("saved", out_path, os.path.getsize(out_path), "bytes")
    print("featured=%d wang=%d other=%d years=%d-%d"
          % (len(featured), len(wang), len(other), ymin, ymax))
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "curriculum_map.png"
    build_curriculum_map(out)
