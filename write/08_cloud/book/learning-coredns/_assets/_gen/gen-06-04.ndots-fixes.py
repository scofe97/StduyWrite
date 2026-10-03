# 06-04 §4 「해법이 넷 있습니다」 — 외부 이름 하나의 질의 여섯 번을 어디서 줄이고 무엇을 남기는가.
# 본문 근거: 이 노트 §4 의 네 해법과 한계(원서). FQDN 끝 점이 검색 경로를 건너뛴다는 점은 리졸버 동작(정답 5).
# 타입 스펙: type-dp-security-matrix — 해법(행) × 고치는 곳·질의 수·남는 한계(열) 격자가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 520
d = D(W, H, "LEARNING COREDNS · 06-04 §4",
      "질의 여섯 번을 어디서 줄이나",
      "네 해법은 고치는 자리가 다르다. 앞의 둘은 클라이언트를, 노드 로컬 캐시는 노드를, autopath 는 CoreDNS 서버를 고치고, "
      "각자 다른 한계를 남긴다.",
      "주황 행이 다음 절의 해법입니다")

COLS = [(20, 190, "해법"), (220, 170, "고치는 자리"), (400, 220, "외부 이름 하나의 왕복"), (630, 230, "남는 한계")]
rows = [
    (("PodSpec dnsConfig", ""), ("파드마다", "PodSpec"), ("설정한 파드만 준다", ""), ("사용자가 잊지 않아야 한다", "")),
    (("FQDN 으로 적기", "끝에 점"), ("호출 코드", "이름 문자열"), ("한 번", "검색 경로를 건너뜀"), ("있을 법하지 않은 환상", "원서의 말")),
    (("노드 로컬 캐시", ""), ("노드마다", "캐시 CoreDNS"), ("여섯 번 · 노드 안에서", "중앙 부하만 준다"), ("노드마다 자원", "로컬은 인스턴스 하나")),
    (("autopath", ""), ("CoreDNS 서버", "Corefile 한 줄"), ("한 번", "CNAME 과 A 가 함께"), ("pods verified 메모리", "5절")),
]
FOCAL = 3
Y0, PITCH, RH = 132, 76, 66

for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, cells in enumerate(rows):
    y = Y0 + i * PITCH
    if i == FOCAL:
        d.tone(16, y - 2, 848, RH + 4, ACC, 8, "12", 1.4)
    for k, (x, w, _) in enumerate(COLS):
        if i != FOCAL:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
        main, sub = cells[k]
        fam = MONO if main in ("autopath",) or main.startswith("PodSpec") else KR
        col = ACC if (i == FOCAL and k == 0) else INK
        if sub:
            d.t(x + 12, y + 28, main, 13, col, fam, "start", 600)
            d.t(x + 12, y + 50, sub, 12, MUTED, KR, "start")
        else:
            d.t(x + 12, y + 39, main, 13, col, fam, "start", 600)

d.t(20, 450, "왕복 수 · 원서 환경 기준 여섯 · 호스트 검색 도메인이 늘면 같이 는다", 13, MUTED, KR, "start")

d.legend(472, [("서버를 고치는 해법", ACC)])
d.save("06-04.ndots-fixes.svg")
