# 04-02.cni-contract — 명세가 작아서 구현이 다양해졌다
# 본문 요구: "지원해야 하는 연산은 넷뿐 (ADD·DEL·CHECK·VERSION) … 설정 JSON 을 stdin 으로
#           주고 결과 JSON 을 stdout 으로 받는다 … 플러그인 바이너리는 얇은" + IPAM 분리.
# 타입 스펙: type-architecture.md — 런타임·플러그인 바이너리·IPAM 세 구성요소와 stdin/stdout 연결
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, PAPER, KR, MONO

W, H = 1000, 496
d = D(W, H, "CNI SPEC · FOUR OPERATIONS",
      "플러그인이 지켜야 할 것은 네 연산과 JSON 두 줄기뿐",
      "런타임이 바이너리를 실행하며 설정 JSON 을 stdin 으로 주고 결과 JSON 을 stdout 으로 받는다.",
      lead="계약이 작아서 구현이 다양해졌다 — 이 절의 제목이 뜻하는 바다")

BY, BH = 168, 216
d.box(32, BY, 232, BH, PAPER2, INFO, 1.1, 8)
d.t(148, BY + 56, "런타임", 14, INFO, KR, "middle", 600)
for i, ln in enumerate(["Kubernetes 에서는", "kubelet", "한 번에 플러그인 하나"]):
    d.t(148, BY + 96 + i * 26, ddx.fit(ln, 12, 200, ln), 12, MUTED, KR)

PX, PW = 336, 328
d.box(PX, BY, PW, BH, PAPER2, RULE, 1.1, 8)
d.t(PX + PW // 2, BY + 36, "플러그인 바이너리", 13, INK, KR, "middle", 600)
d.t(PX + PW // 2, BY + 58, "얇은 실행 파일", 11, SOFT, KR)
d.tone(PX + 16, BY + 76, PW - 32, 116, ACC, 6, "12", 1.4)
for i, op in enumerate(["ADD", "DEL", "CHECK", "VERSION"]):
    cx = PX + 16 + 74 + (i % 2) * 148
    cy = BY + 112 + (i // 2) * 48
    d.t(cx, cy, op, 13, ACC, MONO, "middle", 600)
    d.t(cx, cy + 20, ["네트워크에 추가", "제거", "이상 시 오류", "버전 보고"][i], 11, MUTED, KR)

d.box(728, BY, 240, BH, PAPER2, WARN, 1.1, 8)
d.t(848, BY + 56, "IPAM", 14, WARN, MONO, "middle", 600)
for i, ln in enumerate(["IP 할당은", "한 번 더 분리된", "별도 플러그인"]):
    d.t(848, BY + 96 + i * 26, ddx.fit(ln, 12, 208, ln), 12, MUTED, KR)

d.path(f"M 272 {BY+72} L {PX-10} {BY+72}", MUTED, 1.5, m="ar")
d.t(300, BY + 60, "stdin", 11, MUTED, MONO)
d.path(f"M {PX-2} {BY+152} L 274 {BY+152}", MUTED, 1.5, m="ar")
d.t(300, BY + 140, "stdout", 11, MUTED, MONO)
d.path(f"M {PX+PW+8} {BY+108} L 718 {BY+108}", MUTED, 1.5, m="ar", dash="4 4")

d.t(36, 424, "설정 JSON 이 들어가고 결과 JSON 이 나오는 것이 전부다 — 데몬도 상주 프로세스도 요구하지 않는다",
    12, MUTED, KR, "start")
d.legend(436, [("호출하는 쪽", INFO), ("IP 할당 분리", WARN), ("명세가 요구하는 전부", ACC)])
d.save("04-02.cni-contract.svg")
print("ok cni-contract")
