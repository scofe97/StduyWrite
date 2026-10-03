# 06-01 §5 — 같은 모양의 Service 둘이 clusterIP 한 필드로 레코드 종류별 응답이 어떻게 갈리는가.
# 명세 근거: kubernetes/dns specification.md §2.3.1(ClusterIP A)·§2.3.2(포트마다 SRV, 대상은 서비스 이름)·§2.3.3(PTR)·
#            §2.4.1(Ready 엔드포인트마다 A, Ready 가 없으면 NXDOMAIN)·§2.4.2(N × M SRV)·§2.4.3(hostname 있는 Ready 엔드포인트의 PTR).
# 값 근거: 원서 Example 6-1(10.0.0.100)·6-4(10.5.88.4~7).
# 타입 스펙: type-dp-security-matrix — 레코드 종류(행) × Service 종류(열) 격자에서 칸마다 답이 다른 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, KR, MONO

W, H = 880, 470
d = D(W, H, "LEARNING COREDNS · 06-01 §5",
      "같은 질문에 두 Service 가 다르게 답한다",
      "hello-world 는 clusterIP 를 가진 Service, headless 는 clusterIP: None 인 Service 다. "
      "레코드 종류마다 무엇이 나오는지 DNS 명세의 규칙과 원서 예의 값으로 채웠다.",
      "주황 칸이 이 절이 짚는 차이입니다")

COLS = [(20, 190, "질의"), (220, 310, "ClusterIP · hello-world"), (540, 320, "헤드리스 · headless")]
rows = [
    (("A", "이름으로 묻기"), ("10.0.0.100", "가상 IP 하나"), ("10.5.88.4 · .5 · .6 · .7", "Ready 엔드포인트마다")),
    (("PTR", "주소로 묻기"), ("가상 IP 의 PTR", "서비스 이름을 가리킴"), ("hostname 있는 엔드포인트만", "엔드포인트 이름을 가리킴")),
    (("SRV", "_http._tcp"), ("한 줄", "대상은 서비스 이름"), ("엔드포인트 × 포트 줄", "대상은 엔드포인트 이름")),
    (("Ready 0", "엔드포인트 없음"), ("A 10.0.0.100 그대로", "가상 IP 는 남는다"), ("NXDOMAIN", "명세가 정한 답")),
]

for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, cells in enumerate(rows):
    y = 132 + i * 64
    for k, (x, w, _) in enumerate(COLS):
        main, sub = cells[k]
        focal = (i == 0 and k == 2)
        if focal:
            d.tone(x, y, w, 56, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 56, PAPER2, RULE, 1.0, 6)
        ascii_main = not any("가" <= ch <= "힣" for ch in main)
        col = ACC if focal else (BAD if main == "NXDOMAIN" else INK)
        d.t(x + 12, y + 24, main, 14 if k == 0 else 13, col, MONO if ascii_main else KR, "start", 600)
        d.t(x + 12, y + 44, sub, 12, MUTED, KR, "start")

d.t(20, 412, "원서 예는 IPv4 · 이중 스택이면 A 와 AAAA 가 함께", 13, MUTED, KR, "start")
d.legend(428, [("clusterIP: None 이 바꾸는 칸", ACC)])
d.save("06-01.record-matrix.svg")
