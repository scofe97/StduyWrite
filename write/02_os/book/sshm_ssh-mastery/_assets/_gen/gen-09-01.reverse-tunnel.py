# 타입 스펙: type-architecture
# 사실 출처: RFC 4254 §7.1·§7.2, OpenSSH V_10_6_P1 ssh.1 (-R), 2026-11-07 재현 (채널 서버 2 ↔ 클라이언트 0)
# 논지: 연결을 안쪽이 먼저 걸고, 그 연결 위로 바깥의 요청이 되돌아 들어온다. 경계(NAT) 안팎이 논지라 존 + 번호 화살표로 그린다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, INK, MUTED, SOFT, ACC, OK, WARN, INFO, KR, MONO

W, H = 984, 488

d = D(W, H, "ARCHITECTURE · 09-01 REVERSE TUNNEL",
      "안쪽이 먼저 건 연결 위로 바깥의 요청이 들어온다",
      "NAT 뒤 안쪽 장비의 ssh 클라이언트가 공개 서버의 sshd 로 연결을 먼저 걸고(1), 서버가 수신 포트를 엽니다(2). "
      "서버 안의 curl 요청이 수신 포트에 닿으면(3) 서버가 forwarded-tcpip 채널을 열어 같은 연결로 되돌려 보냅니다(4). "
      "클라이언트가 안쪽 서비스에 연결해 요청을 넘깁니다(5).",
      lead="NAT 는 안에서 밖으로 건 연결만 지나갑니다. 번호는 일이 일어나는 순서입니다.")


def badge(x, y, n, c):
    d.o.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{PAPER}" stroke="{c}" stroke-width="1.2"/>')
    d.t(x, y + 4, str(n), 11, c, MONO, "middle", 600)


def node(x, y, w, h, title, sub, c=None):
    if c:
        d.tone(x, y, w, h, c, 6, "14", 1.1)
    else:
        d.box(x, y, w, h)
    d.t(x + w / 2, y + h / 2 - 2, title, 13, c or INK, KR, "middle", 600)
    d.t(x + w / 2, y + h / 2 + 18, sub, 11, MUTED, MONO if sub[0] in "0123456789-p" else KR, "middle")


# 존
d.box(24, 104, 360, 316, "#161B2200", "rgba(191,192,192,0.22)", 1.0)
d.t(40, 128, "NAT 뒤 안쪽 장비", 13, INK, KR, "start", 600)
d.box(464, 104, 496, 316, "#161B2200", "rgba(191,192,192,0.22)", 1.0)
d.t(480, 128, "공개 서버", 13, INK, KR, "start", 600)

# NAT 문: 위아래 막힌 칸, 가운데는 안 → 밖 연결이 지나는 틈
d.tone(400, 104, 48, 88, WARN, 6, "14", 1.1)
d.tone(400, 304, 48, 116, WARN, 6, "14", 1.1)
d.t(424, 152, "NAT", 12, WARN, KR, "middle", 600)

# SSH 연결 관: 상자가 아니라 위아래 두 선으로 그려 존 테두리와 겹치는 상자를 만들지 않는다
d.line(196, 196, 504, 196, OK, 1.2)
d.line(196, 304, 504, 304, OK, 1.2)
d.t(300, 188, "SSH 연결 1개", 12, OK, KR, "middle", 600)

# 노드
node(48, 192, 144, 96, "ssh 클라이언트", "ssh -N -R", OK)
node(504, 192, 168, 96, "sshd", "포트 22", OK)
node(48, 340, 144, 60, "안쪽 서비스", "127.0.0.1:18099", ACC)
node(504, 340, 168, 60, "수신 포트", "127.0.0.1:2222", INFO)
node(776, 340, 152, 60, "curl", "서버 안의 요청")

# 1. 안 → 밖 연결 (+ tcpip-forward)
d.arrow([(196, 228), (500, 228)], OK, "ok", 2.0)
badge(214, 216, 1, OK)
d.t(232, 220, "안 → 밖 연결", 12, OK, KR, "start", 600)

# 2. tcpip-forward 수락 → 수신 포트 listen
d.arrow([(560, 288), (560, 336)], SOFT, "soft", 1.4)
badge(560, 314, 2, MUTED)
d.t(580, 310, "tcpip-forward", 11, MUTED, MONO, "start", 600)
d.t(580, 326, "수락 → listen", 11, MUTED, KR, "start")

# 3. 요청 → 수신 포트
d.arrow([(772, 370), (676, 370)], SOFT, "soft", 1.4)
badge(700, 352, 3, MUTED)
d.t(716, 356, "요청", 12, MUTED, KR, "start", 600)

# 4. forwarded-tcpip 로 연결 위를 되돌아간다
d.arrow([(504, 370), (488, 370), (488, 272), (196, 272)], ACC, "acc", 1.8)
badge(214, 258, 4, ACC)
d.t(232, 262, "forwarded-tcpip", 11, ACC, MONO, "start", 600)
d.t(208, 292, "서버 채널 2 → 클라이언트 0", 11, MUTED, KR, "start")

# 5. 안쪽 서비스에 연결
d.arrow([(120, 288), (120, 336)], ACC, "acc", 1.8)
badge(120, 314, 5, ACC)
d.t(140, 324, "안쪽 서비스에 연결", 12, ACC, KR, "start", 600)

d.legend(444, [("SSH 연결", OK), ("수신 지점", INFO), ("요청이 들어가는 길", ACC), ("NAT", WARN)])
svg_path = pathlib.Path(__file__).resolve().parent.parent / "09-01.reverse-tunnel.svg"
d.save(str(svg_path))
print("ok 09-01 reverse-tunnel")
