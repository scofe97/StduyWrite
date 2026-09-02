# 06-01 §2 — CI · 지속 전달 · 지속 배포의 자동화 범위 (원문 CONTINUOUS INTEGRATION VERSUS DELIVERY VERSUS DEPLOYMENT).
# 저자는 이 셋을 겹으로 그리지 않는다. 겹으로 묶은 것은 노트의 읽기이며, 각 겹의 문구는 원문 정의를 옮긴 것이다.
# 오른쪽 태그가 "파이프라인이 어디서 멈추는가"이고, 그 자리가 셋을 가른다.
# 타입 스펙: type-nested — 바깥이 넓은 범위, 안으로 갈수록 좁다. 포함 관계가 곧 자동화 범위다.
#           축약: 03-06 의 링 기하를 승계하되 밴드를 68px 로 넓혀 오른쪽 정지 지점 태그를 실었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, KR, MONO

W = 1000
# 밴드 68px 씩 — 각 겹의 머리글 · 이름 · 설명 세 줄이 들어가는 최소 높이다.
rings = [
    (60, 100, 900, 348, "CONTINUOUS DEPLOYMENT", "지속 배포",
     "커밋된 코드로 빌드한 아티팩트를 프로덕션에 곧바로 배포한다", "멈추지 않는다",
     f"{INK}4D", 1.0, f"{INK}04", INK),
    (110, 168, 800, 212, "CONTINUOUS DELIVERY", "지속 전달",
     "테스트 뒤 배포 준비가 끝난 아티팩트를 만들어 둔다", "배포 대시보드 앞에서 멈춘다",
     ACC, 1.4, f"{ACC}12", ACC),
    (160, 236, 700, 76, "CONTINUOUS INTEGRATION", "지속 통합",
     "main 으로 머지될 때마다 파이프라인이 돈다", "릴리스 브랜치 앞에서 멈춘다",
     MUTED, 1.1, f"{INK}06", INK),
]
LEGEND_Y = 448 + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-01 §2",
      "세 전략의 자동화 범위",
      "안쪽이 좁은 범위이고 바깥으로 갈수록 사람의 손이 빠진다. 색이 붙은 겹이 대시보드의 클릭 하나를 남겨 둔 단계다.",
      "오른쪽 태그가 그 전략에서 파이프라인이 멈추는 자리입니다")

for x, y, w, h, eyebrow, name, desc, stops, stroke, sw, fill, ink in rings:
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    lw = len(eyebrow) * 6.4 + 16
    d.o.append(f'<rect x="{x + 24}" y="{y - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
    d.t(x + 24 + lw / 2, y + 3, eyebrow, 7.5, stroke if stroke == ACC else SOFT, MONO)
    d.t(x + 24, y + 30, name, 14, ink, KR, "start", 600)
    d.t(x + 24, y + 50, desc, 11, MUTED, KR, "start")
    d.t(x + w - 24, y + 30, stops, 10, ink, KR, "end", 600)

d.legend(LEGEND_Y, [("사람의 클릭이 남아 있는 단계", ACC)])
d.save("06-01.ci-cd-scope.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
