# 02-02.chain-comes-alive — 사용자 체인은 세 줄이 다 있어야 산다
# 본문 요구: 학습자 질문 "-A 에 PREROUTING 같은 방향만 들어오는 줄 알았다 / 커스텀이 가능한가".
#           내장 체인은 커널이 부르지만 사용자 체인은 선언·규칙·호출 셋이 다 있어야 실행된다.
#           셋 중 호출이 빠지는 것이 가장 흔한 실패라 그 단계가 초점이다.
# 타입 스펙: type-process.md — 단계마다 [무엇을 만드나 · iptables 줄 · 빠지면] 이라는
#           같은 의미 슬롯이 반복된다. semantic-patterns 의 "Stage framework with semantic slots".
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 616
d = D(W, H, "iptables · BUILT-IN vs USER CHAIN",
      "체인은 어떻게 존재하게 되는가",
      "내장 체인은 커널이 부르지만 사용자 체인은 선언·규칙·호출 세 줄이 다 있어야 실행된다.",
      lead="셋 중 하나만 빠져도 목록에는 보이는데 아무 패킷도 안 지난다")

# 상단 대조 띠 — 콜론 줄의 정책 자리가 둘을 가른다
BY, BH, HALFW = 98, 74, 464
for i, (lab, dump, note, col) in enumerate([
        ("내장 체인 다섯", ":PREROUTING ACCEPT [93:5148]", "정책이 있다 · 커널이 직접 부른다", INFO),
        ("사용자 체인", ":KUBE-SERVICES - [0:0]", "정책 자리가 - · 끝나면 부른 자리로 돌아간다", MUTED)]):
    x = 24 + i * (HALFW + 24)
    d.box(x, BY, HALFW, BH, PAPER2, RULE, 1.0)
    d.t(x + 16, BY + 24, ddx.fit(lab, 12, 200, f"band {lab}"), 12, col, KR, "start", 600)
    d.t(x + 16, BY + 46, ddx.fit(dump, 11, HALFW - 32, f"dump {dump}"), 11, INK, MONO, "start")
    d.t(x + 16, BY + 64, ddx.fit(note, 11, HALFW - 32, f"note {note}"), 11, MUTED, KR, "start")

d.t(24, BY + BH + 26, "오른쪽은 저절로 생기지 않는다. 아래 세 줄이 모두 있어야 한다.",
    12, SOFT, KR, "start")

STAGES = [
    ("선언", "이름만 있는 빈 체인", "-N KUBE-SERVICES", "규칙을 넣을 곳이 없다", False),
    ("규칙", "그 체인 안에 넣는 줄", "-A KUBE-SERVICES -d ... -j SVC", "들어와도 할 일이 없다", False),
    ("호출", "내장 체인에서 점프", "-A PREROUTING -j KUBE-SERVICES", "죽은 코드 — 패킷이 안 온다", True),
]
SLOTS = ["MAKES", "IPTABLES", "IF MISSING"]
SX0, SW, SGAP, SY, SH = 24, 300, 26, 214, 282

for i, (title, makes, line, miss, focal) in enumerate(STAGES):
    x = SX0 + i * (SW + SGAP)
    col = ACC if focal else INK
    if focal:
        d.tone(x, SY, SW, SH, ACC, 8, "0E", 1.4)
    else:
        d.box(x, SY, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, SY + 24, f"STEP {i+1}", 8, SOFT, MONO, "start")
    d.t(x + 18, SY + 48, ddx.fit(title, 15, SW - 36, f"title {title}"), 15, col, KR, "start", 600)
    vals = [(makes, KR, 12, INK), (line, MONO, 11, INK), (miss, KR, 12, ACC if focal else MUTED)]
    for j, (slot, (val, fam, size, vc)) in enumerate(zip(SLOTS, vals)):
        sy = SY + 76 + j * 70
        d.line(x + 18, sy, x + SW - 18, sy, RULE, 0.8)
        d.t(x + 18, sy + 18, slot, 8, SOFT, MONO, "start")
        d.t(x + 18, sy + 42, ddx.fit(val, size, SW - 36, f"{title}/{slot}"), size, vc, fam, "start")
    if i < len(STAGES) - 1:
        d.path(f"M {x+SW+4} {SY+SH/2} L {x+SW+SGAP-6} {SY+SH/2}", SOFT, 1.5, m="soft")

d.t(24, 530, "세 줄은 순서대로 필요하지만 셋 다 있어야 비로소 한 줄이 평가된다. 가장 자주 빠지는 것이 호출이다.",
    12, MUTED, KR, "start")
d.t(24, 550, "커널이 아는 것은 훅 다섯뿐이고, 사용자 체인은 그 다섯에서 누가 불러 줄 때만 실행된다.",
    12, MUTED, KR, "start")
d.legend(568, [("내장 체인 — 커널이 부른다", INFO), ("여기가 빠지면 죽은 코드", ACC)])
d.save("02-02.chain-comes-alive.svg")
print("ok chain-comes-alive")
