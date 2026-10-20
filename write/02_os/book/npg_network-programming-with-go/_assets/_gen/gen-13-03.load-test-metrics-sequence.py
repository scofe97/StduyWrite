# 타입 스펙: type-sequence
# 사실 출처: NPG Ch.13 Load Testing & Output (Listing 13-28~13-30), 실제 50,000회 실행 측정 결과
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, MUTED, SOFT, ACC, OK, WARN, INFO, MONO, KR

W, H = 960, 560
s = Seq(W, H, "SEQUENCE · LOAD TEST & SCRAPE",
        "부하 발생 클라이언트와 메트릭 스크랩 수집 순서",
        "클라이언트 500개가 100회씩 요청하고 테스트가 메트릭 엔드포인트에서 실제 측정값을 읽습니다",
        lead="직접 돌린 측정값: web_server1_open_connections 500, web_server1_request_count 50000")

s.lanes([("클라이언트 500개", "독립 커넥션 풀"),
         ("앱 서버 (:8082)", "helloHandler"),
         ("메트릭 저장소", "client_golang 기본 레지스트리"),
         ("테스트 러너", "GET :8081/metrics")], y0=104, lane_w=180)

# 1. 500개 클라이언트 연결 수립
s.msg("클라이언트 500개", "앱 서버 (:8082)", "TCP 연결 수립 (500개 소켓)", 166, INFO, "info",
      sub="StateNew 이벤트 500회 발생")

# 2. 게이지 갱신
s.msg("앱 서버 (:8082)", "메트릭 저장소", "OpenConnections.Add(1)", 218, OK, "ok",
      sub="open_connections 500 도달")

# 3. 100회 GET 요청 반복 (총 50,000회)
s.msg("클라이언트 500개", "앱 서버 (:8082)", "GET / (500 x 100 = 50,000회)", 270, ACC, "acc",
      sub="독립 커넥션 풀로 HTTP 요청 전송")

# 4. 요청 수 및 지연시간 누적
s.msg("앱 서버 (:8082)", "메트릭 저장소", "Requests.Add(1) · Observe(s)", 322, ACC, "acc",
      sub="request_count 50000 및 버킷 누적")

# 5. 본문 소진 및 연결 풀 유지
s.selfmsg("클라이언트 500개", "소켓 재사용 대기", 374, INFO,
          sub="io.Copy(io.Discard) + Close()")

# 6. 메트릭 스크랩 요청
s.msg("테스트 러너", "메트릭 저장소", "GET :8081/metrics", 426, OK, "ok",
      sub="접두사 web_server1_ 메트릭 조회")

# 7. 스크랩 응답 반환
s.msg("메트릭 저장소", "테스트 러너", "메트릭 텍스트 반환", 478, OK, "ok",
      sub="open_conn 500 · req_count 50000")

s.rails(496)
s.legend(518, [("연결 수명주기 감지", INFO), ("부하 요청 및 메트릭 기록", ACC), ("스크랩 검증 통과", OK)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-03.load-test-metrics-sequence.svg"
s.save(str(svg_path))
print("ok 13-03 load-test-metrics-sequence")
