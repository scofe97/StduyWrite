# 타입 스펙: type-dp-security-matrix — N = 3 에서 W(행)·R(열) 아홉 쌍마다 W + R 과 읽기·쓰기 겹침 서버 수를 같은 격자에 놓고, 겹침 0 과 1 이상을 상태색으로 가른다. focal 은 (W, R) = (2, 2).
# 사실 출처: W + R > N 이면 겹치는 노드가 있고 R = 1 · W = N 은 읽기 최적화, W = 1 · R = N 은 쓰기 최적화는 추출본 v2.txt 1667~1673행, Dynamo 논문 §6 의 흔한 (N,R,W) = (3,2,2).
#   겹침 = max(0, W + R − N) 은 계산값이다(3 × 3 전부 python3 로 열거).
# Layout conventions: 행 이름 열 x=24 폭 168, 셀 폭 232 · stride 240(x=200·440·680), 머리 y=100 높이 40, 행 stride 92(y=148·240·332) 높이 80. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER2, RULE, KR, MONO

N = 3
W, H = 960, 520
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 06-01 §5",
      "N = 3 에서 W + R 이 3 을 넘어야 읽기와 쓰기가 겹친다",
      "쓰기 확인 W 곳과 읽기 응답 R 곳의 합에서 N 을 빼면 둘이 반드시 겹치는 서버 수이고, 음수면 겹침 0 이다.",
      "겹침 = W + R − N")

XS = (200, 440, 680)
YS = (148, 240, 332)
CW, CH = 232, 80
d.t(24, 124, "쓰기 확인 W ↓", 13, MUTED, KR, "start", 600)
for j in range(3):
    d.t(XS[j] + CW / 2, 124, f"R = {j + 1}", 14, INK, MONO, "middle", 600)
NOTE = {(3, 1): "읽기 빠름", (1, 3): "쓰기 빠름", (2, 2): "흔한 설정 (3, 2, 2)"}
for i in range(3):
    w = i + 1
    d.t(24, YS[i] + 46, f"W = {w}", 14, INK, MONO, "start", 600)
    for j in range(3):
        r = j + 1
        s = w + r
        ov = max(0, s - N)
        x, y = XS[j], YS[i]
        focal = (w, r) == (2, 2)
        c = ACC if focal else (OK if ov else WARN)
        d.tone(x, y, CW, CH, c, 6, "12", 1.4 if focal else 1.0)
        d.t(x + CW / 2, y + 36, f"합 {s} · 겹침 {ov}", 15, INK, KR, "middle", 600)
        if (w, r) in NOTE:
            d.t(x + CW / 2, y + 62, NOTE[(w, r)], 12, c, KR, "middle")

d.legend(H - 56, [("겹침 0", WARN), ("겹침 1 이상", OK), ("Dynamo 의 흔한 설정", ACC)])
d.save("06-01.quorum-grid.svg")
