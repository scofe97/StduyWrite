# a0-03 §2 규격 넷이 맡은 자리.
# 본문(부록 C.2): SPIFFE ID 는 신뢰 도메인 안에서 서비스를 유일하게 가리키고, Workload Endpoint 는
#       워크로드의 신원을 부트스트랩하며, Workload API 는 SPIFFE ID 가 담긴 인증서를 서명해 발급하고,
#       SVID 는 그 인증서로 표현된다.
# 타입 스펙: type-uml-class — 규격 넷이 각각 책임을 갖고 서로를 참조하는 구조가 논점이다.
#           클래스 상자에 이름과 책임을 적고 관계선에 방향과 의미를 단다.
#           축약: 상속이 없는 규격 묶음이라 연관(association)만 그린다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 596
d = D(W, H, "ISTIO IN ACTION · A0-03 §2",
      "이름 · 부트스트랩 · 발급 · 결과물이 하나씩",
      "규격 넷은 겹치지 않는 자리를 하나씩 맡는다. 엔드포인트가 데이터 플레인에 서고 API 가 컨트롤 "
      "플레인에 서며, 그 둘이 협력해 이름을 문서로 만든다. 색이 붙은 것이 그 결과물이다.",
      "SPIFFE ID 는 이름이고 SVID 는 그 이름이 서명까지 받은 문서입니다")

def cls(x, y, w, tag, name, rows, focal=False, c=None):
    hh, fh = 46, 22
    h = hh + fh * len(rows) + 12
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.line(x, y + hh, x + w, y + hh, RULE, 0.9)
    d.t(x + 16, y + 20, tag, 11, SOFT, MONO, "start", 600)
    d.t(x + 16, y + 38, name, 13, ACC if focal else (c or INK), MONO, "start", 600)
    for i, r in enumerate(rows):
        d.t(x + 16, y + hh + 18 + i * fh, r, 11, MUTED, KR, "start")
    return h

def lab(x, y, txt, c=MUTED):
    lw = sum(11 if '가' <= ch <= '힣' else 7 for ch in txt) + 16
    d.o.append(f'<rect x="{x - lw / 2}" y="{y - 13}" width="{lw}" height="18" rx="3" fill="{PAPER}"/>')
    d.t(x, y, txt, 11, c, KR, "middle", 600)

cls(28, 132, 280, "SPEC · 이름", "SPIFFE ID", ["신뢰 도메인 안에서", "서비스를 유일하게 가리킨다"])
cls(28, 320, 280, "SPEC · 데이터 플레인", "Workload Endpoint",
    ["워크로드 곁에 배포된다", "신원을 부트스트랩한다", "워크로드 증명을 한다"], c=INFO)
cls(400, 320, 280, "SPEC · 컨트롤 플레인", "Workload API",
    ["CA 키로 CSR 에 서명한다", "그 기능을 API 로 연다"], c=INFO)
cls(692, 132, 280, "SPEC · 결과물", "SVID",
    ["SPIFFE ID 를 담는다", "유효한 서명을 담는다", "공개 키는 선택"], focal=True)

# 관계 — 이름이 결과물에 인코딩되고, 엔드포인트가 API 에 요청해 결과물을 받는다
d.path("M 308 178 L 688 178", MUTED, 1.3, m="ar")
lab(498, 168, "인코딩된다")
d.arrow([(308, 380), (396, 380)], INFO, "info", 1.4)
lab(352, 366, "CSR 제출", INFO)
d.path("M 680 380 L 832 380 L 832 262", ACC, 1.5, m="acc")
lab(756, 366, "서명해 발급", ACC)

d.t(28, 500, "규격은 이름을 SVID 에 인코딩하는 과정과, 두 부품이 협력해 신원을 검증하고 할당하고 확인하는 방법을 함께 정의한다", 11, SOFT, KR, "start")
d.legend(524, [("규격이 내놓는 결과물", ACC), ("협력하는 두 부품", INFO)])
d.save("a0-03.spiffe-specs.svg")
