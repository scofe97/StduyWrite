# 04-02.cni-contract — 명세가 작아서 구현이 다양해졌다
# 본문 요구: "CNI 명세 1.1.0 의 연산은 여섯 (ADD·DEL·CHECK·STATUS·VERSION·GC) … 설정 JSON 을 stdin 으로
#           주고 결과 JSON 을 stdout 으로 받는다 … 플러그인 바이너리는 얇은" + IPAM 분리.
# 타입 스펙: type-architecture.md — 런타임·플러그인 바이너리·IPAM 세 구성요소와 stdin/stdout 연결
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, PAPER, KR, MONO

W, H = 1000, 448
d = D(W, H, "CNI SPEC 1.1.0 · SIX OPERATIONS",
      "플러그인이 지켜야 할 것은 연산 여섯과 JSON 두 줄기뿐",
      "런타임이 바이너리를 실행하며 설정 JSON 을 stdin 으로 주고 결과 JSON 을 stdout 으로 받는다.",
      lead="계약이 작아서 구현이 다양해졌다")

BY, BH = 124, 216
d.box(32, BY, 232, BH, PAPER2, INFO, 1.1, 8)
d.t(148, BY + 56, "런타임", 14, INFO, KR, "middle", 600)
for i, ln in enumerate(["kubelet 의 요청을 받은", "컨테이너 런타임이", "플러그인을 실행"]):
    d.t(148, BY + 96 + i * 26, ddx.fit(ln, 12, 200, ln), 12, MUTED, KR)

PX, PW = 336, 328
d.box(PX, BY, PW, BH, PAPER2, RULE, 1.1, 8)
d.t(PX + PW // 2, BY + 36, "플러그인 바이너리", 13, INK, KR, "middle", 600)
d.t(PX + PW // 2, BY + 58, "얇은 실행 파일", 11, SOFT, KR)
d.tone(PX + 16, BY + 76, PW - 32, 116, ACC, 6, "12", 1.4)
OPS = [("ADD", "네트워크에 추가"), ("DEL", "제거"), ("CHECK", "상태 확인"),
       ("STATUS", "플러그인 상태"), ("VERSION", "버전 보고"), ("GC", "남은 자원 정리")]
for i, (op, sub) in enumerate(OPS):
    cx = PX + 16 + 49 + (i % 3) * 99
    cy = BY + 112 + (i // 3) * 48
    d.t(cx, cy, op, 13, ACC, MONO, "middle", 600)
    d.t(cx, cy + 20, ddx.fit(sub, 11, 92, sub), 11, MUTED, KR, "middle")

d.box(728, BY, 240, BH, PAPER2, WARN, 1.1, 8)
d.t(848, BY + 56, "IPAM", 14, WARN, MONO, "middle", 600)
for i, ln in enumerate(["IP 할당은", "한 번 더 분리된", "별도 플러그인"]):
    d.t(848, BY + 96 + i * 26, ddx.fit(ln, 12, 208, ln), 12, MUTED, KR)

d.path(f"M 272 {BY+72} L {PX-10} {BY+72}", MUTED, 1.5, m="ar")
d.t(300, BY + 60, "stdin", 11, MUTED, MONO)
d.path(f"M {PX-2} {BY+152} L 274 {BY+152}", MUTED, 1.5, m="ar")
d.t(300, BY + 140, "stdout", 11, MUTED, MONO)
d.path(f"M {PX+PW+8} {BY+108} L 718 {BY+108}", MUTED, 1.5, m="ar", dash="4 4")

d.t(36, 376, "입력은 설정 JSON, 출력은 결과 JSON · 명세는 상주 데몬을 요구하지 않음",
    12, MUTED, KR, "start")
d.legend(396, [("호출하는 쪽", INFO), ("IP 할당 분리", WARN), ("명세가 요구하는 전부", ACC)])
d.save("04-02.cni-contract.svg")
print("ok cni-contract")
