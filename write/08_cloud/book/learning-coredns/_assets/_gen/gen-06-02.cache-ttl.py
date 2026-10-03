# 06-02 §4 — cache 30 아래에서 응답이 캐시에 남는 시간: 상한 30 으로 자르고 하한 5 로 받친다.
# 소스 근거: cache README — "TTL only caps the cache duration and does not extend it" ·
#            "The minimum cache duration defaults to 5 seconds". kubernetes README — "ttl ... The default is 5 seconds."
#            kubeadm 판의 ttl 30 은 manifests.go. 상류 TTL 300·2 는 설명용 예시 값이다.
# 타입 스펙: type-process — 레코드 TTL → 상한 → 하한 → 캐시 기간의 단계를 경우 넷이 같은 열로 지난다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 520
d = D(W, H, "LEARNING COREDNS · 06-02 §4",
      "상한 30 으로 자르고 하한 5 로 받친다",
      "cache 30 은 레코드 TTL 을 30초 위로 넘기지 않게 자를 뿐 늘리지는 않는다. 현행 cache 는 여기에 최소 캐시 기간 5초를 두어, "
      "TTL 이 2초인 응답도 5초 동안 캐시에 남긴다.",
      "주황 칸이 원서에 없는 하한이 일하는 자리입니다")

COLS = [(20, 220, "응답"), (250, 140, "레코드 TTL"), (400, 160, "상한 30 적용"),
        (570, 140, "하한 5 적용"), (720, 140, "캐시 기간")]
rows = [
    (("외부 이름", "상류 TTL 300"), "300", "30", "30", "30초"),
    (("외부 이름", "상류 TTL 2"), "2", "2", "5", "5초"),
    (("클러스터 이름", "kubernetes 기본 ttl"), "5", "5", "5", "5초"),
    (("클러스터 이름", "ttl 30 을 준 경우"), "30", "30", "30", "30초"),
]
FOCAL = (1, 3)
Y0, PITCH, RH = 132, 70, 60

for k, (x, w, head) in enumerate(COLS):
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, (name, *vals) in enumerate(rows):
    y = Y0 + i * PITCH
    x0, w0, _ = COLS[0]
    d.box(x0, y, w0, RH, PAPER2, RULE, 1.0, 6)
    d.t(x0 + 12, y + 26, name[0], 14, INK, KR, "start", 600)
    d.t(x0 + 12, y + 46, name[1], 12, MUTED, KR, "start")
    for k, v in enumerate(vals, start=1):
        x, w, _ = COLS[k]
        focal = (i, k) == FOCAL
        if focal:
            d.tone(x, y, w, RH, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
        d.t(x + 12, y + 37, v, 15, ACC if focal else INK, KR if "초" in v else MONO, "start", 600)
        if k < 4:
            nx = COLS[k + 1][0]
            d.path(f"M {x + w + 2} {y + RH / 2} L {nx - 3} {y + RH / 2}", SOFT, 1.1, m="soft")

d.t(20, 430, "원서 · 레코드 TTL 과 캐시 TTL 중 작은 쪽 · 현행 README · 최소 캐시 기간 5초 (MINTTL)", 13, MUTED, KR, "start")
d.t(20, 454, "클러스터 이름 두 줄은 원서 판 Corefile 기준 · kubeadm 판은 cluster.local 성공 응답을 캐시하지 않음", 13, MUTED, KR, "start")

d.legend(472, [("하한이 올린 값", ACC)])
d.save("06-02.cache-ttl.svg")
