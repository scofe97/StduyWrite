# 타입 스펙: type-sequence
# 09-02 HTTP/2 서버 푸시 프레임 교환과 103 Early Hints 대조 시퀀스
# 사실 출처: NPG Ch.9 Listing 9-17~9-19 (http.Pusher), RFC 9113 §5.1.1, §8.4.1, §8.4.2, RFC 8297 §2
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 980

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        if sub:
            s.t(mx, y - 20, label, 11, c, _kr(label), "middle", 600)
            s.t(mx, y - 7, sub, 11, MUTED, _kr(sub), "middle")
        else:
            s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)

    def selfmsg(s, a, label, y, c=MUTED, mk="ar", sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 52} {y - 10} L {x + 52} {y + 10} L {x + 13} {y + 10}", c, 1.4, m=mk)
        s.t(x + 64, y - 3, label, 11, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 64, y + 17, sub, 11, MUTED, _kr(sub), "start")

d = SeqKR(W, H, "NPG CH.9 — HTTP/2 SERVER PUSH & 103 EARLY HINTS",
          "HTTP/2 서버 푸시와 103 Early Hints",
          "서버 주도 선제 전송의 한계와 브라우저 주도 103 Early Hints 대안",
          "약속 스트림 전송의 캐시 중복과 대역폭 선점, 브라우저 로컬 캐시 확인 기반 사전 로딩")

# 1. 참여자 레인 배치
y0 = 96
lane_w = 200
bx = 200  # 웹 브라우저 중심 x
sx = 760  # Go HTTP/2 서버 중심 x

d.LX = {"웹 브라우저": bx, "Go HTTP/2 서버": sx}

# 레인 상자
d.box(bx - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
d.t(bx, y0 + 19, "웹 브라우저", 12, INK, KR, "middle", 600)
d.t(bx, y0 + 35, "Client / Chrome · Firefox", 11, MUTED, MONO, "middle")

d.box(sx - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
d.t(sx, y0 + 19, "Go HTTP/2 서버", 12, INK, KR, "middle", 600)
d.t(sx, y0 + 35, "Server / http.Pusher", 11, MUTED, MONO, "middle")

d.lane_top = y0 + 44

# 2. 레일
y_bot = 860
d.line(bx, d.lane_top + 6, bx, y_bot, RULE, 1.0, "3 6")
d.line(sx, d.lane_top + 6, sx, y_bot, RULE, 1.0, "3 6")

# 3. 활성화 바 (구역별)
d.box(bx - 4, 218, 8, 312, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(sx - 4, 218, 8, 312, fill=MUTED, stroke=RULE, sw=0.8, r=2)

d.box(bx - 4, 622, 8, 228, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(sx - 4, 622, 8, 228, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# 4. 구역 1 — 서버 푸시
d.box(48, 156, 864, 28, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(60, 174, "구역 1 · HTTP/2 서버 푸시", 12, INK, KR, "start", 600)

# 4-1: 브라우저 -> 서버: GET / (Stream 1)
d.msg("웹 브라우저", "Go HTTP/2 서버", "GET / (Stream 1)", 224, c=INFO, mk="info", sub="클라이언트 시작 (홀수)")

# 4-2: 서버 -> 브라우저: PUSH_PROMISE 두 개
d.msg("Go HTTP/2 서버", "웹 브라우저", "PUSH_PROMISE (Stream 1 → 2)", 276, c=WARN, mk="warn", dash="4 3", sub="약속: /static/style.css (짝수)")
d.msg("Go HTTP/2 서버", "웹 브라우저", "PUSH_PROMISE (Stream 1 → 4)", 328, c=WARN, mk="warn", dash="4 3", sub="약속: /static/hiking.svg (선제 발송)")

# 4-3: 서버 -> 브라우저: 스트림 2·4 데이터 전송 시작
d.msg("Go HTTP/2 서버", "웹 브라우저", "HEADERS + DATA (Stream 2, 4)", 380, c=OK, mk="ok", sub="약속 자원 전송")

# 4-4: 브라우저 -> 서버: 스트림 2 거절 (서버 전송 도중 도착)
d.msg("웹 브라우저", "Go HTTP/2 서버", "RST_STREAM (Stream 2: CANCEL)", 432, c=BAD, mk="bad", dash="4 3", sub="로컬 캐시 중복 시 스트림 거절")

# 문제 꼬리표 둘 (거절 시점에 발생한 손실 및 지연)
d.chip(360, 464, "캐시 중복 전송", BAD, 11)
d.chip(600, 464, "대역폭 선점으로 HTML 밀림", BAD, 11)

# 4-5: 서버 -> 브라우저: 스트림 1 HTML 본문 완성 (지연 완료)
d.msg("Go HTTP/2 서버", "웹 브라우저", "HEADERS + DATA (Stream 1)", 524, c=OK, mk="ok", sub="index.html 본문 완성")

# 5. 구역 2 — 대안 103 Early Hints
d.box(48, 560, 864, 28, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(60, 578, "구역 2 · 103 Early Hints 대안", 12, INK, KR, "start", 600)

# 5-1: 브라우저 -> 서버: GET /
d.msg("웹 브라우저", "Go HTTP/2 서버", "GET /", 628, c=INFO, mk="info", sub="메인 HTML 요청")

# 5-2: 서버 -> 브라우저: 103 Early Hints
d.msg("Go HTTP/2 서버", "웹 브라우저", "103 Early Hints", 680, c=WARN, mk="warn", dash="4 3", sub="Link: </static/style.css>; rel=preload")

# 5-3: 브라우저 자기 호출: 캐시 확인 (focal)
d.selfmsg("웹 브라우저", "로컬 캐시 확인", 728, c=ACC, mk="acc", sub="없는 자원만 후속 요청")

# 5-4: 브라우저 -> 서버: 없는 자원만 요청
d.msg("웹 브라우저", "Go HTTP/2 서버", "GET /static/hiking.svg", 792, c=INFO, mk="info", sub="캐시 미보유 자원 요청")

# 5-5: 서버 -> 브라우저: index.html 200 OK (스트림 번호 제외)
d.msg("Go HTTP/2 서버", "웹 브라우저", "200 OK", 844, c=OK, mk="ok", sub="index.html 응답 완료")

# 6. 브라우저 생태계 퇴출 현황 띠
d.tone(48, 876, 864, 30, BAD, op="14", sw=1.0)
d.t(480, 895, "Chrome 106 기본 비활성 · Firefox 132 완전 제거", 11, BAD, KR, "middle", 600)

# 7. 범례
d.legend(928, [
    ("클라이언트 요청", INFO),
    ("서버 약속 · 힌트", WARN),
    ("데이터 응답", OK),
    ("스트림 거절", BAD),
    ("캐시 확인 (focal)", ACC),
])

out_path = os.path.join(os.path.dirname(__file__), "..", "09-02.server-push.svg")
d.save(out_path)
print("saved:", out_path)

