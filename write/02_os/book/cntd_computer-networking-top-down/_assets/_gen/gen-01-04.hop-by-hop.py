# 01-04 §3 — 종단 간 지연은 홉마다 넷이 되풀이된 합이고, 그중 흔들리는 것은 큐잉 하나뿐이다.
# 본문 근거(수치는 전부 traceroute 예제에서 온 것만 쓴다):
#   "4번 라우터까지의 세 값 0.351 · 0.392 · 0.380 밀리초에는 전송·전파·처리·큐잉 지연이 모두 들어 있습니다."
#   "12번 라우터까지의 지연이 11번보다 작습니다" — 큐잉 지연이 시시각각 변하기 때문.
#   "7.311 밀리초에서 77.826 밀리초로 열 배 넘게 뜁니다" — 대서양 횡단 광케이블, 전파 지연.
#   식 (1.2) d(end-end) = N × (d_proc + d_trans + d_prop) — 홉마다 같은 넷이 되풀이된다는 뜻.
# 타입 스펙: type-bar — 같은 축 위에 홉별 구성을 쌓아 견준다. 무엇이 홉마다 같고 무엇이 다른지가
#   칸 높이의 규칙성과 불규칙성으로 드러난다.
#   축약: 눈금 없는 질적 그림이다. 홉별 네 성분의 실제 비율은 예제 출력에 없으므로 지어내지 않는다
#   (traffic-intensity.svg 가 같은 이유로 y축 눈금을 두지 않는 것과 같은 규약). 숫자를 적은 자리는
#   예제 출력이 실제로 준 값뿐이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 714
BASE, BW, X0, GAP = 452, 92, 118, 168

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-04 §3",
      "홉마다 같은 넷이 되풀이됩니다",
      "종단 간 지연은 홉마다의 네 성분을 다 더한 값이다. 셋은 홉이 정해지면 값이 정해지고 "
      "큐잉만 지날 때마다 다르다. 거리가 갑자기 멀어지면 전파 칸이 통째로 뛴다.",
      "눈금 없는 질적 그림입니다 — 적힌 숫자만 예제 출력이 준 값입니다")

# (처리, 큐잉, 전송, 전파) — 높이는 질적이다
HOPS = [
    ("홉 1~6", (10, 18, 22, 24), None),
    ("홉 7",   (10, 40, 22, 26), "7.311 ms"),
    ("홉 8",   (10, 20, 22, 150), "77.826 ms"),
    ("홉 11",  (10, 46, 22, 24), None),
    ("홉 12",  (10, 14, 22, 24), None),
]
SEG = [("처리", SOFT), ("큐잉", WARN), ("전송", INFO), ("전파", ACC)]

for i, (name, hs, note) in enumerate(HOPS):
    x = X0 + i * GAP
    y = BASE
    for (lab, col), h in zip(SEG, hs):
        y -= h
        focal = (lab == "전파" and name == "홉 8")
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{h}" rx="3" '
                   f'fill="{col}{"33" if focal else "22"}" stroke="{col}" stroke-width="{1.4 if focal else 1.0}"/>')
    d.t(x + BW / 2, BASE + 22, name, 11.5, INK, KR, "middle", 600)
    if note:
        d.t(x + BW / 2, BASE + 40, note, 11, ACC if name == "홉 8" else SOFT, MONO)

d.line(X0 - 24, BASE, X0 + 4 * GAP + BW + 24, BASE, MUTED, 1.0)
d.t(X0 - 30, BASE + 4, "0", 11, SOFT, MONO, "end")

d.t(636, 276, "← 이 칸 하나가 열 배를 만듭니다", 11, ACC, KR, "start")
d.t(636, 294, "대서양 횡단 광케이블", 11, MUTED, KR, "start")
d.t(752, 500, "↑ 큐잉 칸만 지날 때마다 다릅니다 — 그래서 12번이 11번보다 작습니다", 11, WARN, KR, "middle")

d.box(24, 532, W - 48, 116, PAPER2, RULE, 0.9, 6)
d.t(44, 558, "예제 출력이 실제로 보여 주는 것 셋", 12, INK, KR, "start", 600)
d.t(44, 580, "4번 라우터까지의 세 값 `0.351 · 0.392 · 0.380 ms` 에는 네 성분이 모두 들어 있습니다. 왕복 하나에 넷이 다 섞여 돌아옵니다.",
    11, MUTED, KR, "start")
d.t(44, 602, "`12번`이 `11번`보다 작게 나옵니다. 뒤 홉이 앞 홉보다 빠를 수 있다는 뜻이고, 그렇게 만드는 것은 큐잉 하나뿐입니다.",
    11, WARN, KR, "start")
d.t(44, 624, "`7번 7.311 ms` 에서 `8번 77.826 ms` 로 열 배 넘게 뜁니다. 거리가 뛰었기 때문이고, 거리에 달린 성분은 전파 하나입니다.",
    11, ACC, KR, "start")

d.legend(H - 44, [("처리", SOFT), ("큐잉 — 홉마다 다름", WARN), ("전송", INFO), ("전파 — 거리가 정함", ACC)])
d.save("01-04.hop-by-hop.svg")
print("ok hop-by-hop")
