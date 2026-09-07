# 타입 스펙: type-sequence — 참여자 레인 + 시간축 왕복. 질의는 브로드캐스트, 응답은 유니캐스트로 갈린다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.4.1 Figure 6.17 · Figure 6.18 —
#   주소와 TTL 20 분은 원문 수치 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO


def kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """Seq 프리미티브가 라벨 font 를 MONO 로 고정하므로 한글만 KR 로 돌려 씁니다."""

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dx = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dx} {y} L {x2 - 12 * dx} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, KR)

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 11, c, kr(label), "start")
        if sub:
            s.t(x + 68, y + 13, sub, 11, MUTED, KR, "start")


W, H = 940, 552
d = SeqKR(W, H, "SECTION 6.4.1 · ADDRESS RESOLUTION PROTOCOL",
          "물을 때는 모두에게, 답할 때는 한 명에게",
          "같은 서브넷 안에서 IP 주소에 대응하는 MAC 주소를 알아내는 절차. 질의는 브로드캐스트 프레임에, 응답은 보통 프레임에 실린다.",
          "주소와 표는 원문 Figure 6.17 · Figure 6.18 의 값입니다")

LX = d.lanes([("222.222.222.220", "묻는 호스트"),
              ("서브넷의 모든 어댑터", "브로드캐스트"),
              ("222.222.222.222", "답하는 호스트")], y0=110, lane_w=250)
d.rails(330)

d.msg("222.222.222.220", "서브넷의 모든 어댑터", "ARP query", 176, INFO, "info",
      sub="목적지 MAC 을 FF-FF-FF-FF-FF-FF 로 두고 보냅니다")
d.msg("서브넷의 모든 어댑터", "222.222.222.222", "flood", 228, MUTED, "ar", dash="4 5",
      sub="모든 어댑터가 받아 자기 ARP 모듈로 올립니다")
d.msg("222.222.222.222", "222.222.222.220", "ARP response", 290, ACC, "acc",
      sub="IP 가 일치한 하나만 보통 프레임으로 답합니다")

for i, line in enumerate([
    "표에 없으면 위 세 걸음을 밟습니다.",
    "표는 관리자가 채우지 않고 저절로 채워집니다.",
    "항목은 보통 20 분 뒤 지워집니다.",
    "서브넷 밖의 주소는 ARP 로 풀 수 없습니다.",
]):
    d.t(24, 380 + i * 26, "·  " + line, 11, MUTED, KR, "start")

TX, TW = 470, 446
d.box(TX, 356, TW, 140, PAPER2, RULE, 1.0)
d.t(TX + 16, 380, "222.222.222.220 의 ARP 표", 11, INK, KR, "start", 600)
d.line(TX + 16, 390, TX + TW - 16, 390, RULE, 0.8)
d.t(TX + 16, 412, "IP 주소", 10, SOFT, KR, "start")
d.t(TX + 190, 412, "MAC 주소", 10, SOFT, KR, "start")
d.t(TX + TW - 16, 412, "TTL", 10, SOFT, KR, "end")
ROWS = [("222.222.222.221", "88-B2-2F-54-1A-0F", "13:45:00", MUTED),
        ("222.222.222.223", "5C-66-AB-90-75-B1", "13:52:00", MUTED),
        ("222.222.222.222", "49-BD-D2-C7-56-2A", "응답 뒤 추가", ACC)]
for i, (ip, mac, ttl, c) in enumerate(ROWS):
    y = 436 + i * 22
    d.t(TX + 16, y, ip, 11, c, MONO, "start", 600 if c is ACC else 400)
    d.t(TX + 190, y, mac, 11, c, MONO, "start", 600 if c is ACC else 400)
    d.t(TX + TW - 16, y, ttl, 11, c, KR if c is ACC else MONO, "end")

d.legend(512, [("이번에 알아낸 매핑", ACC), ("브로드캐스트 질의", INFO)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-03.arp-exchange.svg"
d.save(out)
print("→", out)
