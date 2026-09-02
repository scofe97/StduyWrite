# 06-03 §1 — 모든 프로젝트가 한 저장소 안에 있다 (원문 Figure 6-1 과 Monorepo 정의).
# 아래의 공유 라이브러리는 저자가 첫 이점으로 든 것이다 — 코드를 추상화해 이득 볼 모든 프로젝트에 연다.
# 점선이 그 참조이고, 저자가 조각에 대해 남긴 경고("너무 많이 결합하면 독립 배포성을 잃는다")가 이 선에 붙는다.
# 타입 스펙: type-nested — 바깥이 넓은 범위이고 안이 그 안에 담긴 것. 포함 관계가 곧 저장소 경계다.
#           축약: 03-06 의 링 기하를 승계하되 안쪽에 형제 상자를 나란히 두는 depth 2 배치로 썼다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1000
ZX, ZY, ZW, ZH = 60, 100, 880, 320
PX, PY, PW, PH, PGAP = 104, 168, 248, 88, 24
SX, SY, SW, SH = 104, 296, 792, 76
LEGEND_Y = ZY + ZH + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-03 §1",
      "모든 프로젝트가 한 저장소 안에 있다",
      "바깥 상자가 저장소이고 안이 그 안에 함께 놓인 것들이다. 색이 붙은 것이 저자가 첫 이점으로 든 공유 라이브러리다.",
      "점선은 배포나 버전 없이 바로 닿는 참조입니다")

# 저장소 경계
d.o.append(f'<rect x="{ZX}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="{INK}04" stroke="{INK}4D" stroke-width="1.0"/>')
lab = "ONE REPOSITORY"
lw = len(lab) * 6.4 + 16
d.o.append(f'<rect x="{ZX + 24}" y="{ZY - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
d.t(ZX + 24 + lw / 2, ZY + 3, lab, 7.5, SOFT, MONO)
d.t(ZX + 24, ZY + 30, "모든 팀이 같은 저장소를 쓴다", 13.5, INK, KR, "start", 600)

projects = [("팀 A 의 프로젝트", "project"), ("팀 B 의 프로젝트", "project"), ("팀 C 의 프로젝트", "project")]
for i, (name, en) in enumerate(projects):
    x = PX + i * (PW + PGAP)
    d.box(x, PY, PW, PH, PAPER2, RULE, 1.0, 6)
    d.t(x + PW / 2, PY + 36, name, 12.5, INK, KR, "middle", 600)
    d.t(x + PW / 2, PY + 58, en, 9, MUTED, MONO)
    d.arrow([(x + PW / 2, PY + PH), (x + PW / 2, SY - 2)], SOFT, "soft", 1.1, "4 4")

d.o.append(f'<rect x="{SX}" y="{SY}" width="{SW}" height="{SH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(SX + 20, SY + 32, "공유 라이브러리", 13, ACC, KR, "start", 600)
d.t(SX + 20, SY + 56, "코드를 추상화해 이득 볼 모든 프로젝트에 연다 · 배포도 버전도 거치지 않는다", 10.5, MUTED, KR, "start")

d.legend(LEGEND_Y, [("한자리에 있어서 생기는 것", ACC), ("바로 닿는 참조", SOFT)])
d.save("06-03.monorepo-shape.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", PX + 3 * PW + 2 * PGAP)
