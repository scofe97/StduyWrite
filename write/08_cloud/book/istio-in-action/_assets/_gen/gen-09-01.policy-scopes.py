# 09-01 §3 정책 범위 셋과 좁은 쪽이 이기는 규칙.
# 본문: 저자는 메시 전역에 STRICT 를 깔아 평문을 막고, 아직 메시에 못 들어온 sleep 을 위해 webapp 하나에만
#       PERMISSIVE 를 얹는다. catalog 는 STRICT 로 남는다. 실습이 이 세 범위를 차례로 쓴다.
# 네임스페이스 층은 저자가 "그러지 말자"며 건너뛴 자리라 흐리게 둔다 — 쓸 수는 있지만 쓰지 않았다.
# 타입 스펙: type-layers — 위아래로 쌓인 적용 범위. 층 3, 층 높이 72, 폭 880/1160, 왼쪽 여백에 방향 표시,
#           초점 1층(워크로드 — 예외를 얹는 자리).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1160, 540
d = D(W, H, "ISTIO IN ACTION · 09-01 §3",
      "넓게 닫고 좁게 연다",
      "PeerAuthentication 의 적용 범위는 셋이다. 저자는 메시 전역을 STRICT 로 닫은 뒤 아직 못 들어온 "
      "워크로드 하나에만 예외를 얹는다. 색이 붙은 층이 그 예외가 놓이는 자리다.",
      "7 장의 두 자리 · 8 장의 세 수준과 같은 모양이 세 번째로 나옵니다")

LX, LW, LH, Y0 = 200, 880, 72, 136
rows = [
    ("MESH", "메시 전역", "PeerAuthentication · STRICT", "루트 네임스페이스 · 이름은 관례", "have"),
    ("NS", "네임스페이스", "저자가 쓰지 않고 건너뛴 층", "\"더 잘할 수 있다\"며 넘어간다", "skip"),
    ("WORKLOAD", "워크로드", "selector + PERMISSIVE", "webapp 만 평문을 받는다", "focal"),
]
for i, (tag, name, mid, right, kind) in enumerate(rows):
    y = Y0 + i * LH
    if kind == "focal":
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="4" fill="{ACC}10" stroke="{ACC}" stroke-width="1.4"/>')
    elif kind == "skip":
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="4" fill="{INK}04" '
                   f'stroke="{MUTED}" stroke-width="1.0" stroke-dasharray="5 5"/>')
    else:
        d.box(LX, y, LW, LH, PAPER2, RULE, 1.0, 4)
    c = ACC if kind == "focal" else (SOFT if kind == "skip" else INK)
    d.t(LX + 20, y + 42, tag, 9, SOFT, MONO, "start", 600)
    d.t(LX + 132, y + 42, name, 15, c, KR, "start", 600)
    d.t(LX + 300, y + 42, mid, 11, ACC if kind == "focal" else MUTED, MONO, "start")
    d.t(LX + LW - 20, y + 42, right, 11, MUTED, KR, "end")

d.path(f"M {LX - 44} {Y0 + 8} L {LX - 44} {Y0 + 3 * LH - 8}", MUTED, 1.2, m="ar")
d.t(LX - 60, Y0 + 24, "적용 범위", 11, SOFT, KR, "end")
d.t(LX - 60, Y0 + 3 * LH - 24, "좁아진다", 11, SOFT, KR, "end")

d.t(32, 420, "결과 — sleep 은 webapp 에만 평문으로 닿고, catalog 는 상호 인증된 요청만 받는다", 11, SOFT, KR, "start")
d.t(32, 444, "기본값이 PERMISSIVE 인 것은 실수가 아니라 도입을 막지 않으려는 설계 결정이다", 11, MUTED, KR, "start")
d.legend(476, [("예외를 얹는 자리", ACC), ("쓸 수 있지만 쓰지 않은 층", MUTED)])
d.save("09-01.policy-scopes.svg")
