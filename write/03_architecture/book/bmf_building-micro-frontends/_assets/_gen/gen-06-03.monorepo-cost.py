# 06-03 §3 — 모노레포가 치르는 값 다섯을 하나의 결과에 붙인다 (원문 Monorepo 의 challenges 목록).
# 원문은 다섯을 목록으로 늘어놓고 결과를 따로 세지 않는다. 하나의 결과로 묶은 것은 노트의 읽기이며,
# 그 결과 문구는 원문이 첫째 값에 적은 "entire workforce being slowed down"을 옮긴 것이다.
# accent 는 저자가 조각에 대해 따로 경고를 남긴 원인("프로젝트 결합")에 준다.
# 타입 스펙: type-fishbone — 관측된 결과 하나에 원인을 범주로 묶어 단다. 좌표는 01-01 의 공식을 그대로 승계한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1440, 592
HEAD, CY = 1200, 320
d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-03 §3",
      "모노레포가 치르는 값 다섯",
      "오른쪽 끝이 값을 안 냈을 때의 결과이고, 뼈 다섯은 원문이 목록으로 든 난제다. 색이 붙은 뼈가 조각에 따로 경고가 붙은 원인이다.",
      "결과 하나로 묶은 것은 노트의 읽기이고, 뼈 다섯은 원문의 목록입니다")

# k → (범주명, [하위 원인 두 개], accent 여부). 홀수 k 가 위, 짝수 k 가 아래.
bones = [
    (1, "자동화 도구 투자",  [(2, "모노레포에 안 맞는 도구가 많다"), (4, "저장소가 지수적으로 커진다")], False),
    (2, "코드베이스 확장",   [(2, "임계를 넘으면 투자가 계속 는다"), (4, "Google · Facebook · X 가 자체 도구를 만들었다")], False),
    (3, "프로젝트 결합",     [(2, "함께 배포될 때만 존재한다"), (4, "다른 모노레포에 공유하지 못한다")], True),
    (4, "트렁크 기반 개발",  [(2, "하루 수천 커밋을 받는 브랜치"), (4, "조직 전체의 규율과 성숙도")], False),
    (5, "개발자 규율",       [(2, "수십에서 수백 명이 함께"), (4, "히스토리가 지저분해진다")], False),
]

def attach_x(k):  return HEAD - 160 - k * 160
def above(k):     return k % 2 == 1

# 1) 등뼈
d.arrow([(attach_x(5) - 160, CY), (HEAD - 4, CY)], INK, "ar", 1.2)

# 2) 뼈와 하위 원인 눈금 (선을 먼저 — 상자 채움이 선 끝을 덮게)
for k, name, subs, acc in bones:
    ax, up = attach_x(k), above(k)
    fx, fy = ax - 96, CY - 168 if up else CY + 168
    d.line(ax, CY, fx, fy, ACC if acc else MUTED, 1.4 if acc else 1.1)
    for m, label in subs:
        tx, ty = ax - 16 * m, CY - 28 * m if up else CY + 28 * m
        d.line(tx, ty, tx - 32, ty, SOFT, 1.0)
        d.t(tx - 36, ty - 4 if up else ty + 12, label, 9, MUTED, KR, "end")

# 3) 범주 태그 상자
for k, name, subs, acc in bones:
    fx = attach_x(k) - 96
    fy = CY - 168 if above(k) else CY + 168
    tw = len(name) * 13 + 24
    if acc:
        d.o.append(f'<rect x="{fx - tw / 2}" y="{fy - 14}" width="{tw}" height="28" rx="4" fill="{ACC}14" stroke="{ACC}" stroke-width="1.3"/>')
    else:
        d.box(fx - tw / 2, fy - 14, tw, 28, PAPER2, RULE, 1.0, 4)
    d.t(fx, fy + 5, name, 12, ACC if acc else INK, KR, "middle", 600)

# 4) 결과 상자
d.o.append(f'<rect x="{HEAD}" y="{CY - 40}" width="200" height="80" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
d.t(HEAD + 100, CY - 10, "값을 안 내면", 12, ACC, KR, "middle", 600)
d.t(HEAD + 100, CY + 10, "전체가 함께 느려진다", 12, ACC, KR, "middle", 600)
d.t(HEAD + 100, CY + 30, "OBSERVED EFFECT", 8, SOFT, MONO)

d.legend(540, [("조각에 따로 경고가 붙은 원인 · 그 결과", ACC)])
d.save("06-03.monorepo-cost.svg")
print("h 필요:", 540 + 22 + 16, " 실제:", H, " 최좌측 태그:", attach_x(5) - 96 - (len("개발자 규율") * 13 + 24) / 2)
