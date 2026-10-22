# 타입 스펙: type-sequence — 앱의 시스템 콜을 Sentry 가 가로챈 뒤 갈린다. 파일과 무관한 syscall 은 Sentry 안에서 재구현되어 호스트 커널로 가지 않고, 파일 접근 syscall 만 Gofer 를 거쳐 호스트 커널로 간다. focal 은 Sentry 안 재구현.
# 사실 출처: 노트 L159~L167(Sentry 가 syscall 가로챔 · seccomp 샌드박싱 · 파일시스템 직접 접근 불가 · Gofer 로 위임 · 그 밖은 Sentry 안 재구현), L180~L190(runsc-sandbox = Sentry · runsc-gofer · 호스트 ps 에 sleep 안 보임)
# Layout conventions: 라이프라인 4개(중심 x=132·372·612·852, stride 240), 레인 머리 폭 192 h=44 y=100, 메시지 stride 40(y=232 · 420~540), ALT 틀 x=300~924 y=256~564, 마지막 응답 y=604. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, INFO, KR, MONO, RULE, PAPER

W, H = 984, 676


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "SEQUENCE · 08-01 §4",
      "gVisor 에서 시스템 콜은 Sentry 가 받아 안에서 재구현하고, 파일 접근만 Gofer 로 넘어갑니다",
      "컨테이너 안 앱, Sentry, Gofer, 호스트 커널 네 라이프라인의 시퀀스. 앱의 시스템 콜을 Sentry 가 가로챈 뒤 분기한다. "
      "파일과 무관한 시스템 콜은 Sentry 안에서 재구현되어 호스트 커널로 전달되지 않는다. 파일 접근 시스템 콜은 Sentry 가 Gofer 에 위임하고 "
      "Gofer 가 호스트 커널에 요청해 결과가 거꾸로 돌아온다.",
      lead="Sentry 는 seccomp 로 샌드박싱되어 파일시스템에 직접 닿지 못하므로, 파일 접근은 별개 프로세스 Gofer 가 맡습니다.")

LANES = [
    (132, "컨테이너 안 앱", "sleep"),
    (372, "Sentry", "runsc-sandbox"),
    (612, "Gofer", "runsc-gofer"),
    (852, "호스트 커널", "Linux"),
]
LX = {n: x for x, n, _ in LANES}
LW, LY, LH = 192, 100, 44

# 라이프라인(레인 머리보다 먼저)
for x, n, sub in LANES:
    d.line(x, LY + LH + 6, x, 628, RULE, 1.0, "3 6")

# ALT 틀(메시지보다 먼저 깔아 둔다)
FX, FY, FW, FH = 300, 256, 624, 308
d.o.append(f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="4" fill="#F5F5F30A" stroke="{RULE}" stroke-width="1"/>')
d.o.append(f'<rect x="{FX}" y="{FY}" width="44" height="16" rx="2" fill="{PAPER}" stroke="{RULE}" stroke-width="1"/>')
d.t(FX + 22, FY + 12, "ALT", 9, MUTED, MONO)
d.t(FX + 84, FY + 32, "[파일과 무관한 syscall]", 12, MUTED, KR, "start")
DIV = 360
d.line(FX + 8, DIV, FX + FW - 8, DIV, RULE, 1.0, "4 3")
d.t(FX + 84, DIV + 20, "[파일 접근 syscall]", 12, MUTED, KR, "start")

for x, n, sub in LANES:
    d.box(x - LW // 2, LY, LW, LH, "#161B22", RULE, 1.0)
    d.t(x, LY + 20, n, 13, INK, kr(n), "middle", 600)
    d.t(x, LY + 37, sub, 12, MUTED, MONO)

# 레인 옆 칩
d.chip(LX["컨테이너 안 앱"], 180, "호스트 ps 에 안 보임", MUTED, 11)
d.chip(LX["Sentry"], 180, "seccomp 샌드박싱", MUTED, 11)


def msg(a, b, label, y, col=MUTED, mk="ar", dash=None, sw=1.5):
    x1, x2 = LX[a], LX[b]
    s = 1 if x2 > x1 else -1
    d.arrow([(x1 + 6 * s, y), (x2 - 8 * s, y)], col, mk, sw, dash)
    fit(label, 12, abs(x2 - x1) - 24)
    d.t((x1 + x2) / 2, y - 9, label, 12, col, kr(label), "middle", 600)


# 1. 앱 → Sentry
msg("컨테이너 안 앱", "Sentry", "syscall", 232)

# 2. 파일과 무관: Sentry 안 재구현(focal)
x = LX["Sentry"]
d.o.append(f'<path d="M {x + 6} 318 L {x + 56} 318 L {x + 56} 338 L {x + 10} 338" fill="none" stroke="{ACC}" stroke-width="1.8" marker-end="url(#acc)"/>')
d.t(x + 68, 332, "Sentry 안에서 재구현", 12, ACC, KR, "start", 600)

# 3. 파일 접근: Sentry → Gofer → 호스트 커널, 응답 두 개
msg("Sentry", "Gofer", "파일 요청 위임", 420, INFO, "info")
msg("Gofer", "호스트 커널", "파일 syscall", 460, INFO, "info")
msg("호스트 커널", "Gofer", "결과", 500, MUTED, "ar", "5 4", 1.3)
msg("Gofer", "Sentry", "결과", 540, MUTED, "ar", "5 4", 1.3)

# 4. 마지막 응답
msg("Sentry", "컨테이너 안 앱", "결과", 604, MUTED, "ar", "5 4", 1.3)

d.legend(H - 44, [("가로챈 syscall", MUTED), ("Sentry 안 재구현", ACC), ("파일 접근 위임", INFO)])
d.save(str(ASSETS / "08-01.gvisor-sentry.svg"))
print("ok 08-01 gvisor-sentry")
