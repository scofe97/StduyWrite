---
topic: gonet-lab
scope: durable
level: 기본
last_verified: 2026-09-28
blocked_count: 3
next_lesson: "(1) 랩 Phase 2 UDP 의 Phase 4 복습 문답(2026-09-30 예정, 02-01~02-03 — 표적: RACK 조건 1 의 역할·재정렬 창 크기, SEQ=바이트, ReadFrom 한 데이터그램, A·B·C 는 요청 셋) (2) 랩 Phase 3 DNS Client 의 Phase 2 메타인지(03-01 읽고 가장 자신 없는 절) → Phase 3 실습(인코더·디코더, tcpdump -X 대조, 바이트 순서 뒤집기, TXT 로 TC 재현) (3) 문서 잔여: 00-02 시그널 표, 00-03 Go 문법 lgo 링크"
updated: 2026-09-29
---

# gonet-lab 학습 상태

## 미션 — 왜 이걸 배우는가

네트워크 장애 앞에서 애플리케이션 로그만 보지 않고, `ss`·`tcpdump`·`strace`·metric·eBPF 가운데 맞는 계층의 도구를 고를 수 있게 되는 것이 미션이다. 그러려면 Go 코드 한 줄이 goroutine, netpoller, epoll, 소켓, FD 로 어떻게 내려가는지 손으로 따라가 봐야 한다. 네트워크 프로그램 하나를 완성하는 것은 목표가 아니다.

## 진행 구조

랩 Phase 하나 = 학습 토픽 하나. 각 Phase 안을 4-Phase(개념 이해 → 학습 문서 → 실습 → 검증)로 돈다. 실습은 늘 정상 동작과 장애 주입이 짝이다. 코드는 `~/study/gonet-lab`, 로드맵은 그 저장소의 `docs/01-01.gonet-lab-roadmap.md`, Phase 상세 계획은 `docs/03-NN.gonet-lab-phase<N>-plan.md` 가 기준이다. Linux 관측은 OrbStack `ubuntu` 머신에서 한다. 이 폴더에는 Phase 별 학습 문서와 이 상태 파일만 둔다.

| 랩 Phase | 학습 문서 | 4-Phase 진행 | 검증일 |
|---|---|---|---|
| 0 Network CLI | [00-01](./00-01.listener%20%EC%86%8C%EC%BC%93%EA%B3%BC%20%EC%97%B0%EA%B2%B0%20%EC%86%8C%EC%BC%93.md) · [00-02](./00-02.strace%20%EC%99%80%20proc%20%EB%A1%9C%20%EC%9D%BD%EC%9D%80%20%EA%B2%83%20-%20%EC%8B%A4%EC%8A%B5%EC%97%90%EC%84%9C%20%EB%A7%8C%EB%82%9C%20syscall%C2%B7FD%C2%B7TCP%20%EC%83%81%ED%83%9C.md) · [00-03](./00-03.Go%20%EB%AC%B8%EB%B2%95%20-%20goroutine%C2%B7io.Copy%C2%B7context%C2%B7WaitGroup.md) (draft) | Phase 1·2 통과 2026-09-26, Phase 3 통과 2026-09-27, Phase 4 2026-09-28(부분 2) | |
| 1 TCP Echo / Chat | [01-01](./01-01.%EC%A1%B0%EC%9A%A9%ED%95%9C%20%EC%97%B0%EA%B2%B0%EC%9D%B4%20%EC%84%9C%EB%B2%84%EB%A5%BC%20%EB%A9%88%EC%B6%98%EB%8B%A4%20-%20goroutine%C2%B7FD%C2%B7idle%20timeout.md) (draft) | Phase 1 통과 2026-09-27, Phase 2 통과 2026-09-27(메타인지 자기 평가), Phase 3 통과 2026-09-28(실험 1~5, deadline 한 번 vs 매번 비교는 사용자 선택으로 미실행), 01-01 반영 완료 2026-09-28, Phase 4 2026-09-28(설명 3) | |
| 2 UDP | [02-01](./02-01.%EA%B2%BD%EA%B3%84%EB%A5%BC%20%EC%A7%80%ED%82%A4%EB%8A%94%20UDP%2C%20%EB%8C%80%EC%8B%A0%20%EB%96%A0%EC%95%88%EB%8A%94%20%EA%B2%83%20-%20%EB%8D%B0%EC%9D%B4%ED%84%B0%EA%B7%B8%EB%9E%A8%C2%B7%EC%86%90%EC%8B%A4%C2%B7%EC%88%9C%EC%84%9C.md) (draft) | Phase 1 통과 2026-09-28(소크라테스 Q1~Q5-2), Phase 2 통과 2026-09-29(메타인지: "RACK 이 가장 어려움, 나머지는 괜찮음"), Phase 3 통과 2026-09-29(실험 1~5), 02-01 실측 반영 + 02-02(손실 판정)·02-03(실습 기록) 신규 2026-09-29, Phase 4 는 사용자 요청으로 2026-09-30 로 연기 | |
| 3 DNS Client | [03-01](./03-01.DNS%20%EC%A7%88%EC%9D%98%20%ED%95%9C%20%EC%9E%A5%EC%9D%84%20%EB%B0%94%EC%9D%B4%ED%8A%B8%EB%A1%9C%20-%20%ED%97%A4%EB%8D%94%C2%B7%EB%9D%BC%EB%B2%A8%C2%B7%EC%95%95%EC%B6%95%20%ED%8F%AC%EC%9D%B8%ED%84%B0%C2%B7TC.md) (draft) | Phase 1 통과 2026-09-29(소크라테스 Q1~Q9), Phase 2 문서 작성 2026-09-29 · 메타인지 대기 | |
| 4 Port Scanner | | | |
| 5 TCP Proxy | | | |
| 6 SOCKS5 Proxy | | | |
| 7 HTTP CONNECT | | | |
| 8 Reverse Tunnel | | | |
| 9 Stream Multiplexing | | | |
| 10 Discovery | | | |
| 11 P2P Overlay | | | |
| 12 Mini DHT | | | |
| 13 Failure / Chaos | | | |
| 14 Observability | | | |
| 15 eBPF Observer | | | |

## 현재 난이도 레벨

기본. Go 로 netpath-lab 1국면(DNS·TCP·HTTP 측정)을 짰고 `errors.Is`·`context`·`httptrace` 는 써 봤다. 서버 쪽 소켓 수명, netpoller, half-close 는 아직 직접 다뤄 보지 않았다.

## 이해 근거 (선택)

- 2026-09-26 Phase 1 (소크라테스 Q1~Q9, 평가 아님 — last_verified 미이동)
  - 독립 응답으로 도달: 서버 쪽 소켓 수 = listener 1 + 접속당 1 (Q1), 4-tuple 로 데이터 패킷은 연결 소켓·SYN 은 listener 로 (Q2), 연결 소켓끼리 local 이 같아도 remote 로 갈려 충돌 없음 (Q7), 접속당 소켓·FD 의 대가 = FD 고갈·커널 자원, UDP 는 단일 소켓 (Q8)
  - 힌트 뒤 도달: 검색에 필요한 건 local 주소 (Q3), 연결 소켓의 remote = 클라이언트 주소 (Q6, 힌트 2회), listener 에 `->` 가 없는 이유 = remote 미정 (Q9)
  - 설명(도움) 받음: `listen()` 의 역할·accept queue·backlog (Q4), `bind()` 의 역할·EADDRINUSE, remote 가 handshake 중 채워지는 시점, FD 는 `socket()` 과 `accept()` 두 곳에서 생김 (Q9), `ss` 출력 읽기
  - AI 가 덧붙인 내용(학습자 도출 아님): accept queue 에는 FD 없는 소켓이 줄 선다, UDP 는 연결 상태를 앱이 든다, LISTEN 줄의 Recv-Q/Send-Q = 대기열 길이/backlog
- 2026-09-29 랩 Phase 3 DNS Client Phase 1 (소크라테스 Q1~Q9, 평가 아님 — last_verified 미이동). 독립 응답: 구분값 방식의 문제 = 이름 안에 구분값이 섞이면 끊김(Q2·Q2 힌트), 고정 길이 필드는 길이 접두사가 필요 없음(Q5), 짝을 맞추려면 페이로드에 식별 정보가 필요·응답에 질문(도메인)을 담고 클라이언트가 기억(Q6·Q7), RD 는 플래그(Q9). 힌트 뒤 도달: 질의에 담을 두 조각 = 이름·타입(Q1, 첫 답은 서버 쪽 재귀 동작), 타입은 목록 번호(Q4, "플래그"라 부름 → 코드와 구분 교정). 설명(도움받은 응답): 길이 접두사 값 세기(9 → 10 → 11, 두 번 틀림), 타입 코드 A=1·MX=15·AAAA=28 2바이트, 체크섬은 위조 방지가 아님·DTLS/DoQ/DoT/DoH/DNSSEC, 무작위 ID 16비트 + 무작위 출발지 포트(RFC 5452)로 경로 밖 위조를 막음(Q8 "모르겠음"), 경로 위·밖 구분(엽서 비유 뒤 재진술 맞음), RD 는 1비트·서버가 직접 끝까지 물어 옴("다시 쏴 준다"로 오해). 재진술: 대조할 값 = ID(스스로) + 질문(상기 뒤). 미다룸(Phase 2 문서·Phase 3 실측으로): 실제 이름 인코딩(라벨 단위 길이 + 0), 헤더 12바이트(플래그·개수 필드), class IN, 네트워크 바이트 순서(빅엔디언), 응답의 이름 압축 포인터

## 막힌 지점
- 2026-09-28~29 랩 Phase 2 UDP Phase 3 (실험 1~5, 코드 internal/udp·cmd udp-listen/udp-send·experiments/phase2-loss 는 AI 작성, 실행은 학습자). 예측 제출 방식: 실험 1·2·4(재)·5 는 예측을 결과와 함께 제출, 실험 2 는 실행 전 예측, 실험 3·4(첫) 은 예측 없음
  - 실험 1 경계 보존 r=5·5, local 포트 = 서버 from 포트: 예측 일치. "서버가 정한 포트" 오해 → 클라이언트 커널이 붙인다로 교정
  - 실험 2 버퍼 3: hel→wor, 에러 없음: 실행 전 예측 4 개 모두 일치
  - 실험 3 ss: UDP 서버 UNCONN 1, TCP LISTEN 1 + ESTAB 3 — 학습자가 개수 해석(UDP 1+3, TCP 4+3). UDP 클라이언트 ESTAB 은 "connect 때 주입?"까지 도달, 나머지(패킷 없는 connect, sk_state=TCP_ESTABLISHED)는 설명(도움받은 응답). 첫 시도는 30s 안에 ss 못 봐 60s 로 재시도
  - 실험 4 loss 20%: 첫 회 UDP 58/TCP 100(280→498ms). echo 두 번 통과·netem·missing 은 설명(도움받은 응답). 재실험: 예측 100→80→64 일치(실측 78·66), 빠른 재전송 우세 예측 일치(FastRetrans 6, Timeouts 2, LossProbes 2, RetransSegs 9)
  - 실험 5 reorder: 예측 4 개(missing 0, reorder≈25%, TCP 0, 손실 없이도 빠른 재전송 가능) 모두 일치(실측 reordered 27, FastRetrans 10, OutSegs 262). 추월 수 해석은 절반 도달("제한 없음, 3 개부터"), 나머지(10ms/1ms, 25%, 상관도)는 설명
  - AI 설명 정정(2026-09-29): 실험 4·5 해석에서 "중복 ACK 셋 → 빠른 재전송"이라 했으나 이 커널(7.0.14)은 RACK 판정(옛 dupthresh 코드는 2025-06 제거), 셋은 RACK 안의 첫 방아쇠로 남음 → 02-02 에 정리, 학습자에게 전달 예정
  - 미확인 가설: 손실 중 메시지 합쳐짐(세그먼트 수), 실험 5 불필요 재전송의 DSACK 경로
  - 2026-09-29 문서 확인 질문 "문턱과 RACK 은 무엇이 다른가" 첫 자답(부분): 문턱 = "몇 번 손실된 이후 데이터가 왔냐"(세는 대상이 손실 횟수로 어긋남 — 실제는 빈자리 뒤 도착 수·중복 ACK 수), RACK = "최근 응답 손실"까지, 두 조건은 문서로 이해. 힌트 뒤 재답: 문턱 = "손실된 것보다 큰 값이 도착했을 때"(맞음, 힌트 뒤 도달). RACK = 기준은 "가장 최근 도착 세그먼트"까지 도달, "먼저 보냈는데 확인 안 됨 = 늦게 도착"으로 결론 어긋남 → 정의 문장 설명(도움받은 응답), 재진술 대기. 재답 2: "문턱은 몇 번 넘어서 패킷을 보냈는지, RACK 은 시간으로 기다린다는데 흐름을 잘 모르겠음 — RACK 이 가장 어려움"(Phase 2 메타인지 자기 평가로 기록: 02-02 §3 RACK 이 가장 자신 없음). 문턱 세는 대상 재교정(보낸 수가 아니라 빈자리 뒤 도착 수), 시각표 설명(도움받은 응답) + 02-02 §3 에 rack-timeline 도식·두 단락 추가. 재답 3: "뒤의 세그먼트가 도착하고"(조건 1 맞음), 조건 2 의 뜻은 질문 → 마감 시각(보낸 시각 + 추정 RTT + 재정렬 창)·택배 비유로 설명(도움받은 응답), 빈칸 재진술 요청. 재진술: "하루 + 반나절 기다렸는데 분실로 판단 → 절반?"(마감 부분은 스스로, 조건 1 누락, 여유를 RTT 절반으로 오해) → 여유는 min_RTT/4 에서 시작해 DSACK 으로 넓어짐, 조건 1 이 있어야 RTO 보다 짧은 마감을 걸 수 있음을 설명(도움받은 응답). Phase 4 표적: RACK 조건 1 의 역할, 재정렬 창 크기 이어서 SACK 개념·양방향 ACK 질문 → 설명, ack-segments 도식을 서버 번호 501 부터로 다시 그림. 또 "A·B·C 가 한 요청-응답을 나눈 것"으로 오해 → 요청 셋·응답 조각 구분으로 교정, 도식 보강
  - AI 설명 정정 2(02-02 사실 검증, 2026-09-29): (1) 실험 5 추월 모양을 "늦춘 1 개를 뒤 패킷 여럿이 추월, 평균 2~3"이라 했으나 netem 은 75% 를 늦추고 25% 를 곧바로 보내므로 곧바로 나간 1 개가 앞의 늦춰진 여럿을 앞지름 (2) TcpOutSegs 262 에 재전송 10 이 들어 있다고 했으나 Linux OutSegs 는 재전송을 세지 않음(ACK·SYN·FIN 포함). 학습자에게 정정 전달
- 2026-09-28 랩 Phase 2 UDP Phase 1 (소크라테스, 평가 아님 — last_verified 미이동). 독립 응답: Read 가 buf 에 채운 바이트 수 = r, 수신 버퍼 두 Write 도착 시 r=10, 커널은 Write 경계를 모름, r=7(hello+wo), 프레이밍에 구분값 필요·구분값이 본문에 섞이면 쪼개짐, UDP 는 길이 칸으로 경계·잘리면 나머지 버림, UDP 서버 소켓 1개(이유: TCP 는 상대별 상태), UDP 떠남은 타이머로 판단, 손실 10개 중 2개면 8번 반환·커널은 모름, 본문 번호로 앱이 빈자리 앎, 순서는 도착순, 늦은 4 버리기 전략 제시, 클라이언트 소켓의 주소가 ReadFrom 주소, 신뢰성 고정(TCP) vs 앱 선택(UDP). 힌트 뒤: UDP ReadFrom 은 데이터그램 하나씩(첫 자답 “5 또는 10” → 발신자 주소 힌트로 도달), 길이 접두(본문 길이), 재정렬 버퍼(5 를 임시 보관). 교정: SEQ 는 바이트 번호(“패킷에 붙는 값” 오해), SYN≠SEQ, 클라이언트도 UDP 소켓 필요, “속도가 훨씬 빠르다”는 미측정.
  - AI 가 덧붙인 내용(학습자 도출 아님): ISN, HOL 블로킹, 수신 윈도·흐름 제어, 중복 ACK, UDP 헤더 8바이트, conntrack udp timeout, QUIC 비교표, Go ReadFrom 잘림 무에러(미측정 — Phase 3 확인)
  - 2026-09-28 Phase 2 중 질문: "중복 ACK 는 무슨 말인가" → 누적 ACK 번호 표로 설명(도움받은 응답). 02-01 §4 에 같은 표와 HTTP/1.1·2·3 HOL 절, §1·§3 도식 추가 요청 반영
  - AI 설명 정정(02-01 사실 검증, 2026-09-28): Phase 1 에서 "같은 ACK 가 세 번 겹치면 재전송"이라 했으나 정확히는 중복 ACK 세 번 더(같은 ACK 네 번). 1~6 에서 4 손실이면 중복 ACK 둘뿐이라 빠른 재전송이 아니라 타이머·RACK 로 복구. 학습자에게 정정 전달함
- 2026-09-28 랩 Phase 1 Phase 4 (6문항, blocked_count 3 = 힌트 뒤에도 설명으로 채운 축). 첫 자답 통과: Q1 스레드를 쥐는 쪽은 [syscall](이유 포함), Q2 연결당 FD 3→1·splice vs 버퍼, Q3 connect 성공·FD 없음, Q4 CLOSED 는 close() 없이도 됨·FD 는 close() 로만 반납, Q5 (a) busy loop CPU (b) 일시 에러에 영구 종료 (c) 2배 backoff 최대 1s, Q6-1 io.Copy 인자 방향(Phase 0·3 에서 두 번 막혔던 축 해소). 힌트 뒤: Q1 IO wait 예(소켓 io.Copy), Q3 위치 = LISTEN Recv-Q(accept 대기열), Q4 판별은 /proc fd 쪽, Q5 net.ErrClosed = 우리가 ln.Close 한 것(‘상대가 닫음’ 오해 재발 → 힌트로 도달), Q6-2 소켓을 Read 하는 쪽이 EOF 로 먼저 앎. 설명으로 채움(막힌 축 3): Q1 [syscall] 예 = stdin 읽기(재진술: 기준은 어디서 읽느냐), Q3 대기열 연결의 상태 = ESTABLISHED(‘closed’ 로 답함), Q4 누수 판별은 /proc fd 소켓 수 vs ss -p 연결 수 비교 + ‘EMFILE 로 연결이 끝난다’ 오해 교정 → _review/_queue.md gonet ph1 대기
- 2026-09-28 랩 Phase 0 Phase 4 (5문항). 첫 자답 통과: Q1 FD 번호는 프로세스별, Q4 CLOSE-WAIT(FIN 받은 쪽, close 대기)·TIME-WAIT(먼저 닫은 쪽, 늦은 패킷 대비), Q5 서버 연결 소켓 local=10.0.0.1:8080·peer=클라이언트, 도착 패킷 목적지=local. 부분: Q2 Ctrl-C 경로(AfterFunc Close → strace close)는 첫 자답, kill -9 는 '안 닫힌다' → 힌트 뒤 '강제 반납', 정리 주체가 커널이고 strace 에 안 찍히는 이유는 설명(init 이 정리한다고 오해) → 재진술로 strace 부분 확인. Q3 결론(wg.Wait 에서 안 끝남) 첫 자답, wg.Done 대기·io.Copy 정지는 힌트 뒤, io.Copy 가 끝나지 않는 이유(연결 소켓 미close·EOF 없음)는 설명. → _review/_queue.md gonet ph0 대기
- 2026-09-28 랩 Phase 1 Phase 3 실험 1(client goroutine 덤프, 평가 아님). 예측: 이름표는 goroutine 이름, 스레드는 모름. 결과: main [chan receive] m=nil, 읽기 [IO wait] m=nil, stdin [syscall] m=2, 런타임 시그널 goroutine [syscall] m=5. 스스로 해석: m= 에 숫자가 있는 stdin goroutine 만 스레드를 쥔다, 읽기는 서버가 보낼 때까지 대기라 IO wait. 힌트 뒤: 보내는 순간엔 stdin 이 아니라 소켓에 쓰는 중. 설명 받음: 이름표는 멈추는 순간 런타임 함수(gopark)가 붙인다("첫 기능 매칭"으로 오해), 쓰기 이름표는 없고 버퍼가 차면 IO wait, SIGQUIT·시그널 표, 레지스터 출력, 스택은 아래→위가 호출 순서, "해 보고 못 하면 멈춘다"
- 막힌 축 (실험 1 코드 읽기): make(chan error, 1) 을 바이트 배열로 읽음, io.Copy(out, conn) 방향을 반대로 읽음(Phase 0 에 이어 두 번째), <-readDone 을 컨텍스트 대기로 읽음, 타입 단언 conn.(*net.TCPConn) 모름 → 설명
- 2026-09-28 실험 2 해석·실험 3~5(평가 아님, 막힘 기록용)
  - 스스로 도달: 연결당 FD 3(소켓+pipe 2), io.Copy(conn,conn)=in→out, m=nil 이면 스레드 없음, 스레드 수는 연결 수와 무관(예측 적중), Go 가 soft 를 올림, Recv-Q=accept 못 한 연결, pipe 36=18 연결, 클라이언트는 handshake 만으로 성공, wg.Wait 가 io.Copy 에 묶여 로그까지 못 감(Phase 1 에선 설명 받았던 사슬), 37=7+30, pipe 는 io.Copy 가 만듦, CLOSE-WAIT=close 안 한 쪽, idle-clients 는 ctx.Done 뒤에만 Close, 일시적 에러는 쉬었다 재시도, 대기열 13 개도 결국 받음
  - 힌트 뒤: 연결당 FD 3 의 뜻(수용 1/3), +1 은 listener 대기 goroutine, busy loop(초당 수많은 호출·로그)
  - 설명 받음: pipe·splice·두 차선, G·M·P, netpoller 는 런타임 안(커널 장치로 오해), 셸 한도≠서버 한도(셸 값을 서버 값으로 오해), hard−1·prlimit, ESTABLISHED≠accept, CLOSED≠close(), FIN-WAIT-2 60s→keepalive→RST, net.ErrClosed 는 우리 쪽이 닫았다는 뜻(상대가 닫았다로 오해), FD 를 푼 것은 idle timeout(Write 의 EOF 로 오해), 27 의 계산, accept 에러 종류, 1s 는 정해 둔 천장
  - 막힌 축: 이름표를 함수 이름으로 예측(실험 1·4 두 번), io.Copy 방향, 자기 쪽 vs 상대 쪽 구분(ErrClosed·셸/서버·양측 close), 과정 실수(클라이언트 pid 측정, 자리표시자 붙여넣기, 예측 생략 1회)
- 2026-09-28 실험 2(평가 아님). 예측: FD = 0~2 + 연결 수(100 개면 103), 스레드는 1,000 까지 안 늘어남. 첫 측정 106·1006 / Threads 8 은 idle-clients 의 pid 를 잰 것(ps 로 확정). 서버 재측정(연결 100): FD 307 = socket 101 + pipe 200 + anon_inode 2 + cgroup cpu.max 1 + 0~2, Threads 11. pipe 는 "모르겠음" → 설명(io.Copy(conn,conn) → spliceFrom → poll.Splice 가 연결마다 pipe 하나를 EOF 까지 쥠). 해석 두 개는 미응답
- 2026-09-27 랩 Phase 1 Phase 2 메타인지 체크(학습자 자기 평가): "전반적인 내용은 모두 이해했다" — 통과. 추가 질문 두 개(EAGAIN 말고 goroutine 의 기다림을 가르는 말, EAGAIN 없이 스레드가 막히는 때)는 설명으로 답함(도움받은 응답) → 01-01 §1 의 두 ### 와 experiments/phase1-two-waits 로 반영. 이 두 주제는 Phase 4 표적에 넣는다
- 2026-09-27 랩 Phase 1 Q4~Q6 (평가 아님): 끊을 곳 = io.Copy 의 Read(힌트 뒤), 기준 = 일정 시간 무응답(독립), 트레이드오프 짧음/긺(독립). SetReadDeadline 이 절대 시각이라 매번 미뤄야 idle timeout 이 된다는 점은 설명으로 채움. 역방향 설명(Q6): 뼈대 독립, "에러 로그 없음"은 wg.Wait 로 스스로 설명, "시간 초과"는 FD 부족 때문에 패킷을 버린다고 봄 → 실제는 listener 가 열려 있어 accept 대기열이 차고 SYN 이 버려짐(설명으로 교정). 막힌 축: defer 가 도는 함수와 wg.Wait 의 인과 방향을 뒤집음, 서버 쪽 io.Copy 위치
- 2026-09-27 랩 Phase 1 개념 이해 (평가 아님): Q1 "OS 스레드는 훨씬 적다" 방향 맞음(독립) — 근거가 "goroutine 은 유저 스레드"에 머물러, 기다리는 goroutine 이 스레드를 붙잡는지(런타임이 아는 기다림 vs 커널 안 blocking syscall)는 설명 후 이해. Q2 "다른 스레드가 이어받는다"(설명 뒤). Q3 EMFILE 뒤 서버 상태 — FD 할당 실패와 goroutine 을 섞음, Accept 루프가 Accept 에서 멈춘다는 것·goroutine 등록 시점·WaitGroup 은 세기만 한다는 전제를 설명으로 채움. 막힌 축: goroutine 스케줄링 기초(돌고 있음/기다림), 반복문이 Accept 에서 멈추는 구조
- 2026-09-27 Phase 3 메타인지 체크(학습자 자기 설명): "FD 를 만드는 syscall 은 socket 과 accept, 클라이언트가 먼저 끝내면 그 연결 소켓을, 서버를 끄면 연결 소켓 전체와 리슨 소켓을 닫는다" — 통과. 누가(어느 코드가) 닫는지는 말하지 않았으므로 Phase 4 에서 확인
- 2026-09-27 Phase 3 실험(평가 아님, 막힘 기록용). 예측 대조: 실험1 같은 FD(맞음), 1-C 새 FD=5(맞음, 근거는 "순차"), 2 LISTEN1·ESTAB4(맞음, TIME-WAIT·FD 10 은 예상 밖), 3 서버가 close(4) 예측 → 실제 close(5)(틀림), 4 close 4·10(번호 맞음, 근거는 "프로세스 종료" → 실제는 코드 Close), 5 listener 만 close(맞음)·FIN-WAIT-2 예측 → 실제 ESTAB(틀림)
- 막힌 축 (Phase 3): FD 번호가 프로세스마다 따로라는 것(실험3, 힌트 뒤에도 "모르겠음" → 설명 후 재진술), 코드 Close 와 프로세스 종료 정리의 구분(실험4 예측 근거), CLOSE-WAIT 를 2MSL 대기로 혼동(TIME-WAIT 와 섞음), io.Copy 가 src 의 EOF/에러까지 기다리므로 핸들러가 wg.Done 에 못 가는 사슬(실험5 "모르겠음" → 설명), goroutine·메인 goroutine·io.Copy(dst, src) 인자 방향 기초
- 스스로 도달 (Phase 3): "가장 작은 빈 번호" 규칙 판정(실험3), strace 의 close 가 shutdown 로그보다 먼저 → 코드가 부른 close(실험4), close 를 안 했으니 FIN 없음 → ESTAB(실험5)
- 2026-09-26 Phase 2 메타인지 체크(학습자 자기 평가): `socket → bind → listen`, `accept` 흐름은 설명 가능하다고 답함. 00-01 §3(두 소켓의 수명, conns 루프)은 자기 설명 가능 여부를 밝히지 않음 — Phase 3 종료 경로 실험과 Phase 4 에서 확인할 것

- 2026-09-26 Phase 1 (평가 아님, 막힘 기록용): 9문항 중 설명으로 넘어간 문항 1 (Q4 `listen()` 이 알리는 "역할")
- local/remote 를 패킷 기준(출발지·목적지)과 소켓 기준으로 섞어 씀 — Q3·Q6 에서 반복, 힌트로 교정
- FD 는 `accept()` 에서만 생긴다고 봄, syscall 순서를 `bind → socket → listen` 으로 적음 (Q9 독립 응답) — 설명 후 재진술에서 순서는 교정
- 재진술에서 "리슨 소켓"과 "연결 소켓" 이름이 뒤바뀜 — 확인 질문(fd=6 은 socket(), fd=7 은 연결 소켓)에서 바로 교정. Phase 4 에서 도움 없이 다시 확인할 것

## 미해결 질문

- 실험 4 미니 실험에서 몇 시간 방치된 CLOSE-WAIT 클라이언트가 첫 write 에 곧바로 EPIPE 를 냈다. Go Dialer 기본 TCP keepalive 가 먼저 상대 부재를 알아챘다는 추정(AI 추정, 미확인). Phase 1 에서 확인.
- ~~서버 프로세스 FD 8·9·11·12 의 pipe 두 쌍은 누가 만드는가~~ — 해결(2026-09-28 실험 2): echo 핸들러 io.Copy(conn, conn) 의 splice 가 연결마다 pipe 하나(FD 2)를 EOF 까지 쥔다. go1.25.1 internal/poll/splice_linux.go Splice·getPipe. strace 로 pipe2 는 아직 미확인
- (2026-09-28 01-01 에 반영 완료, 남은 것은 00-02 시그널 표와 00-03 lgo 링크) 01-01 보강 목록: 연결당 FD 3→1(splice 유무), 두 차선·pipe 유무 도식, splice vs 버퍼 복사 표, accept 에러 종류 표·재시도 범위 트레이드오프, G·M·P 한 줄, CLOSED≠close()·FD 누수 판별(/proc fd vs ss -p), FIN-WAIT-2→keepalive→RST, 00-03·01-01 Go 문법을 lgo 12~14장 링크로, 시그널 표(00-02)
- Phase 0 미해결 "CLOSE-WAIT 클라이언트의 즉시 EPIPE" — 실험 5 관찰(서버 FIN-WAIT-2 60s 만료 뒤 keepalive 에 RST)로 뒷받침, 패킷 캡처는 미실행

- OrbStack 커널(7.0.14-orbstack)이 eBPF kprobe·tracepoint·BTF 를 어디까지 지원하는가. Phase 15 직전에 `bpftool feature` 로 확인한다.
- ~~`tc netem` 을 OrbStack 머신의 `lo` 에 걸 수 있는가~~ → 해결 2026-09-28: 커널 7.0.14-orbstack, `CONFIG_NET_SCH_NETEM=m`, sch_netem 로드됨, `tc` 있음(실제 qdisc 적용은 Phase 3 에서)

## 다음 레슨 후보 + 고른 이유

- Phase 0 학습 문서(Phase 2) → 실습(Phase 3, `ss`·`strace` 로 FD 6/7/8 과 syscall 순서 직접 확인) → 검증(Phase 4). 원래 이유: 코드는 이미 돌지만, `lsof` 에 LISTEN 소켓과 ESTABLISHED 소켓이 FD 번호를 따로 받는 이유를 설명하지 못하면 Phase 1 의 "접속 1,000 개에서 먼저 바닥나는 자원" 질문에 답할 수 없다.

## 물어볼 곳

- Go 표준 라이브러리 `net` 패키지 문서 (https://pkg.go.dev/net) — Listener·Conn·Dialer 동작이 기대와 다를 때.
- Linux man pages `socket(7)`, `tcp(7)`, `epoll(7)` (https://man7.org/linux/man-pages/) — syscall 과 소켓 옵션.
