# 타입 스펙: type-bar — 함정 URL 이 /foo/bar 를 한 마디 더할 때마다 8 자씩 길어져 매번 "처음 보는 URL" 이 된다. 막대 길이 = 문자 수, 길이 상한을 넘는 줄에서 필터가 끊는다.
# 사실 출처: 추출본 v2.txt 2620~2628행(무한히 깊은 디렉터리 예 www.spidertrapexample.com/foo/bar/foo/bar/…, 최대 길이로 회피),
#   계산: len("www.spidertrapexample.com") = 25, len("/foo/bar") = 8, 깊이 k 의 길이 = 25 + 8k (python 으로 측정). 상한 값은 추출본에 없어 숫자를 쓰지 않았고 점선 위치는 개념 표시다.
# Layout conventions: 막대 시작 x=168, 문자당 8px, 높이 28, 세로 stride 56(y=136부터), 오른쪽 칩 중심 x=820. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, WARN, BAD, INFO, MUTED, INK, SOFT, KR, MONO

W, H = 960, 480
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 09-01 §7",
      "함정 URL 은 매번 새 주소라 중복 검사를 지난다",
      "마디를 하나 붙일 때마다 문자열이 달라져 URL Seen? 이 막지 못하고, 길이 상한을 넘는 순간에야 필터가 끊는다.",
      "상한 값은 운영자가 정하며 점선 위치는 개념 표시")

X0, PX, BH, ST, Y0 = 168, 8, 28, 56, 136
LIM_X = X0 + 53 * PX
d.t(X0, 112, "길이 = 25 + 8 × k", 13, MUTED, MONO, "start", 600)
d.t(LIM_X, 112, "길이 상한 L", 13, WARN, KR, "middle", 600)

for k in range(5):
    y = Y0 + k * ST
    n = 25 + 8 * k
    over = k == 4
    c = BAD if over else INFO
    d.t(24, y + 20, f"깊이 {k}", 13, INK, KR, "start", 600)
    d.tone(X0, y, n * PX, BH, c, 4, "14", 1.1)
    d.t(X0 + 12, y + 20, f"{n} 자", 12, MUTED, MONO, "start")
    if over:
        d.chip(820, y + 14, "필터가 버림", BAD, 13)
    else:
        d.chip(820, y + 14, "URL Seen? 없음", INFO, 13)
d.line(LIM_X, 124, LIM_X, Y0 + 4 * ST + BH + 12, WARN, 1.2, "5 4")

d.legend(H - 56, [("새 URL 로 통과", INFO), ("길이 상한 초과", BAD), ("상한 위치", WARN)])
d.save("09-01.trap-depth.svg")
