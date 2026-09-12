# 타입 스펙: type-bar — 루트 DNS 13개 주소 가운데 넷에 물어본 왕복 시간. BGP 가 고른 인스턴스가 어디냐로 갈린다.
# 출처: 이 기계에서 2026-09-11 측정. dig @<letter>.root-servers.net hostname.bind CH TXT 로 인스턴스 확인,
#       같은 응답의 ';; Query time' 줄로 왕복 시간 측정(+short 에는 안 나온다). 국내 가정용 회선이라
#       다른 위치·시각에서는 다르게 나온다. 닷새 전 같은 주소들의 인스턴스는 sel1f · kr-icn-aa ·
#       nnn1-jptyo-1a · lax1a 였다 — 주소는 그대로인데 받는 기계가 바뀐다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, BAD, OK, KR, MONO

# (루트 문자, 응답한 인스턴스 이름, 추정 위치, 왕복 시간 ms)
M = [("f", "192.5.5.241", "ICN.cf.f.root-servers.org", "인천", 5),
     ("l", "199.7.83.42", "kr-icn-aa", "인천", 4),
     ("a", "198.41.0.4", "nnn1-jptyo-1b", "도쿄", 32),
     ("c", "192.33.4.12", "lax1a.c.root-servers.org", "로스앤젤레스", 132)]

W, H = 1000, 620
d = D(W, H, "SECTION 5.4.4 · IP ANYCAST MEASURED",
      "주소는 하나, 대답하는 기계는 여럿입니다",
      "루트 DNS 서버 네 곳에 같은 질의를 보내고 응답한 물리 인스턴스와 왕복 시간을 잰 결과. 주소가 가리키는 곳을 BGP 의 경로 선택이 정한다.",
      "이 기계에서 2026-09-11 에 잰 값입니다 — 다른 위치와 시각에서는 다르게 나옵니다")

X0, BASE, GAP, BW = 150, 430, 56, 128
MAXV = 150
PX = 250 / MAXV

for i, (letter, addr, inst, loc, ms) in enumerate(M):
    x = X0 + i * (BW + GAP)
    h = ms * PX
    hot = ms > 100
    c = BAD if hot else (OK if ms < 10 else MUTED)
    d.box(x, BASE - h, BW, h, f"{c}{'2E' if hot else '18'}", c, 1.5 if hot else 1.0, 5)
    d.t(x + BW / 2, BASE - h - 12, f"{ms} ms", 12, c, MONO, "middle", 600)
    d.t(x + BW / 2, BASE + 22, addr, 12, INK, MONO)
    d.t(x + BW / 2, BASE + 42, loc, 12, c, KR)
    d.t(x + BW / 2, BASE + 60, inst, 10, SOFT, MONO)

d.line(X0 - 20, BASE, X0 + 4 * (BW + GAP) - GAP + 20, BASE, RULE, 1.0)
for v in (0, 50, 100, 150):
    d.line(X0 - 20, BASE - v * PX, X0 + 4 * (BW + GAP) - GAP + 20, BASE - v * PX, RULE, 0.6)
    d.t(X0 - 28, BASE - v * PX + 4, str(v), 10, SOFT, MONO, "end")
d.t(30, 128, "왕복 시간 (ms)", 11, MUTED, KR, "start")

# 설명 블록은 격자선 위에 얹히므로 종이색 판을 깔고 그 위에 쓴다.
# 판의 왼쪽 끝은 y축 라벨(x=122)보다 오른쪽에 둔다 — 34 에서 시작하면 100 라벨을 덮어 축이 지워진다.
d.o.append(f'<rect x="140" y="236" width="550" height="86" rx="6" fill="{PAPER}"/>')
d.t(154, 260, "주소 넷을 이 기계에서 재 봤습니다. 주소마다 세계 곳곳에", 12, MUTED, KR, "start")
d.t(154, 284, "같은 주소를 쓰는 기계가 여럿 있고, 그중 누가 대답할지는", 12, MUTED, KR, "start")
d.t(154, 308, "BGP 경로 선택이 정합니다.", 12, ACC, KR, "start")

d.t(30, 522, "f 와 l 은 국내 인스턴스가 받아 5 ms 안쪽이고, c 는 국내에 인스턴스가 없어 로스앤젤레스까지 갑니다.", 12, MUTED, KR, "start")
d.t(30, 542, "애니캐스트의 증거는 이 네 칸의 차이가 아니라, 같은 주소가 며칠 사이 다른 기계로 바뀐다는 쪽입니다.", 12, MUTED, KR, "start")

d.legend(564, [("10 ms 미만", OK), ("100 ms 초과", BAD), ("그 사이", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.anycast-rtt.svg"
d.save(out)
print("측정값:", [(l, ms) for l, _, _, _, ms in M], "→", out)
