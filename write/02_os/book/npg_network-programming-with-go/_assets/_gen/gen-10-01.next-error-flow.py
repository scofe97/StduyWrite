# 타입 스펙: type-sequence
# NPG Ch.10 §5 Caddy restrict_prefix 미들웨어의 next 호출과 error 전달 시퀀스
# 사실 출처: NPG Ch.10 Listing 10-14~10-16, Caddy handle_errors 공식 문서 (https://caddyserver.com/docs/caddyfile/directives/handle_errors)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 1120

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, sw=1.5):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, sw, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        if sub:
            s.t(mx, y - 20, label, 11, c, _kr(label), "middle", 600)
            s.t(mx, y - 7, sub, 11, MUTED, _kr(sub), "middle")
        else:
            s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)

    def selfmsg(s, a, label, y, c=MUTED, mk="ar", sub=None):
        x = s.LX[a]
        s.path(f"M {x + 8} {y - 10} L {x + 36} {y - 10} L {x + 36} {y + 10} L {x + 11} {y + 10}", c, 1.4, m=mk)
        s.t(x + 46, y - 3, label, 11, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 46, y + 17, sub, 11, MUTED, _kr(sub), "start")

    def legend(s, y, items):
        s.line(12, y, s.w - 48, y, RULE, 0.8)
        s.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
        x = 96
        for lab, c in items:
            s.o.append(f'<rect x="{x}" y="{y+12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
            s.t(x + 22, y + 22, lab, 11, MUTED, KR, "start")
            w = sum(11.5 if '가' <= ch <= '힣' else 7.0 for ch in lab)
            x += int(w + 38)

d = SeqKR(W, H, "NPG CH.10 — CADDY MIDDLEWARE NEXT & ERROR FLOW",
          "Caddy 미들웨어의 next 호출과 error 전달 흐름",
          "요청 경로에 따른 next 호출 분기와 error 반환 시 handle_errors 전환 절차",
          "매 요청마다 Handler 가 직접 전달되며, error 반환 시 즉시 중단되어 오류 처리 체인으로 제어를 위임합니다")

# 1. 참여자 레인 정의
y0 = 100

LX = {
    "Caddy HTTP 서버": 115,
    "restrict_prefix": 320,
    "next": 660,
    "handle_errors": 860,
}
d.LX = LX

roles = [
    ("Caddy HTTP 서버", "라우트", 160),
    ("restrict_prefix", "RestrictPrefix.ServeHTTP", 190),
    ("next", "다음 핸들러", 160),
    ("handle_errors", "오류 처리 경로", 170),
]

for name, sub, lane_w in roles:
    x = LX[name]
    d.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
    d.t(x, y0 + 19, name, 12, INK, _kr(name), "middle", 600)
    d.t(x, y0 + 35, sub, 11, MUTED, _kr(sub), "middle")

d.lane_top = y0 + 44

# 2. 레일
y_bot = 1024
for x in LX.values():
    d.line(x, d.lane_top + 6, x, y_bot, RULE, 1.0, "3 6")

# 3. 활성화 바
# Caddy HTTP 서버
d.box(LX["Caddy HTTP 서버"] - 4, 224, 8, 228, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["Caddy HTTP 서버"] - 4, 550, 8, 120, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["Caddy HTTP 서버"] - 4, 768, 8, 228, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# restrict_prefix
d.box(LX["restrict_prefix"] - 4, 224, 8, 228, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["restrict_prefix"] - 4, 550, 8, 120, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["restrict_prefix"] - 4, 768, 8, 174, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# next (구역 2에서는 호출되지 않으므로 활성화 바 없음)
d.box(LX["next"] - 4, 332, 8, 66, fill=MUTED, stroke=RULE, sw=0.8, r=2)
d.box(LX["next"] - 4, 822, 8, 66, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# handle_errors (구역 3에서만 호출)
d.box(LX["handle_errors"] - 4, 984, 8, 34, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# ── 구역 1: 통과 (GET /index.html) ──────────────────────────────────────────
d.box(40, 164, 880, 28, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(52, 182, "구역 1 · 정상 통과 (GET /index.html)", 12, INK, KR, "start", 600)

# 1-1: 서버 -> restrict_prefix: ServeHTTP(w, r, next)
d.msg("Caddy HTTP 서버", "restrict_prefix", "ServeHTTP(w, r, next)", 230, c=INFO, mk="info", sub="GET /index.html 전달")

# 1-2: restrict_prefix 내부 검사
d.selfmsg("restrict_prefix", "경로 세그먼트 검사", 284, c=MUTED, mk="ar", sub="접두사 '.' 없음")

# 1-3: restrict_prefix -> next: next.ServeHTTP (focal)
d.msg("restrict_prefix", "next", "next.ServeHTTP(w, r)", 338, c=ACC, mk="acc", sub="인자로 받은 next 호출", sw=1.6)

# 1-4: next -> restrict_prefix: nil 반환
d.msg("next", "restrict_prefix", "nil 반환", 392, c=OK, mk="ok", dash="4 3", sub="응답 본문 작성")

# 1-5: restrict_prefix -> 서버: nil 반환
d.msg("restrict_prefix", "Caddy HTTP 서버", "nil 반환", 446, c=OK, mk="ok", dash="4 3", sub="return next.ServeHTTP(w, r)")

# ── 구역 2: 차단 (GET /.secret) ─────────────────────────────────────────────
d.box(40, 490, 880, 28, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(52, 508, "구역 2 · 숨김 파일 차단 (GET /.secret)", 12, INK, KR, "start", 600)

# 2-1: 서버 -> restrict_prefix: ServeHTTP(w, r, next)
d.msg("Caddy HTTP 서버", "restrict_prefix", "ServeHTTP(w, r, next)", 556, c=INFO, mk="info", sub="GET /.secret 전달")

# 2-2: restrict_prefix 자체 차단: http.Error(404)
d.selfmsg("restrict_prefix", "http.Error(w, \"Not Found\", 404)", 606, c=BAD, mk="bad", sub="접두사 '.' 발견 즉시 차단")

# next 생명선에 단락 표지 (호출 없음)
d.chip(LX["next"], 648, "호출 없음 (단락)", MUTED, 11)

# 2-3: restrict_prefix -> 서버: return nil
d.msg("restrict_prefix", "Caddy HTTP 서버", "nil 반환", 668, c=OK, mk="ok", dash="4 3", sub="return nil (단락)")

# ── 구역 3: 오류 (next 가 error 반환) ────────────────────────────────────────
d.box(40, 708, 880, 28, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
d.t(52, 726, "구역 3 · next 오류 시 handle_errors 위임", 12, INK, KR, "start", 600)

# 3-1: 서버 -> restrict_prefix: ServeHTTP(w, r, next)
d.msg("Caddy HTTP 서버", "restrict_prefix", "ServeHTTP(w, r, next)", 774, c=INFO, mk="info", sub="요청 전달")

# 3-2: restrict_prefix -> next: next.ServeHTTP
d.msg("restrict_prefix", "next", "next.ServeHTTP(w, r)", 828, c=MUTED, mk="ar", sub="다음 핸들러 호출")

# 3-3: next -> restrict_prefix: error 반환
d.msg("next", "restrict_prefix", "error 반환", 882, c=BAD, mk="bad", dash="4 3", sub="next 가 error 반환")

# 3-4: restrict_prefix -> 서버: error 반환
d.msg("restrict_prefix", "Caddy HTTP 서버", "error 반환", 936, c=BAD, mk="bad", dash="4 3", sub="return next.ServeHTTP(w, r)")

# 3-5: 서버 -> handle_errors: handle_errors 실행
d.msg("Caddy HTTP 서버", "handle_errors", "handle_errors 실행", 990, c=WARN, mk="warn", sub="정상 처리 중단 · 오류 핸들러 위임")

# 범례
d.legend(1056, [
    ("요청 전달", INFO),
    ("next 호출", ACC),
    ("정상 반환 (nil)", OK),
    ("차단 및 오류 (error)", BAD),
    ("오류 체인 위임", WARN),
])

out_path = os.path.join(os.path.dirname(__file__), "..", "10-01.next-error-flow.svg")
d.save(out_path)
print("saved:", out_path)
