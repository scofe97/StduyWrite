# 02-01 §2 — 수평 분할과 수직 분할 (원문 Figure 2-1). 같은 화면 셋을 두 방식으로 나눠 나란히 둔다.
# 화면 이름은 지어내지 않고 저자가 도메인 예로 든 인증(authentication)·카탈로그(catalog)를 쓰고
# 나머지 한 칸은 저자가 §Defining 에서 든 랜딩 페이지를 쓴다.
# 타입 스펙: type-architecture — 두 신뢰 경계(분할 방식)로 묶은 구성요소와 소유 관계.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1240, 448
d = D(W, H, "BUILDING MICRO-FRONTENDS · 02-01 §2",
      "수평 분할과 수직 분할 — 같은 화면을 두 방식으로",
      "수평 분할은 한 화면 안을 여러 팀이 나눠 갖고, 수직 분할은 화면 하나를 한 팀이 통째로 갖는다. 색이 붙은 것이 팀 사이 조율이 필요한 자리다.",
      "왼쪽은 한 화면을 여럿이 나눠 갖고, 오른쪽은 화면마다 임자가 하나입니다")

def zone(x, y, w, h, label, sub):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" stroke="{RULE}" stroke-width="0.8"/>')
    lw = len(label) * 7 + 16
    d.o.append(f'<rect x="{x + 16}" y="{y - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw / 2, y + 3, label, 7.5, SOFT, MONO)
    d.t(x + w / 2, y + h - 14, sub, 11, MUTED, KR)

ZY, ZH = 112, 268
zone(40, ZY, 560, ZH, "HORIZONTAL SPLIT", "한 화면을 여러 팀이 나눠 갖는다 — 조율이 늘고 재사용이 는다")
zone(660, ZY, 540, ZH, "VERTICAL SPLIT", "화면 하나를 한 팀이 통째로 갖는다 — 조율이 준다")

# 왼쪽 — 화면 하나 안에 팀 셋
d.box(80, 150, 480, 190, PAPER2, RULE, 1.0, 6)
d.t(320, 172, "카탈로그 화면 하나", 12, INK, KR, "middle", 600)
bands = [("헤더 · 검색", "팀 A"), ("상품 목록", "팀 B"), ("추천 영역", "팀 C")]
for i, (name, team) in enumerate(bands):
    by = 186 + i * 50
    d.box(100, by, 440, 42, PAPER, RULE, 0.9, 4)
    d.t(116, by + 26, name, 12, INK, KR, "start")
    d.t(524, by + 26, team, 10, MUTED, MONO, "end")
# 조율 표시 — accent 하나
# 라벨을 윗변에 두면 첫 밴드에 겹친다. 점선 상자 아랫변으로 옮긴다 (밴드 끝 328 아래).
d.o.append(f'<rect x="88" y="180" width="464" height="156" rx="6" fill="none" stroke="{ACC}" stroke-width="1.3" stroke-dasharray="5 4"/>')
d.o.append(f'<rect x="256" y="330" width="128" height="12" rx="2" fill="{PAPER}"/>')
d.t(320, 339, "TEAMS MUST COORDINATE", 7.5, ACC, MONO)

# 오른쪽 — 화면 셋, 각각 한 팀
views = [("랜딩", "팀 D"), ("인증", "팀 E"), ("카탈로그", "팀 F")]
for i, (name, team) in enumerate(views):
    x = 670 + i * 180
    d.box(x, 150, 160, 190, PAPER2, RULE, 1.0, 6)
    d.t(x + 80, 176, f"{name} 화면", 12, INK, KR, "middle", 600)
    d.box(x + 14, 192, 132, 130, PAPER, RULE, 0.9, 4)
    d.t(x + 80, 256, team, 12, MUTED, MONO)
    d.t(x + 80, 276, "혼자 소유", 10, MUTED, KR)

d.legend(400, [("팀 사이 조율이 필요한 자리", ACC)])
d.save("02-01.split-approaches.svg")
print("h:", 400 + 38, "/", H)
