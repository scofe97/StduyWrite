# 05-02 §Pod 접근 — 왜 방법마다 Client IP 가 다른가
# 본문: "kiada 가 보는 Client IP 는 '마지막으로 kiada 에게 직접 연결을 연 그 주체' 의 IP 입니다."
#       "각 홉이 다음 홉에게 자기를 클라이언트로 보여주고, 최종 목적지는 맨 앞의 원래 요청자를
#        알 수 없습니다." + 택배 중계 비유 한 문단.
# 타입 스펙: type-dp-security-matrix.md — 네 방법 × 축 넷이라 비교 행렬. 판정 열은 본문이 한 문장으로 꿴 '마지막으로 붙은 것'
#           이다 — 그 열만 읽으면 Client IP 열이 따라 나온다.
#           본문이 한 문단을 들여 설명하는 택배 비유는 아래에 사슬로 한 번 더 놓는다.
#           행은 접근 방법 넷, 열은 홉 수·마지막으로 붙은 것·Client IP 인 격자다. focal 열이
#           "마지막으로 붙은 것" 이라 그 열만 읽으면 Client IP 가 따라 나온다.
#           아래 택배 사슬은 그 판정을 비유로 한 번 더 놓은 보조 띠라 격자 밖이다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 768
d = D(W, H, "KUBERNETES IN ACTION · 05-02",
      "Client IP 는 마지막으로 붙은 것의 IP 다",
      "홉이 몇 개 끼든 kiada 는 원래 요청자를 보지 못한다. TCP 연결은 바로 붙은 두 끝점 "
      "사이의 것이라, 각 중계점이 다음 상대에게 자기를 클라이언트로 소개하며 새 연결을 연다.",
      lead="그래서 중계가 가장 많은 방법 3 에서 원래 요청자와 가장 멀어져 127.0.0.1 이 찍힌다")

ddx.band(d, 104, 712, "판정 열 하나만 읽으면 오른쪽 열이 따라 나온다")

ddx.matrix(
    d, x0=56, hdr_y=190, row_h=74, gap=10, focal_col=2,
    # "2. 임시 클라이언트 Pod" 가 190-40=150px 를 5px 넘었다(fit 가드가 잡음).
    # 방법 열을 10px 넓히고 홉 수 열에서 그만큼 뺀다 — 전체 폭은 그대로다.
    cols=[(200, "방법"), (120, "홉 수"), (280, "마지막으로 붙은 것"),
          (260, "kiada 가 보는 Client IP")],
    rows=[
        ([("1. 워커 노드에서", "노드에 로그인해 curl"), ("0 개", "중계 없음"),
          ("노드", "브리지"), ("10.244.2.1", "노드 · 브리지 IP")], OK),
        ([("2. 임시 클라이언트 Pod", "클러스터 안에서 curl"), ("0 개", "중계 없음"),
          ("임시 Pod", "요청한 그 Pod"), ("10.244.1.13", "임시 Pod 의 IP")], OK),
        ([("3. port-forward", "로컬 포트로 터널"), ("3 개", "가장 많다"),
          ("Pod 자신의 loopback", "kubelet 이 lo 로 붙는다"),
          ("127.0.0.1", "자기 자신")], WARN),
        ([("4. API 서버 프록시", "kubectl get --raw"), ("1 개", "한 홉"),
          ("API 서버", "kubelet 을 건너뛴다"), ("172.18.0.5", "API 서버 IP")], INFO),
    ])

d.t(56, 578, "택배 중계로 비유하면 — 친구 문 앞에 마지막으로 물건을 놓고 간 사람만 보인다",
     12, SOFT, KR, "start")

CHAIN = [(120, "부산", "나 · 원래 요청자"), (310, "대전", "중계"), (500, "안양", "중계"),
         (690, "서울센터", "마지막 배달원"), (880, "친구", "받는 쪽")]
for i, (cx, t, s) in enumerate(CHAIN):
    last = i == len(CHAIN) - 2
    ddx.node(d, cx, 630, t, s, 150, 60, ACC if last else None, focal=last)
for (a, _, _), (b, _, _) in zip(CHAIN, CHAIN[1:]):
    ddx.hop(d, a, b, 630, ACC if a == 690 else MUTED, "acc" if a == 690 else "ar", half=75)

d.t(56, 688, "친구가 아는 것은 \"서울센터에서 왔다\" 뿐이고 부산은 연결 정보에 남지 않는다 — "
             "kiada 도 자기 문 앞의 마지막 배달원만 본다", 12, MUTED, KR, "start")
d.legend(728, [("중계 없음", OK), ("중계가 가장 많다", WARN), ("한 홉", INFO),
               ("마지막으로 붙은 것", ACC)])
d.save("05-02-access-methods-client-ip.svg")
print("ok access-methods")
