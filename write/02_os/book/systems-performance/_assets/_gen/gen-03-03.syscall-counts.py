# 03-03 §1 — 원서 표 3.3: man page 섹션 2 로 센 문서화된 syscall 수.
# 타입 스펙: type-bar — 범주(커널 버전)마다 수치 하나를 비교한다.
#           축약: 버전 이름이 길어 가로 막대로 눕힌다(스펙: 라벨이 길면 horizontal 허용). 막대 8개는 상한 안.
#           값 1 = 1.2px. focal 은 가장 큰 Linux 5.3.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 556
X0, K, Y0, ST, BH = 312, 1.2, 128, 44, 28

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-03 §1",
       "문서화된 syscall 수 — UNIX V7 48 에서 Linux 5.3 493 까지",
       "원서 표 3.3. man page 섹션 2 항목 수로 센 거친 비교다. 커널은 OS 소프트웨어가 사적으로 쓰는 syscall 을 보통 더 제공한다.",
       "같은 2.6.32 도 배포판 빌드에 따라 408 과 427 로 갈립니다")

ROWS = [("UNIX Version 7", 48), ("SunOS (Solaris) 5.11", 142), ("FreeBSD 12.0", 222),
        ("Linux 2.6.32-21-server", 408), ("Linux 2.6.32-220.el6.x86_64", 427),
        ("Linux 3.2.6-3.fc16.x86_64", 431), ("Linux 4.15.0-66-generic", 480), ("Linux 5.3.0-1010-aws", 493)]
# 눈금
for v in (0, 100, 200, 300, 400, 500):
    x = X0 + v * K
    d.line(x, Y0 - 8, x, Y0 + len(ROWS) * ST - 8, RULE, 0.8)
    d.t(x, Y0 + len(ROWS) * ST + 12, str(v), 12, SOFT, MONO)
for i, (name, v) in enumerate(ROWS):
    y = Y0 + i * ST
    focal = i == len(ROWS) - 1
    c = ACC if focal else (INFO if name.startswith("Linux") else MUTED)
    d.tone(X0, y, v * K, BH, c, 3, "22" if not focal else "33", 1.0)
    d.t(X0 - 16, y + 19, name, 12, INK if not focal else ACC, MONO, "end", 600 if focal else 400)
    d.t(X0 + v * K + 10, y + 19, str(v), 13, c, MONO, "start", 600)

d.legend(Y0 + len(ROWS) * ST + 32, [("가장 많은 Linux 5.3", ACC), ("Linux", INFO), ("다른 커널", MUTED)])
d.save("03-03.syscall-counts.svg")
