# 타입 스펙: type-timeline — 0~40 초 가로 축 위에 하트비트 세 번(0·5·10 초)과 끊김, 30 초 한도, 40 초 오프라인 전환을 정직한 눈금으로 놓고 아래 띠에 접속 상태를 깐다.
# 사실 출처: 추출본 v2.txt 3480~3487행(5 초마다 하트비트, 세 번 보낸 뒤 끊기고 x = 30 초 안에 재접속하지 않으면 오프라인; 30 초는 임의로 고른 값)·PDF 196쪽 그림 12-18.
#   계산: 마지막 하트비트 10 초 + 한도 30 초 = 40 초.
# Layout conventions: 축 y=176, 0 초 x=80·20 px/초(40 초 x=880), 눈금 5 초 간격, 이벤트 원 r=5·핵심 r=7, 상태 띠 y=328~360. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, SOFT, RULE, KR, MONO

W, H = 1000, 432
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 12-01 §8",
      "하트비트 세 번 뒤 끊기면 마지막 하트비트에서 30 초 뒤인 40 초에 오프라인이 된다",
      "하트비트 간격은 5 초이고 한도는 30 초다. 한도 안에 다시 붙으면 온라인이 이어진다.",
      "10 + 30 = 40 초")

X0, PX, AY = 80, 20, 176


def xt(t):
    return X0 + PX * t


d.line(X0 - 20, AY, 960, AY, MUTED, 1.2)
for t in range(0, 45, 5):
    d.line(xt(t), AY - 6, xt(t), AY + 6, MUTED, 1.0)
    d.t(xt(t), AY + 28, f"{t} s", 12, SOFT, MONO, "middle")

# 하트비트 세 번
for k, t in enumerate((0, 5, 10)):
    x = xt(t)
    d.line(x, AY - 8, x, AY - 36, RULE, 1.0)
    d.o.append(f'<circle cx="{x}" cy="{AY}" r="5" fill="{INFO}"/>')
    d.t(x, AY - 44, f"하트비트 {k + 1}", 13, INFO, KR, "middle", 600)

# 끊김
d.chip(xt(10), AY + 60, "끊김", WARN, 13)

# 한도 30 초
d.line(xt(10), 268, xt(40), 268, WARN, 1.6)
d.line(xt(10), 260, xt(10), 276, WARN, 1.6)
d.line(xt(40), 260, xt(40), 276, WARN, 1.6)
d.t((xt(10) + xt(40)) / 2, 256, "한도 x = 30 s", 13, WARN, KR, "middle", 600)
d.t((xt(10) + xt(40)) / 2, 296, "한도 안 재접속이면 온라인 유지", 13, MUTED, KR, "middle")

# 오프라인 전환
d.line(xt(40), AY - 8, xt(40), AY - 36, RULE, 1.0)
d.o.append(f'<circle cx="{xt(40)}" cy="{AY}" r="7" fill="{ACC}"/>')
d.t(xt(40), AY - 44, "40 s = 10 + 30 · 오프라인", 13, ACC, KR, "end", 600)

# 상태 띠
BY, BH = 328, 32
d.o.append(f'<rect x="{xt(0)}" y="{BY}" width="{xt(40) - xt(0)}" height="{BH}" rx="4" fill="{OK}22" stroke="{OK}" stroke-width="1.1"/>')
d.t((xt(0) + xt(40)) / 2, BY + 21, "온라인", 13, OK, KR, "middle", 600)
d.o.append(f'<rect x="{xt(40)}" y="{BY}" width="{960 - xt(40)}" height="{BH}" rx="4" fill="{BAD}22" stroke="{BAD}" stroke-width="1.1"/>')
d.t((xt(40) + 960) / 2, BY + 21, "오프라인", 13, BAD, KR, "middle", 600)

d.legend(H - 40, [("하트비트", INFO), ("끊김과 한도", WARN), ("온라인", OK), ("오프라인", BAD), ("전환 시각", ACC)])
d.save("12-01.heartbeat-timeline.svg")
