# 04-01 §3 — 열린 포트는 ss 로 찾고, 서비스를 끄고 패키지를 지운 뒤 다시 확인한다. 지울 수 없는 포트는 ufw 로 막는다.
# 본문 근거: 이 노트 ### 3 「열린 포트는 프로세스까지 찾아서 서비스째 닫습니다」.
# 검증 근거: ubuntu:24.04 systemd 컨테이너에서 vsftpd 설치 → ss -ltpn 으로 21/tcp 확인 → systemctl disable --now →
#            apt purge --auto-remove → ss 재확인(21 사라짐). ufw 는 별도 컨테이너에서 enable · default · allow 순서를 실행.
# 타입 스펙: type-flowchart — 다섯 단계의 순차 절차와, 서비스를 없앨 수 없을 때 갈라지는 방화벽 가지.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 356
d = D(W, H, "CKS STUDY GUIDE · 04-01 §3",
      "열린 포트를 찾아 닫는 순서",
      "ss 로 열린 포트와 프로세스를 찾고, systemctl 로 서비스를 끄고, apt 로 패키지를 지운 뒤 ss 로 다시 확인하는 절차와, "
      "서비스를 없앨 수 없을 때 ufw 로 막는 가지를 그린 도식이다.",
      "서비스를 없앨 수 있으면 패키지까지 지우고, 없앨 수 없으면 방화벽으로 막습니다")

BW, BH, PITCH, X0 = 150, 84, 172, 12
Y = 100
steps = [
    ("포트 찾기", "ss -ltpn", INFO),
    ("프로세스 확인", "systemctl status", INFO),
    ("서비스 끄기", "disable --now", ACC),
    ("패키지 지우기", "apt purge", ACC),
    ("다시 확인", "ss -ltpn", OK),
]
for i, (title, sub, c) in enumerate(steps):
    x = X0 + i * PITCH
    d.tone(x, Y, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
    d.t(x + BW / 2, Y + 34, title, 13, INK, KR, "middle", 600)
    d.t(x + BW / 2, Y + 60, sub, 11, MUTED, MONO)
    if i < 4:
        d.path(f"M {x + BW + 2} {Y + BH / 2} L {x + PITCH - 2} {Y + BH / 2}", MUTED, 1.4, m="ar")

# 가지: 서비스를 없앨 수 없을 때
bx, by = X0 + 2 * PITCH, 238
d.box(bx, by, BW * 2 + (PITCH - BW), 60, PAPER2, SOFT, 1.1)
d.t(bx + (BW * 2 + (PITCH - BW)) / 2, by + 26, "방화벽으로 막기", 13, INK, KR, "middle", 600)
d.t(bx + (BW * 2 + (PITCH - BW)) / 2, by + 46, "ufw default deny incoming · ufw allow 22/tcp", 11, MUTED, MONO)
fx = X0 + 1 * PITCH + BW / 2
d.path(f"M {fx} {Y + BH + 2} L {fx} {by + 30} L {bx - 2} {by + 30}", MUTED, 1.2, m="ar", dash="4 4")
d.chip(fx, Y + BH + 30, "없앨 수 없는 서비스", MUTED, 12)

d.legend(312, [("확인", INFO), ("닫는 조치", ACC), ("닫힌 것을 확인", OK)])
d.save("04-01.port-close-flow.svg")
