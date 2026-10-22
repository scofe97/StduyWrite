# 타입 스펙: type-sequence — 컨테이너가 execve 를 부르면 커널 훅이 eBPF 프로그램에 사건을 넘기고, 이름을 목록과 비교해 경보까지 간다. 원문 기준(ALT 첫 영역)으로는 eBPF 가 시스템 콜을 막지 못해 execve 가 그대로 성공하고, BPF LSM 이후(ALT 둘째 영역)에는 -EPERM 으로 거부한다. focal 은 eBPF 프로그램 레인.
# 사실 출처: 노트 L104~L127(Tracee execve 출력 · docker exec nginx ls · 이름을 허용·차단 목록과 비교), L140~L142(경보 · "eBPF 는 시스템 콜을 탐지할 수는 있어도 수정할 수는 없다"), L213~L215(BPF LSM · return -EPERM; · 커널 5.7, 2020-05).
#   마지막 execve 성공·execve 실패 반환 화살표는 "막지 못한다"·"동작을 거부한다"에서 도출했다.
# Layout conventions: 레인 4개 stride 224(x=176·400·624·848), 레인 w=192 h=56, 메시지 stride 52, ALT 프레임은 컨테이너·커널·eBPF 세 레인을 덮는다(좌 x=32 · 우 x=680). 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, RULE, PAPER, PAPER2

W, H = 960, 772


def kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "CONTAINER SECURITY · 13-01 §2",
      "eBPF 는 execve 를 관찰해 경보를 내지만 원문 기준으로 막지는 못합니다",
      "컨테이너가 execve 를 부르면 커널 훅이 eBPF 프로그램에 사건을 넘기고, 프로그램이 실행 파일 이름을 허용 목록·차단 목록과 비교해 경보를 낸다. "
      "원문 시점에는 시스템 콜을 수정하지 못해 execve 가 그대로 성공하고, BPF LSM 이후에는 return -EPERM 으로 거부한다.",
      "BPF LSM 은 커널 5.7(2020년 5월)에 병합됐습니다.")

LX = {"c": 176, "k": 400, "e": 624, "l": 848}
LW, LY, LH = 192, 104, 56
LANES = [
    ("c", "컨테이너", "nginx", False),
    ("k", "커널", "syscall", False),
    ("e", "eBPF 프로그램", "Tracee · Falco", True),
    ("l", "실행 파일 목록", "허용 · 차단", False),
]
YEND = 700


# 생명선과 프레임을 먼저 그려 메시지가 위로 오게 한다
for key, name, sub, focal in LANES:
    d.line(LX[key], LY + LH + 6, LX[key], YEND, RULE, 1.0, "3 6")

# ALT 프레임 — 두 영역
FX, FY, FW, FH = 32, 396, 648, 296
DIV = 556
d.o.append(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="4" fill="#F5F5F30A" stroke="{RULE}" stroke-width="1"/>')
d.o.append(f'<rect x="{FX}" y="{FY}" width="48" height="20" rx="2" fill="{PAPER}" stroke="{RULE}" stroke-width="1"/>')
d.t(FX + 24, FY + 14, "ALT", 11, MUTED, MONO, "middle")
d.t(FX + 12, FY + 40, "[원문 2020]", 12, BAD, KR, "start", 600)
d.line(FX + 8, DIV, FX + FW - 8, DIV, RULE, 1.0, "4 3")
d.t(FX + 12, DIV + 24, "[BPF LSM 이후]", 12, OK, KR, "start", 600)

# 레인 머리
for key, name, sub, focal in LANES:
    x = LX[key] - LW // 2
    fit(name, 14, LW - 24)
    if focal:
        d.tone(x, LY, LW, LH, ACC, 6, "1F", 1.4)
    else:
        d.box(x, LY, LW, LH, PAPER2, RULE, 1.0)
    d.t(LX[key], LY + 24, name, 14, ACC if focal else INK, kr(name), "middle", 600)
    d.t(LX[key], LY + 44, sub, 12, MUTED, kr(sub), "middle")


def msg(a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, sub_c=MUTED, lc=None):
    x1, x2 = LX[a], LX[b]
    s = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 8 * s} {y} L {x2 - 12 * s} {y}", c, 1.5, m=mk, dash=dash)
    mx = (x1 + x2) // 2
    d.t(mx, y - 10, label, 12, lc or c, kr(label), "middle", 600)
    if sub:
        d.t(mx, y + 20, sub, 12, sub_c, kr(sub), "middle")


# 관찰 구간
msg("c", "k", "execve /bin/ls", 212, sub="docker exec -it nginx ls")
msg("k", "e", "execve /bin/ls", 264, sub="관찰")
msg("e", "l", "/bin/ls", 316, sub="이름 비교")
# eBPF 자기 메시지 — 경보
sx, sy = LX["e"], 372
d.path(f"M {sx + 8} {sy - 10} L {sx + 56} {sy - 10} L {sx + 56} {sy + 10} L {sx + 12} {sy + 10}", WARN, 1.5, m="warn")
d.t(sx + 68, sy - 2, "경보 발생", 13, WARN, KR, "start", 600)
d.t(sx + 68, sy + 16, "Falco", 12, MUTED, MONO, "start")

# [원문 2020] — 막지 못한다
y5 = 468
d.path(f"M {LX['e'] - 8} {y5} L {LX['k'] + 56} {y5}", BAD, 1.6, dash="6 4")
xm = LX["k"] + 40
d.line(xm - 8, y5 - 8, xm + 8, y5 + 8, BAD, 2.0)
d.line(xm - 8, y5 + 8, xm + 8, y5 - 8, BAD, 2.0)
d.t((LX["k"] + LX["e"]) // 2 + 20, y5 - 10, "수정 · 차단 불가", 12, BAD, KR, "middle", 600)
d.t((LX["k"] + LX["e"]) // 2 + 20, y5 + 20, "원문: 탐지만 가능", 12, MUTED, KR, "middle")
msg("k", "c", "execve 성공", 520, MUTED, "ar", "6 4")

# [BPF LSM 이후] — 거부한다
msg("e", "k", "return -EPERM;", 616, OK, "ok", None, sub="LSM 훅에서 거부", lc=OK)
msg("k", "c", "execve 실패", 668, BAD, "bad", "6 4")

d.legend(716, [("eBPF 프로그램", ACC), ("경보", WARN), ("막지 못함", BAD), ("BPF LSM 이후", OK)])
d.save(str(ASSETS / "13-01.ebpf-detect-enforce.svg"))
print("ok 13-01 ebpf-detect-enforce")
