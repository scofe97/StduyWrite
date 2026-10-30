# 03-01 §2 — 1970년 관계형 모델 제안부터 NoSQL과 문서 모델의 대중화까지의 연대표.
# 사실 출처: 03-01 §2(L51~L63), 원서 Ch.3 Relational Versus Document Models §The Birth of NoSQL
# 타입 스펙: type-timeline
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, KR, MONO

W = 880
BASE_Y = 250
TOP_Y = 120
BOT_Y = 300
CH = 76
LEG = BOT_Y + CH + 40
H = LEG + 56

d = D(W, H, "03-01 · RELATIONAL VS DOCUMENT HISTORY", "관계형과 문서 모델의 약사",
      "1970년 관계형 제안 이후 RDBMS가 표준으로 안착했고, 2010년대 NoSQL 운동을 거쳐 JSON 문서 모델이 대중화됐다.",
      "관계형 제안 · RDBMS 지배 · 경쟁 모델 퇴조 · NoSQL 문서 모델 대중화 · 관계형의 JSON 흡수")

def circle(cx, cy, r=4, fill=PAPER2, stroke=RULE, sw=1.2):
    d.o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

# 가로 기준선 (하이라인)
d.line(40, BASE_Y, 840, BASE_Y, RULE, 1.0)

# 연도 눈금 (10년 주기)
ticks = [
    (70, "1970"),
    (205, "1980"),
    (340, "1990"),
    (475, "2000"),
    (610, "2010"),
    (745, "2020"),
]

for tx, yr in ticks:
    d.line(tx, BASE_Y - 4, tx, BASE_Y + 4, SOFT, 0.8)
    d.t(tx, BASE_Y + 18, yr, 10, SOFT, MONO, "middle")

# 이벤트 정의: (cx, is_top, card_x, card_w, year_txt, title, sub, color, is_focal)
events = [
    (70, True, 20, 148, "1970 · Codd", "관계형 모델 제안", "테이블·튜플 이론", INFO, False),
    (156, False, 82, 160, "1970~80년대 초", "네트워크·계층 모델", "초기 경쟁 접근", MUTED, False),
    (272, True, 200, 148, "1980년대 중반", "RDBMS·SQL 지배", "규칙적 데이터 표준", OK, False),
    (368, False, 290, 168, "1980년대 말~90년대 초", "객체 데이터베이스", "일시적 부상 후 쇠퇴", MUTED, False),
    (502, True, 430, 148, "2000년대 초", "XML 데이터베이스", "SQL의 기능 흡수", MUTED, False),
    (640, False, 560, 160, "2010년대 · NoSQL", "문서 모델의 대중화", "MongoDB · JSON 저장", ACC, True),
    (750, True, 680, 156, "현재 · 공존", "RDB의 JSON 흡수", "관계형·문서의 병행", OK, False),
]

for cx, is_top, bx, bw, yr_txt, title, sub, c, is_focal in events:
    card_y = TOP_Y if is_top else BOT_Y
    line_y1 = card_y + CH if is_top else card_y
    
    # 카드 외곽
    if is_focal:
        d.tone(bx, card_y, bw, CH, ACC, 6, "18", 1.4)
    elif c in (OK, INFO):
        d.tone(bx, card_y, bw, CH, c, 6, "14", 1.1)
    else:
        d.box(bx, card_y, bw, CH, PAPER2, RULE, 0.9)
    
    # 텍스트
    d.t(bx + bw / 2, card_y + 22, yr_txt, 12, c if is_focal else (INFO if c == INFO else SOFT), KR, "middle", 600)
    d.t(bx + bw / 2, card_y + 44, title, 13, INK, KR, "middle", 600)
    d.t(bx + bw / 2, card_y + 64, sub, 12, MUTED, KR, "middle")
    
    # 연결선 및 원
    d.line(cx, line_y1, cx, BASE_Y, c if is_focal else RULE, 1.2 if is_focal else 0.8)
    
    if is_focal:
        circle(cx, BASE_Y, 6, ACC, PAPER, 1.4)
    else:
        circle(cx, BASE_Y, 4, c if c in (OK, INFO) else PAPER2, c if c in (OK, INFO) else RULE, 1.2)

d.legend(LEG, [("NoSQL 문서 모델 (focal)", ACC), ("관계형 표준·공존", OK), ("관계형 모델 제안", INFO), ("경쟁 모델 (퇴조)", MUTED)])
d.save("03-01.relational-document-history.svg")
