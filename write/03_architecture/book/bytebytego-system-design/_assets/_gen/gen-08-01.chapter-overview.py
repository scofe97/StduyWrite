# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·대표 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: §1 Timelines at Scale(QCon, Raffi Krikorian) 슬라이드의 30 만/초 전달·팔로워 31 million, §2 Google Drive Blog 2010-09-23 의 Luiz·John 예(InsertText 'Hello' @1 · ' world' @6 · '!' @1), §3 Slack Engineering 2017-03-03 글의 알림 판정 흐름도, §4 추출본 v1.txt 1152~1200행·PDF 쪽 45·46 그림(비트 10칸·해시 셋), §5 DeepMind AlphaCode 글과 arXiv 2203.07814(상위 54.3%·10 개 대회·후보 10 개).
# Layout conventions: 카드 폭 168·높이 212, 가로 stride 184(x=20+184k), 카드 y=112, 화살표는 카드 중앙 y=218. 5 카드. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 08-01",
      "한 요청이 규모에서 막히는 자리 다섯",
      "타임라인·동시 편집·알림 판정·중복 URL·코드 생성이 값 하나씩을 들고 이어집니다.",
      "다섯 절이 값 하나씩을 들고 이어집니다")

CW, CH, STRIDE, X0, Y0 = 168, 212, 184, 20, 112
cards = [
    ("§1", "타임라인 팬아웃", "31,000,000 쓰기", "÷ 300,000/초", "쓸 때 밀어 넣기", ACC),
    ("§2", "동시 편집 변환", "!@1 → @6 → @12", "Hello world!", "연산 위치를 옮김", INFO),
    ("§3", "알림 판정 순서", "음소거 · DnD · pref", "예 → 안 보냄", "서버가 먼저 거름", INFO),
    ("§4", "중복 URL 거르기", "10 비트 · 해시 3개", "0 이 있으면 없음", "블룸 필터", INFO),
    ("§5", "AlphaCode", "표본 대량 → 10 개", "상위 54.3%", "만든 뒤 거르기", INFO),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, Y0 + 24, tag, 12, SOFT, MONO, "start")
    d.t(cx, Y0 + 52, title, 13, c if c == ACC else INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 68, x + CW - 12, Y0 + 68, RULE, 0.6)
    d.t(cx, Y0 + 104, v1, 12, c, KR if any("가" <= ch <= "힣" for ch in v1) else MONO, "middle", 600)
    d.t(cx, Y0 + 132, v2, 12, INK, KR if any("가" <= ch <= "힣" for ch in v2) else MONO, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("08-01.chapter-overview.svg")
