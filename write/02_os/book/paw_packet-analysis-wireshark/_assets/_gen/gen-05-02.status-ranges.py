# 05-02 §4 — HTTP 상태 코드는 구간이 곧 조사 방향이다.
# 본문 요구: "원문은 응답의 첫 줄에 상태 코드가 있다고 짚고 http.response.code 로 거르라고
#            안내합니다." 그리고 마지막 문장이 "오류는 없는데 느린 요청"을 가리킨다.
#            5행 표는 부류·범위·예를 나란히 둘 뿐, 어느 구간을 만났을 때 어디를 볼지를 못 세운다.
#            04-01.alert-ranges 가 같은 문제를 같은 방식으로 풀었다 — 그 배치를 따른다.
# 타입 스펙: type-layers — 하나의 축(번호)을 구간으로 나눈 층. 세로 위치가 곧 번호 구간이고,
#           focal 은 2xx 하나 — 본문이 실제로 찾는 대상("오류는 없는데 느린 요청")이 그 구간이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 720
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §4",
      "상태 코드 구간이 볼 곳을 정한다",
      "상태 코드는 임의의 숫자가 아니라 백 단위로 묶인 구간이다. 첫 자리만 봐도 응답이 어느 성격인지, "
      "그래서 다음에 어디를 볼지가 정해진다. 성능 조사에서 실제로 찾는 것은 오류 구간이 아니라 "
      "2xx 인데 느린 요청이라, 상태 코드와 응답 시간을 함께 걸어야 나온다.",
      "찾는 것은 오류가 아니라 성공했는데 느린 요청입니다")

AX = 150
BX, BW = 210, 720
BH, STRIDE = 76, 92
Y0 = 128

BANDS = [
    ("1xx", "100 ~ 101", "중간 응답", MUTED,
     "100 Continue · 101 Switching protocol", "본 응답이 뒤에 따로 옴", False),
    ("2xx", "200 ~ 206", "성공", ACC,
     "200 OK · 201 Created", "http.time 으로 느린 것 추림", True),
    ("3xx", "300 ~ 308", "재지정", INFO,
     "300 Multiple choices · 301 Moved permanently", "다음 요청의 목적지 확인", False),
    ("4xx", "400 ~ 417", "클라이언트 오류", WARN,
     "400 Bad Request · 401 Unauthorized", "요청 헤더 · 인증 정보", False),
    ("5xx", "500 ~ 505", "서버 오류", BAD,
     "500 Internal Server Error · 501 Not implemented", "서버 로그 · 업스트림", False),
]

d.line(AX, Y0 - 8, AX, Y0 + 4 * STRIDE + BH + 8, RULE, 1.2)
d.t(AX, Y0 - 20, "첫 자리", 11, SOFT, KR)

for i, (tag, rng, name, col, examples, nextstep, focal) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    d.tone(BX, y, BW, BH, col, 8, op="14" if focal else "0A", sw=1.5 if focal else 1.1)
    d.line(AX, y + 24, BX - 8, y + 24, col, 1.2)
    d.t(AX - 12, y + 20, tag, 12, col, MONO, "end", 600)
    d.t(AX - 12, y + 38, rng, 9, SOFT, MONO, "end")
    d.t(BX + 24, y + 28, name, 14, col, KR, "start", 600)
    d.t(BX + 24, y + 50, examples, 10, MUTED, MONO, "start")
    d.chip(BX + BW - 130, y + 30, nextstep, col if focal else SOFT, 10, 8)

d.t(24, 620, "부류로 거르기 — http.response.code >= 400 && http.response.code < 500",
     12, SOFT, KR, "start")
d.t(24, 644, "성능 조사의 실제 대상 — http.response.code == 200 && http.time > 1",
     11, ACC, KR, "start")

d.legend(H - 44, [("성공했는데 느린 구간", ACC), ("재지정", INFO), ("요청 쪽 원인", WARN), ("서버 쪽 원인", BAD)])
d.save("05-02.status-ranges.svg")
