# 01-01 §1 — 시스템 성능의 풀 스택(원서 그림 1.1)과 두 분석 관점(그림 1.2).
# 타입 스펙: type-layers — 애플리케이션에서 장치까지 위아래로 쌓인 소프트웨어 스택이고,
#           오른쪽 방향 표시가 두 관점이 스택에 들어오는 방향을 나른다.
#           축약: 층 폭을 스펙(800~880)보다 좁힌 560 으로 두고, 왼쪽 여백에 "풀 스택" 두 정의의 괄호를,
#           오른쪽 여백에 그림 1.2 의 두 화살표를 놓는다. 그림 1.1 의 커널 하위 상자 넷은 커널 층의 서브 라벨로 접었다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 624
BX, BW, BH, Y0, STRIDE = 196, 560, 56, 128, 64

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-01 §1 · FIG 1.1 · 1.2",
       "풀 스택 — 애플리케이션부터 metal 까지",
       "원서 그림 1.1 의 서버 한 대 소프트웨어 스택과 그림 1.2 의 두 분석 관점. 업계 통념의 풀 스택은 맨 위 애플리케이션 환경뿐이지만, 시스템 성능의 풀 스택은 커널과 장치까지 전부다.",
       "시스템 콜 층이 유저 레벨과 커널 레벨을 가릅니다")

LAYERS = [
    ("APP", "애플리케이션 · 데이터베이스", "웹 서버 · 앱 · DB"),
    ("LIB", "컴파일러 · 시스템 라이브러리", "유저 레벨"),
    ("SYS", "시스템 콜", "유저 · 커널 경계"),
    ("KER", "커널", "스레드 스케줄러 · 파일 시스템 · 네트워크 스택 · 가상 메모리"),
    ("DRV", "디바이스 드라이버", "커널 레벨"),
    ("DEV", "장치", "metal (하드웨어)"),
]
for i, (tag, name, sub) in enumerate(LAYERS):
    y = Y0 + i * STRIDE
    d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(BX + 16, y + 34, tag, 9, SOFT, MONO, "start", 600)
    d.t(BX + 60, y + 34, name, 14, INK, KR, "start", 600)
    d.t(BX + BW - 16, y + 34, sub, 12, MUTED, KR, "end")

YT, YB = Y0, Y0 + 5 * STRIDE + BH
# 통념의 풀 스택 — 애플리케이션 층만
XA = 160
d.line(XA, YT + 4, XA, YT + BH - 4, MUTED, 1.2)
d.line(XA, YT + 4, XA + 8, YT + 4, MUTED, 1.2)
d.line(XA, YT + BH - 4, XA + 8, YT + BH - 4, MUTED, 1.2)
d.t(XA - 8, YT + 26, "통념의", 13, MUTED, KR, "end")
d.t(XA - 8, YT + 44, "풀 스택", 13, MUTED, KR, "end")
# 시스템 성능의 풀 스택 — 전부
XB = 176
d.line(XB, YT + 4, XB, YB - 4, ACC, 1.6)
d.line(XB, YT + 4, XB + 8, YT + 4, ACC, 1.6)
d.line(XB, YB - 4, XB + 8, YB - 4, ACC, 1.6)
YM = (YT + YB) / 2
d.t(XB - 12, YM - 8, "시스템 성능의", 14, ACC, KR, "end", 600)
d.t(XB - 12, YM + 12, "풀 스택", 14, ACC, KR, "end", 600)

# 그림 1.2 — 두 관점
XW, XR = 820, 920
d.t(XW, YT - 28, "워크로드 분석", 13, INFO, KR, "middle", 600)
d.t(XW, YT - 10, "앱 개발자", 12, MUTED, KR, "middle")
d.arrow([(XW, YT + 4), (XW, YB - 4)], INFO, "info", 1.6)
d.t(XR, YB + 24, "자원 분석", 13, INFO, KR, "middle", 600)
d.t(XR, YB + 42, "시스템 관리자", 12, MUTED, KR, "middle")
d.arrow([(XR, YB - 4), (XR, YT + 4)], INFO, "info", 1.6)

d.legend(YB + 64, [("시스템 성능이 보는 범위", ACC), ("두 분석 관점", INFO), ("스택의 층", MUTED)])
d.save("01-01.full-stack-and-perspectives.svg")
