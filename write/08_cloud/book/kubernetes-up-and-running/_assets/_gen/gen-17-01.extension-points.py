# 17-01 §클러스터를 확장하는 세 자리
# 본문이 방향을 못 박는다 — "오른쪽으로 갈수록 API 서버에 깊이 손대고, 권한과 책임이 커진다".
# 그래서 셋을 나란한 카드로만 두면 안 되고, 오른쪽 둘이 API 서버 *안에* 들어 있다는 것이
# 그림에서 보여야 한다. 첫째만 상자 밖에 두는 것이 그 깊이의 표현이다.
# 초점은 첫째다 — 확장을 다루는 장인데 저자가 먼저 권하는 것이 "건드리지 말라" 이기 때문이다.
# 타입 스펙: type-process.md — 확장점 셋이 같은 의미 슬롯(이름 · 한 줄 · 항목 목록)으로 반복되고
#           아래 방향 화살표가 순서를 나른다. 본문이 "오른쪽으로 갈수록 API 서버에 깊이 손댄다"
#           라고 축을 못 박으므로 방향이 형태로 있어야 한다.
#           어긋나는 지점: 뒤 둘을 감싼 "API 서버" 상자는 architecture 의 경계 사각형을 빌려
#           *깊이* 를 표현한 것이다. 첫째만 상자 밖에 있는 것이 그 깊이 차이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 614
d = D(W, H, "KUBERNETES UP AND RUNNING · 17-01",
      "먼저 권하는 것은 건드리지 않는 길이다",
      "클러스터 안에 오케스트레이션할 도구는 끝없이 많지만 그걸 다 코어 API 에 넣으면 API 가 "
      "한없이 번진다. 그 사이를 푼 답이 확장점 셋이다.",
      "뒤의 둘은 배타적이지 않아 함께 쓴다")

d.box(408, 126, 816, 284, PAPER, RULE, 1.0, 10)
d.t(816, 150, "API 서버", 11, SOFT, KR)

def card(x, w, title, sub, items, focal=False, tag=None):
    y0, y1 = 176, 390
    if focal:
        d.o.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{y1-y0}" rx="8" '
                   f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y0, w, y1 - y0, PAPER2, RULE, 1.0, 8)
    if tag: d.t(x + w - 18, y0 + 24, tag, 9, ACC if focal else SOFT, KR, "end")
    d.t(x + 18, y0 + 46, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y0 + 68, ddx.fit(sub, 10, w - 36, sub), 10, SOFT, KR, "start")
    d.line(x + 18, y0 + 84, x + w - 18, y0 + 84, RULE, 0.8)
    for i, it in enumerate(items):
        yy = y0 + 100 + i * 30
        d.o.append(f'<rect x="{x+18}" y="{yy}" width="{w-36}" height="24" rx="4" '
                   f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.8"/>')
        d.t(x + 30, yy + 16, ddx.fit(it, 10, w - 60, it), 10, MUTED, KR, "start")

card(24, 366, "건드리지 않는다", "기존 API 테두리 안에서 되는 일부터 살핀다",
     ["자동 로깅·모니터링을 설치하는 DaemonSet",
      "서비스의 XSS 취약점을 훑는 도구"], focal=True, tag="저자가 먼저 권한다")
card(428, 372, "어드미션 컨트롤러", "객체가 백킹 스토리지에 쓰이기 직전에 불린다",
     ["요청을 거부하거나 수정한다",
      "내장 — 한계 없는 파드에 기본 한계를 넣는다",
      "커스텀 — 모든 파드에 사이드카를 주입한다"])
card(820, 384, "커스텀 리소스", "완전히 새로운 API 객체가 표면에 더해진다",
     ["네임스페이스에 들어가고 RBAC 의 적용을 받는다",
      "kubectl 을 비롯한 기존 도구로 그대로 다룬다",
      "타입 이름은 클러스터 안에서 겹칠 수 없다"])

d.path("M 24 438 L 1216 438", SOFT, 1.4, m="soft")
d.t(620, 428, "오른쪽으로 갈수록 API 서버에 깊이 손대고, 그만큼 권한과 책임이 커진다", 11, SOFT, KR)

BT, BB = 468, 538
d.o.append(f'<rect x="12" y="{BT}" width="{W-36}" height="{BB-BT}" rx="8" '
           f'fill="{BAD}0E" stroke="{BAD}" stroke-width="1.2"/>')
d.t(W / 2, BT + 26, "확장은 권한이 아주 높은 행위다. 어드미션 컨트롤러 같은 확장은 클러스터에서 생성되는 모든 객체를 볼 수 있어, "
                    "Secret 을 훔치거나 악성 코드를 실행하는 벡터로 쉽게 쓰인다.", 11, BAD, KR)
d.t(W / 2, BT + 48, "비용이 하나 더 있다 — 확장한 클러스터는 더 이상 표준 쿠버네티스가 아니다.", 11, BAD, KR)

d.legend(BB + 24, [("저자가 먼저 권하는 쪽", ACC), ("장 앞머리의 경고", BAD)])
d.save("17-01.extension-points.svg")
print("h 필요:", BB + 24 + 48, " 실제:", H)
