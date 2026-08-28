# 08-03 §1 — 지금 만든다면 하나였을 둘
# 본문이 "기능이 수렴했지만 각자 진화한 탓에 차이가 남았다"로 틀을 잡고 세 축을 든다.
# 그러니 우열이 아니라 '어느 축에서 갈리는지'가 보이는 표여야 한다.
# 타입 스펙: type-dp-security-matrix.md — 행은 두 오브젝트, 열은 갈리는 축 셋이다. 우열이 아니라 어느 축에서 갈리는지가 논지라
#           칸 대조가 그 일을 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, KR
import ddx

d = D(1260, 604, "KUBERNETES IN ACTION · 08-03",
      "지금 만든다면 하나였을 둘",
      "Secret 이 ConfigMap 보다 먼저 나왔다. 초기 Secret 이 Base64 를 요구해 평문을 다루기 불편했고, "
      "그래서 ConfigMap 이 나중에 나왔다. 시간이 지나며 기능이 수렴했지만 흔적이 남았다.",
      "필드 구조 · type · 취급 방식 세 축에서 갈린다")

ddx.matrix(
    d, x0=24, hdr_y=148, row_h=88, gap=12, focal_col=3,
    cols=[(230, "갈리는 축"), (330, "Secret"), (330, "ConfigMap"), (300, "실제로 다른 점")],
    rows=[
        ([("필드 구조", "같은 것을 다른 이름으로"), ("data — Base64", "stringData — write-only"),
          ("binaryData — Base64", "data — 평문"),
          ("stringData 는 되읽히지 않는다", "쓰기 전용이다")], INFO),
        ([("type 필드", "쓰임을 선언한다"), ("Opaque · tls · dockerconfigjson", "종류가 정해져 있다"),
          ("없다", "전부 같은 취급"),
          ("타입이 형식을 강제한다", "tls 는 두 키를 요구")], INFO),
        ([("쿠버네티스 취급", "어떻게 다루나"), ("필요한 노드에만 배포", "노드에서 메모리에만 둔다"),
          ("제약 없이 배포", "디스크에 놓인다"),
          ("여기가 진짜 차이다", "노출면이 좁다")], ACC),
    ])

d.t(24, 480, "앞의 두 축은 이름과 형식의 흔적이지만, 마지막 축은 지금도 유효한 실질적 차이다 — "
             "그래서 비밀은 Secret 에 담는다.", 11, MUTED, KR, "start")
d.t(24, 502, "다만 Secret 도 기본 설정에서는 etcd 에 평문으로 저장된다. 저장 시 암호화는 따로 켜야 한다.",
     11, MUTED, KR, "start")
d.legend(528, [("남은 흔적", INFO), ("지금도 유효한 차이", ACC)])
d.save("08-03-secret-vs-configmap.svg")
print("ok")
