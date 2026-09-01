# 05-01 §3 — 성공한 SSR 조각 구현 대부분이 고르는 굵은 수평 분할.
# 헤더와 푸터는 공유하고 본문만 페이지나 도메인으로 나눈다는 저자의 서술을 그대로 그린다.
# 타입 스펙: type-architecture — 논리 경계(공유 영역 / 팀이 나눠 갖는 영역)로 묶은 구성요소와 소유 관계.
#           accent 는 팀 경계가 실제로 갈리는 단 하나의 띠.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1160
PX, PW = 60, 1040
HDR_Y, HDR_H = 122, 62
MAIN_Y, MAIN_H = 208, 148
FTR_Y, FTR_H = 380, 62
LEGEND_Y = FTR_Y + FTR_H + 34
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-01 §3",
      "굵게 나누고 위아래는 공유한다",
      "거의 바뀌지 않는 헤더와 푸터는 애플리케이션 전체가 함께 쓰고, 자주 바뀌는 본문만 페이지나 도메인으로 나눈다.",
      "색이 붙은 가운데 띠에서만 팀 경계가 갈립니다")

# 페이지 테두리
d.o.append(f'<rect x="{PX}" y="{HDR_Y - 14}" width="{PW}" height="{FTR_Y + FTR_H + 14 - HDR_Y + 14}" rx="8" '
           f'fill="{INK}03" stroke="{INK}30" stroke-width="1.0" stroke-dasharray="4 4"/>')
lab = "ONE PAGE"
tw = len(lab) * 5.6 + 14
d.o.append(f'<rect x="{PX + 14}" y="{HDR_Y - 22}" width="{tw}" height="16" fill="{PAPER}"/>')
d.t(PX + 20, HDR_Y - 10, lab, 8, SOFT, MONO, "start")

for y, h, name, sub in ((HDR_Y, HDR_H, "헤더", "거의 바뀌지 않아 전체가 공유한다"),
                        (FTR_Y, FTR_H, "푸터", "거의 바뀌지 않아 전체가 공유한다")):
    d.box(PX + 24, y, PW - 48, h, PAPER2, RULE, 1.0, 6)
    d.t(PX + 48, y + 26, name, 13, INK, KR, "start", 600)
    d.t(PX + 48, y + 46, sub, 10, MUTED, KR, "start")

# 본문 — 여기서만 팀이 갈린다
d.o.append(f'<rect x="{PX + 24}" y="{MAIN_Y}" width="{PW - 48}" height="{MAIN_H}" rx="6" '
           f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.3" stroke-dasharray="5 4"/>')
lab2 = "MAIN CONTENT · SPLIT BY PAGE OR DOMAIN"
tw2 = len(lab2) * 5.6 + 14
d.o.append(f'<rect x="{PX + 48}" y="{MAIN_Y - 8}" width="{tw2}" height="16" fill="{PAPER}"/>')
d.t(PX + 54, MAIN_Y + 4, lab2, 8, ACC, MONO, "start")

BW = 300
for i, (name, team) in enumerate((("상품 페이지", "team A"), ("체크아웃 흐름", "team B"), ("그 밖의 도메인", "team C"))):
    x = PX + 56 + i * (BW + 32)
    d.box(x, MAIN_Y + 30, BW, 88, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, MAIN_Y + 58, name, 12.5, INK, KR, "start", 600)
    d.t(x + 20, MAIN_Y + 78, team, 9, MUTED, MONO, "start")
    d.t(x + 20, MAIN_Y + 100, "자주 바뀌므로 팀이 나눠 갖는다", 9.5, MUTED, KR, "start")

d.legend(LEGEND_Y, [("팀 경계가 갈리는 자리", ACC)])
d.save("05-01.coarse-split.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", PX + 56 + 2 * (BW + 32) + BW)
