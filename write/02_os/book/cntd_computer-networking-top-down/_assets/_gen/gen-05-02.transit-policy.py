# 타입 스펙: type-architecture — 같은 AS 여섯의 망 그래프를 좌우 두 칸(장면 1·2)으로 두고, 링크마다 광고·막은 광고·트래픽을 칠한다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.4.5 Figure 5.13 의 정책 시나리오와 상용 ISP 경험칙
# 2026-09-13: type-venn(합집합 원 두 개)에서 바꿨다. 집합 그림은 조건만 보이고 "광고를 막으면 트래픽이
#             어디로 가나"라는 흐름이 안 보였다(사용자 지적).
# 링크는 노트 6절 본문이 전제하는 것만 그린다.
#   A–W (A 를 지나 W 로) · B–A (B 가 A 에게서 배움) · B–C (C 가 B 를 거쳐 W 로) · X–B · X–C (다중 접속) · C–Y (X-C-Y)
#   A–C 는 본문에 나오지 않으므로 그리지 않는다. 그래서 장면 2 에서 C 가 W 로 가는 다른 길도 그리지 않는다.
# 노트의 읽기: 장면 1 의 "Y 행은 B-C-Y" 는 C 가 자기 고객 Y 를 B 에게 광고한다는 경험칙 적용이다.
#   원문 장면에는 "더 짧은 길을 두고 더 긴 길"이 실제로 성립하는 경로가 없어 억지로 그리지 않았다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, OK, KR, MONO

W, H = 1000, 604
d = D(W, H, "SECTION 5.4.5 · TRANSIT POLICY",
      "광고를 막으면 그 길로는 아무도 보내지 않습니다",
      "백본 A·B·C 와 액세스 W·X·Y 로 된 같은 망에서 두 장면을 본다. 장면 1 에서 X 는 X-C-Y 를 B 에게 광고하지 않아 B 의 Y 행 트래픽이 X 를 지나지 않는다. 장면 2 에서 B 는 A 에게서 배운 W 행 경로를 고객 X 에게만 알리고 C 에게는 알리지 않아, C 가 B 를 거쳐 W 로 보내지 않는다.",
      "같은 망에서 두 장면을 봅니다. 파란 화살표는 광고, 빨간 점선은 막은 광고, 초록은 그 결과 트래픽이 타는 길입니다.")

NODES = {  # 칸 안 상대 좌표 (x, y), 상자 72×44
    "A": (24, 184, "백본"), "B": (168, 184, "백본"), "C": (328, 184, "백본"),
    "W": (24, 312, "액세스"), "X": (248, 312, "액세스"), "Y": (360, 312, "액세스"),
}
# 링크 경로 (칸 원점 기준). 직각만 쓴다.
LINKS = {
    "AB": "M 96 206 L 168 206",
    "BC": "M 240 206 L 328 206",
    "AW": "M 60 228 L 60 312",
    "XB": "M 248 334 L 204 334 L 204 228",
    "XC": "M 320 334 L 344 334 L 344 228",
    "CY": "M 384 228 L 384 312",
}


def shift(p, ox):
    out, toks = [], p.split()
    i = 0
    while i < len(toks):
        if toks[i] in ("M", "L"):
            out += [toks[i], str(int(toks[i + 1]) + ox), toks[i + 2]]
            i += 3
        else:
            i += 1
    return " ".join(out)


def panel(ox, num, title, styled, arrows, labels, result):
    d.box(ox, 124, 448, 320, f"{INK}04", RULE, 1.0, 10)
    d.t(ox + 16, 152, f"장면 {num}", 12, SOFT, KR, "start", 600)
    d.t(ox + 72, 152, title, 13, INK, KR, "start", 600)
    # 기본 링크 — 칠하지 않은 것만
    for k, p in LINKS.items():
        if k not in styled:
            d.path(shift(p, ox), MUTED, 1.2)
    # 칠한 링크 (광고·막은 광고·트래픽)
    for k, (c, sw, dash) in styled.items():
        d.path(shift(LINKS[k], ox), c, sw, dash=dash)
    for p, c, m in arrows:
        d.path(shift(p, ox), c, 2.0, m=m)
    for name, (x, y, sub) in NODES.items():
        d.box(ox + x, y, 72, 44, PAPER2, MUTED, 1.0, 6)
        d.t(ox + x + 36, y + 19, name, 14, INK, MONO, "middle", 600)
        d.t(ox + x + 36, y + 36, sub, 12, MUTED, KR)
    for fn in labels:
        fn(ox)
    d.box(ox + 16, 392, 416, 36, PAPER2, RULE, 1.0, 6)
    d.t(ox + 224, 415, result, 13, INK, KR, "middle")


# ── 장면 1 — X 가 B 에게 X-C-Y 를 광고하지 않는다 ─────────────────
def labels1(ox):
    d.chip(ox + 136, 272, "광고 안 함", BAD, 12, 7)
    d.t(ox + 284, 196, "Y 행 트래픽", 12, OK, KR)
    d.t(ox + 284, 380, "X 는 X-C-Y 를 앎", 12, INFO, KR)


panel(24, 1, "X 는 남의 통과 트래픽 차단",
      styled={"XB": (BAD, 1.6, "5 4"), "BC": (OK, 2.0, None), "CY": (OK, 2.0, None), "XC": (INFO, 1.6, None)},
      arrows=[("M 240 206 L 324 206", OK, "ok"), ("M 384 228 L 384 308", OK, "ok"),
              ("M 344 228 L 344 334 L 324 334", INFO, "info")],
      labels=[labels1],
      result="B 의 표에 B-X-C-Y 가 없어 Y 행은 B-C-Y 로 감")


# ── 장면 2 — B 가 A-W 를 X 에게만 알리고 C 에게는 알리지 않는다 ──────
def labels2(ox):
    d.chip(ox + 132, 186, "A-W", INFO, 12, 7)
    d.t(ox + 136, 272, "고객 X 에게 알림", 12, INFO, KR)
    d.chip(ox + 280, 250, "C 에게는 안 알림", BAD, 12, 7)


panel(528, 2, "B 는 A–C 사이를 공짜로 나르지 않음",
      styled={"AB": (INFO, 1.6, None), "XB": (INFO, 1.6, None), "BC": (BAD, 1.6, "5 4")},
      arrows=[("M 96 206 L 164 206", INFO, "info"), ("M 204 228 L 204 334 L 244 334", INFO, "info")],
      labels=[labels2],
      result="C 의 표에 B-A-W 없음 → W 행을 B 로 안 보냄")

# ── 경험칙 (focal) ──────────────────────────────────────────
d.tone(24, 460, 952, 72, ACC, r=8, op="12", sw=1.4)
d.t(44, 488, "경험칙 — 내 백본을 지나는 트래픽은 출발지·목적지 중 하나가 내 고객", 14, INK, KR, "start", 600)
d.t(44, 516, "둘 다 아니면 무임승차 → 광고 안 함 · 광고되지 않은 길은 짧아도 후보 제외", 13, MUTED, KR, "start")

d.legend(556, [("광고", INFO), ("막은 광고", BAD), ("트래픽이 타는 길", OK), ("경험칙", ACC)])
d.t(960, 596, "KUROSE-ROSS 9E FIG 5.13 · §5.4.5", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.transit-policy.svg"
d.save(out)
print("→", out)
