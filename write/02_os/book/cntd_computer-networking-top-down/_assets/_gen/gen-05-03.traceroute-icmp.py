# 타입 스펙: type-data-flow — TTL 을 하나씩 올린 데이터그램이 어디서 죽고 무엇이 돌아오는지의 흐름.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.6 + 이 기계에서 tcpdump 로 잡은 실제 패킷
# 2026-09-29: 캡처 세 줄을 원시 로그 1-6 (가) 380~382행 그대로로 바꿨다(나간 패킷 줄은 로그에 없어 뺐다).
#   종전 세 줄은 출발 포트 47535 와 47699 가 달라 서로 다른 회차를 이어 붙인 것이었다.
#   시간 초과 라벨: RFC 792 형식에 이름 칸이 없다. 주소는 IP 출발지, 이름은 traceroute 의 역방향 DNS.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, OK, KR, MONO

W, H = 1000, 660
d = D(W, H, "SECTION 5.6 · TRACEROUTE OVER ICMP",
      "죽는 자리를 하나씩 옮깁니다",
      "traceroute 가 TTL 을 1 부터 올려 보내며 매번 다른 라우터에서 데이터그램을 죽이고, 그 라우터가 보내는 ICMP 시간 초과로 경로를 알아내는 흐름.",
      "이 기계에서 잡은 패킷으로 확인했습니다 — 목적지 포트는 33435 부터 하나씩 올라갑니다")

d.box(24, 120, 150, 66, PAPER2, ACC, 1.4, 7)
d.t(99, 148, "출발지", 12, ACC, KR, "middle", 600)
d.t(99, 168, "타이머를 켬", 11, MUTED, KR)

# 홉 2·3 은 이 회선의 ISP 라우터라 주소를 적지 않는다. 공개 저장소로 나가는 문서다
HOPS = [("라우터 1", "TTL 1 이 여기서 0", "집 안 게이트웨이"),
        ("라우터 2", "TTL 2 가 여기서 0", "ISP 라우터"),
        ("라우터 3", "TTL 3 이 여기서 0", "ISP 라우터")]
for i, (name, sub, addr) in enumerate(HOPS):
    x = 232 + i * 200
    d.box(x, 120, 176, 66, PAPER2, RULE, 1.0, 7)
    d.t(x + 88, 144, name, 12, INK, KR, "middle", 600)
    d.t(x + 88, 164, sub, 11, MUTED, KR)
    d.t(x + 88, 180, addr, 11, SOFT, KR)
    # 각 라우터가 돌려보내는 ICMP
    d.path(f"M {x + 88} 186 L {x + 88} 232 L 99 232 L 99 190" if i == 0
           else f"M {x + 88} 186 L {x + 88} {232 + i * 26} L 99 {232 + i * 26} L 99 190",
           BAD, 1.3, m="bad", dash="5 4")

d.box(832, 120, 144, 66, PAPER2, OK, 1.4, 7)
d.t(904, 144, "목적지", 12, OK, KR, "middle", 600)
d.t(904, 164, "쓰지 않는 포트", 11, MUTED, KR)

for i in range(4):
    x0 = 174 if i == 0 else 232 + (i - 1) * 200 + 176
    x1 = 232 + i * 200 if i < 3 else 832
    d.path(f"M {x0 + 4} 153 L {x1 - 6} 153", ACC, 1.6, m="acc")

d.path("M 904 186 L 904 320 L 99 320 L 99 190", OK, 1.5, m="ok", dash="5 4")
d.t(500, 336, "type 3 code 3 · 포트 도달 불가 — 여기서 멈춤", 11, OK, KR)
d.t(500, 296, "type 11 code 0 · 시간 초과 — 라우터 주소는 출발지로 옴 · 이름은 역조회", 11, BAD, KR)

# 실측한 패킷
d.box(24, 366, 952, 132, PAPER2, RULE, 1.0, 8)
d.t(44, 392, "이 기계에서 잡은 실제 패킷 · 시간 초과 한 통과 그 안에 인용된 원본", 12, INK, KR, "start", 600)
for i, line in enumerate([
        "192.168.0.1 > 192.168.0.184: ICMP time exceeded in-transit, length 48",
        "    IP (tos 0x0, ttl 1, id 47845, offset 0, flags [none], proto UDP (17), length 40)",
        "    192.168.0.184.47844 > 1.1.1.1.33435: UDP, length 12"]):
    d.t(44, 418 + i * 24, line, 10, MUTED if i == 0 else SOFT, MONO, "start")
d.t(44, 488, "ICMP 48 = 헤더 8 + 인용된 원본 40 · 원본 데이터그램 통째로", 11, ACC, KR, "start")

d.t(30, 546, "원문은 ICMP 메시지가 문제의 데이터그램의 헤더와 앞 8바이트를 담는다고 적음 · 그것은 RFC 792 가 정한 범위이고", 11, MUTED, KR, "start")
d.t(30, 566, "RFC 1122 이후로는 최소치 · 이 라우터는 40바이트 전부를 돌려보냄", 11, MUTED, KR, "start")

d.legend(590, [("나가는 데이터그램", ACC), ("시간 초과 응답", BAD), ("멈춤 신호", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "05-03.traceroute-icmp.svg"
d.save(out)
print("→", out)
