# 44-02 §1 — 같은 AES 키라도 가능한 키가 몇 가지로 줄어들면 무차별 대입이 몇 번째에 끝나는지를 로그 눈금 막대로 보인다.
# 본문 근거: 이 노트 §1 「암호가 깨지는 자리」의 소절 「무차별 대입과 키 길이」·「키는 무작위로 만든다」.
# 검증 근거: 2026-11-08 macOS(Darwin 25.6.0) OpenSSL 3.6.4 실행. 키 32가지 AES-256 은 32번 중 6번째(색인 5)에 발견되고 0초,
#            시각(초)의 SHA-256 키는 키를 만들고 3초 뒤 기준 후보 126개 중 118번째에 발견되고 2초. 2^127 = 1.70e38 번, 초당 1e12 번이면 5.40e18 년(python 계산).
#            번호와 초는 무작위 선택과 실행 시각에 따라 다르다.
# 타입 스펙: type-bar — 가로 막대. 값이 수십 자리까지 벌어져 눈금을 log10 으로 쓴다(막대 길이 = log10(시도 횟수), 기준선은 10^0 = 1번).
import sys; sys.path.insert(0, ".")
import math
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER, KR, MONO

W, H = 880, 428
PX0, PX1 = 264, 832            # 플롯 가로 범위(10^0 .. 10^40)
DEC = (PX1 - PX0) / 40         # 한 자리(decade) 당 폭
Y0, PITCH, BH = 112, 88, 28

d = D(W, H, "OSTEP · 44-02 §1",
      "가능한 키가 줄면 키 길이는 소용없다",
      "무차별 대입으로 키를 찾을 때 시도해야 하는 횟수를 10의 거듭제곱 눈금으로 그린 가로 막대 세 줄이다. "
      "결함 때문에 가능한 키가 32가지로 줄면 6번째 시도에서 찾고, 시각을 시드로 쓴 키는 후보 126개 중 118번째에서 찾는다. "
      "무작위로 만든 AES-128 키는 평균 1.7×10^38 번을 시도해야 하고 초당 1조 번이어도 약 5.4×10^18 년이 걸린다.",
      "막대 길이는 시도 횟수의 자릿수 — 짧은 두 막대가 키 선택이 무너진 경우")

# 세로 눈금선과 눈금 이름
for k in range(0, 41, 10):
    x = PX0 + k * DEC
    d.line(x, 96, x, 356, RULE, 0.8, None if k == 0 else "3 6")
    lab = "1번" if k == 0 else f"10^{k}"
    d.t(x, 376, lab, 12, MUTED, MONO)
d.t((PX0 + PX1) / 2, 408, "시도 횟수 (로그 눈금)", 12, SOFT)

ROWS = [
    ("결함으로 줄어든 키", "가능한 키 32가지", 32, True,
     "6번째 시도에 발견 · 0초"),
    ("시각을 시드로 쓴 키", "후보 시각 126개", 126, False,
     "118번째 시도에 발견 · 2초"),
    ("무작위 AES-128 키", "평균 2^127 번 시도", 2 ** 127, False,
     "1.7×10^38 번 · 초당 1조 번이면 약 5.4×10^18 년"),
]
for i, (name, sub, n, focal, note) in enumerate(ROWS):
    y = Y0 + i * PITCH
    d.t(PX0 - 16, y + 12, name, 12, INK, KR, "end", 600)
    d.t(PX0 - 16, y + 32, sub, 12, MUTED, KR, "end")
    w = max(4, math.log10(n) * DEC)
    if focal:
        d.tone(PX0, y, w, BH, ACC, 3, "20", 1.4)
    else:
        d.box(PX0, y, w, BH, "#8B98A91F", MUTED, 1.0, 3)
    d.t(PX0 + 4, y + BH + 22, note, 12, ACC if focal else MUTED, KR, "start", 600 if focal else 400)

d.save("44-02.key-space.svg")
