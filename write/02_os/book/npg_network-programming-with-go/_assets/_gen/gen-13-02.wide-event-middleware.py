# 타입 스펙: type-sequence
# 사실 출처: NPG Ch.13 Wide Event Logging Listing 13-15~13-17, net/http
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, MUTED, SOFT, ACC, OK, WARN, INFO, MONO, KR

W, H = 980, 720
s = Seq(W, H, "SEQUENCE · WIDE EVENT MIDDLEWARE",
        "요청 계측부터 단일 구조화 와이드 이벤트 로그 기록까지",
        "미들웨어가 ResponseWriter 를 감싸 상태 코드와 길이를 기록하고, 핸들러가 끝난 뒤 필드를 모아 한 줄의 로그를 작성합니다.",
        lead="트랜잭션 전체를 포괄하는 필드를 단일 레코드에 집약해 로그 조각맞춤을 없앱니다.")

s.lanes([("클라이언트", "http.Client"),
         ("미들웨어", "WideEventLog"),
         ("감싼 라이터", "wideResponseWriter"),
         ("핸들러", "http.Handler"),
         ("로거", "zap.Logger")], y0=104, lane_w=140)

def selfmsg_left(s, a, label, y, c=MUTED, sub=None):
    x = s.LX[a]
    s.path(f"M {x-10} {y-10} L {x-58} {y-10} L {x-58} {y+10} L {x-13} {y+10}", c, 1.4, m="ar")
    s.t(x - 68, y - 4, label, 11, c, MONO, "end")
    if sub:
        s.t(x - 68, y + 13, sub, 11, MUTED, KR, "end")

# 1. 클라이언트 요청 전송
s.msg("클라이언트", "미들웨어", "GET /test", 175, INFO, "info", sub="HTTP/1.1 요청 인입")

# 2. ResponseWriter 래핑
s.msg("미들웨어", "감싼 라이터", "&wideResponseWriter{w}", 230, INFO, "info", sub="status · length 수집 준비")

# 3. 다음 핸들러로 위임
s.msg("미들웨어", "핸들러", "ServeHTTP(wideWriter, r)", 285, OK, "ok", sub="비즈니스 로직 실행")

# 4. 핸들러 본문 쓰기
s.msg("핸들러", "감싼 라이터", "Write([]byte(\"Hello!\"))", 340, OK, "ok", sub="응답 본문 출력")

# 5. 상태 코드 및 바이트 수 내부 기억
s.selfmsg("감싼 라이터", "status=200, length=6", 395, OK, sub="초기 쓰기 시 200 설정")

# 6. 핸들러 복귀
s.msg("핸들러", "미들웨어", "핸들러 처리 완료", 450, SOFT, "soft", sub="제어가 미들웨어로 반환")

# 7. 단일 와이드 이벤트 로깅 요청
s.msg("미들웨어", "로거", "logger.Info(\"wide event\")", 505, ACC, "acc", sub="메서드·URI·상태·길이 수집")

# 8. 구조화 로그 1줄 출력
selfmsg_left(s, "로거", "단일 JSON 레코드 출력", 560, ACC,
             sub='{"status_code":200,"response_length":6,...}')

# 9. 클라이언트에 응답 완료
s.msg("미들웨어", "클라이언트", "200 OK (6 bytes)", 615, OK, "ok", sub="트랜잭션 정상 종료")

s.rails(640)
s.legend(665, [("요청 및 래핑", INFO), ("핸들러 계측", OK), ("와이드 이벤트 출력", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-02.wide-event-middleware.svg"
s.save(str(svg_path))
print("ok 13-02 wide-event-middleware")
