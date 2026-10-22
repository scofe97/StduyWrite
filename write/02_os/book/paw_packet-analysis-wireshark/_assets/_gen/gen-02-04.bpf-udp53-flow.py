# 타입 스펙: type-flowchart — udp port 53 이 컴파일된 BPF 가 프레임 하나를 가르는 길
# 사실 출처: 노트 L120~L141 (tcpdump -d 'udp port 53' 출력), L149~L151 (해석 산문)
# 02-04 §4 — 명령어 번호·피연산자·점프 대상은 본문 출력 그대로다. IPv6 갈래(001~007)는 한 상자로 접고,
# IPv4 갈래(008~018)만 판단 노드로 편다. 모든 점프가 앞 번호로만 가는 것이 이 절의 논지라 버림 버스가 focal 이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, PAPER2, RULE, KR, MONO

W, H = 880, 880
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-04 §4",
      "udp port 53 필터가 프레임 하나를 가르는 길",
      "tcpdump -d 'udp port 53' 이 낸 20줄 가운데 IPv4 쪽 (008)~(018) 의 실행 흐름. EtherType 0x800, Protocol 0x11, 단편 비트, 포트 두 번의 검사를 차례로 거치고 하나라도 어긋나면 (019) ret #0 으로 버려진다. IPv6 쪽 (001)~(007) 은 같은 검사를 포트 54·56 자리에서 한다.",
      "버림으로 가는 점프는 모두 아래쪽 (019) 으로만 갑니다")

CX, BUS_X, ANN_X = 420, 700, 24
HW, HH = 120, 28
TOPS = [156, 236, 316, 396]                      # D1~D4 마름모 윗변
STEP_Y = 480                                     # (013) 상자 윗변
TOP5, TOP6 = 568, 648
ACC_Y = 740

def oval(cx, y, w, h, txt, c=INK, fam=KR):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, y + h / 2 + 5, txt, 13, c, fam, "middle", 600)

def diamond(top, txt, fam=MONO):
    cy = top + HH
    d.o.append(f'<polygon points="{CX},{top} {CX + HW},{cy} {CX},{top + 2 * HH} {CX - HW},{cy}" '
               f'fill="{PAPER2}" stroke="{INK}" stroke-width="1.1"/>')
    d.t(CX, cy + 5, txt, 13, INK, fam, "middle", 600)

def ann(cy, lines):
    y0 = cy - 9 * (len(lines) - 1) + 4
    for i, s in enumerate(lines):
        d.t(ANN_X, y0 + i * 18, s, 12, MUTED, MONO, "start")

# (키, 마름모 글자, 글꼴, 왼쪽 명령어, 아래로 가는 갈래 라벨, 오른쪽으로 가는 갈래 라벨)
NODES = [
    (TOPS[0], "EtherType = 0x86dd", MONO, ["(000) ldh [12]", "(001) jeq #0x86dd"], "아니오 · jf 8", "예 · jt 2"),
    (TOPS[1], "EtherType = 0x800", MONO, ["(008) jeq #0x800"], "예 · IPv4", "아니오 · jf 19"),
    (TOPS[2], "Protocol = 0x11", MONO, ["(009) ldb [23]", "(010) jeq #0x11"], "예 · UDP", "아니오 · jf 19"),
    (TOPS[3], "단편 비트 0x1fff 켜짐", KR, ["(011) ldh [20]", "(012) jset #0x1fff"], "아니오 · 첫 조각", "예 · 뒷조각 · jt 19"),
]

# 본선 연결선
d.arrow([(CX, 100 + 36), (CX, TOPS[0] - 4)], MUTED, "ar", 1.4)
for i in range(3):
    y_from = TOPS[i] + 2 * HH
    d.arrow([(CX, y_from), (CX, TOPS[i + 1] - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, TOPS[3] + 2 * HH), (CX, STEP_Y - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, STEP_Y + 52), (CX, TOP5 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, TOP5 + 2 * HH), (CX, TOP6 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, TOP6 + 2 * HH), (CX, ACC_Y - 4)], MUTED, "ar", 1.4)

# 아래 갈래 라벨
for i, n in enumerate(NODES):
    y_from = n[0] + 2 * HH
    nxt = TOPS[i + 1] if i < 3 else STEP_Y
    d.t(CX + 12, (y_from + nxt) / 2 + 5, n[4], 12, MUTED, KR, "start", 600)

# 버림 버스 — 오른쪽으로 나와 BUS_X 에서 (019) 로 내려간다 (D2, D3, D4, D6)
drops = [(TOPS[1] + HH, NODES[1][5]), (TOPS[2] + HH, NODES[2][5]), (TOPS[3] + HH, NODES[3][5]),
         (TOP6 + HH, "아니오 · jf 19")]
for cy, lab in drops:
    d.line(CX + HW, cy, BUS_X, cy, ACC, 1.6)
    d.t(CX + HW + 12, cy - 8, lab, 12, MUTED, KR, "start", 600)
    d.o.append(f'<circle cx="{BUS_X}" cy="{cy}" r="4" fill="{INK}"/>')
d.arrow([(BUS_X, drops[0][0]), (BUS_X, ACC_Y - 4)], ACC, "acc", 1.6)
d.t(BUS_X + 12, drops[0][0] - 10, "뒤로 가는 선 없음", 12, ACC, KR, "start", 600)

# 노드
oval(CX, 100, 200, 36, "프레임 도착")
for top, txt, fam, lines, _, _ in NODES:
    diamond(top, txt, fam)
    ann(top + HH, lines)

# IPv6 갈래 — 접은 상자
d.line(CX + HW, TOPS[0] + HH, 640, TOPS[0] + HH, MUTED, 1.4)
d.t(CX + HW + 12, TOPS[0] + HH - 8, NODES[0][5], 12, MUTED, KR, "start", 600)
d.box(640, TOPS[0] + 4, 220, 68, PAPER2, RULE, 1.0, 6)
d.t(750, TOPS[0] + 24, "IPv6 쪽 (002)~(007)", 13, INK, KR, "middle", 600)
d.t(750, TOPS[0] + 42, "포트 [54]·[56] = 0x35", 12, MUTED, MONO)
d.t(750, TOPS[0] + 62, "맞으면 (018) · 아니면 (019)", 12, MUTED, KR)

# (013) 상자 — 가변 길이 IP 헤더
d.box(CX - HW, STEP_Y, 2 * HW, 52, PAPER2, RULE, 1.0, 6)
d.t(CX, STEP_Y + 22, "IP 헤더 길이 계산", 13, INK, KR, "middle", 600)
d.t(CX, STEP_Y + 42, "x = 4*([14]&0xf)", 12, MUTED, MONO)
ann(STEP_Y + 26, ["(013) ldxb 4*([14]&0xf)"])

# 포트 두 번
diamond(TOP5, "[x+14] = 0x35")
ann(TOP5 + HH, ["(014) ldh [x + 14]", "(015) jeq #0x35"])
d.t(CX + 12, (TOP5 + 2 * HH + TOP6) / 2 + 5, "아니오 · jf 16", 12, MUTED, KR, "start", 600)
diamond(TOP6, "[x+16] = 0x35")
ann(TOP6 + HH, ["(016) ldh [x + 16]", "(017) jeq #0x35"])
d.t(CX + 12, (TOP6 + 2 * HH + ACC_Y) / 2 + 5, "예 · jt 18", 12, MUTED, KR, "start", 600)

# [x+14] 가 맞으면 (018) 로 — 왼쪽 버스
LB = 240
d.line(CX - HW, TOP5 + HH, LB, TOP5 + HH, OK, 1.6)
d.t(CX - HW - 12, TOP5 + HH - 8, "예 · jt 18", 12, MUTED, KR, "end", 600)
d.arrow([(LB, TOP5 + HH), (LB, ACC_Y + 20), (CX - 120, ACC_Y + 20)], OK, "ok", 1.6)

oval(CX, ACC_Y, 240, 40, "받아들임", OK)
d.t(CX, ACC_Y + 60, "(018) ret #524288", 12, MUTED, MONO)
oval(BUS_X, ACC_Y, 160, 40, "버림", BAD)
d.t(BUS_X, ACC_Y + 60, "(019) ret #0", 12, MUTED, MONO)

d.legend(828, [("앞 번호로만 가는 버림 점프", ACC), ("받아들임", OK), ("버림", BAD)])
d.save("02-04.bpf-udp53-flow.svg")
