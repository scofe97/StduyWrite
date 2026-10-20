# 타입 스펙: type-state
# 사실 출처: NPG Ch.13 Listing 13-12~13-14, go.uber.org/zap AtomicLevel
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, INFO, ACC, KR, MONO

W, H = 920, 460
d = D(W, H, "STATE · ATOMIC LEVEL TRANSITIONS",
      "세마포어 파일과 원자 레벨 상태 전이",
      "InfoLevel 과 DebugLevel 사이의 무중단 상태 전이와 조건입니다.",
      lead="atomic.Int32 를 포인터로 공유해 락 경합 없는 안전한 상태 전이")

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

# 초기 진입점
d.o.append(f'<circle cx="40" cy="235" r="8" fill="{INK}"/>')
d.arrow([(48, 235), (136, 235)], c=INFO, m="info", sw=1.3)
d.t(88, 218, "생성", 11, INFO, KR, "middle", 600)
d.t(88, 252, "NewAtomicLevel", 11, MUTED, MONO, "middle")

# 상태 1: InfoLevel
d.tone(140, 160, 250, 150, INFO, 8, "12", 1.2)
d.t(265, 190, "InfoLevel (기본 상태)", 14, INFO, KR, "middle", 600)
d.t(265, 212, "세마포어 파일 없음", 11, MUTED, KR, "middle")
d.line(160, 226, 370, 226, RULE, 0.8)
d.t(265, 248, "Debug 로그 차단", 11, INK, KR, "middle")
d.t(265, 268, "Info · Warn · Error 출력", 11, INK, KR, "middle")
d.t(265, 288, "I/O 및 스토리지 부하 최소화", 11, MUTED, KR, "middle")

# 상태 2: DebugLevel
d.tone(530, 160, 250, 150, OK, 8, "12", 1.2)
d.t(655, 190, "DebugLevel (진단 상태)", 14, OK, KR, "middle", 600)
d.t(655, 212, "level.debug 파일 감지됨", 11, MUTED, KR, "middle")
d.line(550, 226, 760, 226, RULE, 0.8)
d.t(655, 248, "Debug 로그 즉시 출력", 11, INK, KR, "middle")
d.t(655, 268, "모든 레벨 로그 수집", 11, INK, KR, "middle")
d.t(655, 288, "실시간 트러블슈팅 분석", 11, MUTED, KR, "middle")

# 순방향 전이: Info -> Debug (상단 곡선)
d.path("M 390 195 C 435 150, 485 150, 526 195", c=OK, sw=1.5, m="ok")
d.t(460, 140, "세마포어 파일 생성 (fsnotify.Create)", 11, OK, KR, "middle", 600)
d.t(460, 158, "SetLevel(DebugLevel) 호출", 11, MUTED, KR, "middle")

# 역방향 전이: Debug -> Info (하단 곡선)
d.path("M 530 275 C 485 320, 435 320, 394 275", c=ACC, sw=1.5, m="acc")
d.t(460, 332, "세마포어 파일 삭제 (fsnotify.Remove)", 11, ACC, KR, "middle", 600)
d.t(460, 350, "SetLevel(originalLevel) 원복", 11, MUTED, KR, "middle")

# 대안 경로 칩
d.chip(460, 385, "HTTP ServeHTTP 지원: PUT /log/level {\"level\":\"debug\"}", SOFT, 11, 8)

d.legend(415, [("기본 운영 레벨", INFO), ("디버그 진단 레벨", OK), ("레벨 원복 전이", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-02.atomic-level-state.svg"
d.save(str(svg_path))
print("ok 13-02 atomic-level-state")
