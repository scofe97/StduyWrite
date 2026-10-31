# 13-03 §4 — 서버 상태 변경의 클라이언트 능동 푸시와 쓰기 경로 연장 시퀀스.
# 사실 출처: 13-03 §4(L55~L65), DDIA 2판 Ch.13 p.24~26 ("Extending the write path to end users",
#   "Local-First Software", "EventSource / WebSocket", "Consumer offsets catch-up", "React/Elm UI").
# 2026-10-31 검증: 원서 p.24~25 대조. "스냅샷"·"Event Store" 제거, 연결 수립 화살표를 초기 읽기 경로(INFO) 색에서 중립으로
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
LEG = 716
H = LEG + 52

class PushStateSeq(Seq):
    def lanes(self, names, xs, y0=104, lane_w=150):
        self.LX = {}
        for (nm, sub), x in zip(names, xs):
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            self.t(x, y0 + 37, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
        self.lane_top = y0 + 44
        return self.LX

    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, is_mono=False, lx=None, sub_c=MUTED):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = lx if lx is not None else (x1 + x2) / 2
        self.t(mx, y - 8, label, 12, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            self.t(mx, y + 17, sub, 11, sub_c, KR, "middle")

    def chip_state(self, a, txt, y, c):
        x = self.LX[a]
        w = len(txt) * 9.5 + 18
        self.box(x - w / 2, y - 11, w, 22, PAPER, c, 1.0, r=4)
        self.t(x, y + 4, txt, 11, c, KR, "middle", 600)

d = PushStateSeq(W, H, "13-03 · §4 EXTENDING THE WRITE PATH", "클라이언트까지 연장되는 쓰기 경로와 상태 동기화",
                 "서버가 상태 변경을 능동 푸시하여 쓰기 경로를 최종 사용자 장치 UI까지 연장하는 상호작용 순서.",
                 "초기 읽기 경로 · WebSocket/SSE 능동 푸시 · 로컬 모델 갱신 · 재접속 후 오프셋으로 따라잡기")

lx = d.lanes([
    ("사용자 화면", "Rendered UI / View"),
    ("클라이언트 앱", "Local State / Model"),
    ("서버 · 이벤트 브로커", "Server & Log Broker"),
], [140, 440, 740], y0=104, lane_w=160)

d.rails(690)

# Phase 1: 초기 접속 (읽기 경로)
d.t(440, 168, "1단계: 초기 접속 시 읽기 경로로 초기 상태 로드", 11, INFO, KR, "middle", 600)
d.line(60, 176, 820, 176, INFO, 0.8, "3 3")

d.seq_msg("사용자 화면", "클라이언트 앱", "페이지 접근", 204, INFO, "info")
d.seq_msg("클라이언트 앱", "서버 · 이벤트 브로커", "초기 상태 요청", 244, INFO, "info", sub="HTTP 읽기 경로 요청")
d.seq_msg("서버 · 이벤트 브로커", "클라이언트 앱", "초기 상태 반환", 286, INFO, "info", sub="서버 상태 데이터 수신")
d.chip_state("클라이언트 앱", "로컬 상태 모델 초기화", 320, OK)
d.seq_msg("클라이언트 앱", "사용자 화면", "초기 뷰 렌더링", 352, OK, "ok", sub="모델 객체의 화면 픽셀 구체화")

# Phase 2: 능동 푸시 스트림 (쓰기 경로 연장)
d.t(440, 388, "2단계: 서버 능동 푸시로 쓰기 경로를 화면까지 연장", 11, ACC, KR, "middle", 600)
d.line(60, 396, 820, 396, ACC, 0.8, "3 3")

d.seq_msg("클라이언트 앱", "서버 · 이벤트 브로커", "TCP 지속 연결 수립", 424, MUTED, "ar", dash="3 3", sub="WebSocket / SSE 스트림 연결")
d.seq_msg("서버 · 이벤트 브로커", "클라이언트 앱", "상태 변경 이벤트 푸시", 466, ACC, "acc", sub="서버 쓰기 경로의 클라이언트 연장")
d.chip_state("클라이언트 앱", "로컬 모델 자동 갱신", 500, OK)
d.seq_msg("클라이언트 앱", "사용자 화면", "화면 픽셀 자동 갱신", 534, OK, "ok", sub="React·Elm 반응형 UI 갱신")

# Phase 3: 오프라인 재접속 동기화 (오프셋 추적)
d.t(440, 570, "3단계: 오프라인 후 재접속 시 오프셋 기반 따라잡기", 11, WARN, KR, "middle", 600)
d.line(60, 578, 820, 578, WARN, 0.8, "3 3")

d.chip_state("클라이언트 앱", "오프라인 단절 상태", 604, WARN)
d.seq_msg("클라이언트 앱", "서버 · 이벤트 브로커", "재연결 (오프셋 전달)", 636, WARN, "warn", sub="마지막 수신 이벤트 위치")
d.seq_msg("서버 · 이벤트 브로커", "클라이언트 앱", "놓친 메시지 전달", 678, ACC, "acc", sub="소비자 오프셋으로 따라잡기")

d.legend(LEG, [
    ("능동 푸시 (focal)", ACC),
    ("로컬 모델·뷰 갱신", OK),
    ("초기 읽기 경로", INFO),
    ("오프라인·재접속", WARN),
])

d.save("13-03.push-state-to-client.svg")
