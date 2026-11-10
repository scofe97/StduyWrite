# 08-02 학습 목표 뒤 전체 지도 — 절 여덟을 읽는 순서로, 절마다 그 절에서 여는 명령을 붙인다.
# 본문 절 제목(2026-11-10 개정)과 각 절에서 직접 돌린 명령을 그대로 옮겼다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 여는 명령)이 반복되고 읽는 순서가
#           화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
#           §2~§5 는 기본 도구, §6~§8 은 그 위에 얹히는 층으로 색을 나눈다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 880, 500
d = D(W, H, "LEARNING MODERN LINUX · 08-02",
      "자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다",
      "8장 둘째 구간의 절 여덟을 읽는 순서로 이은 지도. 카드 아래 줄은 그 절에서 직접 돌린 명령이다.",
      "원인 범주가 정해져야 다음 절의 명령이 순서를 갖습니다")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 88, 12, 22, 20, 112
cards = [
    ("§1", "느린 앱의 원인 범주", "메모리 · CPU · 네트워크 I/O", ACC),
    ("§2", "부하 평균과 메모리 열", "uptime · free · vmstat", INFO),
    ("§3", "CPU 시간과 대기", "time → real · user · sys", INFO),
    ("§4", "장치·소켓·열린 파일", "iostat · ss · lsof +L1", INFO),
    ("§5", "top 화면과 배치 모드", "top -b · ps -eo", INFO),
    ("§6", "계측의 밀기와 끌기", "UDP :8125 · GET /metrics", OK),
    ("§7", "추적의 소스와 훅", "uprobes · kprobes · eBPF", OK),
    ("§8", "Prometheus·Grafana", ":9100 · :9090 · :3000", OK),
]


def pos(i):
    return X0 + (i % 3) * (CW + GAPX), Y0 + (i // 3) * (CH + GAPY)


for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.3)
    else:
        bus = y1 + CH + 11
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.3, m="ar")

for i, (n, title, cmd, c) in enumerate(cards):
    x, y = pos(i)
    focal = c is ACC
    if focal:
        d.tone(x, y, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, c, 1.0, 8)
    d.t(x + 16, y + 26, n, 12, c, MONO, "start", 600)
    d.t(x + 48, y + 26, title, 13.5, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 60, cmd, 12, MUTED, MONO, "start")

d.legend(H - 44, [("증상을 범주로 나누는 절", ACC), ("리눅스 기본 도구", INFO), ("그 위에 얹히는 층", OK)])
d.save("08-02.chapter-overview.svg")
print("ok 08-02.chapter-overview")
