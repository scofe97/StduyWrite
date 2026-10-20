# 타입 스펙: type-process
# 사실 출처: NPG Ch.13 Logging and Metrics (Listing 13-1~13-11), go.uber.org/zap, log/slog
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 116
W, H = 984, 750

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

def nx(j):
    return COL_X + j * STRIDE

def ny(i):
    return ROW_Y + i * ROW_STRIDE

d = D(W, H, "PROCESS · 13-01 OVERVIEW",
      "Go 표준 log 로 시작해 레벨 분기와 Zap 구조화·샘플링으로 이어지는 흐름",
      "13-01 의 핵심 로깅 기법 개념도입니다. "
      "§1 은 이벤트 로그의 가치와 부하 비용 관리, "
      "§2 는 log 패키지의 줄 머리 조립과 다중 출력 지속 쓰기, "
      "§3 은 레벨별 로거 분리와 출력 대상 분기, "
      "§4 는 Zap 인코더·출력·레벨을 묶은 구조화 코어, "
      "§5 는 다중 코어 Tee 결합과 샘플링을 통한 반복 부하 삭감입니다.",
      lead="화살표 위 글자는 단계 간 변환 동작, 왼쪽 칩은 각 절의 번호입니다.")

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

# §1 로그의 목적과 비용
node(0, 0, "이벤트 발생", "상태 변화 질의 대상", INFO)
node(0, 1, "과도한 로깅", "CPU · I/O 병목 유발", WARN)
node(0, 2, "비용 균형", "로그 · 메트릭 분업", ACC)
harrow(0, 0, "기록 비용 발생")
harrow(0, 1, "질문 축소·분업", ACC, "acc")

# §2 log 패키지와 다중 출력
node(1, 0, "로그 호출", "l.Print(...) 메시지", INFO)
node(1, 1, "줄 머리 조립", "Lshortfile · Lmsgprefix", OK)
node(1, 2, "다중 출력 지속", "sustainedMultiWriter", ACC)
harrow(1, 0, "접두어 결합")
harrow(1, 1, "에러 지속 쓰기", ACC, "acc")

# §3 레벨 기반 로깅
node(2, 0, "로그 우선순위", "DEBUG 대 ERROR", INFO)
node(2, 1, "로거 인스턴스 분리", "lDebug · lError 구성", OK)
node(2, 2, "출력 대상 분기", "터미널 전용 · 파일 보관", ACC)
harrow(2, 0, "우선순위 판별")
harrow(2, 1, "목적지 분기 전달", ACC, "acc")

# §4 Zap 구조화 로깅
node(3, 0, "EncoderConfig", "키 이름 · 형식 설정", INFO)
node(3, 1, "zapcore.Core", "인코더 · 출력 · 레벨 결합", OK)
node(3, 2, "구조화 출력", "JSON · 콘솔 인코딩", ACC)
harrow(3, 0, "코어 조립")
harrow(3, 1, "직렬화 출력", ACC, "acc")

# §5 코어 겹치기와 샘플링
node(4, 0, "zapcore.NewTee", "복수 코어 동시 전달", INFO)
node(4, 1, "NewSamplerWithOptions", "1초 틱 · first 1 · nth 3", WARN)
node(4, 2, "부하 삭감 출력", "반복 로그 선택 기록", ACC)
harrow(4, 0, "출력 복제")
harrow(4, 1, "빈도 제어 통과", ACC, "acc")

d.legend(690, [("설정·입력", INFO), ("중간 처리", OK), ("최종 결과", ACC), ("비용·제약", WARN)])
svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-01.chapter-overview.svg"
d.save(str(svg_path))
print("ok 13-01 chapter-overview")
