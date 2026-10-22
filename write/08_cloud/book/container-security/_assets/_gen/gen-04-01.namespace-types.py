# 타입 스펙: type-architecture — 프로세스 하나에서 일곱 종류의 namespace 로 갈라지는 팬아웃. 종류마다 격리 대상이 다르고, 이 편에서 unshare 로 만지는 셋(UTS·PID·mount)만 명령을 단다. focal 은 프로세스.
# 사실 출처: 노트 L53~L65(종류 일곱, 종류마다 정확히 하나, lsns), L67~L72(sudo lsns), L95~L96(--uts), L121(--pid), L223(--mount).
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, INFO, KR, MONO, PAPER2

W, H = 984, 652
RX, RW, RH, RS = 372, 576, 52, 64   # 행 상자: x, 폭, 높이, stride
RY0 = 120
PX, PY, PW, PH = 36, 288, 216, 100  # 프로세스 상자
BUS_X = 312


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "ARCHITECTURE · 04-01 §1",
      "프로세스는 일곱 종류의 namespace 에 각각 하나씩 속합니다",
      "프로세스 하나에서 UTS, Process ID, Mount points, Network, User and group IDs, IPC, Control groups 일곱 갈래가 나온다. "
      "종류마다 호스트명, 프로세스 ID, 마운트 지점, 네트워크 스택, 사용자와 그룹 ID, 프로세스 간 통신, cgroup 계층을 따로 보게 만든다. "
      "이 편에서 unshare 로 직접 만드는 것은 UTS, PID, mount 세 종류다.",
      lead="파란 행은 이 편에서 unshare 로 직접 만들어 보는 종류, 나머지는 소개만 합니다.")

# (종류, 격리 대상, 이 편의 명령)
KINDS = [
    ("UTS", "호스트명과 도메인명", "unshare --uts sh"),
    ("Process ID", "보이는 프로세스 ID", "unshare --pid --fork"),
    ("Mount points", "마운트 지점", "unshare --mount sh"),
    ("Network", "네트워크 스택", None),
    ("User and group IDs", "사용자와 그룹 ID", None),
    ("IPC", "프로세스 간 통신", None),
    ("Control groups", "cgroup 계층의 시야", None),
]

# 열 머리
d.t(RX + 16, RY0 - 12, "종류", 12, MUTED, KR, "start", 600)
d.t(RX + 200, RY0 - 12, "격리하는 대상", 12, MUTED, KR, "start", 600)
d.t(RX + 400, RY0 - 12, "이 편의 실습", 12, MUTED, KR, "start", 600)

# 연결선(버스 + 갈래)을 상자보다 먼저
pcy = PY + PH // 2
first_cy = RY0 + RH // 2
last_cy = RY0 + (len(KINDS) - 1) * RS + RH // 2
d.line(PX + PW + 2, pcy, BUS_X, pcy, SOFT, 1.3)
d.line(BUS_X, first_cy, BUS_X, last_cy, SOFT, 1.3)
for i in range(len(KINDS)):
    cy = RY0 + i * RS + RH // 2
    d.arrow([(BUS_X, cy), (RX - 4, cy)], SOFT, "soft", 1.3)

for i, (kind, target, cmd) in enumerate(KINDS):
    y = RY0 + i * RS
    fit(kind, 14, 176 - 16)
    fit(target, 13, 192)
    if cmd:
        d.tone(RX, y, RW, RH, INFO, 6, "14", 1.1)
    else:
        d.box(RX, y, RW, RH)
    d.t(RX + 16, y + RH / 2 + 5, kind, 14, INFO if cmd else INK, MONO, "start", 600)
    d.t(RX + 200, y + RH / 2 + 5, target, 13, INK, KR, "start")
    if cmd:
        fit(cmd, 12, 170)
        d.t(RX + 400, y + RH / 2 + 5, cmd, 12, INFO, MONO, "start")

# 프로세스(focal)
d.tone(PX, PY, PW, PH, ACC, 6, "14", 1.4)
d.t(PX + PW / 2, PY + 32, "프로세스", 14, ACC, KR, "middle", 600)
d.t(PX + PW / 2, PY + 58, "종류마다 정확히 하나", 12, MUTED, KR, "middle")
d.t(PX + PW / 2, PY + 80, "부팅 직후엔 종류별 1개", 12, MUTED, KR, "middle")

d.t(PX + PW / 2, PY + PH + 32, "전체 목록 확인", 12, MUTED, KR, "middle")
d.t(PX + PW / 2, PY + PH + 52, "sudo lsns", 12, INFO, MONO, "middle")

d.legend(588, [("프로세스", ACC), ("이 편에서 실습", INFO), ("소개만", MUTED)])
d.save(str(ASSETS / "04-01.namespace-types.svg"))
print("ok 04-01 namespace-types")
