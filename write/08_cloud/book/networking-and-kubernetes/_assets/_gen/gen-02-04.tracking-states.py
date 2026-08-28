# 02-04.tracking-states — 실험이 지나온 세 상태
# 본문 요구: §5 는 세 번 관측한다 — 규칙이 없을 때 0건, 규칙을 넣었을 때 정확히 뒤집힌 두 줄,
#           MASQUERADE 를 걸었을 때 응답 dst 가 어긋난 두 줄. 그 셋이 상태이고 전이는 규칙 추가다.
# 타입 스펙: type-state.md — 상태는 rx=8 둥근 사각, 시작은 채운 점, 전이 라벨은 event / action,
#           자기 루프는 상태 위로. coral 은 독자가 주목할 상태 하나.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, PAPER, PAPER2, KR, MONO

W, H = 1000, 560
d = D(W, H, "TRACKING · THREE OBSERVED STATES",
      "규칙을 하나씩 얹을 때마다 conntrack 테이블이 달라진다",
      "연결 추적은 요구가 있을 때만 켜지고, NAT 규칙을 얹으면 같은 연결의 응답 튜플이 달라집니다. "
      "세 상태는 규칙을 추가할 때마다 관측한 실제 결과입니다.",
      lead="추적은 규칙이 요구할 때 켜지고, NAT 는 응답 튜플을 바꾼다")

CY, BH = 288, 116
S = [(216, 192, "추적 꺼짐", "규칙이 하나도 없다", "conntrack -L → 0건", RULE),
     (520, 224, "추적 켜짐", "NAT 는 아직 없다", "응답 = 원본을 뒤집은 값", OK),
     (840, 224, "SNAT 적용", "MASQUERADE 를 걸었다", "응답 dst 만 어긋난다", ACC)]

def state(cx, w, name, desc, obs, c, focal=False):
    x, y = cx - w // 2, CY - BH // 2
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="8" '
               f'fill="{c}12" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
    tc = c if c is not RULE else INK
    d.t(cx, CY - 34, ddx.fit(name, 13, w - 24, name), 13, tc, KR, "middle", 600)
    d.t(cx, CY - 8, ddx.fit(desc, 12, w - 24, desc), 12, MUTED, KR)
    d.t(cx, CY + 26, ddx.fit(obs, 11, w - 20, obs), 11, tc, MONO)

def trans(x0, x1, main, sub):
    d.path(f"M {x0} {CY} L {x1-8} {CY}", MUTED, 1.5, m="ar")
    mx = (x0 + x1) // 2
    d.t(mx, CY - 40, main, 12, INK, KR)
    d.t(mx, CY - 20, sub, 11, SOFT, MONO)

d.o.append(f'<circle cx="48" cy="{CY}" r="6" fill="{INK}"/>')
d.path(f"M 56 {CY} L {S[0][0]-S[0][1]//2-8} {CY}", MUTED, 1.5, m="ar")
for cx, w, n, de, o, c in S:
    state(cx, w, n, de, o, c, focal=(c is ACC))
trans(S[0][0] + S[0][1] // 2, S[1][0] - S[1][1] // 2, "매치 규칙 추가", "-m conntrack")
trans(S[1][0] + S[1][1] // 2, S[2][0] - S[2][1] // 2, "NAT 규칙 추가", "MASQUERADE")

# 자기 루프 — 수명이 다하면 항목이 사라진다
LXX, RXX, TOP = S[2][0] - 44, S[2][0] + 44, 196
d.path(f"M {LXX} {CY-BH//2} C {LXX} {TOP}, {RXX} {TOP}, {RXX} {CY-BH//2-8}", MUTED, 1.4, m="ar")
d.t(S[2][0], TOP - 24, "수명 만료", 12, MUTED, KR)
d.t(S[2][0], TOP - 6, "엔트리 삭제", 11, SOFT, KR)

d.t(36, 452, "추적은 공짜가 아니라 커널이 요구가 있을 때만 훅을 등록합니다. 첫 상태에서 통신은 되는데 "
             "테이블만 비어 있던 것이 그래서입니다.", 12, MUTED, KR, "start")
d.t(36, 474, "세 상태 모두 ping 은 통합니다. 달라지는 것은 테이블에 무엇이 적히느냐뿐입니다.",
    12, MUTED, KR, "start")
d.legend(490, [("추적 켜짐 · NAT 없음", OK), ("SNAT 적용 — 응답 줄이 어긋난다", ACC)])
d.save("02-04.tracking-states.svg")
print("ok tracking-states")
