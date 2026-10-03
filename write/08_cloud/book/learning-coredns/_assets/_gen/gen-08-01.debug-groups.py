# 08-01 §7 「켜는 범위도 갈립니다」 — 서버 그룹 둘 중 하나에만 debug 를 적었을 때, 복구와 디버그 로깅이 각각 어떻게 되는가.
# 소스 근거: core/dnsserver/server.go NewServer — 그룹 안 site.Debug 면 s.debug = true; log.D.Set(),
#            함수 끝 `if !s.debug { log.D.Clear() }`(리로드 대비 주석). register.go 는 groups(map) 를 `for addr, group := range`
#            로 돌며 NewServer 를 부르므로 그룹 생성 순서가 정해지지 않는다(Go 맵 순회).
# 타입 스펙: type-dp-security-matrix — 생성 순서(행) × 그룹별 복구·전역 로깅(열) 격자이고, 순서에 따라 갈리는 마지막 열이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, BAD, KR, MONO

W, H = 880, 392
d = D(W, H, "LEARNING COREDNS · 08-01 §7",
      "복구는 그룹마다, 로깅은 마지막 그룹이 정한다",
      "복구를 끄는 s.debug 는 리슨 주소가 같은 서버 그룹 단위로 선다. 디버그 로깅은 패키지 전역이라 그룹을 만들 때마다 켜지거나 "
      "꺼지고, 그룹을 만드는 순서는 맵 순회라 정해지지 않는다.",
      "주황 열이 실행마다 달라질 수 있는 자리입니다")

# SVG 는 연속 공백을 하나로 접으므로 두 블록을 따로 놓는다
d.t(20, 102, ".:53 { debug ... }", 12, MUTED, MONO, "start")
d.t(230, 102, ".:5300 { ... }", 12, MUTED, MONO, "start")

COLS = [(20, 200, "그룹을 만드는 순서"), (230, 200, ".:53 panic 복구"), (440, 200, ".:5300 panic 복구"), (650, 210, "디버그 로깅 log.D")]
rows = [
    (":53 먼저 · :5300 나중", ("꺼짐", "panic 이 프로세스를 끝냄", BAD), ("켜짐", "SERVFAIL 로 버팀", OK), ("꺼짐", ":5300 이 Clear", ACC)),
    (":5300 먼저 · :53 나중", ("꺼짐", "panic 이 프로세스를 끝냄", BAD), ("켜짐", "SERVFAIL 로 버팀", OK), ("켜짐", ":53 이 마지막에 Set", ACC)),
]
for k, (x, w, head) in enumerate(COLS):
    d.t(x + 12, 136, head, 12, ACC if k == 3 else SOFT, KR if k != 3 else KR, "start", 600)

d.tone(646, 146, 218, 2 * 76 - 4 + 8, ACC, 8, "12", 1.4)
for i, (order, *cells) in enumerate(rows):
    y = 150 + i * 76
    d.box(20, y, 200, 64, PAPER2, RULE, 1.0, 6)
    d.t(32, y + 38, order, 13, INK, KR, "start", 600)
    for k, (main, sub, c) in enumerate(cells, start=1):
        x, w, _ = COLS[k]
        if k != 3:
            d.box(x, y, w, 64, PAPER2, RULE, 1.0, 6)
        d.t(x + 12, y + 26, main, 14, c, KR, "start", 600)
        d.t(x + 12, y + 48, sub, 12, MUTED, KR, "start")

d.t(20, 334, "그룹 생성 순서 · Go 맵 순회라 정해지지 않음", 13, MUTED, KR, "start")

d.legend(348, [("실행마다 갈릴 수 있음", ACC), ("복구 꺼짐", BAD), ("복구 켜짐", OK)])
d.save("08-01.debug-groups.svg")
