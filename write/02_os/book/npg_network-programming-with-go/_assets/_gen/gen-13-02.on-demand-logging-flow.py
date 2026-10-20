# 타입 스펙: type-sequence
# 사실 출처: NPG Ch.13 On-Demand Debug Logging Listing 13-12~13-14, go.uber.org/zap, fsnotify
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, MUTED, SOFT, ACC, OK, WARN, INFO, MONO, KR

W, H = 980, 720
s = Seq(W, H, "SEQUENCE · ON-DEMAND LOGGING FLOW",
        "세마포어 파일 생성과 삭제에 따른 무중단 동적 디버그 로깅",
        "운영자가 세마포어 파일을 만들면 fsnotify 가 감지해 AtomicLevel 을 Debug 로 바꾸고, 파일을 지우면 원래의 Info 로 되돌립니다.",
        lead="atomic.Int32 를 포인터로 공유하는 AtomicLevel 로 레이스 컨디션 없이 실행 중에 로그 레벨을 바꿉니다.")

s.lanes([("운영자", "os.Create · Remove"),
         ("파일시스템", "디렉터리 이벤트"),
         ("감시 고루틴", "fsnotify.Watcher"),
         ("AtomicLevel", "원자 레벨 관리자"),
         ("로거", "zap.Logger")], y0=104, lane_w=140)

def selfmsg_left(s, a, label, y, c=MUTED, sub=None):
    x = s.LX[a]
    s.path(f"M {x-10} {y-10} L {x-58} {y-10} L {x-58} {y+10} L {x-13} {y+10}", c, 1.4, m="ar")
    s.t(x - 68, y - 4, label, 11, c, MONO, "end")
    if sub:
        s.t(x - 68, y + 13, sub, 11, MUTED, KR, "end")

# 1. 초기 상태: Info 레벨이므로 Debug 호출 무시
selfmsg_left(s, "로거", "zl.Debug 호출", 170, MUTED, sub="임계치 Info 미달로 출력 안 됨")

# 2. 세마포어 파일 생성
s.msg("운영자", "파일시스템", "os.Create(debugLevelFile)", 225, INFO, "info", sub="세마포어 파일 생성")

# 3. fsnotify.Create 이벤트 전달
s.msg("파일시스템", "감시 고루틴", "fsnotify.Create 이벤트", 280, INFO, "info", sub="debugLevelFile 매칭")

# 4. AtomicLevel 을 DebugLevel 로 변경
s.msg("감시 고루틴", "AtomicLevel", "SetLevel(DebugLevel)", 335, OK, "ok", sub="atomic.Int32 값 Store")

# 5. 디버그 로그 실제 출력
selfmsg_left(s, "로거", "zl.Debug 출력", 390, OK, sub='{"level":"debug","msg":"..."}')

# 6. 세마포어 파일 삭제
s.msg("운영자", "파일시스템", "os.Remove(debugLevelFile)", 445, WARN, "warn", sub="세마포어 파일 삭제")

# 7. fsnotify.Remove 이벤트 전달
s.msg("파일시스템", "감시 고루틴", "fsnotify.Remove 이벤트", 500, WARN, "warn", sub="debugLevelFile 매칭")

# 8. AtomicLevel 을 originalLevel 로 원복
s.msg("감시 고루틴", "AtomicLevel", "SetLevel(originalLevel)", 555, ACC, "acc", sub="InfoLevel 원복")

# 9. 디버그 로그 차단 및 인포 로그 출력
selfmsg_left(s, "로거", "zl.Debug 차단 · Info 출력", 610, MUTED, sub='{"level":"info","msg":"..."}')

s.rails(635)
s.legend(665, [("세마포어 감지", INFO), ("디버그 활성화", OK), ("원복 및 차단", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-02.on-demand-logging-flow.svg"
s.save(str(svg_path))
print("ok 13-02 on-demand-logging-flow")
