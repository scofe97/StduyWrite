# 02-01.conntrack-states — 엔트리 하나가 생겨서 사라지기까지 · 상태 축과 플래그 축은 따로다
# 본문 요구: "[UNREPLIED] 와 [ASSURED] 는 한 번의 전이가 아니라 두 단계다.
#            [UNREPLIED] 는 반대 방향 패킷이 관측되면 그 시점에 떨어지고, [ASSURED] 는 그보다 뒤에
#            붙는다(TCP 라면 양방향으로 데이터가 실제로 오간 뒤). 테이블이 꽉 찼을 때 커널은
#            [ASSURED] 가 없는 항목을 먼저 버린다."
# 2026-09-18 재설계 둘 —
#   (1) 이전 판은 곁가지 셋을 아래 띠에 이름만 늘어놓아 엔트리가 어디서 생겨 어디로 사라지는지가
#       그림에 없었다. 곁가지를 갈라지는 자리에 붙이고 소멸 경로를 둘로 폈다.
#   (2) 더 큰 결함 — 플래그를 상태 박스 **안에** 한 줄씩 박아 둬서 NEW=[UNREPLIED] ·
#       ESTABLISHED=[ASSURED] 라는 1:1 대응으로 읽혔다. 곡선 화살표로 "두 단계"를 덧대도
#       박스 안 표기가 그 보완을 지운다. 본문은 정반대를 말하므로 도식이 자기 제목과 어긋났다.
#       → 플래그를 박스에서 빼내 **별도 축**(아래 시간 레일)으로 옮긴다. 상태 전이는 위 축,
#       플래그 사건 셋은 아래 축이고, 부착·탈락·부착이 서로 다른 x 에 온다. 두 번째와 세 번째
#       사이의 간격이 accent 로 강조되는 것이 이 도식의 존재 이유다.
# 타입 스펙: type-state.md — 상태는 rx=8 둥근 사각, 시작은 채운 점, 끝은 고리 점,
#           전이 라벨은 event / action. "from any state" 는 상태마다 그리지 않고 단일 주석으로
#           둔다 → INVALID 로 가는 전이만 점선 + '어느 상태에서든'.
#           상태 5 · 전이 7 이라 스펙의 '전이 > 상태 x 2' 선을 넘지 않는다.
#           대각선은 dd-lint error 이므로 곁가지는 전부 수직 또는 ㄷ자 직각으로 뻗는다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 656
d = D(W, H, "CONNTRACK ENTRY · STATE AXIS vs FLAG AXIS",
      "conntrack 엔트리가 생겨서 사라지기까지 — 플래그는 상태와 다른 축이다",
      "위 축은 상태 전이(NEW → ESTABLISHED), 아래 축은 플래그가 붙고 떨어지는 시점이다. "
      "[UNREPLIED] 는 상태 전이와 같은 시점에 떨어지지만 [ASSURED] 는 그보다 뒤, "
      "양방향으로 데이터가 실제로 오간 뒤에 붙는다. 그 사이의 간격이 테이블 포화 때 "
      "무엇이 먼저 축출되는지를 가른다.",
      lead="상태 전이와 플래그 부착은 같은 시점이 아니다 · 그 간격이 축출 순서를 가른다")

CY, BH = 300, 96                    # 상태 축 252 .. 348
DOT_X, END_X = 48, 912
NEW_CX, NEW_W = 296, 192            # 200 .. 392
EST_CX, EST_W = 684, 232            # 568 .. 800
SIDE_Y, SIDE_H = 140, 68            # 주 경로 밖 상태 레인 140 .. 208
RAIL_Y = 430                        # 플래그 축


def state(cx, w, name, desc, ttl, c):
    """상태 축의 칸 — 이름 · 설명 · 남은 수명. 플래그는 여기 적지 않는다(아래 축이 맡는다)."""
    x, y = cx - w // 2, CY - BH // 2
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="8" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.4"/>')
    d.t(cx, CY - 26, ddx.fit(name, 12, w - 24, name), 12, c, MONO, "middle", 600)
    d.t(cx, CY, ddx.fit(desc, 12, w - 24, desc), 12, INK, KR)
    d.t(cx, CY + 26, ddx.fit(ttl, 12, w - 24, ttl), 12, MUTED, MONO)


def side(cx, w, name, desc, c):
    """주 경로 밖 상태 — 이름 · 설명 두 줄."""
    d.o.append(f'<rect x="{cx-w//2}" y="{SIDE_Y}" width="{w}" height="{SIDE_H}" rx="8" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, SIDE_Y + 28, ddx.fit(name, 12, w - 24, name), 12, c, MONO, "middle", 600)
    d.t(cx, SIDE_Y + 50, ddx.fit(desc, 12, w - 24, desc), 12, INK, KR)


# ── 상태 축 — 생성 → NEW → ESTABLISHED → 소멸 ──────────────────────
d.o.append(f'<circle cx="{DOT_X}" cy="{CY}" r="6" fill="{INK}"/>')
d.path(f"M {DOT_X+8} {CY} L {NEW_CX-NEW_W//2-8} {CY}", MUTED, 1.5, m="ar")
d.t(160, CY - 30, "첫 패킷", 12, MUTED, KR)
d.t(160, CY - 12, "TCP SYN", 11, SOFT, MONO)

state(NEW_CX, NEW_W, "NEW", "응답이 아직 없음", "120초", WARN)

d.path(f"M {NEW_CX+NEW_W//2} {CY} L {EST_CX-EST_W//2-8} {CY}", MUTED, 1.5, m="ar")
d.t(456, CY - 30, "반대 방향 패킷 관측", 12, MUTED, KR)

state(EST_CX, EST_W, "ESTABLISHED", "양방향으로 패킷 관측", "432000초 · 닷새", OK)

d.path(f"M {EST_CX+EST_W//2} {CY} L {END_X-14} {CY}", MUTED, 1.5, m="ar")
d.t(852, CY - 30, "수명 만료", 12, MUTED, KR)
d.t(852, CY - 12, "테이블에서 삭제", 11, SOFT, KR)

d.o.append(f'<circle cx="{END_X}" cy="{CY}" r="8" fill="none" stroke="{MUTED}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="{END_X}" cy="{CY}" r="5" fill="{MUTED}"/>')

# ── 주 경로 밖 상태 셋 (위 레인 · 수직으로만 뻗는다) ─────────────────
side(180, 216, "UNTRACKED", "엔트리를 만들지 않음", MUTED)
d.path(f"M 120 {CY} L 120 {SIDE_Y+SIDE_H+8}", MUTED, 1.4, m="ar")
d.o.append(f'<circle cx="120" cy="{CY}" r="3" fill="{MUTED}"/>')
d.t(132, 238, "raw 에서 NOTRACK", 12, MUTED, KR, "start")

side(452, 232, "INVALID", "엔트리 없이 폐기", BAD)
d.path(f"M 540 {CY} L 540 {SIDE_Y+SIDE_H+8}", BAD, 1.4, m="bad", dash="5 4")
d.o.append(f'<circle cx="540" cy="{CY}" r="3" fill="{BAD}"/>')
d.t(552, 238, "어느 상태에서든", 12, BAD, KR, "start")

side(728, 248, "RELATED", "부모 연결이 연 딸림 연결", INFO)
d.path(f"M 760 {CY-BH//2} L 760 {SIDE_Y+SIDE_H+8}", INFO, 1.4, m="info")
d.t(772, 238, "헬퍼가 인지", 12, INFO, KR, "start")

# ── 플래그 축 — 세 사건이 서로 다른 자리에 온다 ─────────────────────
E1, E2, E3 = 248, 480, 724
d.t(24, 406, "플래그 축 · 상태 전이와 다른 자리", 12, SOFT, KR, "start")
d.line(120, RAIL_Y, 880, RAIL_Y, RULE, 1.0)
d.t(890, RAIL_Y + 4, "시간", 11, SOFT, KR, "start")

# 두 번째와 세 번째 사이의 간격 — 이 도식의 focal 은 여기 한 곳이다
d.line(E2, RAIL_Y, E3, RAIL_Y, ACC, 2.4)
d.t((E2 + E3) // 2, RAIL_Y - 14, "두 사건 사이의 간격", 12, ACC, KR)

for x, y0, flag, when, c in ((E1, CY + BH // 2, "[UNREPLIED] 부착", "엔트리가 생길 때", MUTED),
                             (E2, CY, "[UNREPLIED] 탈락", "상태 전이와 같은 시점", MUTED),
                             (E3, CY + BH // 2, "[ASSURED] 부착", "상태 전이보다 뒤", ACC)):
    d.line(x, y0, x, RAIL_Y - 6, c, 1.0, "4 4")
    d.o.append(f'<circle cx="{x}" cy="{RAIL_Y}" r="4" fill="{c}"/>')
    d.t(x, RAIL_Y + 28, flag, 11, c, MONO, "middle", 600)
    d.t(x, RAIL_Y + 48, when, 11, c if c is ACC else SOFT, KR)

# ── 두 번째 소멸 경로 — [ASSURED] 가 아직 없는 동안은 먼저 버려진다 ──
d.path(f"M 364 {RAIL_Y} L 364 540 L {END_X} 540 L {END_X} {CY+16}", BAD, 1.4, m="bad")
d.o.append(f'<circle cx="364" cy="{RAIL_Y}" r="3" fill="{BAD}"/>')
d.t(620, 560, "테이블 포화 · [ASSURED] 없는 항목 먼저 축출", 12, BAD, KR)

d.legend(600, [("응답 대기", WARN), ("수립됨", OK), ("폐기 · 축출", BAD),
               ("딸림 연결", INFO), ("[ASSURED] 는 뒤에", ACC)])
d.save("02-01.conntrack-states.svg")
print("ok conntrack-states")
