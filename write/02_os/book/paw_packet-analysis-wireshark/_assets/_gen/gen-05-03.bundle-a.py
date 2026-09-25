# 05-03 묶음 A — 주소를 받는 네 걸음을 직접 잡는다. 단계마다 Phase 1(2026-09-21)에서 어긋난 예측 하나를 겨눈다.
# 타입 스펙: type-flowchart — 단계를 실행 순서대로 잇는 절차 흐름. focal 은 잘못 알던 인과를 겨누는 단계.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _bundle_flow import bundle
from dd import ACC, WARN, INFO
bundle("05-03.bundle-a.svg", "PACKET ANALYSIS WITH WIRESHARK · 05-03 BUNDLE A",
       "묶음 A — 주소를 받는 네 걸음",
       "정상 DORA 를 서버·옆자리 양쪽에서 잡고, 서버를 끈 채 다시 요청해 DISCOVER 반복을 보고, 갱신과 반납의 메시지 수를 세고, 같은 흐름을 DHCPv6 로 한 번 더 잡는다.",
       "서버 쪽 캡처와 옆자리 캡처를 나란히 두고 읽습니다",
       [("A1", "정상 DORA", "주소 지우고 udhcpc", "서버 쪽에서 캡처", "목적지 0.0.0.0/0 · yiaddr 목록", True, False),
        ("A2", "옆자리 캡처", "neighbor 에서 동시에", "ping 은 안 보이고 DHCP 는 보임", "세그먼트 · 브로드캐스트", False, False),
        ("A3", "서버 꺼짐", "dnsmasq 중지 후 요청", "DISCOVER 간격 세기", "첫 메시지만 반복", False, False),
        ("A4", "갱신과 반납", "USR1 · USR2 시그널", "두 개짜리 정상 교환", "메시지 수로 성패 판단", False, False),
        ("A5", "DHCPv6 SARR", "dhclient -6 · 옵션 14", "ff02::1:2 · 트랜잭션 ID 둘", "멀티캐스트 · 두 걸음 조건", False, False)],
       [("잘못 알던 인과를 겨눔", ACC), ("몰랐던 사실을 겨눔", WARN)], per_row=3)
