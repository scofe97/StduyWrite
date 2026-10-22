# 타입 스펙: type-flowchart — 시스템 콜이 어느 세대 seccomp 에 걸리는가에서 갈라진다. 1세대는 허용 4개 → 쓸모 있는 일도 못 하는 막다른 길, seccomp-bpf 는 프로세스별 프로파일이 opcode 와 인자로 판정 → 허용·오류 반환·종료 또는 트레이서 호출. 아래 띠가 Docker 기본 프로파일이 막는 syscall. focal 은 BPF 필터.
# 사실 출처: 노트 L54~L60(1세대 · 허용 4개 · 열려 있던 fd), L64~L66(seccomp-bpf · 프로세스별 프로파일 · opcode 와 인자 · 동작 셋), L72~L80(Docker 기본 프로파일 300개 중 40개 이상 · 막는 syscall 표)
# Layout conventions: 시작 타원 y=96 h=36, 마름모 y=164 h=96 폭 200, 가지 열 중심 x=200·668, 상자 h=72 · stride 104(y=300·404), 결과 상자 y=420 h=64, 띠 y=520. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, KR, MONO

W, H = 984, 724
MID = 492


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def card(d, x, y, w, h, title, subs, col=None, op="14", sw=1.2, tsize=13):
    fit(title, tsize, w - 16)
    if col:
        d.tone(x, y, w, h, col, 6, op, sw)
    else:
        d.box(x, y, w, h)
    n = len(subs)
    tb = round(y + h / 2 - 9 * n + 5)
    d.t(x + w / 2, tb, title, tsize, col or INK, kr(title), "middle", 600)
    for i, s in enumerate(subs):
        fit(s, 12, w - 16)
        d.t(x + w / 2, tb + 20 + 18 * i, s, 12, MUTED, kr(s), "middle")


d = D(W, H, "FLOWCHART · 08-01 §2",
      "1세대는 허용 목록이 고정이고, seccomp-bpf 는 프로세스마다 프로파일로 판정합니다",
      "시스템 콜이 어느 세대 seccomp 에 걸리는지에서 갈라지는 흐름. 1세대(2005)는 sigreturn, exit, read, write 네 개만 허용해 쓸모 있는 일을 거의 못 한다. "
      "seccomp-bpf(2012)는 프로세스마다 BPF 프로파일이 시스템 콜 opcode 와 인자를 보고 허용, 오류 반환, 프로세스 종료, 트레이서 호출 중 하나로 판정한다. "
      "아래 띠는 Docker 기본 프로파일이 막는 호스트 시계, 커널 모듈, 커널 키링 시스템 콜이다.",
      lead="세대가 바뀌며 달라진 것은 판정 단위가 고정 목록에서 프로세스별 프로파일로 옮겨 갔다는 점입니다.")

# 시작 타원
d.o.append(f'<rect x="{MID - 110}" y="96" width="220" height="36" rx="18" fill="#161B22" stroke="#BFC0C038" stroke-width="0.9"/>')
d.t(MID, 119, "프로세스의 시스템 콜", 13, INK, KR, "middle", 600)

# 갈림 마름모
cy = 212
d.arrow([(MID, 134), (MID, 160)], SOFT, "soft", 1.3)
d.o.append(f'<polygon points="{MID},164 {MID + 100},{cy} {MID},260 {MID - 100},{cy}" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
d.t(MID, cy - 2, "seccomp", 12, INK, MONO, "middle", 600)
d.t(MID, cy + 16, "어느 세대인가", 12, INK, KR, "middle", 600)

# 왼쪽 가지: 1세대
LCX, LW = 200, 304
LX = LCX - LW // 2
d.arrow([(MID - 102, cy), (LCX, cy), (LCX, 296)], SOFT, "soft", 1.3)
d.t((MID - 102 + LCX) / 2, cy - 10, "1세대 · 2005", 12, MUTED, KR, "middle", 600)
d.arrow([(LCX, 374), (LCX, 400)], SOFT, "soft", 1.3)
card(d, LX, 300, LW, 72, "허용 syscall 4개", ["sigreturn · exit", "read · write — 열려 있던 fd 만"])
card(d, LX, 404, LW, 72, "쓸모 있는 일도 거의 불가", ["지나치게 좁은 샌드박스"], BAD)

# 오른쪽 가지: seccomp-bpf
RCX, RW = 668, 536
RX = RCX - RW // 2
d.arrow([(MID + 102, cy), (RCX, cy), (RCX, 296)], SOFT, "soft", 1.3)
d.t((MID + 102 + RCX) / 2, cy - 10, "seccomp-bpf · 2012", 12, MUTED, KR, "middle", 600)
card(d, RX, 300, RW, 72, "BPF 필터 — 프로세스마다 프로파일", ["판정 입력: syscall opcode + 호출 인자"], ACC, "1F", 1.6)

# 결과 셋
OW, OGAP, OY, OH = 168, 16, 420, 64
OXS = [RX + i * (OW + OGAP) for i in range(3)]
OCS = [x + OW / 2 for x in OXS]
d.line(RCX, 374, RCX, 396, SOFT, 1.3)
d.line(OCS[0], 396, OCS[2], 396, SOFT, 1.3)
for cx in OCS:
    d.arrow([(cx, 396), (cx, OY - 4)], SOFT, "soft", 1.3)
card(d, OXS[0], OY, OW, OH, "허용", ["컨테이너의 주된 동작"], OK)
card(d, OXS[1], OY, OW, OH, "오류 반환", ["컨테이너의 주된 동작"], BAD)
card(d, OXS[2], OY, OW, OH, "종료 · 트레이서 호출", ["컨테이너에선 드묾"])

# 띠: Docker 기본 프로파일
SX, SW_, SY = 48, 888, 520
d.arrow([(OCS[1], OY + OH + 2), (OCS[1], SY - 4)], BAD, "bad", 1.4)
d.o.append(f'<rect x="{SX}" y="{SY}" width="{SW_}" height="152" rx="8" fill="none" stroke="#BFC0C038" stroke-width="0.9" stroke-dasharray="6 5"/>')
d.t(SX + 16, SY + 26, "Docker 기본 프로파일", 13, INK, KR, "start", 600)
d.t(SX + SW_ - 16, SY + 26, "syscall 300개+ 중 40개+ 차단", 12, MUTED, KR, "end")
CELLS = [
    ("호스트 시계 변경", ["clock_adjtime", "clock_settime"]),
    ("커널 모듈 조작", ["create_module · delete_module", "init_module"]),
    ("커널 키링 접근", ["request_key · keyctl", "namespace 로 격리 안 됨"]),
]
for i, (t, names) in enumerate(CELLS):
    w = (SW_ - 32 - 2 * 16) // 3
    x = SX + 16 + i * (w + 16)
    fit(t, 13, w - 16)
    d.tone(x, SY + 44, w, 92, BAD, 6, "12", 1.0)
    d.t(x + w / 2, SY + 70, t, 13, BAD, KR, "middle", 600)
    for k, nm in enumerate(names):
        fit(nm, 12, w - 16)
        d.t(x + w / 2, SY + 94 + 20 * k, nm, 12, MUTED, kr(nm), "middle")

d.legend(H - 44, [("갈림 · 판정 필터", ACC), ("허용", OK), ("차단", BAD)])
d.save(str(ASSETS / "08-01.seccomp-bpf.svg"))
print("ok 08-01 seccomp-bpf")
