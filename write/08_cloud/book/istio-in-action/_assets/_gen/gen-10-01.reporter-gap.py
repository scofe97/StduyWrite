# 10-01 §8 같은 실패를 두 리포터가 다르게 기록한다.
# 본문(원문 10.4.1): 서버가 성공률 100% 를 보고하는 이유는 "the Envoy proxy marks the response code for
#       downstream terminated requests with the value 0, which is not a 5xx response and hence doesn't count
#       toward the failure rate." 클라이언트는 같은 요청을 504 로 적으므로 실패로 집계된다.
#       그림 10.14 는 클라이언트 성공률이 약 70% 임을 보이고, 저자는 20~30% 실패면 즉시 대응이라고 적는다.
#       10.4.2 의 Prometheus 질의가 reporter="destination" 과 response_flags="DC" 를 쓰는 근거가 이 갈림이다.
# 같은 판정(5xx 인가)을 두 번 두는 것이 요점이다 — 질문은 같고 들어오는 값이 달라 결과가 갈린다.
# 타입 스펙: type-flowchart — 판단 논리. 타원(시작·끝) · 마름모(판단, 출구 둘) · 사각형(행동).
#           예는 오른쪽, 아니오는 아래, 모든 갈래에 라벨, accent 는 갈래 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 880
d = D(W, H, "ISTIO IN ACTION · 10-01 §8",
      "0 은 5xx 가 아니라서 실패로 세지 않는다",
      "같은 타임아웃 하나를 두 프록시가 각자 기록하는데, 실패율 집계가 5xx 여부만 보기 때문에 한쪽에서만 "
      "실패로 잡힌다. 색이 붙은 갈래가 서버 대시보드를 100% 로 만드는 자리다.",
      "그래서 파드를 지목할 때는 destination 이 적은 DC 를 조건으로 겁니다")

def oval(x, y, w, h, label, sub=None, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 22)
    c = ACC if focal else INK
    if sub:
        d.t(x + w / 2, y + h / 2 - 2, label, 13, c, KR, "middle", 600)
        d.t(x + w / 2, y + h / 2 + 18, sub, 11, MUTED, MONO)
    else:
        d.t(x + w / 2, y + h / 2 + 5, label, 13, c, KR, "middle", 600)

def step(x, y, w, h, label, sub):
    d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 26, label, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, y + 46, sub, 9, MUTED, MONO)

def diamond(cx, cy, l1, l2, focal=False):
    c = ACC if focal else RULE
    d.o.append(f'<path d="M {cx-160} {cy} L {cx} {cy-56} L {cx+160} {cy} L {cx} {cy+56} Z" '
               f'fill="{ACC + "0C" if focal else PAPER2}" stroke="{c}" stroke-width="{1.4 if focal else 1}"/>')
    d.t(cx, cy - 4, l1, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(cx, cy + 16, l2, 12, ACC if focal else INK, KR, "middle", 600)

CA, CB = 232, 768

oval(CA - 170, 112, 340, 56, "업스트림이 0.5초를 넘긴다", "catalog v2 인스턴스 하나")
step(CA - 170, 212, 340, 68, "게이트웨이 프록시가 적는다", "504 · response_flags UT")
diamond(CA, 380, "적은 응답 코드가", "5xx 인가")
step(CB - 170, 348, 340, 68, "실패로 집계된다", "client success rate ~ 70%")
step(CA - 170, 500, 340, 68, "업스트림 커넥션을 끊는다", "resetting pool request")
step(CB - 170, 500, 340, 68, "catalog 프록시가 적는다", "0 · response_flags DC")
diamond(CB, 668, "적은 응답 코드가", "5xx 인가", focal=True)
oval(CA - 170, 640, 340, 56, "성공으로 집계된다", "server success rate 100%", focal=True)

d.arrow([(CA, 168), (CA, 206)], MUTED, "ar", 1.4)
d.arrow([(CA, 280), (CA, 322)], MUTED, "ar", 1.4)
d.arrow([(CA + 160, 380), (CB - 172, 380)], MUTED, "ar", 1.4)
d.arrow([(CA, 436), (CA, 494)], MUTED, "ar", 1.4)
d.arrow([(CA + 170, 534), (CB - 172, 534)], MUTED, "ar", 1.4)
d.arrow([(CB, 568), (CB, 610)], MUTED, "ar", 1.4)
d.arrow([(CB - 160, 668), (CA + 172, 668)], ACC, "acc", 1.5)

d.t((CA + CB) / 2, 366, "예", 12, MUTED, KR, "middle", 600)
d.t(CA + 22, 470, "아니오 · 프록시가 먼저 끊는다", 12, MUTED, KR, "start", 600)
d.t((CA + CB) / 2, 654, "아니오 · 0 은 5xx 가 아니다", 12, ACC, KR, "middle", 600)

d.t(32, 772, "같은 판정을 두 번 지나는데 들어오는 값이 달라 결과가 갈린다 — 옳은 쪽은 클라이언트가 적은 값이다", 11, SOFT, KR, "start")
d.t(32, 796, "Grafana 는 서비스 뒤의 모든 워크로드를 합쳐 보이므로 파드 하나를 지목하려면 Prometheus 로 내려간다", 11, MUTED, KR, "start")
d.legend(820, [("서버 대시보드를 100% 로 만드는 갈래", ACC), ("같은 요청의 다른 기록", MUTED)])
d.save("10-01.reporter-gap.svg")
