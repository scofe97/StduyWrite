# 사실 출처: internal/runtime/worker.go:335-375 · internal/runtime/js.go:75,86,540-575,618 · internal/runtime/host.go:79,381 · internal/runtime/protocol.go:27-29
# 타입 스펙: type-data-flow
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 520
d = D(
    W, H,
    "DATA FLOW · FETCH HANDLER PATH",
    "fetch 핸들러와 SQLite 요청 처리 흐름",
    "방문자 요청의 Unix 소켓 수납·VM 풀 할당·동기식 호스트 브리지 호출",
    lead="GET / ──> flats serve ──> worker ServeHTTP ──> jsPool (≤4) ──> host(\"db.query\")"
)

# 4개 구획
def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 14, y + 20, label, 11, SOFT, KR, "start", 600)

zone(20, 100, 210, 380, "1. 호스트 인입")
zone(246, 100, 220, 380, "2. 워커 프로세스")
zone(482, 100, 236, 380, "3. QuickJS VM 풀")
zone(734, 100, 206, 380, "4. SQLite 저장소")

# 1. 호스트 인입 (위 -> 아래)
d.tone(34, 136, 180, 64, INFO, 6, "14", 1.2)
d.t(46, 158, "HTTP 요청 인입", 12, INFO, KR, "start", 600)
d.t(46, 180, "GET / (:17879)", 11, INK, MONO, "start")

d.box(34, 232, 180, 64, PAPER2, RULE, 1.0)
d.t(46, 254, "속도 제한 검사", 12, INK, KR, "start", 600)
d.t(46, 276, "rate_limit_rps 50", 11, WARN, MONO, "start")

d.tone(34, 328, 180, 64, ACC, 6, "14", 1.2)
d.t(46, 350, "Unix 소켓 전송", 12, ACC, KR, "start", 600)
d.t(46, 372, "run/w<id>.sock", 11, INK, MONO, "start")

# 2. 워커 프로세스 (아래 -> 위)
d.box(260, 328, 192, 64, PAPER2, RULE, 1.0)
d.t(272, 350, "worker.ServeHTTP", 12, INK, KR, "start", 600)
d.t(272, 372, "본문 상한 10 MiB", 11, INFO, KR, "start")

d.tone(260, 232, 192, 64, INFO, 6, "14", 1.2)
d.t(272, 254, "요청 JSON 직렬화", 12, INFO, KR, "start", 600)
d.t(272, 276, "reqPayload {method...}", 11, INK, MONO, "start")

d.box(260, 136, 192, 64, PAPER2, RULE, 1.0)
d.t(272, 158, "VM 풀 토큰 획득", 12, INK, KR, "start", 600)
d.t(272, 180, "jsPool.get (크기 ≤ 4)", 11, OK, KR, "start")

# 3. QuickJS VM 풀
d.tone(496, 136, 208, 80, OK, 6, "14", 1.2)
d.t(508, 158, "fetch(request, env)", 12, OK, MONO, "start", 600)
d.t(508, 178, "한계 10s · 64 MiB", 11, WARN, KR, "start")
d.t(508, 196, "JS 힙 48 MiB 상한", 10, MUTED, KR, "start")

d.tone(496, 246, 208, 74, ACC, 6, "14", 1.2)
d.t(508, 268, "동기식 호스트 호출", 12, ACC, KR, "start", 600)
d.t(508, 290, "env.DB.query(sql)", 11, INK, MONO, "start")
d.t(508, 306, "host(\"db.query\")", 10, ACC, MONO, "start")

d.box(496, 348, 208, 64, PAPER2, RULE, 1.0)
d.t(508, 370, "응답 JSON 직렬화", 12, INK, KR, "start", 600)
d.t(508, 392, "serialize(res)", 11, INFO, MONO, "start")

# 4. SQLite 저장소
d.box(748, 154, 178, 66, PAPER2, RULE, 1.0)
d.t(760, 176, "SQL 문법 검증", 12, INK, KR, "start", 600)
d.t(760, 198, "checkSQL (PRAGMA 방어)", 11, BAD, KR, "start")

d.tone(748, 248, 178, 70, OK, 6, "14", 1.2)
d.t(760, 270, "db.sqlite 실행", 12, OK, MONO, "start", 600)
d.t(760, 292, "WAL · 1 GiB 커밋 훅", 11, INK, KR, "start")

d.tone(748, 348, 178, 64, OK, 6, "14", 1.2)
d.t(760, 370, "{\"hits\": 2} 200 OK", 12, OK, MONO, "start", 600)
d.t(760, 392, "0.003s 응답 반환", 11, INK, KR, "start")

# 흐름 화살표
d.arrow([(124, 200), (124, 232)], MUTED, "ar")
d.arrow([(124, 296), (124, 328)], MUTED, "ar")
d.arrow([(214, 360), (260, 360)], ACC, "acc")
d.arrow([(356, 328), (356, 296)], MUTED, "ar")
d.arrow([(356, 232), (356, 200)], MUTED, "ar")
d.arrow([(452, 168), (496, 168)], OK, "ok")
d.arrow([(600, 216), (600, 246)], MUTED, "ar")
d.arrow([(704, 260), (726, 260), (726, 187), (748, 187)], ACC, "acc")
d.arrow([(837, 220), (837, 248)], MUTED, "ar")
d.arrow([(748, 283), (726, 283), (726, 334), (600, 334), (600, 348)], OK, "ok")
d.arrow([(704, 380), (748, 380)], OK, "ok")

out_svg = Path(__file__).parent.parent / "02-03-request-path.svg"
d.save(str(out_svg))
print(f"Generated: {out_svg}")
