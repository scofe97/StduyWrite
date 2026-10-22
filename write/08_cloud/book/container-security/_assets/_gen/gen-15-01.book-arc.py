# 타입 스펙: type-process — 맺음말의 네 갈래(멘탈 모델 → 통신 → 계층 방어 → 컨테이너 고유 예방 조치)가 앞 장에 하나씩 이어지고, 마지막 단서가 1장 위협 모델과 부록 질문으로 되돌아간다. semantic-patterns 의 "Stage framework with semantic slots"(주체 없는 단계 지도)이고 focal 은 계층 방어.
# 사실 출처: 노트 L42~L54(네 갈래·8장 gVisor·Kata·Firecracker·10장 보안의 단위·1장 심층 방어·14장 열 가지 단서·1장 위협 모델·부록 질문)
# Layout conventions: 열 폭 184·gap 24(stride 208, x=108~916), 슬롯 h=72·stride 80(y=156), 왼쪽 행 머리 x=24, 아래 갈림 버스 y=412. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


W, H = 960, 580
COL_X, COL_W, STRIDE = 108, 184, 208
HDR_Y, HDR_H = 100, 44
ROW_Y, ROW_H, ROW_STRIDE = 156, 72, 80
FOCAL = 2

d = D(W, H, "CONTAINER SECURITY · 15-01 §1",
      "맺음말의 네 갈래는 앞 장에 하나씩 이어지고 마지막 단서가 위협 모델로 돌아간다",
      "멘탈 모델은 8장, 통신 이해는 10장, 계층 방어는 1장의 심층 방어, 컨테이너 고유 예방 조치는 14장 OWASP 열 가지로 이어진다. "
      "열 가지는 전부가 아니라서 1장 위협 모델로 돌아가 부록 열아홉 질문으로 가장 취약한 곳을 가늠한다.",
      "저자가 독자가 얻었기를 바란다고 적은 네 갈래의 순서와 이어지는 장")

STAGES = [
    ("01", "멘탈 모델",
     ["컨테이너가 무엇인가", "튼튼한 멘탈 모델"],
     ["8장 샌드박스", "gVisor · Kata", "Firecracker"],
     ["격리가 모자랄 때의", "다른 선택지"]),
    ("02", "통신 이해",
     ["컨테이너끼리 · 바깥과", "통신 이해"],
     ["10장", "컨테이너 네트워크 보안"],
     ["배포의 단위이자", "보안의 단위"]),
    ("03", "계층 방어",
     ["계층 방어의 감각"],
     ["1장 보안 원칙", "심층 방어"],
     ["취약점 하나 뒤에", "남아 있는 벽"]),
    ("04", "고유 예방 조치",
     ["웹 공격별", "컨테이너 고유 예방 조치"],
     ["14장", "OWASP Top 10"],
     ["열 가지 목록은", "전부가 아님"]),
]
ROWS = ["얻은 것", "이어지는 장", "한마디"]

for r, name in enumerate(ROWS):
    d.t(24, ROW_Y + r * ROW_STRIDE + ROW_H // 2 + 4, name, 12, MUTED, KR, "start", 600)

for j, (num, title, got, chap, quip) in enumerate(STAGES):
    x = COL_X + j * STRIDE
    c = ACC if j == FOCAL else INFO
    fit(title, 15, COL_W - 56)
    d.tone(x, HDR_Y, COL_W, HDR_H, c, 6, "1F" if j == FOCAL else "14", 1.4 if j == FOCAL else 1.1)
    d.t(x + 14, HDR_Y + 27, num, 11, SOFT, MONO, "start")
    d.t(x + 44, HDR_Y + 28, title, 15, INK, KR, "start", 600)
    if j < len(STAGES) - 1:
        d.arrow([(x + COL_W + 2, HDR_Y + HDR_H // 2), (x + STRIDE - 4, HDR_Y + HDR_H // 2)], SOFT, "soft", 1.4)
    for r, lines in enumerate((got, chap, quip)):
        y = ROW_Y + r * ROW_STRIDE
        if j == FOCAL:
            d.tone(x, y, COL_W, ROW_H, ACC, 6, "0F", 1.0)
        else:
            d.box(x, y, COL_W, ROW_H)
        n = len(lines)
        y0 = y + ROW_H / 2 - (n - 1) * 9 + 4
        for k, ln in enumerate(lines):
            fit(ln, 13, COL_W - 16)
            head = r == 1 and k == 0          # 이어지는 장 행은 첫 줄이 장 번호
            d.t(x + COL_W / 2, y0 + k * 18, ln, 13, MUTED if r == 1 and not head else INK,
                kr(ln), "middle", 600 if head else 400)

# 단서: 네 번째 갈래 아래에서 갈라져 위협 모델과 부록 질문으로
BUS_Y = 412
SX = COL_X + 3 * STRIDE + COL_W // 2   # 824
RX, RW = 108, 392
QX, QW = 524, 392
R_CX, Q_CX = RX + RW // 2, QX + QW // 2   # 304, 720
BOX_Y, BOX_H = 436, 64
d.line(SX, ROW_Y + 2 * ROW_STRIDE + ROW_H, SX, BUS_Y, WARN, 1.5)
d.line(R_CX, BUS_Y, SX, BUS_Y, WARN, 1.5)
d.arrow([(R_CX, BUS_Y), (R_CX, BOX_Y - 4)], WARN, "warn", 1.5)
d.arrow([(Q_CX, BUS_Y), (Q_CX, BOX_Y - 4)], WARN, "warn", 1.5)
d.chip((R_CX + Q_CX) // 2 + 4, BUS_Y, "열 가지 밖의 약점", WARN, 12, 8)

for x, w, t1, t2 in ((RX, RW, "1장 컨테이너 위협 모델", "공격 벡터 다시 훑기"),
                     (QX, QW, "부록 열아홉 질문", "가장 취약한 곳 가늠")):
    d.tone(x, BOX_Y, w, BOX_H, OK, 6, "14", 1.1)
    d.t(x + w // 2, BOX_Y + 28, t1, 14, INK, KR, "middle", 600)
    d.t(x + w // 2, BOX_Y + 48, t2, 13, MUTED, KR, "middle")

d.legend(524, [("책이 되짚는 갈래", INFO), ("체크리스트가 기대는 갈래", ACC), ("열 가지 이후의 단서", WARN), ("읽고 난 뒤 할 일", OK)])
d.save(str(ASSETS / "15-01.book-arc.svg"))
print("ok 15-01 book-arc")
