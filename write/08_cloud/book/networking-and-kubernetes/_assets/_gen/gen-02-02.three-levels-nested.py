# 02-02.three-levels-nested — 테이블·체인·규칙 3계층이 담고 담기는 관계를 세 겹으로 보인다
# 본문 요구: "구조는 계층적입니다 — 테이블이 체인을 담고, 체인이 규칙을 담습니다."
#            + "어느 체인에 규칙을 넣느냐가 곧 그 규칙이 언제 평가되는지를 정합니다."
#            + §2 "규칙은 매치 조건과 액션(타깃)의 조합입니다."
#            + §2 "ACCEPT 와 RETURN 은 지금 있는 체인의 평가만 멈춥니다."
# 타입 스펙: type-nested.md — "hierarchy through containment. Outer = broader, inner = more specific."
#           바깥 링이 체인(자리), 가운데가 테이블(하는 일), 안쪽이 규칙(조건과 동작)이다.
#           링 라벨은 스펙대로 paper 마스크를 테두리 위에 얹는다(ddx.ring_label).
#           stroke 는 faint → muted → coral 로 올리고 coral 은 최내곽 하나뿐이다(focal 1곳).
#           chain-then-table(swimlane) 이 "패킷이 어느 순서로 지나는가"를 맡고
#           이 도식은 "그 자리를 열면 무엇이 나오는가"를 맡는다 — 형제 도식이다.
# 좌표: Layout conventions 타입이라 공식이 없다. 링 인셋을 28(가로)·36(세로) 하나로 고정하고
#       띠 안 항목은 stride 168, 규칙 행은 stride 56 로 못 박는다. 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, PAPER2, OK, BAD, INFO, KR, MONO

W, H = 960, 744

# 링 셋 — 인셋 28 / 36 을 세 겹 모두 같은 값으로 쓴다(불규칙 인셋은 type-nested 안티패턴)
R1 = (24, 136, 912, 496)
R2 = (52, 172, 856, 424)
R3 = (80, 208, 800, 352)

# 띠 항목은 링 라벨 오른쪽에서 시작한다 — 라벨은 테두리 위에 얹히므로 겹치면 둘 다 못 읽는다
# (2026-09-03 dd-lint: '2 테이블'↔'PREROUTING', '3 규칙'↔'Raw' 두 건이 실제로 겹쳤다)
STRIDE = 144
CX = [264 + i * STRIDE for i in range(5)]          # 264 408 552 696 840
MIDX = [(a + b) // 2 for a, b in zip(CX, CX[1:])]  # 336 480 624 768

ROW_X, ROW_W, ROW_H, ROW_STRIDE, ROW_Y0 = 104, 752, 48, 56, 256
COL = [(104, 328), (448, 176), (640, 216)]         # 매치 · 타깃 · 결과

d = D(W, H, "IPTABLES · THREE NESTED LEVELS",
      "체인을 열면 테이블이, 테이블을 열면 규칙이 나온다",
      "바깥 링이 체인(패킷이 어느 자리에서 평가되는가), 가운데 링이 그 체인이 가진 테이블(무엇을 하는가), "
      "안쪽 링이 그 테이블의 규칙(어떤 조건에 무슨 동작)이다. INPUT 체인의 filter 테이블 하나를 끝까지 연 것이다.",
      lead="바깥이 넓고 안쪽이 구체적이다 — 진한 글자가 다음 겹에서 열어 볼 항목")

# ── 링 (바깥부터) ─────────────────────────────────────────────
d.box(*R1, "none", RULE, 1.0, 8)
d.box(*R2, PAPER2, MUTED, 1.1, 8)
d.o.append(f'<rect x="{R3[0]}" y="{R3[1]}" width="{R3[2]}" height="{R3[3]}" rx="8" '
           f'fill="{ACC}08" stroke="{ACC}" stroke-width="1.4"/>')
ddx.ring_label(d, R1[0], R1[1], "1 체인 · 언제", 13, MUTED)
ddx.ring_label(d, R2[0], R2[1], "2 테이블 · 무엇을", 13, MUTED)
ddx.ring_label(d, R3[0], R3[1], "3 규칙 · 조건과 동작", 13, ACC)

# ── 띠 1: 체인 5개 ────────────────────────────────────────────
for cx, (nm, open_) in zip(CX, [("PREROUTING", 0), ("INPUT", 1), ("FORWARD", 0),
                                ("OUTPUT", 0), ("POSTROUTING", 0)]):
    d.t(cx, 164, ddx.fit(nm, 13, STRIDE - 16, nm), 13,
        INK if open_ else SOFT, MONO, "middle", 600 if open_ else 400)

# ── 띠 2: 그 체인이 가진 테이블 — 평가 순서대로 ──────────────
tables = [("Raw", "없음"), ("Mangle", ""), ("NAT", ""), ("Filter", "열림"), ("Security", "SELinux")]
for cx, (nm, note) in zip(CX, tables):
    has = note not in ("없음", "SELinux")
    d.t(cx, 200, ddx.fit(nm, 13, STRIDE - 16, nm), 13,
        INK if note == "열림" else (MUTED if has else SOFT), MONO, "middle",
        600 if note == "열림" else 400)
# 평가 순서 화살표는 INPUT 이 실제로 가진 셋(Mangle→NAT→Filter) 사이에만 긋는다.
# Raw·Security 까지 이으면 INPUT 에서 평가되지 않는 테이블이 순서에 낀 것처럼 읽힌다.
for mx in MIDX[1:3]:
    d.path(f"M {mx - 28} 196 L {mx + 20} 196", SOFT, 1.2, m="soft")

# ── 링 3 안: filter 테이블의 규칙 목록 ───────────────────────
for (cx0, cw), lab in zip(COL, ["매치 — 조건이 맞는가", "타깃 — 무엇을 하는가", "그래서 어떻게 되는가"]):
    d.t(cx0 + 16, 240, ddx.fit(lab, 13, cw - 24, lab), 13, SOFT, KR, "start", 600)

rules = [
    ("-m state --state ESTABLISHED", "-j ACCEPT",      "이 체인은 여기서 끝",  OK),
    ("-p tcp --dport 22",            "-j incoming-ssh", "서브체인 갔다 돌아옴", INFO),
    ("-s 10.0.0.0/8",                "-j LOG",          "기록만 · 계속 평가",   INFO),
    ("-p tcp --dport 80",            "-j REJECT",       "차단 · 사유 회신",     BAD),
    ("(아무 규칙에도 안 걸림)",       "policy DROP",     "기본 정책으로 차단",   BAD),
]
for i, (match, target, effect, c) in enumerate(rules):
    y = ROW_Y0 + i * ROW_STRIDE
    d.box(ROW_X, y, ROW_W, ROW_H, PAPER2, c, 1.1, 6)
    base = y + ROW_H // 2 + 5
    kr = any("가" <= ch <= "힣" for ch in match)
    d.t(COL[0][0] + 16, base, ddx.fit(match, 13, COL[0][1] - 24, match), 13,
        INK, KR if kr else MONO, "start")
    d.t(COL[1][0] + 16, base, ddx.fit(target, 13, COL[1][1] - 24, target), 13,
        c, MONO, "start", 600)
    d.t(COL[2][0] + 16, base, ddx.fit(effect, 13, COL[2][1] - 24, effect), 13,
        MUTED, KR, "start")

# 위에서 아래로 순서대로 — 규칙 목록의 진행 방향
d.path(f"M 92 {ROW_Y0 - 4} L 92 {ROW_Y0 + 4 * ROW_STRIDE + ROW_H + 4}", MUTED, 1.4, m="ar")

# ── 바깥 두 링의 아래 띠 — 그 겹에 대해 한 줄씩 ──────────────
d.t(R2[0] + 24, 584, "흐린 둘은 INPUT 에 없다 — Raw 는 PREROUTING·OUTPUT 뿐이고 Security 는 SELinux 전용이다.",
    13, MUTED, KR, "start")
d.t(R1[0] + 24, 620, "같은 세 겹이 나머지 네 체인에도 그대로 있다. 달라지는 것은 그 체인이 어느 테이블을 갖느냐뿐이다.",
    13, MUTED, KR, "start")

d.t(24, 664, "규칙은 위에서 아래로 평가되고 처음 걸리는 하나에서 멈춘다. 어느 규칙에도 안 걸리면 그 체인의 기본 정책을 따른다.",
    13, MUTED, KR, "start")
d.legend(688, [("이 체인 종결", OK), ("종결 아님 · 계속", INFO), ("차단", BAD),
               ("여는 항목", INK), ("지금 연 겹", ACC)])
d.save("02-02.three-levels-nested.svg")
print("ok three-levels-nested")
