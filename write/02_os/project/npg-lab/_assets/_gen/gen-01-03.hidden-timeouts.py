# 01-03-hidden-timeouts — net/http 가 기한 초과를 손님 이탈로 숨기는 자리와 세 함정 대처
# 본문 요구: 생명선 셋(손님 · net/http 서버 · 프록시 몸통 마디). 함정 셋을 위에서 아래로: 읽기 기한 초과 → 서버가 연결 context 취소 → 기록이 DC 로 보임(마디가 첫 오류를 적어 CT 로 구분), 몸통 EOF 뒤 서버의 뒤 읽기(EOF 에서 기한을 지움), keep-alive 다음 요청이 앞 쓰기 기한을 들고 옴(요청마다 먼저 지움). focal 은 DC 착시.
# 타입 스펙: type-sequence
# 사실 출처: 01-03.리버스 프록시 다운스트림 층 — 틈 시계·최소 속도·드레인.md:71-75, ADR 0014:13,59-61,71-73, ch09-slow-post-body.md:21-22,42-45, Go server.go connReader
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, OK, WARN, INFO, KR, MONO

W = 960
H = 688

d = D(
    W,
    H,
    "SEQUENCE · NET/HTTP HIDDEN TIMEOUTS & REMEDIES",
    "net/http 가 기한 초과를 숨기는 세 자리와 대처",
    "Go net/http 표준 서버가 읽기 기한 초과를 연결 취소로 숨겨 DC 로 왜곡하는 함정, EOF 뒤 추가 읽기 함정, keep-alive 쓰기 기한 잔존 함정을 마디에서 대처하는 순서",
    lead="표준 서버의 연결 취소는 기한 초과를 손님 이탈(DC)로 왜곡하므로, 마디가 첫 오류를 적어 408 CT 로 바로잡습니다.",
)

# 1. 생명선 셋 (손님, net/http 서버, 프록시 몸통 마디)
X_CLIENT = 160
X_SERVER = 480
X_PROXY = 800

# 상단 참여자 상자
d.box(70, 104, 180, 48, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(X_CLIENT, 126, "손님", 14, INK, KR, "middle", 600)
d.t(X_CLIENT, 142, "npgload", 12, MUTED, MONO)

d.box(390, 104, 180, 48, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(X_SERVER, 126, "net/http 서버", 14, INK, KR, "middle", 600)
d.t(X_SERVER, 142, "server.go connReader", 12, MUTED, MONO)

d.box(710, 104, 180, 48, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(X_PROXY, 126, "프록시 몸통 마디", 14, INK, KR, "middle", 600)
d.t(X_PROXY, 142, "r.Body 래퍼", 13, MUTED, KR)

# 수직 레일
d.line(X_CLIENT, 156, X_CLIENT, 616, RULE, 1.0, "3 6")
d.line(X_SERVER, 156, X_SERVER, 616, RULE, 1.0, "3 6")
d.line(X_PROXY, 156, X_PROXY, 616, RULE, 1.0, "3 6")

# 2. 함정 1: 읽기 기한 초과 왜곡과 DC 착시 (y = 172 ~ 332)
d.box(24, 172, 176, 26, fill=PAPER2, stroke=WARN, sw=1.0, r=4)
d.t(112, 190, "함정 1: 읽기 기한 왜곡", 13, WARN, KR, "middle", 600)

# 메시지 1: 손님 -> 서버
d.arrow([(X_CLIENT, 216), (X_SERVER, 216)], c=MUTED, m="ar", sw=1.4)
d.t((X_CLIENT + X_SERVER) / 2, 204, "느린 POST 몸통 전송 (2s/1B)", 13, MUTED, KR, "middle")

# 서버 읽기 기한 초과 (w=170, x: 395..565, y: 232..258)
d.tone(X_SERVER - 85, 232, 170, 26, WARN, r=4, op="18", sw=1.0)
d.t(X_SERVER, 250, "ReadTimeout 10s 초과", 13, WARN, KR, "middle", 600)

# 메시지 2: 서버 -> 프록시 (연결 context 취소) — y=284, text at 670 (x: 575..765)
d.arrow([(X_SERVER, 284), (X_PROXY, 284)], c=WARN, m="warn", sw=1.4, dash="3 3")
d.t(670, 272, "연결 context 취소 (cancelCtx)", 13, WARN, KR, "middle", 600)

# 대비: 기존 DC 착시(focal) vs 개선 CT 분류
d.box(340, 304, 220, 32, fill="#1F1612", stroke=ACC, sw=1.4, r=6)
d.t(450, 324, "기록: 499 DC (손님 이탈 착시)", 13, ACC, KR, "middle", 600)

d.tone(690, 304, 220, 32, OK, r=6, op="18", sw=1.2)
d.t(X_PROXY, 324, "첫 오류 확인 → 408 CT 분류", 13, OK, KR, "middle", 600)

# 구분선 1
d.line(24, 352, 936, 352, RULE, 0.8, dash="4 4")

# 3. 함정 2: 몸통 끝 뒤 서버의 추가 읽기 (y = 368 ~ 488)
d.box(24, 368, 204, 26, fill=PAPER2, stroke=INFO, sw=1.0, r=4)
d.t(126, 386, "함정 2: 몸통 뒤 추가 읽기", 13, INFO, KR, "middle", 600)

# 메시지 3: 손님 -> 서버
d.arrow([(X_CLIENT, 408), (X_SERVER, 408)], c=MUTED, m="ar", sw=1.4)
d.t((X_CLIENT + X_SERVER) / 2, 396, "몸통 읽기 완료 (io.EOF)", 13, INK, KR, "middle")

# 메시지 4: 서버 -> 프록시
d.arrow([(X_SERVER, 408), (X_PROXY, 408)], c=INFO, m="info", sw=1.4)
d.t((X_SERVER + X_PROXY) / 2, 396, "io.EOF 전달", 13, INFO, KR, "middle")

# 마디: EOF 즉시 기한 해제
d.tone(650, 428, 300, 28, OK, r=4, op="18", sw=1.2)
d.t(X_PROXY, 446, "SetReadDeadline(time.Time{}) 기한 해제", 13, OK, KR, "middle", 600)

# 서버 추가 읽기 통과
d.tone(350, 464, 260, 28, OK, r=4, op="14", sw=1.0)
d.t(X_SERVER, 482, "서버 뒤 읽기 정상 통과 · 연결 유지", 13, OK, KR, "middle", 600)

# 구분선 2
d.line(24, 506, 936, 506, RULE, 0.8, dash="4 4")

# 4. 함정 3: 앞 쓰기 기한 잔존과 초기화 (y = 520 ~ 624)
d.box(24, 520, 204, 26, fill=PAPER2, stroke=WARN, sw=1.0, r=4)
d.t(126, 538, "함정 3: 앞 쓰기 기한 잔존", 13, WARN, KR, "middle", 600)

# 메시지 5: 손님 -> 서버
d.arrow([(X_CLIENT, 556), (X_SERVER, 556)], c=MUTED, m="ar", sw=1.4)
d.t((X_CLIENT + X_SERVER) / 2, 544, "keep-alive 다음 요청 도착", 13, INK, KR, "middle")

# 메시지 6: 서버 -> 프록시
d.arrow([(X_SERVER, 556), (X_PROXY, 556)], c=WARN, m="warn", sw=1.4)
d.t((X_SERVER + X_PROXY) / 2, 544, "앞선 쓰기 기한 잔존 위험", 13, WARN, KR, "middle")

# 대처: 쓰기 기한 초기화 및 응답 정상
d.tone(650, 578, 300, 32, OK, r=4, op="18", sw=1.2)
d.t(X_PROXY, 598, "SetWriteDeadline(time.Time{}) 초기화", 13, OK, KR, "middle", 600)

d.box(360, 578, 240, 32, fill=PAPER2, stroke=OK, sw=1.0, r=4)
d.t(X_SERVER, 598, "새 요청 응답 쓰기 정상 진행", 13, OK, KR, "middle", 600)

# 5. 범례
d.legend(636, [
    ("손님 이탈 착시", ACC),
    ("정상·해법", OK),
    ("초과·위험", WARN),
    ("중립·전달", INFO),
])

out_path = ASSETS_DIR / "01-03-hidden-timeouts.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
