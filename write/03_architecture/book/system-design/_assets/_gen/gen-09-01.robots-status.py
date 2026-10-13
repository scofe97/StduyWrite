# 타입 스펙: type-flowchart — robots.txt 요청의 응답 상태 코드가 크롤러의 행동을 셋으로 가른다. 다이아몬드 하나·출구 셋, 모든 출구에 라벨.
# 사실 출처: RFC 9309 §2.3.1.1(성공 → 파싱한 규칙을 따름)·§2.3.1.3(Unavailable = 4xx → 어떤 자원이든 접근해도 됨)·§2.3.1.4(Unreachable = 5xx·네트워크 오류 → 전부 금지로 간주),
#   https://www.rfc-editor.org/rfc/rfc9309 . 404·503 은 각 범주의 예시 코드, 호스트는 en.wikipedia.org.
# Layout conventions: 시작 타원 폭 320·높이 48, 다이아몬드 반폭 140·반높이 56(중심 480,250), 결과 상자 폭 240·높이 96(x=56·360·664, y=372). 모든 좌표 4의 배수. 화살표는 수평·수직만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, KR, MONO

W, H = 960, 564
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 09-01 §5",
      "robots.txt 는 응답 코드가 행동을 정한다",
      "받아 온 규칙은 그대로 따르고, 파일이 없으면 모두 허용하며, 서버가 응답하지 못하면 모두 금지로 본다.",
      "200 은 규칙대로, 404 는 전부 허용, 503 은 전부 금지")

# 시작
d.tone(320, 100, 320, 48, INFO, 24, "10", 1.1)
d.t(480, 130, "GET en.wikipedia.org/robots.txt", 13, INK, MONO, "middle", 600)
d.arrow([(480, 152), (480, 190)], MUTED, "ar", 1.4)

# 다이아몬드
d.o.append(f'<polygon points="480,194 620,250 480,306 340,250" fill="{INFO}14" stroke="{INFO}" stroke-width="1.2"/>')
d.t(480, 256, "응답 상태", 15, INK, KR, "middle", 600)

# 출구 셋
d.arrow([(336, 250), (176, 250), (176, 368)], MUTED, "ar", 1.4)
d.arrow([(480, 310), (480, 368)], MUTED, "ar", 1.4)
d.arrow([(624, 250), (784, 250), (784, 368)], MUTED, "ar", 1.4)
d.chip(256, 250, "2xx · 200", OK, 12)
d.chip(480, 338, "4xx · 404", WARN, 12)
d.chip(704, 250, "5xx · 503", BAD, 12)

for x, c, title, sub in ((56, OK, "규칙 적용", "파싱한 규칙대로"),
                         (360, WARN, "전부 허용", "규칙이 없는 것으로"),
                         (664, BAD, "전부 금지", "읽을 수 있을 때까지")):
    d.tone(x, 372, 240, 96, c, 6, "12", 1.2)
    d.t(x + 120, 416, title, 16, INK, KR, "middle", 600)
    d.t(x + 120, 444, sub, 13, MUTED, KR, "middle")

d.legend(H - 56, [("판정", INFO), ("규칙 적용", OK), ("접근 가능으로 간주", WARN), ("접근 불가로 간주", BAD)])
d.save("09-01.robots-status.svg")
