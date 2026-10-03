# 04-01 절 지도 넷 — 각 ## 의 > 요약 바로 아래. 실제 플래그·번호·errno·초를 칸에 넣은 흐름 격자.
# 본문 요구: 사용자 선호(2026-09-29·10-03) "## 마다 전체 흐름 도식", "처음 보는 사람도 이해", "도식 적극 사용".
# 타입 스펙: type-flowchart — 단계 열 × 경우 행 격자.
# 사실 출처: RFC 9293 §3.10.7.1, Linux net/ipv4/icmp.c icmp_err_convert, iptables-extensions(8) REJECT,
#            OrbStack ubuntu sysctl(tcp_syn_retries=6, icmp_msgs_per_sec=1000, icmp_msgs_burst=50), ip-sysctl.rst,
#            gonet-lab docs/03-02 Phase 4 계획(naabu 기본값 retries 3 · timeout 1000ms · c 25).
from dd import OK, BAD, ACC, WARN, INFO
from flowk import flow_grid

flow_grid("04-01.map-1.svg", "FLOW · 04-01 §1", "같은 포트를 세 방식으로 묻기",
          "CONNECT 는 net.Dial 로 handshake 를 끝까지 맺고 결과를 errno 로 받는다. SYN 스캔은 SYN 하나만 보내고 돌아온 플래그를 직접 읽는다. "
          "UDP 스캔은 데이터그램을 보내고 응답 데이터그램이나 ICMP port unreachable 을 기다린다. 막힌 포트는 세 방식 모두 아무것도 돌아오지 않는다.",
          "열 넷은 순서가 아니라 경우입니다. 같은 질문을 열린·닫힌·막힌 포트에 던졌을 때 돌아오는 것과 판정입니다.",
          [("보내는 것", ""), ("열린 포트", "듣는 소켓 있음"), ("닫힌 포트", "듣는 소켓 없음"), ("막힌 포트", "방화벽 DROP")],
          [("CONNECT", "일반 권한", [
              ([("net.Dial", None), ("SYN", None)], "커널이 handshake", None),
              ([("SYN-ACK", OK), ("Dial 성공", OK)], "open", OK),
              ([("RST", BAD), ("ECONNREFUSED", BAD)], "closed", BAD),
              ([("무응답", WARN), ("timeout", WARN)], "filtered", WARN)]),
           ("SYN", "raw 소켓 · 특권", [
              ([("raw SYN", ACC)], "헤더를 직접 만듦", ACC),
              ([("SYN-ACK", OK)], "open", OK),
              ([("RST", BAD)], "closed", BAD),
              ([("무응답", WARN)], "filtered", WARN)]),
           ("UDP", "일반 권한", [
              ([("데이터그램", None)], "", None),
              ([("앱 응답 · 또는 침묵", OK)], "open · open|filtered", OK),
              ([("ICMP 3/3", BAD)], "closed", BAD),
              ([("무응답", WARN)], "open|filtered", WARN)])],
          lane_h=112, link=False,
          legend=[("열림의 증거", OK), ("닫힘의 증거", BAD), ("증거 없음", WARN), ("특권 필요", ACC)])

flow_grid("04-01.map-2.svg", "FLOW · 04-01 §2", "패킷이 도착하면 커널이 먼저 소켓을 찾는다",
          "커널은 들어온 패킷마다 받을 소켓을 찾고, 찾은 결과에 따라 앱이 부르지 않아도 답을 보낸다. 연결 중인 TCP 소켓이 있으면 마지막 ACK 를 자동으로 보내고, "
          "TCP 소켓이 없으면 RST 를, UDP 소켓이 없으면 ICMP port unreachable 을 돌려보낸다. raw 소켓은 사본을 받을 뿐 TCP 소켓으로 치지 않는다.",
          "위 두 줄은 스캐너 쪽 커널, 아래 두 줄은 대상 쪽 커널입니다. 네 줄 모두 앱 코드는 아무것도 보내지 않았습니다.",
          [("도착한 패킷", ""), ("커널이 찾은 소켓", ""), ("커널이 보내는 것", "앱 몰래"), ("앱이 보는 것", "")],
          [("CONNECT 중", "스캐너 쪽 커널", [
              ([("SYN-ACK", None)], "", None),
              ([("연결 중 TCP 소켓", OK)], "SYN-SENT", OK),
              ([("ACK", OK)], "handshake 완료", OK),
              ([("Dial 성공", OK)], "", None)]),
           ("SYN 스캔 중", "스캐너 쪽 커널", [
              ([("SYN-ACK", None)], "", None),
              ([("TCP 소켓 없음", ACC)], "raw 소켓엔 사본만", ACC),
              ([("RST → 대상", ACC)], "나는 모르는 연결", ACC),
              ([("SYN-ACK 사본", None)], "스캐너가 읽음", None)]),
           ("닫힌 TCP 포트", "대상 쪽 커널", [
              ([("SYN", None)], "", None),
              ([("없음", BAD)], "", None),
              ([("RST · ACK", BAD)], "", None),
              ([("ECONNREFUSED", BAD)], "보낸 쪽 앱", None)]),
           ("닫힌 UDP 포트", "대상 쪽 커널", [
              ([("데이터그램", None)], "", None),
              ([("없음", BAD)], "UdpNoPorts +1", None),
              ([("ICMP 3/3", BAD)], "port unreachable", None),
              ([("connect 했으면", None), ("ECONNREFUSED", BAD)], "", None)])],
          lane_h=112,
          legend=[("정상 연결 처리", OK), ("raw 소켓 경로", ACC), ("거절", BAD)])

flow_grid("04-01.map-3.svg", "FLOW · 04-01 §3", "원인은 다섯, 스캐너가 보는 것은 셋",
          "스캐너가 보는 것은 RST, ICMP, 무응답 셋뿐이다. 닫힌 포트와 REJECT 는 무언가를 돌려보내 증거를 남긴다. DROP, 유실, ICMP 응답 제한은 모두 아무것도 돌려보내지 않아 스캐너 쪽에서는 똑같이 보인다. "
          "CONNECT 는 커널이 ICMP 를 ECONNREFUSED 로 바꾸므로 닫힌 포트와 REJECT 를 가르지 못한다.",
          "가운데 열은 net.Dial 이 돌려주는 결과, 오른쪽 열은 패킷을 직접 읽는 스캐너의 판정입니다.",
          [("실제 원인", ""), ("돌아오는 것", ""), ("CONNECT 가 보는 것", ""), ("패킷을 읽으면", "")],
          [("닫힌 포트", "", [
              ([("소켓 없음", None)], "", None),
              ([("RST", BAD)], "", None),
              ([("ECONNREFUSED", BAD)], "", None),
              ([("closed", BAD)], "", None)]),
           ("REJECT 기본", "iptables", [
              ([("방화벽 거절", None)], "", None),
              ([("ICMP 3/3", BAD)], "", None),
              ([("ECONNREFUSED", BAD)], "닫힌 포트와 같음", WARN),
              ([("filtered", WARN)], "ICMP 를 따로 읽으면", None)]),
           ("tcp-reset", "REJECT 옵션", [
              ([("방화벽 거절", None)], "", None),
              ([("RST", BAD)], "", None),
              ([("ECONNREFUSED", BAD)], "", None),
              ([("closed", BAD)], "닫힌 척 · 구분 불가", WARN)]),
           ("DROP", "iptables", [
              ([("방화벽 버림", None)], "", None),
              ([("무응답", WARN)], "", None),
              ([("timeout", WARN)], "", None),
              ([("filtered", WARN)], "", None)]),
           ("유실", "가는 길 · 오는 길", [
              ([("열린 포트", OK)], "", None),
              ([("무응답", WARN)], "", None),
              ([("timeout", WARN)], "", None),
              ([("filtered", WARN)], "오판", BAD)])],
          lane_h=96,
          legend=[("거절의 증거", BAD), ("증거 없음 · 구분 불가", WARN), ("실제로는 열림", OK)])

flow_grid("04-01.map-4.svg", "FLOW · 04-01 §4", "포트 1,000개를 묻는 데 걸리는 시간과 오판",
          "모든 포트가 무응답이라는 가장 느린 경우를 timeout 1초로 셈했다. 손실은 시도마다·방향마다 독립이라고 가정했다. 시도를 3번으로 늘리면 오판은 줄지만 시간이 세 배가 되고, worker 를 늘리면 기다림이 겹쳐 시간이 준다. "
          "손실 20% 경로에서 열린 포트를 놓칠 확률은 시도 1번이면 36%, 3번이면 약 4.7% 다.",
          "시간은 무응답 포트 1,000개 기준 계산값이고, 오판율은 가는 길·오는 길 각각 20% 손실을 가정한 계산값입니다.",
          [("설정", "worker · 시도"), ("포트 하나", "무응답일 때"), ("1,000개 전체", ""), ("열린 포트를 놓칠 확률", "손실 20%")],
          [("순서대로", "시도 1번", [
              ([("1 · 1", None)], "", None),
              ([("1초", None)], "", None),
              ([("1,000초", BAD)], "약 17분", None),
              ([("36%", BAD)], "1 − 0.8 × 0.8", None)]),
           ("순서대로", "시도 3번", [
              ([("1 · 3", None)], "", None),
              ([("3초", None)], "", None),
              ([("3,000초", BAD)], "약 50분", None),
              ([("약 4.7%", OK)], "0.36의 세제곱", None)]),
           ("worker 25", "예시", [
              ([("25 · 3", INFO)], "", None),
              ([("3초", None)], "25개씩 겹침", INFO),
              ([("120초", OK)], "3,000 ÷ 25", None),
              ([("약 4.7%", OK)], "넘침이 없을 때", None)]),
           ("worker 1,000", "rate 무제한", [
              ([("1,000 · 3", ACC)], "", None),
              ([("3초", None)], "", None),
              ([("3초", None)], "계산상으로만", ACC),
              ([("오판 증가", ACC)], "대기열 넘침 · ICMP 제한", ACC)])],
          lane_h=96,
          legend=[("느림 · 오판 많음", BAD), ("목표 근처", OK), ("동시 실행", INFO), ("너무 빠르면 생기는 일", ACC)])
