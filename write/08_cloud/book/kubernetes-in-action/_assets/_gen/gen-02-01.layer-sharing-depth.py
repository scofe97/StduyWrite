# 02-01 §4 — 컨테이너마다 공유하는 깊이가 다르다
# 본문 근거(02-01 §4):
#   "컨테이너 A·B는 이미지 레이어 하나를 공유합니다. 즉 애플리케이션 A·B가 같은 파일 일부를
#    읽습니다. 그리고 이 둘은 컨테이너 C와도 아래쪽 레이어를 공유합니다."
#   "Docker 는 각 레이어를 단 한 번만 저장합니다." · "저장 단위가 이미지가 아니라 레이어"
# 타입 스펙: 공유 폭이 층마다 달라지는 것이 논지다 — 층이 아래로 갈수록 넓어지는 스택 비교.
#   manifest 장은 '저장 단위' 를, CoW 장은 '수정 시 격리' 를 진다. 이 장은 '공유 깊이' 만 진다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO
import ddx

COLS = ((220, "컨테이너 A"), (500, "컨테이너 B"), (780, "컨테이너 C"))
CW, RH = 240, 56
APP_Y, AB_Y, BASE_Y = 176, 248, 320
BAND_Y1 = BASE_Y + RH + 36
NOTE_Y, LEG_Y = BAND_Y1 + 28, BAND_Y1 + 52
W, H = 1000, LEG_Y + 40

d = D(W, H, "KUBERNETES IN ACTION · 02-01",
      "아래로 갈수록 함께 쓰는 층이 넓어진다",
      "레이어는 이미지가 아니라 층 단위로 한 벌만 저장된다. 그래서 컨테이너마다 어디까지를 "
      "함께 쓰는지가 달라지고, 겹치는 층은 디스크에 하나만 존재한다.",
      lead="A·B 는 위쪽 층까지 함께 쓰고, C 는 맨 아래 층부터 함께 쓴다")

ddx.band(d, 104, BAND_Y1, "겹치는 층은 디스크에 한 벌뿐이다 — 세 컨테이너가 같은 파일을 가리킨다")

for cx, name in COLS:
    d.t(cx, 160, name, 12, SOFT, KR)
    d.box(cx - CW // 2, APP_Y, CW, RH, PAPER2, RULE, 1.1, 6)
    d.t(cx, APP_Y + 26, f"앱 {name[-1]} 레이어", 13, INK, KR, "middle", 600)
    d.t(cx, APP_Y + 44, "자기만 쓰는 층", 10, SOFT, KR)

# A·B 만 함께 쓰는 층
d.box(100, AB_Y, 520, RH, f"{INFO}12", INFO, 1.2, 6)
d.t(360, AB_Y + 26, "A·B 가 함께 쓰는 이미지 레이어", 13, INFO, KR, "middle", 600)
d.t(360, AB_Y + 44, "같은 파일 일부를 함께 읽는다", 10, SOFT, KR)
d.t(780, AB_Y + 32, "C 는 이 층을 쓰지 않는다", 11, MUTED, KR)

# 세 컨테이너가 모두 함께 쓰는 맨 아래 층 — 이 도식의 focal
d.o.append(f'<rect x="100" y="{BASE_Y}" width="800" height="{RH}" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(500, BASE_Y + 26, "세 컨테이너가 함께 쓰는 베이스 레이어", 13, ACC, KR, "middle", 600)
d.t(500, BASE_Y + 44, "디스크에 한 벌만 있고 셋이 가리킨다", 10, SOFT, KR)

d.t(24, NOTE_Y, "저장 단위가 이미지가 아니라 레이어라서 이 겹침이 생긴다 — 같은 층을 담은 이미지를 "
                "여럿 받아도 실물은 한 번만 내려받는다.", 11, MUTED, KR, "start")
d.legend(LEG_Y, [("셋이 함께 쓰는 층", ACC), ("둘만 함께 쓰는 층", INFO)])
d.save("02-01-layer-sharing-depth.svg")
print("ok layer-sharing-depth")
