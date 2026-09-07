# 타입 스펙: type-pyramid — 위아래로 마주 본 두 삼각형. 좁아지는 지점이 곧 결론.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §4.5 Figure 4.31 (narrow-waisted hourglass) + RFC 1958
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, KR, MONO

W, H = 960, 600
d = D(W, H, "THE IP HOURGLASS · RFC 1958",
      "허리가 하나라서 자랐습니다",
      "인터넷 프로토콜 스택의 모래시계 그림. 위아래로는 프로토콜이 많고 네트워크 계층에는 IP 하나뿐이며, 그 좁은 허리가 서로 다른 망을 하나로 묶었다.",
      "목표는 연결성, 도구는 인터넷 프로토콜, 지능은 종단에 — RFC 1958")

LX, RX = 150, 810          # 넓은 쪽
WL, WR = 400, 560          # 허리
TOP, WT, WB, BOT = 118, 292, 340, 508

# 위쪽 깔때기
d.o.append(f'<path d="M {LX} {TOP} L {RX} {TOP} L {WR} {WT} L {WL} {WT} Z" '
           f'fill="{INK}0C" stroke="{RULE}" stroke-width="1.1"/>')
# 아래쪽 깔때기
d.o.append(f'<path d="M {WL} {WB} L {WR} {WB} L {RX} {BOT} L {LX} {BOT} Z" '
           f'fill="{INK}0C" stroke="{RULE}" stroke-width="1.1"/>')
# 허리
d.o.append(f'<rect x="{WL}" y="{WT}" width="{WR - WL}" height="{WB - WT}" rx="4" '
           f'fill="{ACC}1E" stroke="{ACC}" stroke-width="1.6"/>')
d.t(480, 322, "IP", 18, ACC, MONO, "middle", 600)

d.t(480, 152, "애플리케이션 계층", 12, INK, KR, "middle", 600)
d.t(480, 172, "HTTP · SMTP · IMAP · DNS · DASH · BitTorrent · ...", 10, MUTED, MONO)
d.t(480, 216, "트랜스포트 계층", 12, INK, KR, "middle", 600)
d.t(480, 236, "TCP · UDP · QUIC", 10, MUTED, MONO)
d.t(480, 274, "네트워크 계층은 하나뿐입니다", 11, MUTED, KR)

d.t(480, 384, "링크 계층", 12, INK, KR, "middle", 600)
d.t(480, 404, "Ethernet · WiFi · Cellular · PPP · ...", 10, MUTED, MONO)
d.t(480, 446, "물리 계층", 12, INK, KR, "middle", 600)
d.t(480, 466, "동축 · 꼬임쌍선 · 광 · 무선", 11, MUTED, KR)

# 좌우 주석
d.t(LX - 20, 168, "프로토콜이 많습니다", 11, SOFT, KR, "end")
d.t(LX - 20, 424, "프로토콜이 많습니다", 11, SOFT, KR, "end")
d.path(f"M {RX + 24} 316 L {WR + 12} 316", ACC, 1.3, m="acc")
d.t(RX + 32, 306, "미들박스가 이 허리를", 11, ACC, KR, "start")
d.t(RX + 32, 322, "조금씩 굵게 합니다", 11, ACC, KR, "start")

d.t(60, 534, "IP 만 맞추면 되니 이더넷부터 와이파이·셀룰러·광 전송까지 성질이 다른 망이 모두 인터넷의 일부가 됐습니다. "
              "Clark 은 이 허리를 걸침 계층이라 부릅니다.", 11, MUTED, KR, "start")

d.legend(552, [("모두가 구현해야 하는 하나", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "04-04.hourglass.svg"
d.save(out)
print("→", out)
