# 10-04.proxy — go get 은 프록시에서 모듈을 받고 체크섬 데이터베이스로 검증하며, GOPRIVATE 모듈은 저장소에서 직접 받는다
# 본문 요구(10-04 §5 「모듈 프록시와 체크섬 데이터베이스」): 기본으로 go get 은 Google 의 프록시에 요청하고, 프록시는 캐시에 없으면
#           원래 저장소에서 받아 둔다. 받은 모듈의 해시는 체크섬 데이터베이스와 대조하고 맞지 않으면 설치하지 않는다. GOPRIVATE 에 든
#           모듈은 프록시를 거치지 않고 비공개 저장소에서 직접 받는다. 누가 누구에게 묻는가가 논지다.
# 타입 스펙: type-architecture — 왼쪽 개발자 컴퓨터(go get · go.sum), 가운데 Google 서비스 존(프록시 · 체크섬 DB), 오른쪽 저장소들.
#           번호 붙은 직교 화살표. focal 은 체크섬 대조 화살표 하나.
# 사실 출처: Learning Go 2판 10장 「Module Proxy Servers」·「Specifying a Proxy Server」·「Using Private Repositories」.
#           proxy.golang.org·sum.golang.org 라는 호스트 이름은 원문 밖 보충이다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, WARN, PAPER2, KR, MONO

W, H = 984, 520
d = D(W, H, "ARCHITECTURE · 10-04 §5",
      "go get 이 모듈을 받고 검증하는 경로",
      "기본으로 go get 은 저장소가 아니라 Google 의 모듈 프록시에 요청한다. 프록시는 캐시에 없으면 원래 저장소에서 받아 사본을 두고 돌려준다. "
      "go 도구는 받은 모듈의 해시를 체크섬 데이터베이스의 값과 대조해, 맞지 않으면 설치하지 않는다. GOPRIVATE 에 든 모듈은 프록시를 거치지 않고 비공개 저장소에서 직접 받는다.",
      lead="번호는 순서입니다. 호스트 이름 proxy.golang.org·sum.golang.org 는 노트가 더한 것입니다.")


def box(x, y, w, h, title, sub, c=None):
    if c:
        d.tone(x, y, w, h, c, 6, "14", 1.0)
    else:
        d.box(x, y, w, h)
    d.t(x + w // 2, y + h // 2 - 4, title, 13, c or INK, MONO if title.isascii() else KR, "middle", 600)
    d.t(x + w // 2, y + h // 2 + 16, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "middle")


box(24, 176, 200, 88, "go get", "go.sum 에 해시 기록")
d.o.append(f'<rect x="300" y="116" width="336" height="312" rx="10" fill="none" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="6 5"/>')
d.t(316, 140, "Google 운영", 13, INFO, KR, "start", 600)
box(332, 164, 272, 88, "모듈 프록시", "proxy.golang.org · 캐시", INFO)
box(332, 300, 272, 88, "체크섬 데이터베이스", "sum.golang.org · 버전별 해시", INFO)
box(724, 164, 236, 88, "공개 저장소", "GitHub · GitLab")
box(724, 332, 236, 88, "비공개 저장소", "GOPRIVATE 에 든 경로", WARN)

d.arrow([(224, 208), (330, 208)], SOFT, "soft", 1.4)
d.t(276, 200, "1 요청", 11, MUTED, KR, "middle", 600)
d.arrow([(604, 208), (722, 208)], SOFT, "soft", 1.4)
d.t(646, 200, "2 캐시에 없으면", 11, MUTED, KR, "start", 600)
d.arrow([(160, 264), (160, 344), (330, 344)], ACC, "acc", 1.6)
d.t(244, 336, "3 해시 대조", 11, ACC, KR, "middle", 600)
d.path("M 96 264 L 96 456 L 842 456 L 842 422", WARN, 1.4, m="warn", dash="5 4")
d.t(470, 450, "GOPRIVATE · 프록시를 거치지 않고 직접", 11, WARN, KR, "middle", 600)

d.legend(476, [("Google 서비스", INFO), ("체크섬 대조", ACC), ("비공개 경로", WARN)])
d.save("10-04.proxy.svg")
print("ok 10-04 proxy")
