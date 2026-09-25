# 05-03 묶음 B — 교환이 어긋나는 경우들. B2 는 "REQUEST 를 보내면 바로 써도 된다"(잘못 알던 인과)를 겨눈다.
# 타입 스펙: type-flowchart — 단계를 실행 순서대로 잇는 절차 흐름. focal 은 잘못 알던 인과를 겨누는 단계.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _bundle_flow import bundle
from dd import ACC, WARN
bundle("05-03.bundle-b.svg", "PACKET ANALYSIS WITH WIRESHARK · 05-03 BUNDLE B",
       "묶음 B — 어긋나는 경우들",
       "서버 둘이 제안하는 자리, 줄 수 없는 주소를 요청해 NAK 을 받는 자리, 풀이 빈 서버, 남이 먼저 쓰는 주소를 서버와 클라이언트가 각각 걸러내는 자리, 라우터 너머의 릴레이를 차례로 만든다.",
       "한 단계에 서버 설정 하나씩 바꿉니다 — serve.sh 가 임대 기록을 지우고 새로 띄웁니다",
       [("B1", "서버 두 대", "server2 에 .200 대 범위", "OFFER 둘 · 진 서버 장부", "REQUEST 가 거절을 겸함", False, False),
        ("B2", "NAK", "범위 옮긴 뒤 옛 주소 요청", "dhclient 만 재현 가능", "ACK 없이 써도 된다", True, False),
        ("B3", "풀 소진", "주소 하나짜리 범위", "둘째 클라이언트의 침묵", "거부를 알려 주나", False, False),
        ("B4", "주소 충돌", "옆자리에 수동 설정", "서버 ICMP · 클라이언트 ARP", "OFFER 단계 ICMP 예측", False, False),
        ("B5", "릴레이", "seg-b 클라이언트 · router", "giaddr 유니캐스트", "게이트웨이를 거치나", False, False)],
       [("잘못 알던 인과를 겨눔", ACC), ("몰랐던 사실을 겨눔", WARN)], per_row=3)
