# 타입 스펙: type-process — 질문 여섯 개가 확정 값 여섯 개로 바뀌고, 그중 수치 둘이 다음 단계의 어림셈 입력으로 넘어간다.
# 사실 출처: 추출본 v2.txt 729~743행·2973~2986행(뉴스 피드 요구사항 대화: 모바일·웹 모두 · 게시와 친구 피드 보기 · 역시간순 · 친구 5000 · DAU 1000만 · 이미지·영상 포함)
# Layout conventions: 질문 열 x=24 폭 224, 값 열 x=312 폭 304, 줄 stride 68(y=116~), 노드 높이 52, 어림셈 상자 x=704 폭 224, 값 열 → 상자 화살표는 두 줄(y+26)에서 수평. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 612
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 03-01 §2",
      "질문 여섯 개가 범위를 확정하고 수치 둘이 규모를 정한다",
      "모바일과 웹 모두, 게시와 친구 피드 보기, 역시간순, 친구 5,000명, 일간 사용자 1,000만 명, 이미지와 영상 포함으로 범위가 정해지고 친구 수와 일간 사용자가 규모를 정하는 수치다.",
      "뉴스 피드 예시의 질문과 답")

QX, QW = 24, 224
AX, AW = 312, 304
NH, STRIDE, Y0 = 52, 68, 116

d.t(QX, Y0 - 16, "물은 것", 13, SOFT, KR, "start", 600)
d.t(AX, Y0 - 16, "확정된 값", 13, SOFT, KR, "start", 600)

ROWS = (
    ("클라이언트", "모바일 · 웹 모두", False),
    ("핵심 기능", "게시 · 친구 피드 보기", False),
    ("정렬", "역시간순", False),
    ("친구 수 상한", "5,000명", True),
    ("하루 사용자", "1,000만 명 (DAU)", True),
    ("피드 내용", "이미지 · 영상 포함", False),
)
ys = []
for i, (q, a, hot) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    ys.append(y)
    d.box(QX, y, QW, NH, PAPER2, RULE, 0.9, 6)
    d.t(QX + QW / 2, y + 32, q, 14, INK, KR, "middle", 600)
    c = ACC if hot else OK
    d.tone(AX, y, AW, NH, c, 6, "12", 1.2)
    d.t(AX + AW / 2, y + 32, a, 14, c, KR, "middle", 600)
    d.arrow([(QX + QW + 2, y + NH // 2), (AX - 6, y + NH // 2)], MUTED, "ar", 1.5)

# 어림셈 입력 상자: 친구 수 · 하루 사용자 두 줄 가운데
BX, BW = 704, 224
by = ys[3]
bh = ys[4] + NH - ys[3]
d.tone(BX, by, BW, bh, ACC, 6, "12", 1.4)
d.t(BX + BW / 2, by + 44, "어림셈 입력", 14, ACC, KR, "middle", 600)
d.t(BX + BW / 2, by + 72, "5,000 · 1,000만", 13, MUTED, MONO)
for y in (ys[3], ys[4]):
    d.arrow([(AX + AW + 2, y + 26), (BX - 6, y + 26)], ACC, "acc", 1.6)

d.legend(H - 56, [("확정된 값", OK), ("어림셈 입력이 되는 값", ACC)])
d.save("03-01.scope-values.svg")
