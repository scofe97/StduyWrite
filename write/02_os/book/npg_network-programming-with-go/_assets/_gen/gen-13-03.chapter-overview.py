# 타입 스펙: type-process
# 사실 출처: NPG Ch.13 Instrumenting Your Code ~ Instrumenting a Basic HTTP Server, Go kit metrics, Prometheus client_golang
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 116
W, H = 984, 750

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

def nx(j):
    return COL_X + j * STRIDE

def ny(i):
    return ROW_Y + i * ROW_STRIDE

d = D(W, H, "PROCESS · 13-03 OVERVIEW",
      "Go kit 메트릭 추상화와 Prometheus 계측 서버",
      "13-03 의 5개 절 핵심 흐름입니다. "
      "§1 은 백엔드 교체를 지원하는 Go kit metrics 인터페이스와 프로메테우스 어댑터 연동입니다. "
      "§2 는 단조 증가하는 카운터와 오르내리는 게이지의 분담입니다. "
      "§3 은 고정 버킷 히스토그램과 클라이언트 계산 서머리의 차이입니다. "
      "§4 는 비즈니스 핸들러와 메트릭 노출을 다른 포트로 격리하는 이중 HTTP 서버입니다. "
      "§5 는 부하 환경에서 전송 계층 복제와 메트릭 덤프 검증입니다.",
      lead="화살표는 단계별 제어 흐름, 왼쪽 칩은 해당 절입니다.")

def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, kr(sub), "middle")

def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 11, c if c != SOFT else MUTED, kr(label), "middle", 600)

for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1 메트릭 추상화
node(0, 0, "Go kit 인터페이스", "metrics.Counter · Gauge", INFO)
node(0, 1, "Prometheus 어댑터", "NewCounterFrom · Opts", OK)
node(0, 2, "메트릭 엔드포인트", "promhttp.Handler() 노출", ACC)
harrow(0, 0, "백엔드 결합 분리")
harrow(0, 1, "레지스트리 등록", ACC, "acc")

# §2 카운터와 게이지
node(1, 0, "누적 카운터", "Requests.Add(1)", INFO)
node(1, 1, "연결 상태 감지", "ConnState 이벤트 수신", OK)
node(1, 2, "오르내림 게이지", "OpenConnections.Add(±1)", ACC)
harrow(1, 0, "단조 증가 기록")
harrow(1, 1, "연결 증감 반영", ACC, "acc")

# §3 히스토그램과 서머리
node(2, 0, "버킷 경계 설정", "[]float64{1e-7, ...}", INFO)
node(2, 1, "관측값 버킷 누적", "Observe(seconds)", OK)
node(2, 2, "서버 측 집계", "histogram_quantile 계산", ACC)
harrow(2, 0, "구간별 빈도 분류")
harrow(2, 1, "인스턴스 합산 가능", ACC, "acc")

# §4 이중 포트 서버
node(3, 0, "앱 서버 (:8082)", "helloHandler 계측", INFO)
node(3, 1, "연결 훅 등록", "Server.ConnState", OK)
node(3, 2, "메트릭 서버 (:8081)", "내부망 스크랩 격리", ACC)
harrow(3, 0, "요청 수명주기 감시")
harrow(3, 1, "관리 포트 분리", ACC, "acc")

# §5 부하 시험과 검증
node(4, 0, "클라이언트 500개", "DefaultTransport 복제", INFO)
node(4, 1, "100회 요청 전송", "소켓 500개 재사용", OK)
node(4, 2, "스크랩 출력 확인", "카운터 50000 도달", ACC)
harrow(4, 0, "독립 커넥션 풀 유지")
harrow(4, 1, "전송 완료 대기", ACC, "acc")

d.legend(690, [("설정·입력", INFO), ("계측·처리", OK), ("최종 노출·수집", ACC)])
svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-03.chapter-overview.svg"
d.save(str(svg_path))
print("ok 13-03 chapter-overview")
