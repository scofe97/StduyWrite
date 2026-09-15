# 타입 스펙: type-architecture — 이 기계 → 경로 위 라우터 → 주소 존(같은 주소) 안의 인스턴스 여럿. 존은 주소 둘이라 2개.
# 출처: 노트 §5 실측 (dig @<root> hostname.bind CH TXT) — 2026-09-06 과 2026-09-11, 국내 가정용 회선.
#       198.41.0.4 (a): 09-06 nnn1-jptyo-1a · 09-11 같은 날 30분 사이 nnn1-jptyo-1c 와 nnn1-jptyo-1b (모두 도쿄)
#       192.5.5.241 (f): 09-06 sel1f (서울) · 09-11 ICN.cf (인천)
#       원리 서술은 원문 §5.4.4 IP-anycast: 같은 주소를 여러 서버가 BGP 로 광고하고 라우터가 하나를 고른다.
# 2026-09-13: anycast-rtt 를 대신한다. 그 도식은 주소가 서로 다른 네 루트의 왕복 시간을 늘어놓아
#       "같은 주소를 여럿이 나눠 쓴다"는 절 제목과 반대로 읽혔다(사용자 지적). 네 주소 비교는 본문 표가 맡는다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER2, INK, MUTED, SOFT, ACC, INFO, KR, MONO

W, H = 1000, 604
d = D(W, H, "SECTION 5.4.4 · IP ANYCAST",
      "주소 하나 뒤에 기계가 여럿 있습니다",
      "같은 루트 DNS 주소로 여러 날 물었을 때 대답한 기계. 198.41.0.4 는 도쿄의 세 기계가, 192.5.5.241 은 서울과 인천의 기계가 답했다. 인스턴스마다 같은 주소를 BGP 로 광고하고 경로 위 라우터가 그중 하나로 가는 경로를 고르기 때문이다.",
      "같은 주소로 물어도 BGP 가 고른 경로에 따라 대답하는 기계가 바뀝니다. 이 기계에서 두 날에 걸쳐 잰 기록입니다.")


def node(x, y, w, name, sub, name_font=KR, stroke=MUTED):
    d.box(x, y, w, 56, PAPER2, stroke, 1.0, 7)
    d.t(x + w / 2, y + 24, name, 13 if name_font == KR else 12, INK, name_font, "middle", 600)
    d.t(x + w / 2, y + 44, sub, 12, MUTED, KR)


# 연결선을 먼저 — 상자가 선 끝을 덮는다
d.path("M 168 296 L 204 296", MUTED, 1.4, m="ar")
d.path("M 352 284 L 376 284 L 376 140 L 556 140", INFO, 1.4, m="info")
d.path("M 352 308 L 376 308 L 376 348 L 556 348", INFO, 1.4, m="info")

node(24, 268, 144, "이 기계", "국내 가정용 회선")
node(208, 268, 144, "경로 위 라우터", "BGP 경로 선택")

# ── 주소 존 A: 198.41.0.4 ──
d.box(400, 108, 576, 192, f"{INK}07", f"{MUTED}88", 1.2, 10)
d.box(560, 124, 256, 32, PAPER2, INFO, 1.2, 6)
d.t(576, 145, "a 루트", 12, MUTED, KR, "start")
d.t(800, 146, "198.41.0.4", 16, INFO, MONO, "end", 600)
d.path("M 688 156 L 688 180", INFO, 1.2)
d.path("M 508 180 L 868 180", INFO, 1.2)
for cx in (508, 688, 868):
    d.path(f"M {cx} 180 L {cx} 200", INFO, 1.2, m="info")
for x, name, sub in ((424, "nnn1-jptyo-1a", "도쿄 · 09-06"), (604, "nnn1-jptyo-1c", "도쿄 · 09-11"),
                     (784, "nnn1-jptyo-1b", "도쿄 · 09-11")):
    node(x, 204, 168, name, sub, MONO)
# focal — 같은 날, 같은 주소가 다른 기계로 갔다
d.path("M 604 264 L 604 272 L 952 272 L 952 264", ACC, 1.4)
d.t(778, 292, "같은 날 30분 사이에 갈아 가며 답함", 12, ACC, KR, "middle", 600)

# ── 주소 존 F: 192.5.5.241 ──
d.box(400, 316, 576, 168, f"{INK}07", f"{MUTED}88", 1.2, 10)
d.box(560, 332, 256, 32, PAPER2, INFO, 1.2, 6)
d.t(576, 353, "f 루트", 12, MUTED, KR, "start")
d.t(800, 354, "192.5.5.241", 16, INFO, MONO, "end", 600)
d.path("M 688 364 L 688 388", INFO, 1.2)
d.path("M 598 388 L 778 388", INFO, 1.2)
for cx in (598, 778):
    d.path(f"M {cx} 388 L {cx} 408", INFO, 1.2, m="info")
node(514, 412, 168, "sel1f", "서울 · 09-06", MONO)
node(694, 412, 168, "ICN.cf", "인천 · 09-11", MONO)

d.t(24, 516, "주소는 그대로인데 대답한 기계가 바뀜", 13, INK, KR, "start", 600)
d.t(24, 540, "인스턴스마다 같은 주소를 BGP 로 광고함 · 라우터는 그 광고들을 한 곳으로 가는 여러 경로로 보고 하나를 고름", 13, MUTED, KR, "start")

d.legend(556, [("같은 주소 · BGP 가 고른 경로", INFO), ("대답한 인스턴스", MUTED), ("같은 날에도 바뀐 자리", ACC)])
d.t(960, 596, "DIG HOSTNAME.BIND · 2026-09-06 / 2026-09-11 · KUROSE-ROSS 9E §5.4.4", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.anycast-same-address.svg"
d.save(out)
print("→", out)
