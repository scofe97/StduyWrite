# 02-01 §6 — 명령 한 줄이 커널로 내려갔다 돌아오는 경로.
# 타입 스펙: type-data-flow — 유저 랜드와 커널 사이로 데이터(레지스터 · 번호)와 제어권이 건너가는 경로.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 560
d = D(W, H, "LEARNING MODERN LINUX · 02-01 §6",
      "x86-64 시스템 콜 진입과 복귀 흐름",
      "syscall 로 커널에 진입해 switch 분기를 거쳐 복귀하는 세 걸음.",
      "레지스터 인자 적재 → entry_SYSCALL_64 → do_syscall_64 → x64_sys_call → SYSRETQ 복귀")

# 좌우 구획 (간격을 70px로 확보해 경계 칩 겹침 방지)
UX = 30
UW = 200
KX = 300
KW = 550

# 경계선
d.line(258, 96, 258, 396, RULE, 1.0, "4 4")
d.t(258, 88, "Ring 3 (유저) | Ring 0 (커널)", 11, SOFT, MONO, "middle")

# 1. 유저 랜드 상단: 시스템 콜 요청
U1_Y = 104
U1_H = 160
d.box(UX, U1_Y, UW, U1_H, PAPER2, RULE, 1.0, 8)
d.t(UX + 14, U1_Y + 22, "1. 유저 랜드 (래퍼)", 12, INK, KR, "start", 600)
d.chip(UX + 155, U1_Y + 20, "glibc", INFO, 11)

lines_u1 = [
    ("openat() 호출", "라이브러리 호출", INK),
    ("rax = 257", "__NR_openat 번호 적재", ACC),
    ("syscall 실행", "CPU 특권 모드 전환", ACC),
]
for k, (lcode, ldesc, lc) in enumerate(lines_u1):
    ly = U1_Y + 38 + k * 38
    d.box(UX + 10, ly, UW - 20, 34, PAPER, RULE, 0.8, 4)
    d.t(UX + 18, ly + 15, lcode, 11, lc, MONO if k > 0 else KR, "start", 600)
    d.t(UX + 18, ly + 28, ldesc, 11, MUTED, KR, "start")

# 2. 커널 진입: entry_SYSCALL_64
K1_X, K1_Y, K1_W, K1_H = KX, 104, 255, 160
d.box(K1_X, K1_Y, K1_W, K1_H, PAPER2, ACC, 1.2, 8)
d.t(K1_X + 14, K1_Y + 22, "2. 어셈블리 진입점", 12, ACC, KR, "start", 600)
d.chip(K1_X + 185, K1_Y + 20, "entry_64.S", ACC, 11)

lines_k1 = [
    ("entry_SYSCALL_64", "하드웨어 진입점", ACC),
    ("커널 스택 전환", "유저 rsp 는 따로 보관", MUTED),
    ("pt_regs 스택 저장", "유저 레지스터 백업", INK),
]
for k, (lcode, ldesc, lc) in enumerate(lines_k1):
    ly = K1_Y + 38 + k * 38
    d.box(K1_X + 10, ly, K1_W - 20, 34, PAPER, RULE, 0.8, 4)
    d.t(K1_X + 18, ly + 15, lcode, 11, lc, MONO if k == 0 else KR, "start", 600)
    d.t(K1_X + 18, ly + 28, ldesc, 11, MUTED, KR, "start")

# 3. C 레벨 디스패처: do_syscall_64 & x64_sys_call
K2_X, K2_Y, K2_W, K2_H = KX + 285, 104, 265, 160
d.box(K2_X, K2_Y, K2_W, K2_H, PAPER2, WARN, 1.2, 8)
d.t(K2_X + 14, K2_Y + 22, "3. C 디스패처", 12, WARN, KR, "start", 600)
d.chip(K2_X + 195, K2_Y + 20, "common.c", WARN, 11)

lines_k2 = [
    ("do_syscall_64()", "ptrace · seccomp 검사", INK),
    ("do_syscall_x64()", "번호 범위 검사", MUTED),
    ("x64_sys_call(nr)", "switch 문으로 분기", WARN),
]
for k, (lcode, ldesc, lc) in enumerate(lines_k2):
    ly = K2_Y + 38 + k * 38
    d.box(K2_X + 10, ly, K2_W - 20, 34, PAPER, RULE, 0.8, 4)
    d.t(K2_X + 18, ly + 15, lcode, 11, lc, MONO, "start", 600)
    d.t(K2_X + 18, ly + 28, ldesc, 11, MUTED, KR, "start")

# 4. 실제 핸들러 실행: __x64_sys_openat
K3_X, K3_Y, K3_W, K3_H = KX + 285, 290, 265, 96
d.box(K3_X, K3_Y, K3_W, K3_H, PAPER2, OK, 1.2, 8)
d.t(K3_X + 14, K3_Y + 22, "4. 핸들러 실행", 12, OK, KR, "start", 600)
d.t(K3_X + 18, K3_Y + 48, "__x64_sys_openat()", 12, OK, MONO, "start", 600)
d.t(K3_X + 18, K3_Y + 68, "VFS 파일 열기 수행", 11, MUTED, KR, "start")
d.t(K3_X + 18, K3_Y + 84, "결과(fd)를 regs->ax 에 저장", 11, INK, KR, "start")

# 5. 복원 및 복귀 처리
K4_X, K4_Y, K4_W, K4_H = KX, 290, 255, 96
d.box(K4_X, K4_Y, K4_W, K4_H, PAPER2, OK, 1.2, 8)
d.t(K4_X + 14, K4_Y + 22, "5. 레지스터 복원 & 복귀", 12, OK, KR, "start", 600)
d.t(K4_X + 18, K4_Y + 48, "pt_regs 레지스터 복원", 11, INK, KR, "start", 600)
d.t(K4_X + 18, K4_Y + 68, "시그널 · 재스케줄링 점검", 11, MUTED, KR, "start")
d.t(K4_X + 18, K4_Y + 84, "대개 SYSRETQ, 아니면 IRET", 11, OK, MONO, "start")

# 6. 유저 랜드 복귀 후 결과 수신
U2_Y = 290
U2_H = 96
d.box(UX, U2_Y, UW, U2_H, PAPER2, RULE, 1.0, 8)
d.t(UX + 14, U2_Y + 22, "6. 유저 랜드 실행 재개", 12, INK, KR, "start", 600)
d.t(UX + 18, U2_Y + 48, "rax 반환값 수신 (fd)", 11, INK, MONO, "start", 600)
d.t(UX + 18, U2_Y + 68, "오류 시 errno 설정", 11, MUTED, KR, "start")
d.t(UX + 18, U2_Y + 84, "애플리케이션 다음 코드 진행", 11, MUTED, KR, "start")

# 직교 화살표 연결 1 -> 2: syscall 진입
mid_u_k = (UX + UW + K1_X) / 2  # (230 + 300) / 2 = 265
d.arrow([(UX + UW - 10, U1_Y + 131), (mid_u_k, U1_Y + 131), (mid_u_k, K1_Y + 55), (K1_X - 4, K1_Y + 55)], ACC, "acc", 1.4)
d.chip(mid_u_k, U1_Y + 93, "syscall", ACC, 11)

# 화살표 연결 2 -> 3: do_syscall_64 C 진입 (수평 직교)
d.arrow([(K1_X + K1_W - 8, K1_Y + 76), (K2_X + 8, K2_Y + 76)], WARN, "warn", 1.3)
d.t((K1_X + K1_W + K2_X) / 2, K1_Y + 66, "C 진입", 11, WARN, KR, "middle")

# 화살표 연결 3 -> 4: switch 분기 (수직 직교)
d.arrow([(K2_X + K2_W / 2, K2_Y + K2_H - 8), (K3_X + K3_W / 2, K3_Y + 6)], WARN, "warn", 1.3)
d.t(K2_X + K2_W / 2 + 36, (K2_Y + K2_H + K3_Y) / 2, "switch", 11, WARN, KR, "middle")

# 화살표 연결 4 -> 5: 반환 (수평 직교)
d.arrow([(K3_X + 8, K3_Y + K3_H / 2), (K4_X + K4_W - 8, K4_Y + K4_H / 2)], OK, "ok", 1.3)
d.t((K3_X + K4_X + K4_W) / 2, K3_Y + K3_H / 2 - 8, "반환", 11, OK, KR, "middle")

# 화살표 연결 5 -> 6: SYSRETQ 복귀 (수평 직교)
d.arrow([(K4_X - 4, K4_Y + 54), (UX + UW + 4, U2_Y + 54)], OK, "ok", 1.4)
d.chip(mid_u_k, K4_Y + 36, "SYSRETQ", OK, 11)

# 하단 강조 배너
d.tone(UX, 404, W - 60, 72, ACC, 8, "0C", 1.2)
d.t(UX + 16, 426, "모드 전환 비용 (Mode Switch)", 13, ACC, KR, "start", 600)
d.t(UX + 16, 446, "진입마다 레지스터 저장과 복원이 붙는다", 11, INK, KR, "start")
d.t(UX + 16, 464, "호출 횟수를 줄이는 배치 읽기가 이득을 내는 이유", 11, MUTED, KR, "start")

# 범례
d.legend(496, [
    ("유저 랜드", INFO),
    ("어셈블리 진입점", ACC),
    ("C 디스패처 (switch)", WARN),
    ("핸들러 및 복귀", OK),
])

d.save("02-01.syscall-path.svg")
print("ok 02-01.syscall-path")
