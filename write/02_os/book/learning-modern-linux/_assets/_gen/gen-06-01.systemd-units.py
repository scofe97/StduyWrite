# 06-01 §4 — 단위 파일이 디스크의 세 디렉터리에 실제로 놓이고, systemd[1] 이 그것을 읽어 단위로 삼는다.
# 원문("Units"): "A unit in systemd is a logical grouping with different semantics depending on its
#       function and/or the resource it targets."
#       주요 넷 — service units("Describe how to manage a service or application"),
#       target units("Capture dependencies"), mount units("Define a mountpoint"),
#       timer units("Define timers for cron jobs and the like").
#       덜 중요한 것 — socket, device, automount, swap, path, snapshot, slice, scope.
#       파일 자리 — "/lib/systemd/system: Package-installed units", "/etc/systemd/system: System
#       admin–configured units", "/run/systemd/system: Nonpersistent runtime modifications".
#  실제 값 — §6 의 `sudo ls -al /run/systemd/system/` 출력:
#       "-rw-r--r--  1 root root 117 Sep 12 13:08 greeter.service"
#       "-rw-r--r--  1 root root 107 Sep 12 13:08 greeter.timer"
#  §5 — "systemctl daemon-reload: 모든 단위 파일을 다시 읽고 의존성 트리 전체를 다시 만듭니다".
#  결정 치트시트 — 패키지가 깔아 준 단위를 고치려면 /etc/systemd/system (패키지 갱신에 덮이지 않음).
# 타입 스펙: type-tree — 파일시스템 뿌리 / 에서 세 디렉터리로 내려가는 실제 트리, 직교 연결.
#           accent 는 §6 예제의 두 파일이 실제로 놓인 /run/systemd/system 하나.
# 축약: 단위 종류는 greeter.service · greeter.timer 의 이름 끝 자리로 보였다. /lib · /etc 안의
#       XXXXX.service 는 §5 의 자리표시 이름을 쓴 예시라 점선으로 그렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 760
d = D(W, H, "LEARNING MODERN LINUX · 06-01 §4",
      "단위는 세 디렉터리에 놓인 파일이고, systemd[1] 이 그것을 읽는다",
      "단위 파일은 /lib/systemd/system(패키지가 설치), /etc/systemd/system(관리자가 설정), "
      "/run/systemd/system(재부팅에 사라지는 런타임 수정) 세 자리에 놓인다. §6 예제의 "
      "greeter.service(117 바이트)와 greeter.timer(107 바이트)는 /run 쪽에 있다. "
      "systemctl daemon-reload 가 세 자리를 다시 읽어 의존성 트리를 다시 만들고, "
      "파일 이름 끝(.service · .timer …)이 단위 종류다.",
      "§6 예제의 두 파일은 재부팅에 사라지는 /run 쪽에 놓였다")

# 파일시스템 트리 — 줄기와 가지를 글자보다 먼저 그린다
TX, BX0, BX1 = 52, 80, 548
rows = [  # (y, h, 경로, 설명, 색, 파일 줄들, 예시 여부)
    (160, 92, "/lib/systemd/system/", "패키지가 설치한 단위 · 영속", INFO,
     ["XXXXX.service (예)"], True),
    (272, 92, "/etc/systemd/system/", "관리자가 설정 · 패키지 갱신에 안 덮임", INFO,
     ["XXXXX.service 고친 판 (예)"], True),
    (384, 116, "/run/systemd/system/", "런타임 수정 · 재부팅에 사라짐", ACC,
     ["-rw-r--r--  root  117  greeter.service", "-rw-r--r--  root  107  greeter.timer"], False),
]
d.t(44, 140, "/", 16, INK, MONO, "start", 600)
d.line(TX, 148, TX, rows[-1][0] + 40, MUTED, 1.2)
for y, h, *_ in rows:
    d.line(TX, y + 40, BX0, y + 40, MUTED, 1.2)

# 세 자리 → systemd[1] : 버스로 모은다
SX, SY, SW, SH = 652, 284, 268, 76
BUSX = 604
for y, h, *_ in rows:
    d.line(BX1, y + 40, BUSX, y + 40, MUTED, 1.2)
d.line(BUSX, rows[0][0] + 40, BUSX, rows[-1][0] + 40, MUTED, 1.2)
d.arrow([(BUSX, SY + SH / 2), (SX - 2, SY + SH / 2)], MUTED, "ar", 1.4)

for y, h, path, note, c, files, example in rows:
    if c is ACC:
        d.o.append(f'<rect x="{BX0}" y="{y}" width="{BX1 - BX0}" height="{h}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(BX0, y, BX1 - BX0, h, PAPER2, c, 1.2, 8)
    d.t(BX0 + 16, y + 26, path, 14, c, MONO, "start", 600)
    d.t(BX0 + 16, y + 48, note, 12, MUTED, KR, "start")
    for j, f in enumerate(files):
        fy = y + 60 + j * 24
        if example:
            d.o.append(f'<rect x="{BX0 + 16}" y="{fy}" width="{BX1 - BX0 - 32}" height="20" rx="4" '
                       f'fill="none" stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
            d.t(BX0 + 28, fy + 15, f, 12, SOFT, MONO, "start")
        else:
            d.o.append(f'<rect x="{BX0 + 16}" y="{fy}" width="{BX1 - BX0 - 32}" height="20" rx="4" '
                       f'fill="{PAPER}" stroke="{ACC}" stroke-width="0.8"/>')
            d.t(BX0 + 28, fy + 15, f, 12, INK, MONO, "start")

d.box(SX, SY, SW, SH, PAPER2, INK, 1.2, 8)
d.t(SX + 16, SY + 30, "systemd[1]", 15, INK, MONO, "start", 600)
d.t(SX + 16, SY + 54, "의존성 트리를 다시 만듦", 12, MUTED, KR, "start")
d.t(SX, SY - 14, "systemctl daemon-reload", 12, MUTED, MONO, "start")
d.t(SX, SY + SH + 26, "세 자리 모두 읽음", 12, SOFT, KR, "start")

# 단위 종류 — 파일 이름 끝 자리
KY = 544
d.t(24, KY - 16, "단위 종류 — 파일 이름 끝 자리 (greeter.service · greeter.timer)", 13, INK, KR, "start", 600)
main = [(".service", "서비스 · 앱 관리", True), (".target", "의존성 묶음", False),
        (".mount", "마운트 지점", False), (".timer", "cron 같은 타이머", True)]
CW, CG = 216, 16
for i, (suf, role, used) in enumerate(main):
    x = 24 + i * (CW + CG)
    d.box(x, KY, CW, 56, PAPER2, OK, 1.4 if used else 1.0, 6)
    d.t(x + 14, KY + 24, suf, 14, OK, MONO, "start", 600)
    d.t(x + 14, KY + 45, role, 12, MUTED, KR, "start")
    if used:
        d.t(x + CW - 14, KY + 24, "§6 예제", 12, ACC, KR, "end")

d.t(24, KY + 92, "덜 중요하다고 저자가 묶은 여덟", 12, SOFT, KR, "start", 600)
minor = [".socket", ".device", ".automount", ".swap", ".path", ".snapshot", ".slice", ".scope"]
x = 24
for name in minor:
    w = len(name) * 7.5 + 20
    d.chip(x + w / 2, KY + 120, name, MUTED, 12)
    x += w + 16

d.t(24, 704, "XXXXX.service 는 §5 의 자리표시 이름 · 점선은 예시 · 파일 줄은 ls -al 출력을 줄인 것",
    11, SOFT, KR, "start")
d.legend(716, [("영속 자리", INFO), ("§6 예제가 놓인 자리", ACC), ("주요 단위 종류", OK)])
d.save("06-01.systemd-units.svg")
print("ok 06-01.systemd-units")
