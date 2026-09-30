# 02-03 절 도식 셋 — 실습 문서의 ## 요약 아래. 실제 명령·포트·출력 값을 칸에 넣은 흐름 격자.
# 본문 요구: 사용자 요청(2026-09-29) 실습 문서 분리, "## 마다 전체 흐름 도식", "실제 흐름이 보이게".
# 타입 스펙: type-flowchart — 단계 열 × 경우 행 격자. 사실 출처: 2026-09-28~29 Phase 3 실측 출력(학습자 터미널 붙여넣기).
from dd import OK, BAD, ACC
from flowk import flow_grid

flow_grid("02-03.terminals.svg", "FLOW · 02-03 §1", "터미널 넷이 맡은 일",
          "터미널 A 는 UDP echo 서버를 :8080 에 띄우고 로그를 파일로 남긴다. C 는 TCP echo 서버를 :9000 에 띄운다. B 는 클라이언트 쪽 명령을 "
          "돌려 임시 포트로 서버에 붙고 결과를 표준 출력에 찍는다. D 는 tc 로 lo 에 netem 을 걸고 ss 와 nstat 으로 커널 쪽을 본다.",
          "모두 OrbStack ubuntu 안에서 /Users/simbohyeon/study/gonet-lab 을 작업 폴더로 씁니다.",
          [("터미널", ""), ("실행하는 것", ""), ("소켓 · 장치", ""), ("남는 기록", "")],
          [("A", "UDP 서버", [
              ([("A", None)], "", None),
              ([("gonet-linux", None), ("udp-listen :8080", None)], "", None),
              ([("UDP :8080", OK)], "소켓 1", OK),
              ([("stderr", None), ("/tmp/udp.log", None)], "recv 줄", None)]),
           ("C", "TCP 서버", [
              ([("C", None)], "", None),
              ([("gonet-linux", None), ("listen :9000", None)], "", None),
              ([("TCP :9000", None)], "연결마다 소켓", None),
              ([("stderr", None)], "listen 줄", None)]),
           ("B", "클라이언트", [
              ([("B", None)], "", None),
              ([("udp-send · connect", None), ("phase2-loss", None)], "", None),
              ([("임시 포트", None)], "32768~60999", None),
              ([("stdout", None)], "echo · 집계", None)]),
           ("D", "관측 · 장치", [
              ([("D", None)], "", None),
              ([("tc qdisc", ACC), ("ss · nstat", None)], "", None),
              ([("lo · netem", ACC)], "손실 · 뒤바뀜", ACC),
              ([("소켓 줄", None), ("카운터", None)], "", None)])],
          lane_h=112,
          legend=[("UDP 서버 소켓", OK), ("일부러 건 장치", ACC)])

flow_grid("02-03.ss-sockets.svg", "FLOW · 02-03 §3", "ss 가 보여 준 소켓 줄",
          "클라이언트 셋을 붙인 채 ss 를 돌리자 UDP 서버는 UNCONN 한 줄이었고 UDP 클라이언트 셋은 connect 로 상대를 적어 ESTAB 이었다. "
          "TCP 서버는 LISTEN 한 줄과 연결마다 ESTAB 한 줄씩 넷이었고, 클라이언트 쪽 줄은 로컬과 상대를 뒤집은 한 쌍이었다.",
          "실험 3 의 ss -uanp · ss -tanp 출력을 프로세스별로 다시 묶었습니다.",
          [("프로세스", ""), ("Local", "주소:포트"), ("Peer", "주소:포트"), ("State", "")],
          [("UDP 서버", "pid 3860709", [
              ([("gonet-linux", None)], "fd 4", None),
              ([("*:8080", OK)], "", None),
              ([("*:*", None)], "상대 없음", None),
              ([("UNCONN", OK)], "", OK)]),
           ("UDP 클라이언트", "pid 3862514~16", [
              ([("gonet-linux ×3", None)], "", None),
              ([("[::1]:59141", None), ("[::1]:40496", None), ("[::1]:49540", None)], "", None),
              ([("[::1]:8080", ACC)], "connect 메모", ACC),
              ([("ESTAB", ACC)], "패킷 없이", ACC)]),
           ("TCP 서버", "pid 3861643", [
              ([("gonet-linux", None)], "fd 4 · 5 · 8 · 9", None),
              ([("*:9000", None), ("[::1]:9000 ×3", None)], "", None),
              ([("*:*", None), ("55602 · 55618", None), ("55626", None)], "", None),
              ([("LISTEN", None), ("ESTAB ×3", None)], "연결마다 1", None)]),
           ("TCP 클라이언트", "pid 3862523~27", [
              ([("gonet-linux ×3", None)], "", None),
              ([("[::1]:55602", None), ("[::1]:55618", None), ("[::1]:55626", None)], "", None),
              ([("[::1]:9000", None)], "", None),
              ([("ESTAB", None)], "handshake 뒤", None)])],
          lane_h=124,
          legend=[("모두가 함께 쓰는 UDP 서버 소켓", OK), ("이름만 같은 UDP ESTAB", ACC)])

flow_grid("02-03.measure-points.svg", "FLOW · 02-03 §4", "100 개가 가는 길에서 센 곳",
          "phase2-loss 가 번호 붙은 메시지 100 개를 보내면 lo 를 두 번 지나 돌아온다. 손실 20% 에서 UDP 는 가는 길에 22 개, 오는 길에 12 개를 잃어 "
          "서버 로그 78 줄, 클라이언트 66 개였고 TCP 는 재전송으로 100 개를 모두 받았다. 뒤바뀜만 건 실험 5 에서 UDP 는 100 개를 뒤섞인 채 "
          "받았고 TCP 는 순서를 맞춰 받았지만 불필요한 재전송을 10 번 했다.",
          "세는 곳은 셋입니다. 서버 로그 줄 수, 클라이언트 집계, 그리고 커널 카운터(nstat).",
          [("보냄", "phase2-loss"), ("가는 길", "lo · netem"), ("서버", ""), ("오는 길", "lo · netem"), ("받음", "phase2-loss")],
          [("실험 4 UDP", "loss 20%", [
              ([("100", None)], "", None),
              ([("22 사라짐", BAD)], "", None),
              ([("recv 78", None)], "로그 줄 수", None),
              ([("12 사라짐", BAD)], "", None),
              ([("66", ACC)], "missing 34", ACC)]),
           ("실험 4 TCP", "loss 20%", [
              ([("100", None)], "", None),
              ([("손실 → 재전송", ACC)], "", None),
              ([("100", None)], "", None),
              ([("손실 → 재전송", ACC)], "", None),
              ([("100", OK)], "461ms · 재전송 9", OK)]),
           ("실험 5 UDP", "reorder 25%", [
              ([("1 … 100", None)], "", None),
              ([("25% 곧바로", ACC)], "추월", None),
              ([("100", None)], "", None),
              ([("25% 곧바로", ACC)], "추월", None),
              ([("100", None)], "reordered 27", ACC)]),
           ("실험 5 TCP", "reorder 25%", [
              ([("1 … 100", None)], "", None),
              ([("25% 곧바로", ACC)], "", None),
              ([("100", None)], "", None),
              ([("25% 곧바로", ACC)], "", None),
              ([("100 순서대로", OK)], "헛재전송 10", BAD)])],
          lane_h=92,
          legend=[("netem 이 버린 것", BAD), ("netem 이 흔든 것", ACC), ("앱이 온전히 받은 것", OK)])
print("ok 02-03 maps")
