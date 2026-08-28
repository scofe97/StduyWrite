# 12-02 §1 — 조용히 지나가고 접속에서 터진다
# 본문이 "당위만 알면 어긋났을 때를 대비할 수 없다"고 짚는다. 그러니 규칙이 아니라
# 배포 단계가 전부 초록불인 장면을 보여야 한다. 실패 지점 하나만 focal.
# 타입 스펙: type-flowchart.md — 관문 다섯을 차례로 지나며 판정하는 사슬. 앞 넷이 다 통과하고 마지막에서만 실패한다는 것이
#           "여기까지 아무도 검증하지 않는다"는 주장이다.

#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 560, "KUBERNETES IN ACTION · 12-02",
      "검증하는 쪽이 클러스터 밖에 있다",
      "쿠버네티스는 인증서 내용과 host 규칙이 맞는지 보지 않는다. 배포 파이프라인은 전부 초록불인데 "
      "브라우저가 CN·SAN 을 접속한 도메인과 비교해 스스로 끊는다.",
      "인증서는 *.example.com, host 규칙은 kiada.other.com")

STEP = [("kubectl apply", "성공"), ("kubectl get ingress", "정상 표시"),
        ("컨트롤러 로그", "에러 없음"), ("프록시 설정 반영", "정상")]
BW, GP = 232, 26
X0 = 40
CX = [X0 + BW // 2 + i * (BW + GP) for i in range(4)]
for cx, (t, s) in zip(CX, STEP):
    d.box(cx - BW // 2, 220, BW, 84, PAPER2, OK, 1.1, 6)
    d.t(cx, 252, ddx.fit(t, 12, BW - 16, t), 12, OK, KR, "middle", 600)
    d.t(cx, 276, s, 11, MUTED, KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+5} 262 L {b-BW//2-9} 262", MUTED, 1.4, m="ar")
d.path(f"M {CX[3]+BW//2+5} 262 L 1052 262", BAD, 1.5, m="bad")

d.o.append(f'<rect x="1058" y="214" width="150" height="96" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(1133, 246, "브라우저 접속", 12, ACC, KR, "middle", 600)
d.t(1133, 270, "ERR_CERT_", 10, ACC, MONO)
d.t(1133, 286, "COMMON_NAME_INVALID", 8, ACC, MONO)

ddx.bracket(d, 40, 330, 336, "여기까지 아무도 검증하지 않는다", SOFT)
d.t(24, 424, "서버는 잘못된 인증서라도 그냥 내밀고, 검증은 클라이언트가 한다. 그래서 배포 파이프라인은 "
             "전부 초록불인데 사용자만 막힌다.", 11, MUTED, KR, "start")
d.t(24, 446, "와일드카드에도 12-01 §5 의 요소 단위 규칙이 그대로 적용된다 — *.example.com 은 "
             "api.example.com 을 덮지만 foo.api.example.com 은 덮지 못한다.", 11, MUTED, KR, "start")
d.legend(482, [("조용히 지나가는 단계", OK), ("처음 드러나는 자리", ACC)])
d.save("12-02-cert-host-mismatch-silent-failure.svg")
print("ok")
