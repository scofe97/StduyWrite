# 00-03-dhcp-lease — 주소가 없는 상태에서 주소를 받아 오는 네 번의 교환
# 본문 요구: "앞의 두 번은 출발지 IP 칸이 비어 있어 브로드캐스트로 오간다" — 확정 응답(ACK)이 초점.
# 타입 스펙: type-sequence.md — 참여자 둘 사이의 시간순 메시지. 생명선과 왕복 순서가 논지다.
#           이 폴더의 다른 시퀀스 여섯 장과 같은 ddx.lanes 골격을 쓴다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·순서를 그대로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, KR, MONO

W, H = 1000, 540
d = D(W, H, "SEQUENCE · DHCP LEASE",
      "주소가 없는 상태에서 주소를 받아 온다",
      "새로 켠 기계와 DHCP 서버 사이의 네 번의 교환을 시간순으로 그린 시퀀스. 앞의 두 번은 출발지 IP 가 "
      "비어 있어 브로드캐스트로 오가고, 마지막 확정 응답을 초점으로 강조했다.",
      lead="앞의 두 번은 출발지 IP 칸이 비어 있어 브로드캐스트로 오갑니다. MAC 이 이미 붙어 있어 이 대화가 가능합니다.")

LX = ddx.lanes(d, [("새로 켠 기계", "0.0.0.0"), ("DHCP 서버", "주소를 빌려주는 쪽")], y0=132, lane_w=240)
for x in LX.values():
    d.line(x, d.lane_top + 4, 444, x if False else 444, RULE, 1.0, "4 4") if False else None
    d.line(x, d.lane_top + 4, x, 444, RULE, 1.0, "4 4")

MSGS = [("새로 켠 기계", "DHCP 서버", "DISCOVER · 브로드캐스트로 서버를 찾는다", 236, MUTED, None),
        ("DHCP 서버", "새로 켠 기계", "OFFER · 이 주소는 어떠십니까", 292, MUTED, "5 4"),
        ("새로 켠 기계", "DHCP 서버", "REQUEST · 그것으로 쓰겠습니다", 348, MUTED, None),
        ("DHCP 서버", "새로 켠 기계", "ACK · 확정 · 임대 시간까지 당신 것", 404, ACC, None)]
for a, b, lab, y, c, dash in MSGS:
    x1, x2 = LX[a], LX[b]
    dx = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 8 * dx} {y + 12} L {x2 - 12 * dx} {y + 12}", c, 1.5,
           m="acc" if c is ACC else "ar", dash=dash)
    d.t((x1 + x2) / 2, y, lab, 12, c, KR)

d.t(100, 456, "받는 것은 IP 하나가 아니라 마스크·게이트웨이·DNS 서버까지 네 가지 묶음입니다.", 12, MUTED, KR, "start")
d.legend(472, [("브로드캐스트로 오가는 교환", MUTED), ("주소가 확정되는 자리", ACC)])
d.save("00-03-dhcp-lease.svg")
print("ok dhcp-lease")
