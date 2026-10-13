# 타입 스펙: type-process — 작업 하나(영상 인코딩)가 작업 큐에서 나와 스케줄러 손을 거쳐 실행 큐로 들어갔다 나가는 여섯 시점을 같은 객체의 위치 이동으로 그린다. 열은 시점, 줄은 큐 셋과 스케줄러다.
# 사실 출처: 구조와 다섯 동작은 추출본 v2.txt 4136~4154행(작업 큐·작업자 큐·실행 큐·작업 스케줄러, 최우선 작업 꺼냄 → 최적 작업자 → 실행 지시 → 실행 큐에 짝 기록 → 끝나면 제거), PDF 234쪽 그림.
#   작업 이름 영상 인코딩·썸네일·오디오 인코딩은 4133~4135행(DAG 스케줄러 예). 작업자 이름 encoder-1·encoder-2 와 가동률 70 %·20 % 는 설명을 위해 정한 값이다.
# Layout conventions: 줄 이름 열 x=24 폭 100, 시점 열 폭 128·stride 136(x=136 부터), 줄 y=132 부터 stride 92 높이 84, 머리 y=100. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, WARN, SOFT, MUTED, INK, RULE, KR, MONO

W, H = 972, 600
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 14-02 §3",
      "작업 하나가 세 큐 사이를 옮겨 간다",
      "영상 인코딩이 작업 큐 맨 앞에서 꺼내져 encoder-2 와 짝이 되어 실행 큐에 들어갔다가 끝나면 지워진다. 작업자 이름과 가동률은 설명용 값이다.",
      "열은 작업 스케줄러의 동작 순서 · 줄은 큐")

X0, CW, XS_ = 136, 128, 136
Y0, RS, RH = 132, 92, 84
LANES = ("작업 큐", "작업 스케줄러", "작업자 큐", "실행 큐")
HEAD = ("시작", "1 꺼냄", "2 고름", "3 지시", "4 기록", "5 지움")


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


# 열 머리와 시간 화살표
for i, h in enumerate(HEAD):
    x = X0 + XS_ * i
    d.t(x + CW / 2, 104, h, 13, SOFT, KR, "middle", 600)
d.arrow([(X0, 116), (X0 + XS_ * 5 + CW, 116)], SOFT, "soft", 1.0)

for r, nm in enumerate(LANES):
    y = Y0 + RS * r
    d.t(24, y + RH / 2 + 5, nm, 13, INK, KR, "start", 600)

TASK, W2, W1 = "영상 인코딩", "encoder-2 20 %", "encoder-1 70 %"
# cells[lane][col] = list of (text, color) ; None → 빈 칸(점선)
CELLS = {
    0: [[(TASK, ACC), ("썸네일", INK), ("오디오 인코딩", INK)]] + [[("썸네일", INK), ("오디오 인코딩", INK)]] * 5,
    1: [None, [(TASK, ACC)], [(TASK, ACC), ("encoder-2", OK)], [(TASK, ACC), ("→ encoder-2", OK)], None, None],
    2: [[(W2, INK), (W1, INK)], [(W2, INK), (W1, INK)], [(W2, OK), (W1, INK)], [(W2, OK), (W1, INK)], [(W2, OK), (W1, INK)], [(W2, INK), (W1, INK)]],
    3: [None, None, None, None, [(TASK + " ↔", ACC), ("encoder-2", OK)], None],
}

for r in range(4):
    y = Y0 + RS * r
    for i in range(6):
        x = X0 + XS_ * i
        items = CELLS[r][i]
        if not items:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{RH}" rx="6" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="4 4"/>')
            continue
        hot = any(c == ACC for _, c in items)
        d.tone(x, y, CW, RH, ACC if hot else INFO, 6, "14" if hot else "0C", 1.3 if hot else 1.0)
        n = len(items)
        top = y + RH / 2 - (n - 1) * 11 + 4
        for k, (txt, c) in enumerate(items):
            d.t(x + CW / 2, top + k * 22, txt, 13 if fam(txt) == KR else 12, c, fam(txt), "middle", 600 if c != INK else 400)

d.legend(H - 56, [("옮겨 가는 작업", ACC), ("고른 작업자", OK), ("큐에 서 있는 것", INFO)])
d.save("14-02.queue-trace.svg")
