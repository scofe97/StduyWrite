# 13-04 §1 — End-to-End 인수와 중복 억제: 클라이언트 생성 요청 ID(UUID)를 통한 네트워크 재시도 중복 차단 시퀀스.
# 사실 출처: 13-04 본문 §1(L22~L30), DDIA 2판 Ch.13 p.32~34 (Example 13-2 및 Saltzer 1984 인용).
# 타입 스펙: type-sequence
# 2026-10-31 검증: 지어낸 /transfer·200 OK·타임아웃을 원서 p31~32(HTTP POST·사용자 재시도·INSERT 실패와 트랜잭션 중단)로 교체
import sys; sys.path.insert(0, ".")
from dd import Seq, D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, BAD, OK, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1+10*d} {y} L {x2-12*d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11.5, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 15, sub, 11, MUTED, _kr(sub))

    def lanes(s, names, y0=104, lane_w=180):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            s.t(x, y0 + 36, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def state(s, a, txt, y, c):
        x = s.LX[a]
        fam = _kr(txt)
        w = len(txt) * (11.0 if fam == KR else 7.0) + 18
        s.o.append(f'<rect x="{x-w/2}" y="{y-10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, fam)

W = 880
Y0 = 104
LANE_W = 180
RAIL_BOT = 612
LEG = RAIL_BOT + 28
H = LEG + 48

d = SeqKR(W, H, "13-04 · §1 END-TO-END ARGUMENT", "요청 ID와 End-to-End 중복 억제 시퀀스",
          "클라이언트가 생성한 UUID 요청 ID가 TCP 계층 단절과 네트워크 재시도를 넘어 데이터베이스 유니크 제약으로 중복 실행을 차단하는 과정을 보인다.",
          "end-to-end 인수 · TCP 연결 경계 · UNIQUE(request_id) 제약 · 같은 요청 ID 한 번만 실행")

# 참여자 레인 4개
d.lanes([
    ("클라이언트", "Client / Browser"),
    ("네트워크 (TCP)", "TCP Connections"),
    ("앱 서버", "App Server"),
    ("데이터베이스", "DB: requests 테이블")
], Y0, LANE_W)

d.rails(RAIL_BOT)

# Phase 1: 최초 시도와 응답 유실 (Y = 156 ~ 380)
d.box(28, 156, W - 56, 24, PAPER2, RULE, 0.8)
d.t(W / 2, 172, "1차 시도: DB 커밋 후 네트워크 장애로 응답 유실", 11.5, INK, KR, "middle", 600)

d.state("클라이언트", "UUID 생성 (요청 ID)", 200, INFO)
d.msg("클라이언트", "네트워크 (TCP)", "HTTP POST (요청 ID)", 232, INFO, mk="ar", sub="TCP 연결 1 생성")
d.msg("네트워크 (TCP)", "앱 서버", "요청 전달 (conn 1)", 262, INFO, mk="ar")
d.msg("앱 서버", "데이터베이스", "INSERT INTO requests (UUID)", 292, OK, mk="ar")
d.state("데이터베이스", "커밋 완료 (계좌 갱신)", 318, OK)
d.msg("앱 서버", "네트워크 (TCP)", "응답 전송", 346, OK, mk="ar")
d.state("네트워크 (TCP)", "응답 패킷 유실 (연결 끊김)", 372, BAD)

# Phase 2: 재시도와 DB 수준 중복 차단 (Y = 404 ~ 596)
d.box(28, 404, W - 56, 24, PAPER2, WARN, 0.8)
d.t(W / 2, 420, "2차 재시도: 새 TCP 연결과 UNIQUE 제약 중복 차단", 11.5, WARN, KR, "middle", 600)

d.state("클라이언트", "오류 표시 · 사용자 재시도", 446, WARN)
d.msg("클라이언트", "네트워크 (TCP)", "HTTP POST (같은 요청 ID)", 478, WARN, mk="ar", sub="새 TCP 연결 2 생성")
d.msg("네트워크 (TCP)", "앱 서버", "요청 전달 (conn 2)", 508, WARN, mk="ar", sub="TCP 계층 중복 미인지")
d.msg("앱 서버", "데이터베이스", "INSERT INTO requests (동일 UUID)", 538, WARN, mk="ar")
d.state("데이터베이스", "INSERT 실패 · 트랜잭션 중단", 564, ACC)
d.msg("앱 서버", "클라이언트", "응답", 592, OK, mk="ar", sub="이체는 한 번만 실행")

d.legend(LEG, [
    ("정상 처리 흐름", OK),
    ("네트워크 전달", INFO),
    ("재시도 구간", WARN),
    ("네트워크 유실", BAD),
    ("중복 차단", ACC)
])

d.save("13-04.end-to-end-request-id-dedup.svg")
