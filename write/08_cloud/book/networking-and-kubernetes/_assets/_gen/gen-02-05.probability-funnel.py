# 02-05.probability-funnel — 도착량이 줄어드니 분모도 줄어야 한다
# 본문 요구: §3 은 실측 27·22·30·21 과 도착량 100·75·50·25 퍼센트를 두 표로 따로 적는다.
#           두 표만으로는 "왜 분모가 줄어드는가"가 산수로만 남는다. 트렁크가 실제로 얇아지는
#           그림이어야 '앞이 걷어간 만큼 뒤에 덜 도착한다'가 눈으로 읽힌다.
#           폭은 실측 잔량(100 → 73 → 51 → 21)에 비례하며 지어낸 값이 아니다.
# 타입 스펙: type-pyramid.md 의 funnel(point down) — 층 4(4~6), 폭은 정직하게 도착량 비례,
#           옆 주석에 각 단이 걷어간 수. coral 은 전환 층 하나 — 확률 없이 남은 것을 다 받는
#           마지막 규칙이고, 그 칸의 성격이 다르다는 것이 이 절의 논점이다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 728
d = D(W, H, "PROBABILITY LADDER · MEASURED",
      "앞이 걷어간 만큼 뒤에는 덜 도착한다",
      "100 번을 보내고 규칙의 pkts 카운터를 읽은 값입니다. 트렁크의 폭이 그 단에 도착한 양이고, "
      "오른쪽 숫자가 그 단이 걷어간 양입니다.",
      lead="폭이 도착량이다 — 좁아지니 같은 몫을 걷으려면 분모가 줄어야 한다")

CX = 430
TOP = 176
LH = 68
K = 6.2                       # px per packet — 100 개가 620px
ARRIVE = [100, 73, 51, 21, 0]  # 실측 잔량: 100-27=73, 73-22=51, 51-30=21, 21-21=0
TOOK = [27, 22, 30, 21]
PROB = ["1/4", "1/3", "1/2", "없음"]
IDEAL = ["25", "25", "25", "25"]
Wd = [round(a * K / 4) * 4 for a in ARRIVE]

for i in range(4):
    y0, y1 = TOP + i * LH, TOP + (i + 1) * LH
    t, b = Wd[i] / 2, Wd[i + 1] / 2
    pts = f"{CX-t},{y0} {CX+t},{y0} {CX+b},{y1} {CX-b},{y1}"
    focal = (i == 3)
    c = ACC if focal else RULE
    fill = f"{ACC}18" if focal else PAPER2
    d.o.append(f'<polygon points="{pts}" fill="{fill}" stroke="{c}" '
               f'stroke-width="{1.4 if focal else 1.0}"/>')
    tc = ACC if focal else INK
    # 사다리꼴은 아래로 갈수록 좁아진다. 라벨을 그 y 의 실제 폭에 대고 재지 않으면
    # 마지막 층(21 → 0, 사실상 삼각형)에서 글자가 빗변을 뚫는다 — 기계 검사는 이걸 못 잡는다.
    def w_at(dy):
        return Wd[i] - (Wd[i] - Wd[i + 1]) * dy / LH
    ty, sy = (y0 + 18, y0 + 32) if focal else (y0 + 27, y0 + 46)   # 11px 라벨을 빗변 안쪽 넓은 자리로
    title = f"규칙 {i+1}"
    sub = "확률 없음" if focal else f"probability {PROB[i]}"
    ddx.fit(title, 12, w_at(ty - y0) - 12, f"funnel title {i+1}")
    ddx.fit(sub, 11, w_at(sy - y0) - 12, f"funnel sub {i+1}")
    d.t(CX, ty, title, 12, tc, KR, "middle", 600)
    d.t(CX, sy, sub, 11, ACC if focal else MUTED, MONO if not focal else KR)
    # 왼쪽 — 이 단에 도착한 양. 오른쪽 — 이 단이 걷어간 양.
    d.t(CX - Wd[i] / 2 - 16, y0 + 30, f"도착 {ARRIVE[i]}", 11, MUTED, MONO, "end")
    # 칩은 층의 *윗변*이 아니라 칩이 놓이는 y 의 실제 변에서 띄운다. 윗변 기준으로 두면
    # 아래로 갈수록 빗변이 안쪽으로 들어와 마지막 층에서 칩이 도형에 닿는다.
    d.chip(CX + w_at(34) / 2 + 70, y0 + 34, f"pkts {TOOK[i]}", ACC if focal else INFO, 11)

d.t(CX, TOP + 4 * LH + 26, "남은 것 0 — 합이 정확히 100", 11, MUTED, MONO)

# 축 — 폭이 무엇을 뜻하는지 왼쪽 여백에 한 번만 적는다.
d.line(60, TOP, 60, TOP + 4 * LH, RULE, 1.0)
d.t(36, TOP - 12, "도착량이 줄어든다", 11, SOFT, KR, "start")

d.t(36, 500, "걷어간 27 · 22 · 30 · 21 은 모두 25 언저리입니다. 100 회 시행의 표준편차가", 12, MUTED, KR, "start")
d.t(36, 522, "약 4.3 이라 이 편차는 1 시그마 안팎이고, 1,000 회면 250 에 훨씬 붙습니다.", 12, MUTED, KR, "start")
d.t(36, 550, "넷을 다 1/4 로 두었다면 25 · 18.75 · 14 · 10.5 로 뒤로 갈수록 굶었을 것입니다.", 12, MUTED, KR, "start")
d.t(36, 572, "백엔드가 n 개면 1/n → 1/(n-1) → … → 1/2 → 없음이고, kube-proxy 의 모양입니다.", 12, MUTED, KR, "start")
d.t(36, 600, "마지막 칸만 성격이 다릅니다. 확률에 당첨된 수가 아니라 앞 셋이 다 빗나가고", 12, MUTED, KR, "start")
d.t(36, 622, "남은 수라, 여기에 확률을 붙이면 어디에도 안 걸린 패킷이 정책으로 샙니다.", 12, MUTED, KR, "start")
d.legend(652, [("확률로 걷어간 단", INFO), ("남은 것을 다 받는 단 — 확률 금지", ACC)])
d.save("02-05.probability-funnel.svg")
print("ok probability-funnel")
