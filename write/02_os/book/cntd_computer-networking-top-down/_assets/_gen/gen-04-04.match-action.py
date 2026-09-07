# 타입 스펙: type-layers — 일치 대상이 어느 계층에 걸쳐 있는지를 층으로 쌓는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §4.4.1 Figure 4.29 (OpenFlow 1.0) + §4.4.2
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, BAD, KR, MONO

W, H = 960, 600
d = D(W, H, "OPENFLOW 1.0 · MATCH + ACTION",
      "일치는 세 계층에 걸칩니다",
      "OpenFlow 1.0 이 일치에 쓸 수 있는 12개 값을 계층별로 쌓고, 그 아래에 가능한 동작 셋을 둔 층 그림. 계층화 원칙을 의도적으로 거스르는 지점이 한눈에 보인다.",
      "헤더 필드 11개와 들어온 포트 하나, 합쳐 12개입니다")

BX, BW, BH, GAP = 150, 740, 62, 12
LAYERS = [
    ("스위치 자체", "INGRESS", ["진입 포트"]),
    ("링크 계층 L2", "L2", ["출발지 MAC", "목적지 MAC", "이더넷 타입", "VLAN ID", "VLAN 우선순위"]),
    ("네트워크 계층 L3", "L3", ["출발지 IP", "목적지 IP", "IP 프로토콜", "서비스 유형"]),
    ("트랜스포트 계층 L4", "L4", ["출발지 포트", "목적지 포트"]),
]

y = 112
for name, tag, fields in LAYERS:
    d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 7)
    d.t(BX - 14, y + 26, name, 11, INK, KR, "end", 600)
    d.t(BX - 14, y + 44, f"{len(fields)}개", 11, MUTED, KR, "end")
    n = len(fields)
    cw = (BW - 24 - (n - 1) * 10) / n
    for i, f in enumerate(fields):
        cx = BX + 12 + i * (cw + 10)
        d.box(cx, y + 15, cw, 32, PAPER, f"{MUTED}66", 0.9, 5)
        d.t(cx + cw / 2, y + 36, f, 11, INK, KR)
    y += BH + GAP

# 일치에 못 쓰는 것
d.t(BX, y + 18, "일치에 쓸 수 없습니다 — TTL · 데이터그램 길이", 11, BAD, KR, "start")
d.t(BX + BW, y + 18, "합 12개", 11, MUTED, MONO, "end", 600)

# 동작
AY = y + 40
d.box(BX, AY, BW, BH, f"{ACC}12", ACC, 1.4, 7)
d.t(BX - 14, AY + 26, "동작", 11, ACC, KR, "end", 600)
d.t(BX - 14, AY + 44, "3종", 11, MUTED, KR, "end")
acts = [("전달", "포트 하나 · 여러 포트 · 컨트롤러"),
        ("폐기", "동작이 없는 항목이 곧 폐기"),
        ("필드 재작성", "2·3·4계층 필드 10개")]
cw = (BW - 24 - 2 * 10) / 3
for i, (a, sub) in enumerate(acts):
    cx = BX + 12 + i * (cw + 10)
    d.box(cx, AY + 12, cw, 38, PAPER, f"{ACC}66", 1.1, 5)
    d.t(cx + cw / 2, AY + 28, a, 11, ACC, KR, "middle", 600)
    d.t(cx + cw / 2, AY + 44, sub, 11, MUTED, KR)

d.path(f"M {BX + BW / 2} {AY - 22} L {BX + BW / 2} {AY - 6}", ACC, 1.4, m="acc")

d.t(BX, AY + BH + 34, "같은 장비가 이더넷 주소로 일치를 걸면 2계층 스위치처럼, "
                       "IP 주소로 걸면 3계층 라우터처럼 굽니다. 바꾸는 것은 표뿐입니다.",
     11, MUTED, KR, "start")

d.legend(AY + BH + 56, [("동작", ACC), ("일치 대상", MUTED), ("일치에 못 쓰는 필드", BAD)])
d.t(920, AY + BH + 78, "KUROSE-ROSS 9E FIG 4.29 · OPENFLOW 1.0", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "04-04.match-action.svg"
d.save(out)
print("일치 대상 합계", sum(len(f) for _, _, f in LAYERS), "→", out)
