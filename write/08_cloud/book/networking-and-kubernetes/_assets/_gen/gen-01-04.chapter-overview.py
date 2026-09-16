# 01-04.chapter-overview — 경계 두 개 + 그 밖에 하나
# 본문: "점선 두 개가 어느 인터페이스에서 잡는지를 가릅니다. 통제된 lo0 에서 시작해
#        실제 랜인 en0 으로 넓히는 흐름이고, §4 만 두 점선 밖에 있는데 그 절은
#        패킷을 잡는 대신 소켓 상태를 조회하기 때문입니다."
# 타입 스펙: type-nested.md 의 경계 링 둘. §4 를 한 단 올려 두 링이 끊기지 않게 한다 —
#           경계 밖이라는 사실이 자리로 드러나야 하므로 링 안에 두고 색만 바꾸지 않는다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 552
d = D(W, H, "01-04 · LAB MAP",
      "1장 패킷 캡처 실습 전체 지도 — 관측 방법이 절을 가른다",
      "점선 두 개가 어느 인터페이스에서 잡는지를 가른다. §4 만 두 점선 밖에 있는데, 그 절은 패킷을 잡는 대신 소켓 상태를 조회한다.",
      lead="점선 두 개가 어느 인터페이스에서 잡는지 가른다 · §4 만 그 밖에 있다")

BW, BH = 172, 108
ROW, LIFT = 380, 224
S1, S2, S3, S5 = 142, 356, 616, 860
S4 = 738
RING_LO = (40, 312, 418, 136)
RING_EN = (514, 312, 448, 136)

def sec(cx, cy, name, sub, tag, c=None, focal=False):
    x, y = cx - BW // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, BW, BH, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, cy - 24, name, 13, tc, KR, "middle", 600)
    d.t(cx, cy - 2, ddx.fit(sub, 11, BW - 16, sub), 11, MUTED, KR)
    d.t(cx, cy + 26, ddx.fit(tag, 11, BW - 12, tag), 11, SOFT, KR)

ddx.band(d, 104, 492, "통제된 lo0 → 실제 랜 en0 으로 확장")
# 링 라벨 마스크는 테두리와 겹치고, 링 위쪽은 §4 로 가는 화살표가 지난다 — 링 바로 아래에 쓴다
for (rx, ry, rw, rh), lab, c in [(RING_LO, "lo0 캡처 — 잡음 없는 통제 환경", INFO),
                                 (RING_EN, "en0 캡처 — 실제 랜", WARN)]:
    d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
               f'fill="{c}06" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    d.t(rx + 16, ry + rh + 22, lab, 12, c, KR, "start", 600)

sec(S1, ROW, "§1 관측 지점", "lo0 이냐 en0 이냐", "보일 계층이 갈림", INFO)
sec(S2, ROW, "§2 패킷 12개", "요청 하나 세기", "L3 · L4 만", INFO)
sec(S3, ROW, "§3 ARP 일으키기", "캐시를 지우고 다시", "L2 열림", WARN)
sec(S5, ROW, "§5 대조", "TLS 평문 · UDP", "L7 경계 · L4 개수", WARN)
sec(S4, LIFT, "§4 소켓 상태", "TIME-WAIT · CLOSE-WAIT", "캡처가 아니라 ss 로", focal=True)

HB = BW // 2
for a, b, lab in [(S1, S2, "고른 뒤"), (S2, S3, "옮긴 뒤")]:
    d.path(f"M {a+HB+8} {ROW} L {b-HB-10} {ROW}", MUTED, 1.5, m="ar")
    d.t((a + b) // 2, ROW - 16, lab, 11, MUTED, KR)
# §4 는 §3·§5 와 가로로 겹치므로 대각선을 그으면 방향이 거꾸로 읽힌다 — 직교로 돌린다
d.path(f"M {S3} {ROW-BH//2-6} L {S3} {LIFT} L {S4-HB-10} {LIFT}", ACC, 1.5, m="acc")
d.path(f"M {S4+HB+8} {LIFT} L {S5} {LIFT} L {S5} {ROW-BH//2-10}", ACC, 1.5, m="acc")
d.t(S4, LIFT - BH // 2 - 16, "두 점선 밖 · 패킷 캡처 없음", 12, ACC, KR)

# 하단 해설(꼬리표가 열리는 계층)은 도식 앞 본문 문단이 말한다 — 뺐다
d.legend(512, [("lo0 에서", INFO), ("en0 에서", WARN), ("캡처가 아닌 절", ACC)])
d.save("01-04.chapter-overview.svg")
print("ok chapter-overview")
