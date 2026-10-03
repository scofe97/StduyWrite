# 07-01 §9 — 필터링 DNS 가 차단 대상 이름에 답하는 두 방식과 브라우저가 보는 결과.
# 본문 근거: 이 노트 §9 「막는 방법은 1절과 8절에 이미 있습니다」 — NXDOMAIN 은 이유 없이 오류, 안내 페이지 유도는 HTTPS 면 인증서 경고.
# 타입 스펙: type-dp-security-matrix — 응답 방식(행) × DNS 응답·브라우저 결과(열).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, BAD, KR, MONO

W, H = 880, 450
d = D(W, H, "LEARNING COREDNS · 07-01 §9",
      "막을 때는 없다고 하거나 다른 곳을 가리킨다",
      "정상 이름은 진짜 주소를 받는다. 차단 대상이면 없는 이름이라고 답하거나 안내 페이지의 주소로 돌린다. "
      "안내 페이지는 이유를 보여 줄 수 있지만 HTTPS 사이트면 그 이름의 인증서가 없어 경고가 먼저 뜬다.",
      "주황 행이 이유를 보여 주려다 경고를 만나는 길입니다")

COLS = [(20, 200, "응답 방식"), (230, 250, "DNS 응답"), (490, 370, "브라우저가 보는 것")]
rows = [
    (("정상 이름", "블록리스트에 없음"), ("진짜 주소", "A 레코드"), ("사이트가 열린다", ""), OK),
    (("없는 이름으로", "template rcode NXDOMAIN 과 같음"), ("NXDOMAIN", ""), ("이름을 찾지 못했다는 오류", "막힌 이유는 안 보임"), BAD),
    (("안내 페이지로", "싱크홀 · policy 의 두 번째 길"), ("안내 서버 주소", "A 레코드"), ("HTTP 면 안내 페이지", "HTTPS 면 인증서 경고가 먼저"), BAD),
]
FOCAL = 2

for x, w, head in COLS:
    d.t(x + 10, 118, head, 12, SOFT, KR, "start", 600)

for i, (how, ans, view, c) in enumerate(rows):
    y = 132 + i * 80
    foc = i == FOCAL
    if foc:
        d.tone(16, y - 3, 848, 72, ACC, 8, "12", 1.4)
    for k, (a, b) in enumerate((how, ans, view)):
        x, w, _ = COLS[k]
        if not foc:
            d.box(x, y, w, 66, PAPER2, RULE, 1.0, 6)
        col = c if k == 2 else (ACC if (foc and k == 0) else INK)
        fam = KR if any("가" <= ch <= "힣" for ch in a) else MONO
        if b:
            d.t(x + 12, y + 28, a, 13, col, fam, "start", 600)
            d.t(x + 12, y + 50, b, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in b) else MONO, "start")
        else:
            d.t(x + 12, y + 38, a, 13, col, fam, "start", 600)

d.t(20, 386, "어느 쪽이든 질문 이름은 그대로 · 답만 바꾼다", 13, MUTED, KR, "start")

d.legend(402, [("이유를 보이려다 경고를 만나는 길", ACC), ("열린다", OK), ("막힌다", BAD)])
d.save("07-01.block-answers.svg")
