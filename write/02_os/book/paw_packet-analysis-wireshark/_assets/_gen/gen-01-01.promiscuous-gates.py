# 01-01 §3 「셋째, 인터페이스를 고르고 promiscuous 모드를 켭니다」 — 남의 프레임이 캡처에 닿기까지의 관문 둘.
# 타입 스펙: type-flowchart — semantic-patterns 의 Paired policy-evaluation traces 에 가장 가깝다. 같은 순서의 규칙
#           (스위치 MAC 테이블 → NIC MAC 필터)을 트레이스마다 통과 · 막힘 · 닿지 않음으로 적고, 어디서 처음
#           갈리는지를 표시한다.
#           축약: 패턴의 "트레이스 정확히 2개" 를 "입력 하나만 다른 쌍" 두 묶음으로 넓힌다 — 일반 포트 끔/켬은
#           갈림이 없다는 것(promiscuous 가 못 바꾸는 것), SPAN 포트 끔/켬은 NIC 필터에서 갈린다는 것(바꾸는 것)을
#           보인다. 흐름은 스펙의 top→down 대신 좌→우로 편다(계약 §방향이 의미의 핵심이면 가로로).
#           도형 대신 상태 글자 + 기호(✓ · ✕ · —)로 결과를 가른다. focal 은 "켰는데도 스위치에서 막히는" 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 544
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 01-01 §3",
      "promiscuous 가 바꾸는 관문, 못 바꾸는 관문",
      "다른 두 장비 사이의 유니캐스트 프레임이 스위치 MAC 테이블과 NIC MAC 필터 두 관문을 차례로 지나는지 네 조합으로 추적한다. promiscuous 모드는 NIC 필터만 끄고, 스위치 관문을 여는 것은 SPAN(미러) 포트다.",
      "위 두 줄은 켜도 결과가 같고, 아래 두 줄에서만 NIC 필터 칸이 갈립니다")

LABEL_X = 40
COLS = [(296, 176), (520, 176), (744, 112)]      # (x, w) — 칸 사이 corridor 48
RH = 48                                          # 행 높이. 같은 묶음 안 stride 60
GROUPS = [  # (묶음 머리 y, 이름, 갈림 표시, [(행 y, 입력, [칸 상태...])])
    (184, "일반 스위치 포트", None, [
        (196, "promiscuous 끔", [("bad", "이 포트로 안 보냄"), ("none", "닿지 않음"), ("bad", "안 잡힘")]),
        (256, "promiscuous 켬", [("focal", "이 포트로 안 보냄"), ("none", "닿지 않음"), ("bad", "안 잡힘")]),
    ]),
    (344, "SPAN 포트", 1, [
        (356, "promiscuous 끔", [("ok", "미러로 복사"), ("bad", "내 MAC 아님 · 버림"), ("bad", "안 잡힘")]),
        (416, "promiscuous 켬", [("ok", "미러로 복사"), ("ok", "필터 꺼짐 · 통과"), ("ok", "잡힘")]),
    ]),
]
TONE = {"ok": OK, "bad": BAD, "focal": ACC, "none": SOFT}

# 열 머리
HEAD = [("조합", "남의 유니캐스트 프레임"), ("스위치 · MAC 테이블", "목적지 MAC 의 포트로만 전달"),
        ("NIC · MAC 필터", "목적지 MAC 검사"), ("캡처 결과", "libpcap 도달")]
d.t(LABEL_X, 124, HEAD[0][0], 13, INK, KR, "start", 600)
d.t(LABEL_X, 142, HEAD[0][1], 12, MUTED, KR, "start")
for (x, w), (title, sub) in zip(COLS, HEAD[1:]):
    d.t(x + w / 2, 124, title, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, 142, sub, 12, MUTED, KR, "middle")
d.line(24, 160, 856, 160, RULE, 0.8)

def mark(kind, x, cy, c):
    if kind == "ok":                                   # ✓
        d.line(x, cy, x + 4, cy + 4, c, 1.6); d.line(x + 4, cy + 4, x + 12, cy - 4, c, 1.6)
    elif kind in ("bad", "focal"):                     # ✕
        d.line(x, cy - 4, x + 8, cy + 4, c, 1.6); d.line(x, cy + 4, x + 8, cy - 4, c, 1.6)
    else:                                              # — 닿지 않음
        d.line(x, cy, x + 10, cy, c, 1.6)

for gy, gname, split, rows in GROUPS:
    d.t(LABEL_X, gy, gname, 13, SOFT, KR, "start", 600)
    if split is None:
        d.t(856, gy, "갈림 없음", 12, MUTED, KR, "end", 600)
    else:                                              # 처음 갈리는 칸 위에 괄호 막대와 이름
        x, w = COLS[split]
        d.line(x, gy + 6, x + w, gy + 6, INK, 1.2)
        d.line(x, gy + 6, x, gy + 10, INK, 1.2); d.line(x + w, gy + 6, x + w, gy + 10, INK, 1.2)
        d.t(x + w / 2, gy - 4, "여기서 처음 갈림", 12, INK, KR, "middle", 600)
    for ry, label, states in rows:
        cy = ry + RH / 2
        d.t(LABEL_X, cy + 5, label, 13, INK, KR, "start")
        # 연결선 먼저 — 막힌 뒤의 선은 점선으로 흐리게
        d.arrow([(232, cy), (COLS[0][0] - 4, cy)], MUTED, "ar", 1.2)
        blocked = False
        for j in range(2):
            blocked = blocked or states[j][0] in ("bad", "focal")
            x1 = COLS[j][0] + COLS[j][1]
            if blocked:
                d.arrow([(x1, cy), (COLS[j + 1][0] - 4, cy)], SOFT, "soft", 1.0, dash="3,3")
            else:
                d.arrow([(x1, cy), (COLS[j + 1][0] - 4, cy)], MUTED, "ar", 1.4)
        for j, (kind, text) in enumerate(states):
            x, w = COLS[j]
            c = TONE[kind]
            if kind == "focal":
                d.o.append(f'<rect x="{x}" y="{ry}" width="{w}" height="{RH}" rx="6" '
                           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            elif kind == "none":
                d.o.append(f'<rect x="{x}" y="{ry}" width="{w}" height="{RH}" rx="6" fill="{PAPER}" '
                           f'stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="4,3"/>')
            else:
                d.tone(x, ry, w, RH, c, 6)
            if j < 2:
                mark(kind, x + 16, cy, c)
                d.t(x + 36, cy + 5, text, 13, c, KR, "start", 600)
            else:
                d.t(x + w / 2, cy + 5, text, 13, c, KR, "middle", 600)

d.legend(496, [("켜도 그대로인 관문", ACC), ("통과", OK), ("막힘", BAD), ("닿지 않음", SOFT)])
d.save("01-01.promiscuous-gates.svg")
