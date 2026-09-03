# 11-01 §8 istiod 오토스케일링이 진동하는 이유 — 원문 "Autoscaling istiod deployment" 상자.
# 본문(원문 11.3.4): 오토스케일링은 istiod 같은 버스트성 워크로드에 좋은 생각이지만 지금은 효과가 없다.
#       istiod 가 워크로드와 30분짜리 커넥션을 맺어 ADS 로 프록시를 설정·갱신하기 때문이다. 그래서 새로 뜬
#       istiod 레플리카는 기존 프록시와 파일럿 사이의 커넥션이 만료될 때까지 아무 부하도 받지 못한다.
#       부하를 못 받으니 다시 축소되고, 배포가 반복해서 늘었다 줄었다 하는 진동이 생긴다.
# 타입 스펙: type-state — 유한 상태와 전이가 논점이고 마지막 전이가 첫 상태로 돌아온다. 시작은 채운 점,
#           전이마다 라벨, coral 은 독자가 주목할 상태 하나(진동의 원인이 놓인 자리).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1200, 620
d = D(W, H, "ISTIO IN ACTION · 11-01 §8",
      "새 레플리카가 부하를 못 받아 다시 줄어든다",
      "오토스케일러가 레플리카를 늘려도 기존 프록시의 커넥션이 30분 동안 유지되어 새 레플리카에 부하가 "
      "붙지 않는다. 색이 붙은 상태가 그 원인 자리이고, 거기서 곧장 축소로 이어져 진동이 된다.",
      "그래서 현재 권고는 며칠·몇 주 단위의 완만한 증가에 맞추는 것입니다")

SW, SH = 244, 60
def state(x, y, label, sub, c=None, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(x + SW / 2, y + 26, label, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, y + 44, sub, 11, MUTED, KR)

TOP, BOT = 156, 340
S1, S2, S3 = 96, 452, 808
d.o.append(f'<circle cx="60" cy="{TOP + SH / 2}" r="6" fill="{INK}"/>')
d.arrow([(68, TOP + SH / 2), (S1 - 2, TOP + SH / 2)], MUTED, "ar", 1.4)

state(S1, TOP, "CPU 가 오른다", "버스트성 이벤트", WARN)
state(S2, TOP, "레플리카를 늘린다", "오토스케일러가 판단")
state(S3, TOP, "새 레플리카가 뜬다", "ADS 커넥션 없음")
state(S3, BOT, "부하가 붙지 않는다", "기존 커넥션이 30분 유지", focal=True)
state(S2, BOT, "부하 0 으로 읽힌다", "오토스케일러가 다시 판단")
state(S1, BOT, "레플리카를 줄인다", "방금 늘린 것을 되돌린다", WARN)

def lab(x, y, txt, c=MUTED):
    lw = len(txt) * 11 + 12
    d.o.append(f'<rect x="{x - lw / 2}" y="{y - 13}" width="{lw}" height="18" rx="3" fill="{PAPER}"/>')
    d.t(x, y, txt, 11, c, KR, "middle", 600)

d.arrow([(S1 + SW, TOP + SH / 2), (S2 - 2, TOP + SH / 2)], MUTED, "ar", 1.4)
lab((S1 + SW + S2) / 2, TOP + SH / 2 - 14, "임계를 넘는다")
d.arrow([(S2 + SW, TOP + SH / 2), (S3 - 2, TOP + SH / 2)], MUTED, "ar", 1.4)
lab((S2 + SW + S3) / 2, TOP + SH / 2 - 14, "기동한다")
d.arrow([(S3 + SW / 2, TOP + SH), (S3 + SW / 2, BOT - 2)], ACC, "acc", 1.5)
lab(S3 + SW / 2, (TOP + SH + BOT) / 2 + 4, "ADS 를 못 받는다", ACC)
d.arrow([(S3, BOT + SH / 2), (S2 + SW + 2, BOT + SH / 2)], MUTED, "ar", 1.4)
lab((S2 + SW + S3) / 2, BOT + SH / 2 - 14, "쓸 일이 없다")
d.arrow([(S2, BOT + SH / 2), (S1 + SW + 2, BOT + SH / 2)], MUTED, "ar", 1.4)
lab((S1 + SW + S2) / 2, BOT + SH / 2 - 14, "임계 아래로 본다")
d.arrow([(S1 + SW / 2, BOT), (S1 + SW / 2, TOP + SH + 4)], WARN, "warn", 1.3, dash="5 4")
lab(S1 + SW / 2, (TOP + SH + BOT) / 2 + 4, "다시 처음으로", WARN)

d.t(32, 452, "저자의 진단 — istiod 는 워크로드와 30분짜리 커넥션을 맺고 그 커넥션으로 ADS 갱신을 보낸다", 11, SOFT, KR, "start")
d.t(32, 476, "그래서 늘어난 레플리카는 기존 커넥션이 만료될 때까지 놀고, 노는 동안 다시 줄여진다", 11, MUTED, KR, "start")
d.t(32, 500, "저자의 권고 — 두 레플리카 아래로는 절대 내리지 않고 자원은 넉넉히 준다", 11, SOFT, KR, "start")
d.legend(528, [("진동의 원인이 놓인 자리", ACC), ("되돌아오는 구간", WARN)])
d.save("11-01.autoscale-flapping.svg")
