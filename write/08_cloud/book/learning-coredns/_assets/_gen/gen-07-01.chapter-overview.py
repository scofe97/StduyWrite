# 07-01 학습 목표 뒤 전체 지도 — 도구마다 요청에서 무엇을 바꾸고 질문↔답의 대응이 어떻게 되는지를 놓는다.
# 본문 근거: 이 노트 §1(template 은 {{ .Name }} 으로 답을 지음), §3(정확 일치는 Answer 이름 자동 복구, regex 는 answer name),
#            §4(class 응답을 되돌리는 옵션 없음), §5(EDNS0 옵션), §6·§7(서명), §8·§9(사례).
# 2026-10-03 셋째 열 제목을 "요청에서 바꾸는 것"에서 "무엇을 바꾸나"로 — dnssec·차단은 응답 쪽 변경이라 열 제목과 어긋났다(라벨 검증).
# 타입 스펙: type-dp-security-matrix — 도구(행) × 바꾸는 것·대응·되돌리는 법(열) 격자가 논지다.
#           2026-10-03 절 제목을 이은 노드 사슬에서 실제 값이 든 격자로 다시 그렸다. §9 를 넣고 focal 을 하나로 줄였다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 680
d = D(W, H, "LEARNING COREDNS · 07-01",
      "고치는 자리마다 질문과 답의 대응이 달라진다",
      "이 장의 도구를 요청에서 무엇을 바꾸는지, 그 뒤 질문과 답의 대응이 어떻게 되는지, 어긋나면 무엇으로 되돌리는지로 나란히 놓았다. "
      "이름은 되돌릴 수 있고 클래스는 되돌릴 수 없다.",
      "주황 행이 되돌릴 길이 없는 자리입니다")

COLS = [(20, 60, "절"), (90, 170, "도구"), (270, 180, "무엇을 바꾸나"),
        (460, 220, "질문과 답의 대응"), (690, 170, "되돌리는 법")]
rows = [
    ("§1", ("template", ""), ("바꾸지 않음", "질문으로 답을 지음"), ("저절로 지켜짐", "{{ .Name }} 이 질문 이름"), ("필요 없음", "")),
    ("§2·§3", ("rewrite name", "정확 일치"), ("질문 이름", ""), ("자동 복구", "Answer 이름을 되돌림"), ("자동", "")),
    ("§3", ("rewrite name", "regex"), ("질문 이름", ""), ("어긋남", "Answer 에 바뀐 이름"), ("answer name", "직접 적는다")),
    ("§4", ("rewrite class", ""), ("질문 클래스", "CH 를 IN 으로"), ("어긋남", "답의 클래스가 다름"), ("없음", "관대한 클라이언트만")),
    ("§5", ("rewrite edns0", "metadata"), ("EDNS0 옵션", "싣고 상류에서 푼다"), ("영향 없음", ""), ("해당 없음", "")),
    ("§6·§7", ("dnssec", "sign · signzone"), ("답에 서명을 더함", ""), ("다른 문제", "답의 출처를 증명"), ("해당 없음", "")),
    ("§8·§9", ("사례 둘", "B1TD · 가정 필터"), ("요청에 신원 싣기", "차단은 답을 지음"), ("CNAME 으로 지킴", "Safe Search · 9절"), ("—", "")),
]
FOCAL = 3
Y0, PITCH, RH = 132, 62, 54


def fam(t):
    return KR if any("가" <= c <= "힣" for c in t) or t in ("—",) else MONO


for x, w, head in COLS:
    d.t(x + 10, 118, head, 12, SOFT, KR, "start", 600)

for i, (sec, *cells) in enumerate(rows):
    y = Y0 + i * PITCH
    foc = i == FOCAL
    if foc:
        d.tone(16, y - 3, 848, RH + 6, ACC, 8, "12", 1.4)
    x0, w0, _ = COLS[0]
    if not foc:
        d.box(x0, y, w0, RH, PAPER2, RULE, 1.0, 6)
    d.t(x0 + w0 / 2, y + 32, sec, 12, ACC if foc else MUTED, KR)
    for k, (main, sub) in enumerate(cells, start=1):
        x, w, _ = COLS[k]
        if not foc:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
        col = ACC if (foc and k in (1, 4)) else INK
        if sub:
            d.t(x + 10, y + 23, main, 13, col, fam(main), "start", 600)
            d.t(x + 10, y + 42, sub, 12, MUTED, fam(sub) if k != 3 else KR, "start")
        else:
            d.t(x + 10, y + 32, main, 13, col, fam(main), "start", 600)

d.t(20, 588, "1~5절 · 요청과 응답을 고친다 · 6~7절 · 답에 서명한다 · 8~9절 · 둘을 이은 사례", 13, MUTED, KR, "start")
d.t(20, 612, "대응을 검사하는 쪽은 서버가 아니라 클라이언트다", 13, MUTED, KR, "start")

d.legend(630, [("되돌릴 길이 없는 자리", ACC)])
d.save("07-01.chapter-overview.svg")
