# 12-02 §1 — 무엇이 보이느냐가 무엇을 할 수 있느냐를 정한다
# 두 방식 × 할 수 있는 일의 교차라 행렬. 호스트 분기는 양쪽 다 되고 경로 분기에서 갈리므로
# 그 열을 판정 축으로 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, INFO, OK, BAD, MUTED, SOFT, KR
import ddx

d = D(1216, 512, "KUBERNETES IN ACTION · 12-02",
      "TLS 가 감추는 것이 프록시가 읽어야 할 그 부분이다",
      "passthrough 에서 프록시가 보는 것은 17 03 03 으로 시작하는 암호문 바이트뿐이라, "
      "경로가 어디에 적혀 있는지조차 알 수 없다.",
      "암호가 어디서 풀리느냐가 모든 것을 가른다")

ddx.matrix(
    d, x0=24, hdr_y=140, row_h=92, gap=12, focal_col=2,
    cols=[(230, "방식"), (300, "프록시가 보는 것"), (280, "경로 분기"), (330, "호스트 분기")],
    rows=[
        ([("termination", "프록시가 인증서를 쥔다"), ("평문 HTTP", "GET /quote  Host: ..."),
          ("가능", "pathType 이 작동한다"),
          ("가능", "Host 헤더로")], OK),
        ([("passthrough", "파드가 인증서를 쥔다"), ("암호문 바이트", "17 03 03 ..."),
          ("불가능", "읽을 수가 없다"),
          ("가능", "SNI — 핸드셰이크는 평문")], BAD),
    ])

d.t(24, 396, "12-01 에서 커널이 경로로 가르지 못한 이유가 '페이로드를 안 읽어서'였다면 여기서는 "
             "'읽으려 해도 암호문이어서'다. 막히는 지점만 다르고 결과는 같다.", 11, MUTED, KR, "start")
d.legend(422, [("프록시가 읽는다", OK), ("프록시가 못 읽는다", BAD)])
d.save("12-02-termination-vs-passthrough-visibility.svg")
print("ok")
