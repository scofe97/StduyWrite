# 03-01.cgroup-subsystems — 자원마다 다른 컨트롤러, v2 에서 갈린 운명
# 본문 요구: §3 은 자원 네 종류와 컨트롤러 이름을 목록으로 적고, 그 아래 산문에서
#           "v1 기준이라 v2 에서는 달라진다 — cpu+cpuacct 통합, net_cls 는 v2 에 없다"를 말한다.
#           목록과 산문이 갈려 있어 "내 자원은 v2 에서 어떻게 됐나"를 한 자리에서 못 본다.
#           행(자원) × 열(세대)의 대조가 본문이 요구하는 형태다.
# 타입 스펙: type-dp-security-matrix.md 의 격자 문법을 비교 행렬로 쓴다. 행이 자원,
#           마지막 열이 판정 축(v2 에서 어떻게 됐나)이라 focal_col 로 그 열을 세운다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 664
X0, GAP, ROW_H, HDR_Y = 32, 12, 84, 140
COLS = [(180, "자원"), (264, "무엇을 정하는가"), (224, "cgroup v1 — 책 기준"), (224, "cgroup v2 — 현재 기본")]

ROWS = [
    ([("CPU", "프로세서 시간"),
      ("최소 지분을 보장한다", "몰릴 때 나눠 갖는 비율"),
      ("cpu + cpuacct", "제한과 계량이 따로"),
      ("cpu", "둘이 하나로 합쳐졌다")], INFO),
    ([("Memory", "메모리"),
      ("상한을 넘기면 커널이 죽인다", "K8s limits.memory 가 내려오는 자리"),
      ("memory", "이름 그대로"),
      ("memory", "역할도 그대로")], OK),
    ([("Disk I/O", "블록 장치"),
      ("읽기·쓰기 대역폭을 나눈다", "devices 와 헷갈리기 쉽다"),
      ("blkio", "장치 노드 제어는 devices"),
      ("io", "이름이 바뀌었다")], WARN),
    ([("Network", "나가는 패킷"),
      ("패킷에 표시를 남긴다", "실제 제한은 tc 가 그 표시로"),
      ("net_cls · net_prio", "마킹과 우선순위"),
      ("없다 — eBPF 가 대신", "v2 로 옮겨오지 않았다")], BAD),
]

d = D(W, H, "CGROUP SUBSYSTEMS · V1 - V2",
      "cgroup 서브시스템 — 자원마다 다른 컨트롤러, v2 에서 갈린 운명",
      "자원 네 종류를 행으로 두고 cgroup v1 컨트롤러와 v2 의 대응을 나란히 놓은 대조표. "
      "마지막 열이 판정 축이며, 네트워크 행만 v2 에 대응하는 컨트롤러가 없다.",
      lead="cgroup 은 자원 종류별로 컨트롤러가 나뉩니다 · v2 로 오며 통합·개명·소멸이 갈렸습니다")

ddx.matrix(d, X0, COLS, ROWS, HDR_Y, row_h=ROW_H, gap=GAP, focal_col=3)

BOTTOM = HDR_Y + 24 + len(ROWS) * (ROW_H + GAP)
d.t(X0, BOTTOM + 32, "책의 목록은 v1 기준입니다. 지금 배포판 기본은 v2 라, 같은 이름을 찾다 "
                     "없어서 헤매는 자리가 마지막 행입니다.", 12, MUTED, KR, "start")
d.legend(BOTTOM + 64, [("통합됨", INFO), ("그대로", OK), ("이름 바뀜", WARN), ("v2 에 없음", BAD)])
d.save("03-01.cgroup-subsystems.svg")
print("ok cgroup-subsystems")
