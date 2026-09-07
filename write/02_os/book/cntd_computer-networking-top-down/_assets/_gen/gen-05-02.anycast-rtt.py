# 타입 스펙: type-bar — 루트 DNS 13개 주소 가운데 넷에 물어본 왕복 시간. BGP 가 고른 인스턴스가 어디냐로 갈린다.
# 출처: 이 기계에서 2026-09-06 측정. dig @<letter>.root-servers.net hostname.bind CH TXT 로 인스턴스 확인,
#       dig +stats 의 Query time 으로 왕복 시간 측정. 서울에서 잰 값이라 다른 위치에서는 다르게 나온다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, BAD, OK, KR, MONO

# (루트 문자, 응답한 인스턴스 이름, 추정 위치, 왕복 시간 ms)
M = [("f", "sel1f.f.root-servers.org", "서울", 5),
     ("l", "kr-icn-aa", "인천", 6),
     ("a", "nnn1-jptyo-1a", "도쿄", 38),
     ("c", "lax1a.c.root-servers.org", "로스앤젤레스", 140)]

W, H = 1000, 620
d = D(W, H, "SECTION 5.4.4 · IP ANYCAST MEASURED",
      "주소는 하나, 대답하는 기계는 여럿입니다",
      "루트 DNS 서버 네 곳에 같은 질의를 보내고 응답한 물리 인스턴스와 왕복 시간을 잰 결과. 주소가 가리키는 곳을 BGP 의 경로 선택이 정한다.",
      "이 기계에서 2026-09-06 에 잰 값입니다 — 다른 위치에서는 다르게 나옵니다")

X0, BASE, GAP, BW = 150, 430, 56, 128
MAXV = 150
PX = 250 / MAXV

for i, (letter, inst, loc, ms) in enumerate(M):
    x = X0 + i * (BW + GAP)
    h = ms * PX
    hot = ms > 100
    c = BAD if hot else (OK if ms < 10 else MUTED)
    d.box(x, BASE - h, BW, h, f"{c}{'2E' if hot else '18'}", c, 1.5 if hot else 1.0, 5)
    d.t(x + BW / 2, BASE - h - 12, f"{ms} ms", 12, c, MONO, "middle", 600)
    d.t(x + BW / 2, BASE + 22, f"{letter}-root", 12, INK, MONO)
    d.t(x + BW / 2, BASE + 42, loc, 11, c, KR)
    d.t(x + BW / 2, BASE + 60, inst, 9, SOFT, MONO)

d.line(X0 - 20, BASE, X0 + 4 * (BW + GAP) - GAP + 20, BASE, RULE, 1.0)
for v in (0, 50, 100, 150):
    d.line(X0 - 20, BASE - v * PX, X0 + 4 * (BW + GAP) - GAP + 20, BASE - v * PX, RULE, 0.6)
    d.t(X0 - 28, BASE - v * PX + 4, str(v), 10, SOFT, MONO, "end")
d.t(30, 128, "왕복 시간 (ms)", 11, MUTED, KR, "start")

# 설명 블록은 격자선 위에 얹히므로 종이색 판을 깔고 그 위에 쓴다.
# 판의 왼쪽 끝은 y축 라벨(x=122)보다 오른쪽에 둔다 — 34 에서 시작하면 100 라벨을 덮어 축이 지워진다.
d.o.append(f'<rect x="140" y="236" width="550" height="86" rx="6" fill="{PAPER}"/>')
d.t(154, 260, "루트 서버 주소 열셋 가운데 넷을 이 기계에서 재 봤습니다.", 11, MUTED, KR, "start")
d.t(154, 284, "주소마다 세계 곳곳에 같은 주소를 쓰는 기계가 여럿 있고,", 11, MUTED, KR, "start")
d.t(154, 308, "어느 기계가 대답할지는 BGP 경로 선택이 정합니다.", 11, ACC, KR, "start")

d.t(30, 522, "f 와 l 은 국내 인스턴스가 받아 5~6 ms 이고, c 는 국내에 인스턴스가 없어 로스앤젤레스까지 갑니다.", 11, MUTED, KR, "start")
d.t(30, 542, "같은 서비스인데 28배 차이가 납니다. 애니캐스트가 지리가 아니라 경로 선택을 따른다는 증거입니다.", 11, MUTED, KR, "start")

d.legend(564, [("10 ms 미만", OK), ("100 ms 초과", BAD), ("그 사이", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.anycast-rtt.svg"
d.save(out)
print("측정값:", [(l, ms) for l, _, _, ms in M], "→", out)
