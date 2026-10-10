# 타입 스펙: type-process — 설정 준비부터 CA 번들 결합, 롤아웃 재시작, 연결 상태 검증까지의 Cluster Mesh 연결 4단계 프로세스.
# 사실 출처: Cilium Up and Running 9장 cil9.txt 줄 448-473(Helm 템플릿), 584-593(CA 번들 추출), 617-623(rollout restart), 630-641(clustermesh status)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 340
d = D(W, H, "CILIUM UP AND RUNNING · 09-01 §4", "Cluster Mesh 구성과 TLS 신뢰 전파 4단계",
      "클러스터 설정부터 CA 번들 공유, 롤아웃 재시작, 연결 상태 검증까지의 절차",
      "단계마다 실행 명령 하나와 반영되는 구성 리소스")

Y_TOP, H_CARD, W_CARD, GAP, X0 = 104, 168, 200, 24, 26
steps = [
    ("01", "Helm 설정 준비", "클러스터 메타데이터", "cilium.yaml", "helm upgrade", INFO),
    ("02", "CA 번들 결합", "상호 신뢰 구축", "ca-bundle.crt", "cilium-ca 시크릿", WARN),
    ("03", "API 서버 재시작", "인증서 재적용", "rollout restart", "clustermesh-apiserver", ACC),
    ("04", "상태·연결 검증", "메시 연결 확인", "clustermesh status", "3/3 노드 연결 성공", OK),
]

for i, (num, title, sub, c1, c2, col) in enumerate(steps):
    x = X0 + i * (W_CARD + GAP)
    cx = x + W_CARD / 2
    if col == ACC:
        d.tone(x, Y_TOP, W_CARD, H_CARD, ACC, r=6, op="12", sw=1.4)
    else:
        d.box(x, Y_TOP, W_CARD, H_CARD, PAPER2, RULE, sw=0.9, r=6)

    d.chip(x + 28, Y_TOP + 20, num, col, size=10)
    d.t(cx, Y_TOP + 56, title, 13, INK, KR, "middle", 600)
    d.t(cx, Y_TOP + 76, sub, 11, MUTED, KR, "middle")

    d.line(x + 12, Y_TOP + 94, x + W_CARD - 12, Y_TOP + 94, RULE, 0.6)
    d.box(x + 10, Y_TOP + 106, W_CARD - 20, 48, PAPER, RULE, sw=0.7, r=4)
    d.t(cx, Y_TOP + 126, c1, 11, col, MONO if "." in c1 or "/" in c1 else KR, "middle", 600)
    d.t(cx, Y_TOP + 144, c2, 11, MUTED, MONO if any(c.isascii() and c.isalpha() for c in c2) else KR, "middle")

    if i < len(steps) - 1:
        ax = x + W_CARD
        d.arrow([(ax + 2, Y_TOP + 84), (ax + GAP - 2, Y_TOP + 84)], MUTED, "ar", 1.2)

d.legend(296, [
    ("선언적 설정", INFO),
    ("인증서 공유", WARN),
    ("재시작 롤아웃", ACC),
    ("검증 성공", OK),
])
d.save("09-01.mesh-setup-process.svg")
