# 06-04 §1 — 저장소를 나누면 결합이 계약으로 바뀐다 (원문 Polyrepo 정의와 이점 목록).
# 배지의 "0 in"은 저장소끼리 직접 참조가 없다는 뜻이고, 계약 노드의 "3 in"이 모든 통신이 지나는 자리다.
# 폭발 반경 문구는 원문 두 번째 이점("blasting radius ... strictly confined to our project")을 옮긴 것이다.
# 타입 스펙: type-dependency — 무엇이 무엇에 의존하나. 트리로 안 그려지는 fan-in 이 논지다.
#           축약: 03-04.shared-state-cycle 의 배지 표기를 승계하되, 여기서는 순환이 없어 CYCLE 표시를 쓰지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1240
BW, BH, GAP, X0, RY = 340, 96, 48, 88, 140
CX, CY, CW, CH = 380, 320, 480, 96
CAP_Y = 468
LEGEND_Y = CAP_Y + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-04 §1",
      "결합이 계약으로 바뀐다",
      "위가 각자 자기 저장소에 사는 애플리케이션이고 아래가 그들이 통신하는 유일한 경로다. 색이 붙은 것이 모든 통신이 지나는 자리다.",
      "배지는 그 노드로 들어오는 직접 의존의 수입니다")

def badge(x, y, txt, c):
    bw = len(txt) * 7.0 + 16
    d.o.append(f'<rect x="{x - bw}" y="{y}" width="{bw}" height="20" rx="4" fill="{PAPER}" stroke="{c}" stroke-width="0.9"/>')
    d.t(x - bw / 2, y + 14, txt, 9, c, MONO)

repos = [("카탈로그 저장소", "catalog"), ("결제 저장소", "payments"), ("계정 저장소", "my-account")]
for i, (name, en) in enumerate(repos):
    x = X0 + i * (BW + GAP)
    d.box(x, RY, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, RY + 36, name, 13, INK, KR, "start", 600)
    d.t(x + 20, RY + 58, en, 9.5, MUTED, MONO, "start")
    badge(x + BW - 16, RY + 16, "0 in", MUTED)
    d.arrow([(x + BW / 2, RY + BH), (x + BW / 2, CY - 20), (W / 2, CY - 20), (W / 2, CY - 2)],
            SOFT, "soft", 1.2, "4 4")

d.o.append(f'<rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX + 20, CY + 36, "API 계약", 13, ACC, KR, "start", 600)
d.t(CX + 20, CY + 58, "생산자와 소비자 사이 · 릴리스와 깨는 변경을 거버넌스가 관리한다", 10, MUTED, KR, "start")
badge(CX + CW - 16, CY + 16, "3 in", ACC)

d.t(W / 2, CAP_Y, "변경의 폭발 반경이 자기 저장소 안으로 엄격히 갇힌다 · 다른 팀의 프로젝트를 깨뜨릴 길이 없다", 11, MUTED)

d.legend(LEGEND_Y, [("모든 통신이 지나는 자리", ACC), ("계약을 통해서만 닿는다", SOFT)])
d.save("06-04.polyrepo-contracts.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", X0 + 3 * BW + 2 * GAP)
