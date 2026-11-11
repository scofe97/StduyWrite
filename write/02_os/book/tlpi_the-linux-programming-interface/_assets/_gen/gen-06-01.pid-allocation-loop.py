# 06-01 §3 PID 순환 할당과 상한선 — 300번 랩어라운드와 pid_max
# 근거: TLPI 6.2 (06.txt 110-130 줄)
#      "When a new process is created, it is assigned the next sequentially available process ID."
#      "Once it has reached 32,767, the process ID counter is reset to 300, rather than 1."
#      "This is done because many low-numbered process IDs are in permanent use by system processes and daemons..."
#      man proc_sys_kernel(5): /proc/sys/kernel/pid_max default 32768, 64-bit max 2^22 (4,194,304)
# 타입 스펙: type-timeline
import sys
from pathlib import Path

sys.path.insert(0, ".")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 440
d = D(W, H, "TLPI · 06-01 §3",
      "PID 순차 발급과 300번 랩어라운드 재탐색 순환",
      "커널은 PID를 1씩 올리며 발급하다 pid_max에 닿으면 시스템 프로세스가 많이 쓰는 1~299를 건너뛰고 300부터 빈 번호를 다시 찾습니다.",
      "PID 번호 공간(0~32768)과 pid_max 도달 시 300으로 되돌아가는 순환 재탐색 메커니즘")

# 1. 상단: PID 번호 공간 구간 표시
AX, AY, AW, AH = 24, 114, 832, 90
d.box(AX, AY, AW, AH, PAPER2, RULE, 1.0, 6)

# 네 영역 분할:
# 영역 1: 1~299 (시스템 프로세스·데몬이 많이 쓰는 낮은 번호)
Z1_W = 190
d.tone(AX + 8, AY + 8, Z1_W, AH - 16, WARN, 4, "12", 1.0)
d.t(AX + 8 + Z1_W / 2, AY + 30, "PID 1 ~ 299", 13, WARN, MONO, "middle", 600)
d.t(AX + 8 + Z1_W / 2, AY + 50, "시스템·데몬이 다수 사용", 11, INK, KR)
d.t(AX + 8 + Z1_W / 2, AY + 68, "init(1) · kthreadd(2)", 11, MUTED, MONO)

# 영역 2: 300 (랩어라운드 리셋 지점)
Z2_X = AX + 8 + Z1_W + 12
Z2_W = 100
d.tone(Z2_X, AY + 8, Z2_W, AH - 16, ACC, 4, "20", 1.4)
d.t(Z2_X + Z2_W / 2, AY + 30, "PID 300", 14, ACC, MONO, "middle", 600)
d.t(Z2_X + Z2_W / 2, AY + 50, "리셋 기준점", 12, INK, KR, "middle", 600)
d.t(Z2_X + Z2_W / 2, AY + 68, "재탐색 시작", 11, ACC, KR)

# 영역 3: 301 ~ 32767 (일반 프로세스 순차 발급 공간)
Z3_X = Z2_X + Z2_W + 12
Z3_W = 360
d.tone(Z3_X, AY + 8, Z3_W, AH - 16, OK, 4, "10", 1.0)
d.t(Z3_X + Z3_W / 2, AY + 30, "PID 301 ~ 32,767", 13, OK, MONO, "middle", 600)
d.t(Z3_X + Z3_W / 2, AY + 50, "순차 발급 및 빈 번호 탐색 구간", 11, INK, KR)
d.t(Z3_X + Z3_W / 2, AY + 68, "새 프로세스 생성마다 카운터 1씩 증가", 11, MUTED, KR)

# 영역 4: 32768 (pid_max 상한선)
Z4_X = Z3_X + Z3_W + 12
Z4_W = 138
d.tone(Z4_X, AY + 8, Z4_W, AH - 16, BAD, 4, "15", 1.2)
d.t(Z4_X + Z4_W / 2, AY + 30, "32,768 (pid_max)", 12, BAD, MONO, "middle", 600)
d.t(Z4_X + Z4_W / 2, AY + 50, "기본 상한 도달", 11, INK, KR, "middle", 600)
d.t(Z4_X + Z4_W / 2, AY + 68, "랩어라운드 트리거", 11, BAD, KR)

# 2. 순환 경로 (32,768 -> 300)
LOOP_Y = 236
d.path(f"M {Z4_X + Z4_W / 2} {AY + AH - 8} V {LOOP_Y} H {Z2_X + Z2_W / 2 + 10} Q {Z2_X + Z2_W / 2} {LOOP_Y} {Z2_X + Z2_W / 2} {LOOP_Y - 10} V {AY + AH - 6}",
       ACC, 1.5, m="acc")
d.chip(480, LOOP_Y, "상한 도달 시 300으로 랩어라운드 (1~299 건너뜀)", ACC, 11)

# 순환 탐색 화살표 (300에서 301~32767 로 진입)
d.arrow([(Z2_X + Z2_W + 2, AY + AH / 2), (Z3_X - 4, AY + AH / 2)], OK, "ok", 1.4)

# 3. 하단 카드 2장: 핵심 원리와 현행 값
CY = 270
CW, CH = 408, 104

# 하단 왼쪽 카드: 300번 리셋의 이유
d.box(24, CY, CW, CH, PAPER2, RULE, 1.0, 6)
d.t(36, CY + 24, "300번 재탐색의 이유 (TLPI 6.2)", 13, INK, KR, "start", 600)
d.line(36, CY + 34, 24 + CW - 16, CY + 34, RULE, 0.8)
d.t(36, CY + 54, "1~299번 상태", 11, MUTED, KR, "start")
d.t(130, CY + 54, "상당수를 시스템 데몬이 상시 사용", 11, INK, KR, "start")
d.t(36, CY + 74, "1번부터 탐색 시", 11, MUTED, KR, "start")
d.t(130, CY + 74, "사용 중인 번호를 훑느라 시간 낭비", 11, WARN, KR, "start")
d.t(36, CY + 94, "300번 재탐색 시", 11, MUTED, KR, "start")
d.t(130, CY + 94, "빈 번호를 더 빨리 찾음", 11, OK, KR, "start")

# 하단 오른쪽 카드: 현행 pid_max 설정과 64비트 상한
d.box(448, CY, CW, CH, PAPER2, RULE, 1.0, 6)
d.t(460, CY + 24, "현행 커널 한계값 (proc_sys_kernel(5))", 13, INK, KR, "start", 600)
d.line(460, CY + 34, 448 + CW - 16, CY + 34, RULE, 0.8)
d.t(460, CY + 54, "pid_max 기본값", 11, MUTED, KR, "start")
d.t(564, CY + 54, "32,768 (최대 할당 가능 PID: 32,767)", 11, INK, MONO, "start")
d.t(460, CY + 74, "32비트 아키텍처", 11, MUTED, KR, "start")
d.t(564, CY + 74, "pid_max 상한 32,768 고정", 11, INK, KR, "start")
d.t(460, CY + 94, "64비트 아키텍처", 11, MUTED, KR, "start")
d.t(564, CY + 94, "최대 2^22 (4,194,304, PID_MAX_LIMIT)", 11, INFO, MONO, "start")

d.legend(396, [("낮은 번호 (1~299)", WARN), ("재탐색 시작점 (300)", ACC), ("일반 발급 구간", OK), ("상한 도달 (32,768)", BAD)])
out = "06-01.pid-allocation-loop.svg"
d.save(out)
print("ok", out)
