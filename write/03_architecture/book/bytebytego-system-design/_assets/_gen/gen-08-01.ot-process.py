# 타입 스펙: type-process — Luiz 와 John 이 같은 빈 문서에 동시에 쓴 두 삽입이 서버를 거치며 위치가 한 번씩 옮겨져 같은 문서로 수렴하는 네 단계. 칸마다 연산·위치·결과 문자열이 같은 자리에 반복되고 화살표가 시간 순서를 나른다.
# 사실 출처: Google Drive Blog 2010-09-23 "What's different about the new Google Docs: Making collaboration fast" — {InsertText 'Hello' @1}, {InsertText ' world' @6}, John 의 {InsertText '!' @1} 가 Hello 를 만나 5 만큼, ' world' 를 만나 6 만큼 밀려 Revision 3 으로 저장, 결과 "Hello world!". https://drive.googleblog.com/2010/09/whats-different-about-new-google-docs.html
#   @6 → @12 는 같은 글의 "shifted the index over by 6" 를 더한 값이다(6 + 6 = 12, 'Hello world' 11 글자 뒤).
# Layout conventions: 카드 폭 204·높이 212, 가로 stride 228(x=24+228k), 카드 y=112, 화살표는 카드 중앙 y=218. 4 카드. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

assert 1 + 5 == 6 and 6 + 6 == 12 and len("Hello world") + 1 == 12

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 08-01 §2",
      "동시 삽입은 서버를 지나며 위치가 두 번 옮겨진다",
      "John 의 느낌표는 @1 에서 출발해 Hello 와 ' world' 뒤로 밀려 @12 에 저장됩니다",
      "Luiz · John · 서버가 같은 문서 Hello world! 로 수렴")

CW, CH, STRIDE, X0, Y0 = 204, 212, 228, 24, 112
cards = [
    ("1", "Luiz 가 입력", "'Hello' @1", "대기 ' world' @6", "서버 리비전 1", INK),
    ("2", "John 이 변환", "'!' @1 → @6", "Hello 뒤로 +5", "아직 보내지 않은 변경", INFO),
    ("3", "서버가 변환", "'!' @6 → @12", "' world' 뒤로 +6", "리비전 3 으로 저장", ACC),
    ("4", "모두 같은 문서", "Hello world!", "리비전 1·2·3 적용", "Luiz · 서버 · John", OK),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
    elif c == OK:
        d.tone(x, Y0, CW, CH, OK, 6, "14", 1.0)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, Y0 + 24, tag, 12, SOFT, KR, "start")
    d.t(cx, Y0 + 52, title, 14, c if c in (ACC, OK) else INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 68, x + CW - 12, Y0 + 68, RULE, 0.6)
    d.t(cx, Y0 + 104, v1, 13, c, MONO, "middle", 600)
    d.t(cx, Y0 + 132, v2, 12, INK, KR if any("가" <= ch <= "힣" for ch in v2) else MONO, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("서버 변환", ACC), ("수렴한 문서", OK), ("클라이언트 변환", INFO)])
d.save("08-01.ot-process.svg")
