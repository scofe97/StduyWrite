# 타입 스펙: type-data-flow — 필드(레인) 네 줄 × 단계 다섯 칸. 헬퍼 호출이 채운 값이 한 항목으로 모여 화면 한 줄이 된다.
# 사실 출처: 예제 저장소 chapter2/hello-buffer.py (HEAD 91ded4a) — struct data_t{int pid; int uid; char command[16]; char message[12];}
#   pid = bpf_get_current_pid_tgid() >> 32 (tgid 는 상위 32비트: linux v7.2 kernel/bpf/helpers.c 줄 232)
#   uid = bpf_get_current_uid_gid() & 0xFFFFFFFF (uid 는 하위 32비트: 같은 파일 줄 251~252)
#   출력 한 줄은 f"{pid} {uid} {command} {message}" ; 예시 값 11654 · node · Hello World 는 추출본 ebpf2.txt 의 출력(uid 는 그 출력에 없어 숫자를 적지 않는다).
#   data_t 크기 36바이트 = 4 + 4 + 16 + 12 (정렬 패딩 없음)
# Layout formulas(type-data-flow §2) 변형: 레인 4 · lane_h 76 · node_h 64 · header chip 16px. 단계 폭은 균일 112 대신 단계별 값으로 늘렸다(함수 이름이 길어서).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 520
d = D(W, H, "LEARNING EBPF · 02-02 §2",
      "헬퍼가 채운 값이 항목 하나로 모여 화면 한 줄이 된다",
      "hello() 는 pid·uid·command·message 를 헬퍼로 data_t 에 채우고, perf_submit 이 그 36바이트를 output 에 밀면 print_event 가 한 줄로 찍는다.",
      "네 필드가 한 항목으로 합쳐집니다")

TOP, LH, NH = 140, 76, 64
LANES = [("pid", "int"), ("uid", "int"), ("command", "char[16]"), ("message", "char[12]")]
COLX = [120, 360, 508, 660, 816]        # 단계별 노드 x
COLW = [212, 120, 124, 128, 132]
HEAD = ["01 헬퍼", "02 필드", "03 버퍼", "04 콜백", "05 출력"]

# 단계 머리
for i, (x, w) in enumerate(zip(COLX, COLW)):
    d.box(x + w/2 - 40, 100, 80, 20, PAPER2, RULE, 0.9, 10)
    d.t(x + w/2, 114, HEAD[i], 12, ACC if i == 2 else MUTED, KR, "middle", 600)
# 레인 구분선과 라벨
for k, (nm, ty) in enumerate(LANES):
    y = TOP + k * LH
    if k % 2 == 0:
        d.o.append(f'<rect x="12" y="{y}" width="{W-24}" height="{LH}" fill="#F5F5F3" fill-opacity="0.025"/>')
    d.t(24, y + LH/2 - 2, nm, 14, INK, MONO, "start", 600)
    d.t(24, y + LH/2 + 16, ty, 12, MUTED, MONO, "start")

HELP = [("bpf_get_current_pid_tgid()", ">> 32"),
        ("bpf_get_current_uid_gid()", "& 0xFFFFFFFF"),
        ("bpf_get_current_comm()", "버퍼 data.command"),
        ("bpf_probe_read_kernel()", "문자열 → data.message")]
VAL = [("11654", INFO), ("<uid>", INFO), ("\"node\"", INFO), ("\"Hello World\"", INFO)]

ys = []
for k in range(4):
    y = TOP + k * LH + (LH - NH) // 2
    ys.append(y)
    # 단계 1 — 헬퍼
    d.tone(COLX[0], y, COLW[0], NH, OK, 6, "12", 1.2)
    d.t(COLX[0] + COLW[0]/2, y + 28, HELP[k][0], 12, OK, MONO, "middle", 600)
    d.t(COLX[0] + COLW[0]/2, y + 48, HELP[k][1], 12, MUTED, KR if any("가" <= c <= "힣" for c in HELP[k][1]) else MONO)
    # 단계 2 — data_t 필드 값
    d.tone(COLX[1], y, COLW[1], NH, INFO, 6, "12", 1.2)
    d.t(COLX[1] + COLW[1]/2, y + 28, LANES[k][0], 12, MUTED, MONO)
    d.t(COLX[1] + COLW[1]/2, y + 48, VAL[k][0], 13, INFO, MONO, "middle", 600)
    cy = y + NH // 2
    d.arrow([(COLX[0] + COLW[0] + 2, cy), (COLX[1] - 6, cy)], OK, "ok", 1.5)
    d.arrow([(COLX[1] + COLW[1] + 2, cy), (COLX[2] - 6, cy)], INFO, "info", 1.5)

# 단계 3 — output 한 항목 (네 레인에 걸침)
OY, OH = ys[0], ys[3] + NH - ys[0]
d.o.append(f'<rect x="{COLX[2]}" y="{OY}" width="{COLW[2]}" height="{OH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
d.t(COLX[2] + COLW[2]/2, OY + OH/2 - 14, "output", 14, ACC, MONO, "middle", 600)
d.t(COLX[2] + COLW[2]/2, OY + OH/2 + 6, "data_t", 12, MUTED, MONO)
d.t(COLX[2] + COLW[2]/2, OY + OH/2 + 26, "36바이트", 12, MUTED, KR)

# 단계 4·5 — 레인 가운데
my = OY + OH // 2
PY = my - NH // 2
d.tone(COLX[3], PY, COLW[3], NH, OK, 6, "12", 1.2)
d.t(COLX[3] + COLW[3]/2, PY + 28, "print_event", 13, OK, MONO, "middle", 600)
d.t(COLX[3] + COLW[3]/2, PY + 48, "콜백", 12, MUTED, KR)
d.arrow([(COLX[2] + COLW[2] + 2, my), (COLX[3] - 6, my)], ACC, "acc", 1.8)

d.tone(COLX[4], PY, COLW[4], NH, WARN, 6, "12", 1.2)
d.t(COLX[4] + COLW[4]/2, PY + 28, "11654 <uid>", 13, WARN, MONO, "middle", 600)
d.t(COLX[4] + COLW[4]/2, PY + 48, "node Hello World", 12, MUTED, MONO)
d.arrow([(COLX[3] + COLW[3] + 2, my), (COLX[4] - 6, my)], WARN, "warn", 1.5)

d.legend(H - 56, [("헬퍼 호출", OK), ("필드 값", INFO), ("perf 버퍼 항목", ACC), ("화면 출력", WARN)])
d.save("02-02.field-fill.svg")
