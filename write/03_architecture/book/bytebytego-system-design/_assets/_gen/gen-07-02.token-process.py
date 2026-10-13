# 타입 스펙: type-process — 카드 번호(PAN) 하나가 토큰화 시스템에서 토큰이 되어 가맹점에 남고, 결제 때 토큰이 다시 PAN 으로 바뀌는 다섯 단계. 같은 세 자리(요청 앱·토큰화 시스템·vault)를 단계마다 다시 그려 어느 자리에 PAN 이 있고 어느 자리에 토큰이 있는지를 값으로 보인다.
# 사실 출처: PCI SSC PCI DSS Tokenization Guidelines(2011-08) §2.2 Figure 1(요청 앱이 PAN 을 보내면 시스템이 토큰을 만들어 vault 에 기록하고 돌려준다 = 도식의 1~3단계)와 Table 1
#   도식의 4·5단계(가맹점이 토큰만 보내고 토큰화 시스템이 vault 조회로 PAN 을 복원)는 이 문서의 de-tokenization 설명(Figure 2 는 PAN 을 요청 앱에 돌려준다)을 이 편이 가맹점 범위 축소 원칙에 맞춰 옮긴 설명용 배치다.
#   (PAN 5994 0059 0172 3383 → 토큰 599400x18523mw4cw3383, 앞 6자리와 뒤 4자리 유지).
# Layout conventions: 라벨 열 x=24 폭 168, 단계 열 stride 156(x=204+156k, 셀 폭 152), 행 stride 96(y=152 부터 3행), 머리 행 y=96. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 520
d = D(W, H, "BYTEBYTEGO · 07-02 §5",
      "가맹점에는 토큰만 남고 PAN 은 vault 에만 있다",
      "단계마다 PAN 과 토큰이 어느 자리에 있는지 같은 세 자리를 다시 그려 따라갑니다.",
      "값은 PCI SSC 문서의 예시이고 1~3단계가 그 문서의 흐름, 4·5단계는 설명용 배치입니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


PAN, TOK = "5994 0059 0172 3383", "599400x18523mw4cw3383"
LX, LW, CX0, CSTR, CWID = 24, 168, 204, 156, 152
Y_H, Y0, RS = 96, 152, 96
steps = ["1 PAN 전달", "2 토큰 생성·기록", "3 토큰 반환", "4 결제 요청", "5 토큰 → PAN"]
rows = [
    ("요청 앱 · 가맹점 쪽", "app", {0: ("PAN", PAN, WARN), 2: ("토큰만 저장", TOK, OK), 3: ("토큰 전송", TOK, OK)}),
    ("토큰화 시스템", "tokenization system", {1: ("PAN → 토큰", TOK, INFO), 4: ("토큰 → PAN", PAN, INFO)}),
    ("카드 데이터 vault", "card data vault", {1: ("쌍 기록", PAN, WARN), 4: ("토큰 조회", TOK, INFO)}),
]

for k, s in enumerate(steps):
    x = CX0 + k * CSTR
    foc = k == 2
    if foc:
        d.tone(x, Y_H - 4, CWID, 36, ACC, 4, "14", 1.4)
    else:
        d.box(x, Y_H - 4, CWID, 36, PAPER2, RULE, 0.9, 4)
    d.t(x + CWID / 2, Y_H + 19, s, 13, ACC if foc else INK, _kr(s), "middle", 600)

for r, (name, sub, cells) in enumerate(rows):
    y = Y0 + r * RS
    d.line(LX, y - 4, W - 24, y - 4, RULE, 0.5)
    d.t(LX, y + 48, name, 13, INK, KR, "start", 600)
    for k, (a, v, c) in cells.items():
        x = CX0 + k * CSTR
        foc = (r, k) == (0, 2)
        if foc:
            d.tone(x, y + 4, CWID, 76, ACC, 4, "14", 1.4)
        else:
            d.tone(x, y + 4, CWID, 76, c, 4, "18", 1.0)
        d.t(x + CWID / 2, y + 30, a, 13, ACC if foc else c, _kr(a), "middle", 600)
        if r == 2 and k == 1:
            d.t(x + CWID / 2, y + 50, PAN, 11, INK, MONO, "middle")
            d.t(x + CWID / 2, y + 68, TOK, 11, INK, MONO, "middle")
        else:
            d.t(x + CWID / 2, y + 56, v, 11, INK, MONO, "middle")

d.line(LX, Y0 + 3 * RS - 4, W - 24, Y0 + 3 * RS - 4, RULE, 0.5)
d.legend(H - 56, [("PAN 이 있는 자리", WARN), ("토큰이 있는 자리", OK), ("변환 자리", INFO), ("이 절의 초점", ACC)])
d.save("07-02.token-process.svg")
