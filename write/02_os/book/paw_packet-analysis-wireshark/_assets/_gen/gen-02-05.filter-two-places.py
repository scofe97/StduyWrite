# 02-05 §3 — 캡처 필터 -f 는 잡는 동안, 디스플레이 필터 -Y 는 읽는 동안 걸린다. 저장된 파일을 읽으면서 -f 를 주면 tshark 가 거절한다.
# 타입 스펙: type-architecture — 경계(잡는 동안 / 읽는 동안) 안팎에서 무엇이 어디로 흐르는가. 존 두 개와 방향 화살표, focal 은 거절 메시지 하나.
# 사실 출처: 노트 L186~L197 (명령 L190·L192, 거절 메시지 L197)
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 552
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-05 §3",
      "필터가 걸리는 두 자리",
      "-f 는 인터페이스에서 잡는 동안, -Y 는 저장된 파일을 읽는 동안 걸린다. 파일 읽기에 -f 를 주면 거절된다.",
      "같은 18080 포트를 두 문법으로 적었습니다")

def zone(y, h, label):
    d.o.append(f'<rect x="24" y="{y}" width="832" height="{h}" rx="8" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="6 4"/>')
    tw = sum(11 if "가" <= c <= "힣" else 6.2 for c in label)
    d.o.append(f'<rect x="36" y="{y - 8}" width="{int(tw) + 16}" height="16" fill="{PAPER}"/>')
    d.t(44, y + 4, label, 11, SOFT, KR, "start", 600)

def node(x, y, w, h, title, sub=None, fam=MONO):
    d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    ty = y + h / 2 - 6 if sub else y + h / 2 + 4
    d.t(x + w / 2, ty, title, 12 if fam == MONO else 13, INK, fam, "middle", 600)
    if sub: d.t(x + w / 2, ty + 18, sub, 11, MUTED)

zone(104, 124, "잡는 동안 · tshark -i")
node(56, 136, 140, 56, "lo0", "인터페이스")
d.arrow([(196, 164), (628, 164)], INFO, "info", 1.5)
d.t(412, 154, "-f 'tcp port 18080'", 12, INFO, MONO, "middle", 600)
d.t(412, 186, "잡는 동안 거름", 11, MUTED)
node(632, 136, 192, 56, "paw-0202-f.pcapng", "-w 로 저장")

zone(256, 212, "읽는 동안 · tshark -r")
node(56, 288, 192, 140, "paw-0202.pcapng", "저장된 캡처")
d.arrow([(248, 316), (476, 316)], OK, "ok", 1.5)
d.t(362, 306, "-Y 'tcp.port == 18080'", 12, OK, MONO, "middle", 600)
d.t(362, 338, "읽은 뒤 거름", 11, MUTED)
node(480, 288, 344, 56, "화면", "-Y 에 맞는 줄만", fam=KR)
d.arrow([(248, 404), (476, 404)], BAD, "bad", 1.5)
d.t(362, 394, "-f 'tcp port 18080'", 12, BAD, MONO, "middle", 600)
d.t(362, 426, "읽는 파일에는 거절", 11, MUTED)
d.o.append(f'<rect x="480" y="376" width="344" height="56" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(496, 398, "Only read filters, not capture filters,", 11, ACC, MONO, "start")
d.t(496, 416, "can be specified when reading a capture file.", 11, ACC, MONO, "start")

d.legend(488, [("캡처 필터 -f", INFO), ("디스플레이 필터 -Y", OK), ("읽으면서 -f", BAD), ("거절 메시지", ACC)])
d.save("02-05.filter-two-places.svg")
