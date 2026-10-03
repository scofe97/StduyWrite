# 04-01 세부 도식 다섯 — 사용자가 Phase 1 에서 "도식과 함께 자세히" 요청한 네 가지와 UDP 판정.
# 본문 요구: §2 마지막 ACK 자동 송신·커널 RST(handshake), raw 소켓 권한 / §3 UDP 판정과 실제 / §4 worker pool 시간축·대기열 넘침.
# 타입 스펙: type-flowchart — 단계 열 × 경우 행 격자.
# 사실 출처: RFC 9293 §3.10.7.1(RST 의 SEQ·ACK 값), raw(7)·capabilities(7), ip-sysctl.rst icmp_msgs_per_sec·icmp_msgs_burst,
#            OrbStack ubuntu sysctl 기본값(2026-10-03). 순서 번호 1000·5000 은 읽기 쉽게 고른 예시 값.
from dd import OK, BAD, ACC, WARN, INFO
from flowk import flow_grid

flow_grid("04-01.handshake.svg", "FLOW · 04-01 §2", "세 번째 세그먼트를 누가 보내나",
          "CONNECT 에서는 SYN-ACK 를 받은 스캐너 쪽 커널이 앱에 묻지 않고 ACK 를 보내 연결이 성립하고, 대상 서버의 accept 대기열에 오른다. "
          "SYN 스캔에서는 같은 SYN-ACK 를 받은 스캐너 쪽 커널이 기록에 없는 연결이라 RST 를 대상에게 보내고, 대상은 반쯤 열린 연결을 지운다.",
          "두 줄의 차이는 세 번째 칸 하나입니다. 순서 번호 값은 cntd 03-04 와 RFC 9293 §3.10.7.1 에 있습니다.",
          [("1 스캐너", "보냄"), ("2 대상", "답함"), ("3 스캐너 쪽 커널", "앱이 아님"), ("대상 서버에 남는 것", "")],
          [("CONNECT", "net.Dial", [
              ([("SYN", None)], "연결하자", None),
              ([("SYN-ACK", OK)], "좋아 · 네 SYN 받음", None),
              ([("ACK", OK)], "확인 · 자동 송신", OK),
              ([("ESTABLISHED", OK), ("accept · 로그", None)], "", None)]),
           ("SYN 스캔", "raw 소켓", [
              ([("SYN", ACC)], "앱이 직접 만듦", ACC),
              ([("SYN-ACK", OK)], "좋아 · 네 SYN 받음", None),
              ([("RST", ACC)], "그런 연결 모름", ACC),
              ([("SYN-RECV 잠깐", None), ("RST 받고 지움", None)], "", None)])],
          lane_h=128,
          legend=[("연결이 이어짐", OK), ("raw 소켓 · 커널 RST", ACC)])

flow_grid("04-01.raw-socket.svg", "FLOW · 04-01 §2", "헤더를 누가 채우나",
          "일반 TCP 소켓에서 앱은 본문만 넘기고 주소·포트·순서 번호·플래그는 커널이 상태에 맞춰 채운다. raw 소켓에서는 앱이 TCP 헤더 20바이트를 직접 써서 넘기고 "
          "커널은 IP 헤더만 붙인다. 커널의 TCP 상태 관리를 건너뛰므로 CAP_NET_RAW 권한이 있어야 열 수 있다.",
          "raw 소켓은 같은 프로토콜 번호의 패킷 사본도 받습니다. 그래서 SYN-ACK 를 스캐너가 읽을 수 있습니다.",
          [("앱이 넘기는 것", ""), ("커널이 채우는 것", ""), ("커널의 TCP 상태", ""), ("필요한 권한", "")],
          [("일반 TCP 소켓", "net.Dial", [
              ([("본문만", OK)], "", None),
              ([("IP · 포트", None), ("순서 번호 · 플래그", None)], "", None),
              ([("SYN-SENT → ESTAB", OK)], "커널이 기록", OK),
              ([("없음", OK)], "", None)]),
           ("raw 소켓", "ip4:tcp", [
              ([("TCP 헤더 20B", ACC), ("+ 본문", None)], "포트 · 플래그 직접", ACC),
              ([("IP 헤더만", None)], "", None),
              ([("기록 없음", ACC)], "그래서 커널 RST", ACC),
              ([("CAP_NET_RAW", ACC)], "root 또는 setcap", None)])],
          lane_h=136,
          legend=[("커널이 맡음", OK), ("앱이 직접 · 특권", ACC)])

flow_grid("04-01.udp-verdict.svg", "FLOW · 04-01 §3", "UDP 판정과 실제가 어긋나는 곳",
          "UDP 는 열린 포트도 앱이 답하지 않으면 침묵한다. 닫힌 포트는 ICMP 로 답하지만 그 ICMP 가 유실되거나 대상 커널의 응답 제한에 걸리면 역시 침묵이 된다. "
          "그래서 무응답은 open|filtered 로만 적을 수 있고, 그 안에 닫힌 포트까지 섞일 수 있다.",
          "오른쪽 열이 스캐너 판정이 실제와 맞았는지입니다.",
          [("실제", ""), ("돌아오는 것", ""), ("스캐너 판정", ""), ("맞았나", "")],
          [("열림 · 앱이 답함", "echo 서버", [
              ([("open", OK)], "", None),
              ([("응답 데이터그램", OK)], "", None),
              ([("open", OK)], "", None),
              ([("맞음", OK)], "", None)]),
           ("열림 · 앱이 침묵", "빈 데이터그램 받은 DNS", [
              ([("open", OK)], "", None),
              ([("무응답", WARN)], "", None),
              ([("open|filtered", WARN)], "", None),
              ([("반만 맞음", WARN)], "", None)]),
           ("닫힘", "", [
              ([("closed", BAD)], "", None),
              ([("ICMP 3/3", BAD)], "", None),
              ([("closed", BAD)], "", None),
              ([("맞음", OK)], "", None)]),
           ("닫힘 · ICMP 사라짐", "유실 · 응답 제한", [
              ([("closed", BAD)], "", None),
              ([("무응답", WARN)], "", None),
              ([("open|filtered", WARN)], "", None),
              ([("틀림", BAD)], "", None)]),
           ("막힘", "DROP", [
              ([("filtered", WARN)], "", None),
              ([("무응답", WARN)], "", None),
              ([("open|filtered", WARN)], "", None),
              ([("반만 맞음", WARN)], "", None)])],
          lane_h=88,
          legend=[("열림 · 맞음", OK), ("닫힘 · 틀림", BAD), ("증거 없음", WARN)])

flow_grid("04-01.workers.svg", "FLOW · 04-01 §4", "기다림을 겹치는 worker",
          "무응답 포트 하나에 시도 3번 × timeout 1초, 곧 3초가 든다. 순서대로 물으면 9초 동안 포트 셋을 끝내고, worker 셋이 동시에 물으면 같은 9초에 포트 아홉을 끝낸다. "
          "기다리는 동안 CPU 는 놀고 있으므로 기다림을 겹쳐도 각 포트의 판정은 그대로다.",
          "칸 하나가 3초, 곧 timeout 1초 × 시도 3번입니다. 포트 번호는 순서를 보이려고 붙였습니다.",
          [("0 – 3초", ""), ("3 – 6초", ""), ("6 – 9초", ""), ("9초까지 끝낸 포트", "")],
          [("순서대로", "worker 1", [
              ([("포트 1", None)], "", None),
              ([("포트 2", None)], "", None),
              ([("포트 3", None)], "", None),
              ([("3개", BAD)], "", None)]),
           ("동시에", "worker 3", [
              ([("포트 1", INFO), ("포트 2", INFO), ("포트 3", INFO)], "", None),
              ([("포트 4", INFO), ("포트 5", INFO), ("포트 6", INFO)], "", None),
              ([("포트 7", INFO), ("포트 8", INFO), ("포트 9", INFO)], "", None),
              ([("9개", OK)], "", None)])],
          lane_h=124,
          legend=[("동시에 기다리는 포트", INFO), ("같은 시간에 끝낸 수", OK)])

flow_grid("04-01.queues.svg", "FLOW · 04-01 §4", "너무 빨리 물으면 넘치는 자리",
          "패킷은 가는 길과 오는 길의 대기열에서 줄을 서고 대기열마다 한도가 있다. 스캐너가 빠지는 속도보다 빨리 넣으면 넘친 패킷이 버려지고, "
          "대상 커널은 같은 출발지에 ICMP 오류를 6개 몰아 보낸 뒤 초당 1개만 보낸다. 어느 쪽이든 스캐너에게는 무응답으로 보여 오판이 늘어난다.",
          "값은 OrbStack ubuntu(커널 7.0.14) 기본값입니다. ICMP 대상별 제한은 loopback 에는 걸리지 않습니다.",
          [("줄 서는 곳", ""), ("한도", ""), ("넘치면", ""), ("스캐너가 보는 것", "")],
          [("스캐너 송신", "내 장치 대기열", [
              ([("나가는 SYN · 데이터그램", None)], "", None),
              ([("1,000개", None)], "qlen 기본", None),
              ([("버림", BAD)], "보내지도 못함", None),
              ([("무응답", WARN)], "", None)]),
           ("중간 장비", "라우터 · 방화벽", [
              ([("지나가는 패킷", None)], "", None),
              ([("장비마다 다름", None)], "", None),
              ([("버림", BAD)], "", None),
              ([("무응답", WARN)], "", None)]),
           ("대상 커널", "ICMP 오류", [
              ([("port unreachable", None)], "닫힌 UDP 포트마다", None),
              ([("대상별 6개 뒤", ACC), ("초당 1개", ACC)], "icmp_ratelimit", None),
              ([("보내지 않음", BAD)], "", None),
              ([("무응답", WARN)], "closed → open|filtered", BAD)]),
           ("스캐너 수신", "응답이 몰림", [
              ([("SYN-ACK · ICMP", None)], "", None),
              ([("229,376 B", None)], "rmem_default", None),
              ([("버림", BAD)], "", None),
              ([("무응답", WARN)], "", None)])],
          lane_h=120,
          legend=[("버려짐", BAD), ("증거 없음", WARN), ("커널 기본 한도", ACC)])

flow_grid("04-01.icmp-burst.svg", "FLOW · 04-01 §4", "닫힌 UDP 포트 1,000개, 몰아서 묻기와 고르게 묻기",
          "대상 커널은 같은 출발지에 port unreachable 을 6개까지 몰아 보내고, 그 뒤로는 1초에 1개만 보낸다. 1초 안에 1,000개를 물으면 ICMP 는 7개쯤만 돌아오고 "
          "나머지 993개는 무응답이 되어 open|filtered 로 잘못 적힌다. 1초에 1개씩 물으면 전부 ICMP 를 받지만 1,000초가 걸린다. lo 에는 이 대상별 제한이 없다.",
          "커널의 토큰 버킷 규칙(inetpeer 버스트 6 · icmp_ratelimit 1000ms)으로 계산한 값입니다. 실측은 Phase 3 에서 합니다.",
          [("보내는 방식", ""), ("돌아오는 ICMP", ""), ("무응답", ""), ("걸린 시간", "")],
          [("1초에 1,000개", "원격 대상", [
              ([("1,000개", None)], "몰아서", None),
              ([("약 7개", BAD)], "6개 + 1초에 1개", None),
              ([("약 993개", BAD)], "closed → open|filtered", BAD),
              ([("1초", OK)], "", None)]),
           ("1초에 1개", "원격 대상", [
              ([("1,000개", None)], "고르게", None),
              ([("1,000개", OK)], "", None),
              ([("0개", OK)], "", None),
              ([("1,000초", BAD)], "약 17분", None)]),
           ("1초에 1,000개", "lo · 자기 자신", [
              ([("1,000개", None)], "몰아서", None),
              ([("거의 전부", OK)], "대상별 제한 없음", None),
              ([("거의 없음", OK)], "", None),
              ([("1초", OK)], "실험이 쉬워 보이는 이유", ACC)])],
          lane_h=104,
          legend=[("오판 · 느림", BAD), ("정상", OK), ("주의", ACC)])
