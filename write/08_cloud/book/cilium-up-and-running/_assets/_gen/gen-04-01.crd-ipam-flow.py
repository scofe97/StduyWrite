# 타입 스펙: type-data-flow — CRD-backed 모드에서 외부 오퍼레이터가 CiliumNode.spec.ipam.available 을 채우고 에이전트가 Pod IP 와 status.ipam.inuse 를 갱신하는 흐름.
# 사실 출처: 추출본 ch04.txt 줄 636-647, docs.cilium.io/en/v1.20/network/concepts/ipam/crd/ (ipam: crd, spec.ipam.available, status.ipam.inuse, 15초 주기, 직접 라우팅).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 384
d = D(W, H, "CILIUM UP AND RUNNING · 04-01 §5", "CRD-backed 의 주소 목록 전달과 사용 기록",
      "외부 오퍼레이터가 CiliumNode 에 가용 주소를 적고 에이전트가 Pod 에 내준 뒤 사용 중 목록을 되씁니다",
      "ipam.mode=crd · 직접 라우팅만 지원 (노드 간 경로는 관리자 별도 설정)")

# 4열 배치
COLS = [
    (24, 180, "EXTERNAL", "외부 오퍼레이터", "주소 목록 작성", INFO),
    (256, 224, "CRD (AVAILABLE)", "CiliumNode", "spec.ipam.available", ACC),
    (532, 176, "AGENT", "cilium-agent", "Pod IP 선택·배정", OK),
    (760, 136, "POD", "Pod", "직접 라우팅 주소", OK),
]
BY, BH = 128, 76
for x, w, eye, title, sub, col in COLS:
    d.t(x + w / 2, BY - 12, eye, 8, SOFT, MONO, "middle")
    if col == ACC:
        d.tone(x, BY, w, BH, ACC, r=6, op="14", sw=1.4)
    else:
        d.box(x, BY, w, BH, PAPER2, col, 1.0, 6)
    d.t(x + w / 2, BY + 30, title, 13 if any("가" <= c <= "힣" for c in title) else 12, col if col != INFO else INK, KR if any("가" <= c <= "힣" for c in title) else MONO, "middle", 600)
    d.t(x + w / 2, BY + 52, sub, 12 if any("가" <= c <= "힣" for c in sub) else 11, MUTED, KR if any("가" <= c <= "힣" for c in sub) else MONO, "middle")

# 순방향 화살표
d.arrow([(204, BY + 38), (254, BY + 38)], INFO, "info", 1.5)
d.t(229, BY + 26, "기록", 12, MUTED, KR, "middle")
d.arrow([(480, BY + 38), (530, BY + 38)], ACC, "acc", 1.5)
d.t(505, BY + 26, "watch", 10, ACC, MONO, "middle")
d.arrow([(708, BY + 38), (758, BY + 38)], OK, "ok", 1.5)
d.t(733, BY + 26, "할당", 12, MUTED, KR, "middle")

# 역방향 상태 보고: agent -> CiliumNode status.ipam.inuse
SY, SH = 236, 52
d.box(256, SY, 224, SH, PAPER, WARN, 1.0, 6)
d.t(368, SY + 22, "CiliumNode · status.ipam.inuse", 11, WARN, MONO, "middle", 600)
d.t(368, SY + 40, "상태 갱신 최대 15초 간격", 12, MUTED, KR, "middle")
d.arrow([(620, BY + BH), (620, SY + 26), (482, SY + 26)], WARN, "warn", 1.4, "4 3")
d.t(564, SY + 16, "사용 중 보고", 12, WARN, KR, "middle")

d.legend(H - 52, [("외부 입력", INFO), ("가용 풀(핵심)", ACC), ("Pod 할당", OK), ("사용 중 상태", WARN)])
d.save("04-01.crd-ipam-flow.svg")
