# 타입 스펙: type-process
# 사실 출처: NPG Ch.13 On-Demand Debug Logging ~ Log Rotation with Lumberjack, go.uber.org/zap, fsnotify, lumberjack.v2
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 116
W, H = 984, 520

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

def nx(j):
    return COL_X + j * STRIDE

def ny(i):
    return ROW_Y + i * ROW_STRIDE

d = D(W, H, "PROCESS · 13-02 OVERVIEW",
      "온디맨드 디버깅·와이드 이벤트 로깅·Lumberjack 로그 회전",
      "13-02 의 세 절 핵심 흐름입니다. "
      "§1 은 세마포어 파일을 감지해 실행 중 원자 레벨을 바꾸는 온디맨드 디버깅입니다. "
      "§2 는 응답 래퍼로 메트릭을 모아 요청 1건을 단일 구조화 로그로 요약하는 와이드 이벤트입니다. "
      "§3 은 파일 크기와 보존 기간을 검사해 백업을 보관하고 압축하는 Lumberjack 로그 회전입니다.",
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

for i, sec in enumerate(("§1", "§2", "§3")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1 온디맨드 디버깅
node(0, 0, "세마포어 파일 감지", "fsnotify.Create · Remove", INFO)
node(0, 1, "원자 레벨 전환", "atomicLevel.SetLevel", OK)
node(0, 2, "디버그 출력 제어", "zl.Debug 즉시 반영", ACC)
harrow(0, 0, "파일 이벤트 감지")
harrow(0, 1, "무중단 원자 갱신", ACC, "acc")

# §2 와이드 이벤트
node(1, 0, "응답 정보 가로채기", "wideResponseWriter", INFO)
node(1, 1, "핸들러 실행 및 계측", "status · length 수집", OK)
node(1, 2, "단일 구조화 로그", "요청당 1줄 종합 요약", ACC)
harrow(1, 0, "ServeHTTP 위임")
harrow(1, 1, "logger.Info 출력", ACC, "acc")

# §3 Lumberjack 회전
node(2, 0, "로그 파일 기록", "zapcore.AddSync 연동", INFO)
node(2, 1, "임계치 검사", "MaxSize 100MB 도달", OK)
node(2, 2, "회전 및 gzip 압축", "name-timestamp.log.gz", ACC)
harrow(2, 0, "용량 한도 확인")
harrow(2, 1, "오래된 백업 정리", ACC, "acc")

d.legend(470, [("입력·감지", INFO), ("중간 제어·계측", OK), ("최종 결과·보관", ACC)])
svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-02.chapter-overview.svg"
d.save(str(svg_path))
print("ok 13-02 chapter-overview")
