# 01-02 §4 — 저자가 컴포넌트 방식에서 지목한 결합. 여러 컨테이너가 한 컴포넌트로 몰리고,
# 그 컴포넌트의 API 가 다시 컨테이너에 맞춰지면서 변경이 되돌아온다.
# 타입 스펙: type-dependency — 트리로 못 그리는 fan-in 과 되돌아오는 간선이 논지다.
#           back-edge 는 저자가 "unwanted coupling" 이라 부른 그 결합이고, accent 예산 둘은 그 간선과 라벨이 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 940, 384
NW, NH = 160, 56
R0Y, R1Y = 120, 240
d = D(W, H, "BUILDING MICRO-FRONTENDS · 01-02 §4",
      "공유 컴포넌트로 몰리는 의존과 되돌아오는 간선",
      "도메인 컨테이너 셋이 설정형 공유 컴포넌트 하나에 의존하고, 그 컴포넌트의 API 가 컨테이너에 맞춰지면서 변경이 역방향으로 되돌아온다.",
      "우측 상단 배지가 그 노드에 몰린 의존 수이고, 점선이 저자가 원치 않는 결합이라 부른 간선입니다")

containers = [("검색 컨테이너", "search", "0 in"), ("체크아웃 컨테이너", "check-out", "1 in"), ("프로필 컨테이너", "profile", "0 in")]
X0 = (W - (3 * NW + 2 * 80)) / 2                      # 130
def cxr0(i): return X0 + i * (NW + 80) + NW / 2       # 210, 450, 690
SHARED_X = cxr0(1) - NW / 2                           # 370

def node(x, y, name, sub, badge, fill=PAPER2, stroke=RULE):
    d.box(x, y, NW, NH, fill, stroke, 1.0, 6)
    d.t(x + 12, y + 24, name, 11.5, INK, KR, "start", 600)
    d.t(x + 12, y + 42, sub, 9, SOFT, MONO, "start")
    bw = len(badge) * 5.4 + 10
    d.o.append(f'<rect x="{x + NW - bw - 6}" y="{y + 6}" width="{bw}" height="13" rx="2" fill="{PAPER}" stroke="{RULE}" stroke-width="0.7"/>')
    d.t(x + NW - bw / 2 - 6, y + 16, badge, 8, MUTED, MONO)

# 연결선 먼저 — 순방향 의존 (rank0 하단 → rank1 상단, 부착점 56px 간격)
for i, ax in enumerate((394, 450, 506)):
    sx = cxr0(i)
    if sx == ax:
        d.arrow([(sx, R0Y + NH), (ax, R1Y - 2)], MUTED, "ar", 1.2)
    else:
        s = 8 if ax > sx else -8
        d.path(f"M {sx} {R0Y + NH} V {R1Y - 40} Q {sx} {R1Y - 32} {sx + s} {R1Y - 32} "
               f"H {ax - s} Q {ax} {R1Y - 32} {ax} {R1Y - 24} V {R1Y - 2}", MUTED, 1.2, m="ar")

# back-edge — 노드 뒤를 지나지 않게 바깥으로 크게 돌린다
d.path(f"M {SHARED_X + NW} {R1Y + NH / 2} H 842 Q 850 {R1Y + NH / 2} 850 {R1Y + NH / 2 - 8} "
       f"V 108 Q 850 100 842 100 H {cxr0(1) + 8} Q {cxr0(1)} 100 {cxr0(1)} 108 V {R0Y - 2}",
       ACC, 1.3, m="acc", dash="5 4")
d.o.append(f'<rect x="826" y="192" width="48" height="14" rx="2" fill="{PAPER}"/>')
d.t(850, 202, "CYCLE", 8, ACC, MONO)
d.t(838, 250, "컨테이너에 맞춰진 API", 9, MUTED, KR, "end")

for i, (name, sub, badge) in enumerate(containers):
    node(X0 + i * (NW + 80), R0Y, name, sub, badge)
node(SHARED_X, R1Y, "공유 컴포넌트", "configurable", "3 in")
d.t(SHARED_X + NW / 2, R1Y + NH + 20, "여러 도메인에서 함께 쓰는 설정형 컴포넌트", 10, MUTED, KR)

d.legend(340, [("저자가 원치 않는 결합이라 부른 간선", ACC)])
d.save("01-02.component-coupling.svg")
print("h 필요:", 340 + 22 + 16, " 실제:", H)
