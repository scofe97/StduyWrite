# 14-01 §집계 — 역할을 복사하지 않고 합칩니다
# 제목이 "라벨 전파" 다. 정적인 합집합 그림으로는 전파가 안 보이므로, 구성 롤 하나를 고쳤을 때
# 그 변경이 집계 롤까지 가는 경로를 따로 그린다 — 본문이 집계를 쓰는 이유로 든 것이 그것이다.
# 아래 경고 띠는 곁가지가 아니라 위 구조의 결과다. rules 를 컨트롤 플레인이 쓰기 때문에
# 매니페스트에 rules 를 두면 소유권이 부딪힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, WARN, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 664
d = D(W, H, "KUBERNETES UP AND RUNNING · 14-01",
      "복사하지 않고 라벨로 끌어온다",
      "집계 역할은 구성 역할들의 능력을 모두 합치고, 구성 역할 중 어느 하나가 바뀌면 그 변경이 "
      "집계 역할로 자동 전파된다. 합칠 대상은 라벨 셀렉터가 고른다.",
      "rules 배열은 사람이 아니라 컨트롤 플레인이 채운다")

SX, SW, SH = 40, 300, 68
ys = [170, 254, 338]
for i, y in enumerate(ys):
    cy = y + SH / 2
    focal = i == 2      # 초점은 맨 아래 — 전파 경로가 다른 상자를 가로지르지 않는다
    if focal:
        d.o.append(f'<rect x="{SX}" y="{y}" width="{SW}" height="{SH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(SX, y, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(SX + SW / 2, cy - 2, f"잘게 나눈 ClusterRole {i+1}", 12,
        ACC if focal else INK, KR, "middle", 600)
    d.t(SX + SW / 2, cy + 18, 'aggregate-to-edit: "true"', 10, ACC if focal else SOFT, MONO)
d.t(SX + SW / 2, 148, "라벨을 붙여 둔 구성 역할들", 11, SOFT, KR)

EX, EW = 430, 280
d.box(EX, 238, EW, 100, PAPER2, RULE, 1.1, 6)
d.t(EX + EW / 2, 268, "aggregationRule", 12, INK, MONO, "middle", 600)
d.t(EX + EW / 2, 292, "clusterRoleSelectors", 11, INK, MONO)
d.t(EX + EW / 2, 314, "라벨 셀렉터 — 복수형이다", 10, SOFT, KR)

for y, ey in zip(ys, (262, 288, 314)):
    cy = y + SH / 2
    if cy == ey:
        d.path(f"M {SX+SW} {cy} L {EX-4} {cy}", MUTED, 1.4, m="ar")
    else:
        d.path(f"M {SX+SW} {cy} L 385 {cy} L 385 {ey} L {EX-4} {ey}", MUTED, 1.4, m="ar")

AX, AW = 800, 416
d.box(AX, 170, AW, 236, PAPER2, RULE, 1.1, 8)
d.t(AX + AW / 2, 200, "집계 ClusterRole  edit", 14, INK, KR, "middle", 600)
d.t(AX + AW / 2, 222, "aggregationRule 하나만 갖는다", 10, SOFT, KR)
d.box(AX + 20, 240, AW - 40, 146, PAPER, RULE, 0.9, 6)
d.t(AX + 36, 262, "rules", 11, INK, MONO, "start")
d.t(AX + AW - 36, 262, "컨트롤 플레인이 동적으로 채운다", 10, SOFT, KR, "end")
for i in range(3):
    yy = 282 + i * 32
    d.o.append(f'<rect x="{AX+36}" y="{yy}" width="{AW-72}" height="24" rx="4" '
               f'fill="{PAPER2}" stroke="{ACC if i==2 else RULE}" stroke-width="0.9"/>')
    d.t(AX + AW / 2, yy + 16, f"ClusterRole {i+1} 의 규칙", 10,
        ACC if i == 2 else SOFT, KR)
d.path(f"M {EX+EW} 288 L {AX-4} 288", MUTED, 1.4, m="ar")

d.path(f"M {SX+SW/2} 406 L {SX+SW/2} 452 L 1008 452 L 1008 410", ACC, 1.5, m="acc", dash="6 5")
d.t(628, 476, "구성 역할을 한 줄 고치면 집계 역할의 rules 가 따라 바뀐다.", 11, ACC, KR)
d.t(628, 498, "복사해 두었다면 한쪽이 바뀌어도 따라가지 않는다 — 집계를 쓰는 이유가 이것이다.", 11, ACC, KR)

BT, BB = 518, 588
d.o.append(f'<rect x="12" y="{BT}" width="{W-36}" height="{BB-BT}" rx="8" '
           f'fill="{WARN}0E" stroke="{WARN}" stroke-width="1.2"/>')
d.t(W / 2, BT + 26, "집계 ClusterRole 매니페스트에는 rules 필드를 아예 두지 않는다. 컨트롤 플레인이 채우는 자리이기 때문이다.",
     11, WARN, KR)
d.t(W / 2, BT + 48, "빈 리스트라도 적어 두면 server-side apply 가 그 필드의 소유권을 주장해, 이후 apply 가 충돌하거나 규칙을 지웠다 채웠다 반복한다.",
     11, WARN, KR)

d.legend(BB + 24, [("고치면 전파되는 경로", ACC), ("GitOps 에서 걸리는 자리", WARN)])
d.save("14-01.clusterrole-aggregation.svg")
print("h 필요:", BB + 24 + 48, " 실제:", H)
