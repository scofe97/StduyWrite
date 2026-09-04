# 06-03 §4 — Deployment 한 장을 바깥에서 안으로 다섯 겹으로 읽는다.
# 원문 근거: replicas 2 와 RollingUpdate maxUnavailable 1 / serviceAccountName·볼륨·dnsPolicy Default 이고
#            "the dnsPolicy called 'Default' is not the default for pods. The default for pods is
#            ClusterFirst" / 컨테이너 하나에 프로세스 하나이며 "In the earlier kube-dns implementation,
#            these different functions ran as separate processes" / "CoreDNS requests a minimum of
#            one-tenth of a CPU, but does not put a limit on the CPU consumption" /
#            "The limit of 170 Mi ... was the same amount as set for the original kube-dns container" /
#            liveness 5회 실패면 재시작, readiness 통과면 clusterIP 부하 분산 풀에 들어간다.
# 타입 스펙: type-layers — 바깥 겹이 안쪽 겹을 품는 계층이고, 왼쪽 여백의 방향 표시가 논지다.
#           축약: 스펙의 폭 800~880 은 1000 viewBox 기준이라 880 캔버스에 비례로 줄여 740 을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 620
d = D(W, H, "LEARNING COREDNS · 06-03 §4",
      "Deployment 한 장을 다섯 겹으로 읽는다",
      "위에서 아래로 갈수록 안쪽 겹이다. 각 겹이 정하는 것과 그 값이 어디서 왔는지가 다르고, "
      "넷째 겹의 두 값이 이 편 제목의 숫자다.",
      "주황 겹이 kube-dns 에서 그대로 가져온 값입니다")

LX, LW, LH, Y0 = 100, 740, 68, 112
layers = [
    ("01", "Deployment spec", "복제본 2 · RollingUpdate maxUnavailable 1", False),
    ("02", "파드 템플릿", "serviceAccountName · 볼륨 · dnsPolicy Default", False),
    ("03", "컨테이너 하나", "프로세스 하나 · kube-dns 는 셋이었다", False),
    ("04", "자원과 보안", "CPU 상한 없음 · 메모리 170Mi · NET_BIND_SERVICE", True),
    ("05", "두 프로브", "활성 5회 실패면 재시작 · 준비 통과면 풀에 편입", False),
]

for i, (tag, name, sub, focal) in enumerate(layers):
    y = Y0 + i * LH
    if focal:
        d.tone(LX, y, LW, LH, ACC, 0, "12", 1.4)
    else:
        d.box(LX, y, LW, LH, PAPER2, RULE, 1.0, 0)
    d.t(LX + 16, y + 40, tag, 9, ACC if focal else SOFT, MONO, "start", 600)
    d.t(LX + 64, y + 40, name, 16, ACC if focal else INK, KR, "start", 600)
    d.t(LX + LW - 16, y + 40, sub, 12, MUTED, KR, "end")

d.path(f"M 60 {Y0 + 12} L 60 {Y0 + 5 * LH - 12}", SOFT, 1.4, m="soft")
d.t(20, Y0 - 8, "바깥에서", 12, SOFT, KR, "start")
d.t(20, Y0 + 5 * LH + 20, "안으로", 12, SOFT, KR, "start")

BOT = Y0 + 5 * LH
d.t(LX, BOT + 44, "2겹의 Default 는 파드의 기본값이 아니다 — 파드 기본은 ClusterFirst 이고 그것은 클러스터 DNS 를 본다", 13, MUTED, KR, "start")
d.t(LX, BOT + 68, "4겹의 CPU 는 상한이 없고 메모리만 있다. 메모리를 넘기면 커널이 죽이지만 CPU 는 느려질 뿐이다", 13, MUTED, KR, "start")
d.t(LX, BOT + 92, "170Mi 는 성능 계산이 아니라 kube-dns 와 같은 값이어야 해서 정해졌다", 13, MUTED, KR, "start")

d.legend(BOT + 120, [("호환에서 나온 값", ACC)])
d.save("06-03.deployment-layers.svg")
