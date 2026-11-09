# 04-01 학습 목표 뒤 전체 지도 — 절 넷이 호스트 문 앞에서 감사 로그까지 간다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 호스트가 맡는 일 · 그 절이 주는 것)이
#           반복되고 화살표가 읽는 순서를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 420
d = D(W, H, "LAMPSON LAB · 04-01",
      "호스트에는 개인 계정이 없다 — 읽는 순서",
      "절 넷. 호스트가 믿는 것에서 시작해 포워딩 차단, 역할 계정의 권한, 감사 로그로 이어진다.",
      "첫 절이 이 편의 핵심이다 — 호스트는 CA 공개키 하나와 principal 파일 셋만 믿는다")

CW, CH, GAP, X0 = 404, 108, 24, 24
Y1, Y2 = 120, 252
cards = [
    ("§1", "믿는 것 · CA 와 principal 파일", "authorized_keys 없음 · 역할 계정 셋"),
    ("§2", "막는 것 · 포워딩", "sshd 는 허용 · 인증서가 막는다"),
    ("§3", "허락하는 것 · 역할 계정의 권한", "operator 는 명령 하나 · readonly 는 없음"),
    ("§4", "남기는 것 · 감사 로그", "Key ID · Serial · 테스트용 완화"),
]

def pos(i):
    return X0 + (i % 2) * (CW + GAP), (Y1 if i < 2 else Y2)

for i in range(3):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 4, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        cy = Y1 + CH + 16
        d.path(f"M {x1 + CW / 2} {y1 + CH} V {cy} H {X0 + CW / 2} V {y2 - 4}", MUTED, 1.4, m="ar")

for i, (n, title, mark) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 0)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, y + 30, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 20, y + 58, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, y + 84, mark, 12, MUTED, KR, "start")

d.t(24, 392, "누가 들어왔는지는 계정이 아니라 인증서의 Key ID 가 말한다", 12, SOFT, KR, "start")
d.save("04-01.chapter-overview.svg")
