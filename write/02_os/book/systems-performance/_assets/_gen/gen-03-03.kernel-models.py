# 03-03 §7 — 커널 모델 넷 × 구성요소 다섯: 같은 구성요소가 어디서 도는가(원서 3.2.1 · 3.5.2 · 3.5.3).
# 타입 스펙: type-dp-security-matrix — 모델 × 구성요소의 비교 격자다.
#           축약: 보안 격자가 아니라 위치 격자로 문법만 빌리고, §2 공식 대신 칸 폭 168 · 행 52 stride 로 놓는다(11-04 와 같은 방식).
#           hybrid 칸의 "핵심 서비스는 커널"은 원서 3.5.3 의 performance-critical services 를 줄인 말이다.
#           focal 은 microkernel 의 IPC 단계(성능 비용의 출처).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 520
CW, RH, X0, Y0, GAP = 168, 48, 232, 140, 12

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-03 §7",
       "커널 모델별 구성요소의 위치",
       "같은 구성요소가 모델마다 다른 곳에서 돈다. microkernel 은 파일시스템 · 네트워크 스택 · 드라이버를 유저 모드로 내보내 IPC 로 부르고, hybrid 는 성능이 중요한 서비스를 커널로 되돌리며, unikernel 은 모두 한 이미지 · 한 주소 공간에 둔다.",
       "구성요소가 경계를 넘을수록 호출 비용이 붙습니다")

COLS = ["monolithic", "microkernel", "hybrid", "unikernel"]
for i, c in enumerate(COLS):
    d.t(X0 + i * (CW + GAP) + CW / 2, Y0 - 16, c, 14, INK, MONO, "middle", 600)

K, U, ONE = ("커널", INFO), ("유저 모드", OK), ("한 이미지", WARN)
ROWS = [("앱", [U, U, U, ONE]),
        ("파일시스템 · 네트워크 스택", [K, U, ("핵심 서비스는 커널", INFO), ONE]),
        ("드라이버", [K, U, ("핵심 서비스는 커널", INFO), ONE]),
        ("메모리 · 스레드 · IPC", [K, K, K, ONE]),
        ("구성요소 사이 호출", [("직접 함수 호출", MUTED), ("IPC 단계", ACC), ("핵심은 직접 호출", MUTED), ("한 주소 공간", WARN)])]
for r, (label, cells) in enumerate(ROWS):
    y = Y0 + r * (RH + 4)
    d.t(X0 - 20, y + RH / 2 + 5, label, 13, SOFT, KR, "end", 600)
    for i, (txt, c) in enumerate(cells):
        x = X0 + i * (CW + GAP)
        if c in (ACC,): d.tone(x, y, CW, RH, c, 6)
        elif c is MUTED: d.box(x, y, CW, RH, PAPER2, RULE, 1.0, 6)
        else: d.tone(x, y, CW, RH, c, 6, "12", 0.9)
        d.t(x + CW / 2, y + RH / 2 + 5, txt, 13, c if c is not MUTED else INK, KR, "middle", 600)

YB = Y0 + len(ROWS) * (RH + 4) + 20
d.legend(YB, [("성능 비용의 출처", ACC), ("커널 공간", INFO), ("유저 모드", OK), ("한 이미지", WARN)])
d.save("03-03.kernel-models.svg")
