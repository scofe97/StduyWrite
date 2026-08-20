# 01-03.arp-resolution — 시퀀스 3참여자
# 본문: "브로드캐스트로 묻고 유니캐스트로 답한다", "다른 호스트는 받고 버린다"
# 타입 스펙: type-sequence.md (Layout conventions — 계산식 없음, 관례 + 범위)
#   actors 가로 한 줄 / lifeline 점선 / 시간 위→아래 / return 은 dashed + filled marker
import dd
from dd import D, Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 636
d = Seq(W, H,
        "ARP · IP TO MAC RESOLUTION",
        "ARP — 전원에게 묻고 한 대에게만 답한다",
        "묻는 길은 브로드캐스트, 답하는 길은 유니캐스트. 한 번의 교환으로 양쪽 표가 채워진다.",
        lead="묻는 길은 브로드캐스트, 답하는 길은 유니캐스트 · 한 번의 교환으로 양쪽 표가 채워진다")

# ── 좌표 (4의 배수 stride) ────────────────────────────────
LANE_Y  = 104
SEG1    = (164, 392)          # 캐시 미스 구간
SEG2    = (408, 512)          # 프레임 전송 구간
Y_REQ   = 232                 # ARP 요청 (브로드캐스트)
Y_DROP  = 292                 # 다른 호스트가 버리는 자리 (focal)
Y_RESP  = 348                 # ARP 응답 (유니캐스트)
Y_FRAME = 476                 # Ethernet 프레임
Y_TABLE = 548                 # 양쪽 표 기록
Y_RAILS = 576
BAND_X, BAND_W = 24, 952

def band(y0, y1, label):
    d.box(BAND_X, y0, BAND_W, y1 - y0, PAPER2, RULE, 0.9, 8)
    d.t(BAND_X + 12, y0 + 20, label, 12, SOFT, KR, "start")

def focal(cx, cy, txt, w):
    d.o.append(f'<rect x="{cx-w/2}" y="{cy-14}" width="{w}" height="28" rx="6" '
               f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    d.t(cx, cy + 5, txt, 12, ACC, KR)

def note(cx, cy, txt, c, w):
    d.o.append(f'<rect x="{cx-w/2}" y="{cy-13}" width="{w}" height="26" rx="5" '
               f'fill="{c}14" stroke="{c}" stroke-width="1.0"/>')
    d.t(cx, cy + 4, txt, 12, c, KR)

# ── 레인 → 구간 띠 → 레일 (그리는 순서가 곧 겹침 순서) ──────
LX = d.lanes([("요청 컴퓨터", "10.0.0.5"),
              ("다른 호스트", "10.0.0.7"),
              ("대상 서버",   "10.0.0.1")], y0=LANE_Y, lane_w=212)
B, O, S = LX["요청 컴퓨터"], LX["다른 호스트"], LX["대상 서버"]

band(*SEG1, "ARP 캐시에 없을 때만 — 있으면 이 구간을 통째로 건너뛴다")
band(*SEG2, "MAC 을 알았으니 이제 프레임을 보낸다")
d.rails(Y_RAILS)

# ── ① ARP 요청: 한 줄이 세 레인을 관통한다 ─────────────────
d.path(f"M {B+10} {Y_REQ} L {S-12} {Y_REQ}", INFO, 1.6, m="info")
d.t(B + 18, Y_REQ - 12, "ARP 요청 — 목적지 MAC = FF:FF:FF:FF:FF:FF", 12, INFO, KR, "start", 600)
d.t(B + 18, Y_REQ + 22, "같은 프레임이 브로드캐스트 도메인 전체에 닿는다", 12, MUTED, KR, "start")
d.o.append(f'<circle cx="{O}" cy="{Y_REQ}" r="4.5" fill="{INFO}"/>')
d.line(O, Y_REQ + 8, O, Y_DROP - 16, INFO, 1.0, "3 4")
focal(O, Y_DROP, "내 IP 가 아니다 → 받고 버린다", 232)

# ── ② ARP 응답: 되돌아오는 길이라 dashed + filled ──────────
d.path(f"M {S-10} {Y_RESP} L {B+12} {Y_RESP}", OK, 1.6, m="ok", dash="6 5")
d.t(S - 18, Y_RESP - 12, "ARP 응답 — 10.0.0.1 의 MAC 은 나다", 12, OK, KR, "end", 600)
d.t(S - 18, Y_RESP + 22, "그 한 대에게만 · 유니캐스트", 12, MUTED, KR, "end")

# ── ③ 알아낸 MAC 으로 실제 프레임 ──────────────────────────
d.path(f"M {B+10} {Y_FRAME} L {S-12} {Y_FRAME}", MUTED, 1.6, m="ar")
d.t(B + 18, Y_FRAME - 12, "Ethernet 프레임 — 목적지 = 서버 MAC · EtherType 0x0800", 12, INK, KR, "start", 600)

# ── ④ 한 번의 교환으로 양쪽 표가 채워진다 ──────────────────
note(B, Y_TABLE, "표에 서버 MAC 기록", INFO, 176)
note(S, Y_TABLE, "요청자 MAC 도 함께 기록", INFO, 208)

d.legend(Y_RAILS + 20, [("브로드캐스트", INFO), ("유니캐스트 응답", OK), ("받고 버린다", ACC)])
d.save("01-03.arp-resolution.svg")
print("ok")
