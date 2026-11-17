# 08-01 §2 「세부 — 로그를 이루는 세 자리」 — 로그 하나가 무엇으로 이루어지는가를 실제 파일로 보인다.
# 원문("Logging"): "From a structural perspective, overall, a log comprises the following:
#       A collection of log items, messages, or lines — Captures information about a discrete event.
#       Metadata or context — Can be present on a per-message basis as well as on a global scope (the
#       entire log file, for example).
#       A format for how an individual log message is to be interpreted — Defines the log's parts and
#       meanings."
# 실제 값: 본문 §3 「/var/log 배포판별」의 `tail -f /var/log/syslog` 출력 다섯 줄을 그대로 쓴다.
#       줄 끝이 잘린 것(… fa)은 본문 출력이 지면 폭에서 자른 자리라 채우지 않는다.
#       파일 이름이 곧 분류라는 것은 본문 표(Debian 12 `syslog` = 대부분의 시스템 메시지)와
#       "이름을 정하는 것은 … rsyslog 의 기본 규칙" 문장에서 왔다.
# 축약: 칸 이름(시각·호스트·프로그램[PID]·메시지)은 출력의 열을 읽어 이 노트가 붙인 이름이다.
#       세 번째 줄(systemd[1])만 확대해 칸을 갈랐고, 나머지 줄도 같은 칸 순서를 따른다.
# 타입 스펙: type-nested — 파일(전역 문맥)이 항목 줄들을 담고, 줄 하나가 다시 칸들을 담는 포함 관계.
#           형식은 칸의 순서와 뜻이라 파일 위 눈금으로 모든 줄에 걸었다. accent 는 확대한 줄 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 612
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §2",
      "로그는 항목과 문맥과 형식 셋으로 이루어진다",
      "Debian 의 /var/log/syslog 를 tail -f 로 본 다섯 줄. 파일 이름이 파일 전체의 문맥이고, "
      "한 줄이 사건 하나를 담는 항목이다. 줄마다 시각·호스트·프로그램[PID] 이 메시지마다 붙는 문맥으로 "
      "앞에 서고, 그 뒤가 사람이 읽는 텍스트 페이로드다. 칸의 순서와 뜻을 정하는 것이 형식이다.",
      "같은 칸 순서가 다섯 줄 모두에 걸린다 — 그 순서가 형식이다")

CW = 7.8                                  # 13px mono 한 글자 폭 근사
COLS = [48, 180, 264, 420]                # 시각 · 호스트 · 프로그램[PID]: · 메시지
NAMES = ["시각", "호스트", "프로그램[PID]", "메시지"]
LINES = [
    ("Sep 26 15:06:41", "starlite", "nm-applet[31555]:", "... 'GTK_IS_WIDGET (widget)' fa"),
    ("Sep 26 15:06:41", "starlite", "nm-dispatcher:", "... new request (3 scripts)"),
    ("Sep 26 15:06:41", "starlite", "systemd[1]:", "Starting PackageKit Daemon..."),
    ("Sep 26 15:06:41", "starlite", "nm-dispatcher:", "... start running ordered scripts."),
    ("Sep 26 15:06:42", "starlite", "PackageKit:", "daemon start"),
]
FOCAL = 2

# 형식 — 파일 위 눈금. 칸이 시작하는 자리마다 눈금을 내린다.
RY = 116
d.t(24, RY, "형식 — 칸의 순서와 뜻", 13, MUTED, KR, "start", 600)
d.t(896, RY, "스키마로 적으면 자동 검증", 12, SOFT, KR, "end")
TY = 140
d.line(COLS[0], TY, 872, TY, MUTED, 1.0, "4 3")
for x, nm in zip(COLS, NAMES):
    d.line(x, TY - 6, x, TY + 6, MUTED, 1.2)
    d.t(x + 6, TY - 6, nm, 12, MUTED, KR if any("가" <= c <= "힣" for c in nm) else MONO, "start")

# 파일 — 전역 문맥 머리와 항목 다섯 줄
FX, FY, FW = 24, 160, 872
LY0, LS = 220, 28
FH = (LY0 - FY) + LS * len(LINES) - 4
d.box(FX, FY, FW, FH, PAPER2, INFO, 1.2, 8)
d.t(FX + 24, FY + 26, "/var/log/syslog", 14, INFO, MONO, "start", 600)
d.t(FX + 172, FY + 26, "파일 전체의 문맥 — 대부분의 시스템 메시지 · rsyslog 규칙이 고른 이름",
    12, MUTED, KR, "start")
d.line(FX + 12, FY + 40, FX + FW - 12, FY + 40, RULE, 0.8)

for i, cells in enumerate(LINES):
    by = LY0 + i * LS
    if i == FOCAL:
        d.tone(FX + 12, by - 18, FW - 24, 26, ACC, 4, "1A", 1.2)
    for x, txt in zip(COLS, cells):
        d.t(x, by, txt, 13, INK if i == FOCAL else MUTED, MONO, "start", 600 if i == FOCAL else 400)

# 항목 하나 확대 — 확대한 줄은 파일 아래에 같은 칸 자리로 다시 쓴다
FBOT = FY + FH
EY = FBOT + 68
d.arrow([(FX + FW - 40, LY0 + FOCAL * LS + 8), (FX + FW - 40, EY - 26)], ACC, "acc", 1.4)
d.t(FX + FW - 52, FBOT + 30, "항목 하나 = 사건 하나", 12, ACC, KR, "end", 600)
d.tone(FX + 12, EY - 22, FW - 24, 34, ACC, 6, "14", 1.4)
focal = LINES[FOCAL]
for x, txt in zip(COLS, focal):
    d.t(x, EY, txt, 13, INK, MONO, "start", 600)

# 칸마다 괄호 — 앞 세 칸은 메시지마다 붙는 문맥, 마지막 칸은 페이로드
BY = EY + 24
spans = []
for k, (x, txt) in enumerate(zip(COLS, focal)):
    x1 = x + len(txt) * CW
    spans.append((x, x1))
    c = OK if k == 3 else INFO
    d.line(x, BY, x1, BY, c, 1.4)
    d.line(x, BY - 6, x, BY, c, 1.4)
    d.line(x1, BY - 6, x1, BY, c, 1.4)
    d.t((x + x1) / 2, BY + 20, NAMES[k], 12, c, KR if any("가" <= ch <= "힣" for ch in NAMES[k]) else MONO)

GY = BY + 48
gx0, gx1 = spans[0][0], spans[2][1]
d.line(gx0, GY, gx1, GY, INFO, 1.4)
d.line(gx0, GY - 6, gx0, GY, INFO, 1.4)
d.line(gx1, GY - 6, gx1, GY, INFO, 1.4)
d.t((gx0 + gx1) / 2, GY + 22, "메시지마다 붙는 문맥", 13, INFO, KR, "middle", 600)
px0, px1 = spans[3]
d.line(px0, GY, px1, GY, OK, 1.4)
d.line(px0, GY - 6, px0, GY, OK, 1.4)
d.line(px1, GY - 6, px1, GY, OK, 1.4)
d.t((px0 + px1) / 2, GY + 22, "텍스트 페이로드 · 사람이 읽음", 13, OK, KR, "middle", 600)

NY = GY + 52
d.t(24, NY, "다섯 줄은 본문 tail -f 출력 그대로 · 줄 끝 잘림도 본문 그대로 · 칸 이름은 이 노트가 붙임",
    11, SOFT, KR, "start")

d.legend(NY + 20, [("확대한 항목", ACC), ("문맥 · 메타데이터", INFO),
                  ("텍스트 페이로드", OK), ("형식 눈금", MUTED)])
d.save("08-01.log-anatomy.svg")
print("ok 08-01.log-anatomy")
