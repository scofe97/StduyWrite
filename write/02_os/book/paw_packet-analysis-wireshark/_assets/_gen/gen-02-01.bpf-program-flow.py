# 02-01 §4 「BPF 는 커널 안의 작은 가상머신입니다」 — `tcpdump -i en0 -d 'ip and tcp dst port 443'` 이
# macOS 15.7(tcpdump 4.99.1)에서 낸 11줄을 프레임 하나의 판정 흐름으로 편다. 명령어 번호와 피연산자는 본문 출력 그대로다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 도형이 종류를 나른다(타원=시작·끝, 사각형=계산,
#           마름모=판단). 흐름은 스펙대로 위→아래이고, 아니오 갈래는 오른쪽 한 줄 버스로 모아 (010) 으로 보낸다.
#           focal 은 그 버스 하나 — 모든 점프가 앞 번호로만 간다는 것이 이 절의 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, PAPER2, RULE, KR, MONO

W, H = 880, 704
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-01 §4",
      "BPF 프로그램이 프레임 하나를 가르는 길",
      "tcpdump -d 로 컴파일한 'ip and tcp dst port 443' 필터 11줄의 실행 흐름. 프레임은 EtherType, Protocol, 조각 오프셋, 목적지 포트를 차례로 검사받고, 하나라도 어긋나면 (010) ret #0 으로 앞으로 점프해 버려진다. 뒤로 가는 점프가 없어 모든 경로가 ret 에서 끝난다.",
      "아니오 갈래는 모두 아래쪽 (010) 으로만 뛰고, 위로 돌아가는 선은 하나도 없습니다")

CX, BUS_X, ANN_X = 320, 640, 40
HW, HH = 120, 28                                   # 마름모 반폭 · 반높이
STRIDE = 84                                        # 판단 노드 사이 간격
Y_START = 100
TOPS = [164 + i * STRIDE for i in range(6)]        # 164 248 332 416 500 584

def oval(cx, y, w, h, txt, c=INK):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, y + h / 2 + 5, txt, 13, c, KR, "middle", 600)

def diamond(cy, txt, fam=KR):
    d.o.append(f'<polygon points="{CX},{cy - HH} {CX + HW},{cy} {CX},{cy + HH} {CX - HW},{cy}" '
               f'fill="{PAPER2}" stroke="{INK}" stroke-width="1.1"/>')
    d.t(CX, cy + 5, txt, 13, INK, fam, "middle", 600)

def ann(cy, lines):                                # 왼쪽 여백의 명령어 번호 — 본문 출력 그대로
    y0 = cy - 9 * (len(lines) - 1) + 4
    for i, s in enumerate(lines):
        d.t(ANN_X, y0 + i * 18, s, 12, MUTED, MONO, "start")

# 판단 노드: (마름모 글자, 글꼴, 왼쪽 명령어, 예 라벨, 아니오 점프 라벨)
DECISIONS = {
    0: ("EtherType = 0x800", MONO, ["(000) ldh [12]", "(001) jeq #0x800"], "예 · IPv4", "jf 10"),
    1: ("Protocol = 6", MONO, ["(002) ldb [23]", "(003) jeq #0x6"], "예 · TCP", "jf 10"),
    2: ("조각 오프셋 = 0", KR, ["(004) ldh [20]", "(005) jset #0x1fff"], "예 · 첫 조각", "jt 10"),
    4: ("목적지 포트 = 443", KR, ["(008) jeq #0x1bb"], "예", "jf 10"),
}

# 연결선 먼저 — 위→아래 본선
d.arrow([(CX, Y_START + 36), (CX, TOPS[0] - 4)], MUTED, "ar", 1.4)
for i in range(5):
    y_from = TOPS[i] + 2 * HH if i != 3 else TOPS[3] + 56
    d.arrow([(CX, y_from), (CX, TOPS[i + 1] - 4)], MUTED, "ar", 1.4)
    if i in DECISIONS:
        d.t(CX + 12, (y_from + TOPS[i + 1]) / 2 + 5, DECISIONS[i][3], 12, MUTED, KR, "start", 600)

# 아니오 갈래 — 오른쪽 버스 하나로 모여 (010) 으로 내려간다
junctions = [TOPS[i] + HH for i in DECISIONS]
for i, cy in zip(DECISIONS, junctions):
    d.line(CX + HW, cy, BUS_X, cy, ACC, 1.6)
    d.t(CX + HW + 12, cy - 8, "아니오", 12, MUTED, KR, "start", 600)
    d.t(BUS_X + 12, cy + 5, DECISIONS[i][4], 12, SOFT, MONO, "start")
d.arrow([(BUS_X, junctions[0]), (BUS_X, TOPS[5] - 4)], ACC, "acc", 1.6)
for cy in junctions:
    d.o.append(f'<circle cx="{BUS_X}" cy="{cy}" r="4" fill="{INK}"/>')
d.t(BUS_X + 12, junctions[0] - 24, "뒤로 가는 선 없음", 12, ACC, KR, "start", 600)

# 노드
oval(CX, Y_START, 200, 36, "프레임 도착")
for i, (txt, fam, lines, _, _) in DECISIONS.items():
    diamond(TOPS[i] + HH, txt, fam)
    ann(TOPS[i] + HH, lines)
d.box(CX - HW, TOPS[3], 2 * HW, 56, PAPER2, RULE, 1.0, 6)
d.t(CX, TOPS[3] + 24, "포트 위치 계산", 13, INK, KR, "middle", 600)
d.t(CX, TOPS[3] + 44, "x = 4*([14]&0xf)", 12, MUTED, MONO)
ann(TOPS[3] + 28, ["(006) ldxb", "(007) ldh [x + 16]"])
oval(CX, TOPS[5], 240, 40, "받아들임", OK)
ann(TOPS[5] + 20, ["(009) ret #524288"])
oval(BUS_X, TOPS[5], 200, 40, "버림", BAD)
d.t(BUS_X + 112, TOPS[5] + 25, "(010) ret #0", 12, MUTED, MONO, "start")

d.legend(656, [("앞 번호로만 가는 점프", ACC), ("받아들임", OK), ("버림", BAD)])
d.save("02-01.bpf-program-flow.svg")
