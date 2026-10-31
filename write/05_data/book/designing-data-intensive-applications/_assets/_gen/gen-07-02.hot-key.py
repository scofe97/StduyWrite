# 07-02 §6 핫 키 우회 — 2자리 랜덤 숫자를 붙여 100개 키로 쓰기를 나누고, 읽을 때 100개 키를 모두 조회해 합산.
# 사실 출처: 07-02 본문 §6(L92~L94), DDIA 2판 7장 p.17 "Skewed Workloads and Relieving Hot Spots"
# 원서·본문은 "100개 키"라 했다(샤드 수는 말하지 않음). 이전 판의 'post_9921' 예시 키와 "100개 샤드"·병렬·Scatter 는 걷어냈다.
# 타입 스펙: type-process
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 34
Y_WRITE = 154
H_BAND = 118
Y_READ = 286
LEG = Y_READ + H_BAND + 28
H = LEG + 56

d = D(W, H, "07-02 · §6 PROCESS", "핫 키를 100개 키로 나눠 쓰고 모두 읽어 합산",
      "요청이 몰리는 핫 키 앞뒤에 2자리 랜덤 숫자를 붙여 100개 키로 쓰기를 나누고, 읽을 때는 100개 키를 모두 조회해 합산한다.",
      "2자리 랜덤 숫자 · 100개 키에 쓰기 · 100개 키 조회 후 합산")

# 상단 안내 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 22, "핫 키 앞뒤에 2자리 랜덤 숫자 → 서로 다른 키 100개 · 읽기는 100개 키 모두 조회 후 합산", 12, INK, KR, "middle", 600)

# ── Band 1: 쓰기 경로 (Write Path) ──
d.box(28, Y_WRITE, W - 56, H_BAND, PAPER2, ACC, 1.2)
d.chip(92, Y_WRITE + 20, "쓰기 경로", ACC, 12)
d.t(160, Y_WRITE + 24, "쓰기는 100개 키에 고르게", 12, SOFT, KR, "start")
d.line(38, Y_WRITE + 34, W - 38, Y_WRITE + 34, RULE, 0.8)

# 1-1. 핫 키 입력
d.box(42, Y_WRITE + 46, 170, 56, PAPER, RULE, 0.8)
d.t(127, Y_WRITE + 68, "핫 키 쓰기 요청", 12, INK, KR, "middle", 600)
d.t(127, Y_WRITE + 86, "key", 11, ACC, MONO, "middle")

d.arrow([(214, Y_WRITE + 74), (252, Y_WRITE + 74)], ACC, "acc", 1.4)

# 1-2. 난수 접미어 부착
d.tone(254, Y_WRITE + 46, 210, 56, ACC, 4, "18", 1.1)
d.t(359, Y_WRITE + 68, "2자리 랜덤 숫자 붙이기", 12, INK, KR, "middle", 600)
d.t(359, Y_WRITE + 86, "앞뒤에 00 ~ 99", 11, ACC, KR, "middle")

d.arrow([(466, Y_WRITE + 74), (504, Y_WRITE + 74)], ACC, "acc", 1.4)

# 1-3. 100개 분할 키
d.box(506, Y_WRITE + 46, 170, 56, PAPER, RULE, 0.8)
d.t(591, Y_WRITE + 66, "서로 다른 키 100개", 12, INK, KR, "middle", 600)
d.t(591, Y_WRITE + 86, "숫자 00 ~ 99 마다 하나", 11, SOFT, KR, "middle")

d.arrow([(678, Y_WRITE + 74), (716, Y_WRITE + 74)], ACC, "acc", 1.4)

# 1-4. 100개 샤드 분산 쓰기
d.tone(718, Y_WRITE + 46, 120, 56, ACC, 4, "18", 1.1)
d.t(778, Y_WRITE + 68, "100개 키", 12, INK, KR, "middle", 600)
d.t(778, Y_WRITE + 86, "쓰기 분산", 11, ACC, KR, "middle")

# ── Band 2: 읽기 경로 (Read Path) ──
d.box(28, Y_READ, W - 56, H_BAND, PAPER2, RULE, 0.9)
d.chip(92, Y_READ + 20, "읽기 경로", INFO, 12)
d.t(160, Y_READ + 24, "100개 키를 모두 조회해 합산", 12, SOFT, KR, "start")
d.line(38, Y_READ + 34, W - 38, Y_READ + 34, RULE, 0.8)

# 2-1. 읽기 요청
d.box(42, Y_READ + 46, 170, 56, PAPER, RULE, 0.8)
d.t(127, Y_READ + 68, "핫 키 읽기 요청", 12, INK, KR, "middle", 600)
d.t(127, Y_READ + 86, "key", 11, INFO, MONO, "middle")

d.arrow([(214, Y_READ + 74), (252, Y_READ + 74)], INFO, "info", 1.4)

# 2-2. 100개 키 모두 조회
d.tone(254, Y_READ + 46, 210, 56, INFO, 4, "18", 1.1)
d.t(359, Y_READ + 68, "100개 키 모두 조회", 12, INK, KR, "middle", 600)
d.t(359, Y_READ + 86, "100개 키 전부", 11, INFO, KR, "middle")

d.arrow([(466, Y_READ + 74), (504, Y_READ + 74)], INFO, "info", 1.4)

# 2-3. 합산
d.tone(506, Y_READ + 46, 170, 56, OK, 4, "18", 1.1)
d.t(591, Y_READ + 68, "읽은 값 합산", 12, INK, KR, "middle", 600)
d.t(591, Y_READ + 86, "100개 결과를 하나로", 11, OK, KR, "middle")

d.arrow([(678, Y_READ + 74), (716, Y_READ + 74)], WARN, "warn", 1.4)

# 2-4. 별도 관리 (본문 L94: 핫 키 추적·단일 키로 되돌리기)
d.tone(718, Y_READ + 46, 120, 56, WARN, 4, "18", 1.1)
d.t(778, Y_READ + 68, "별도 관리", 12, INK, KR, "middle", 600)
d.t(778, Y_READ + 86, "핫 키 추적", 11, WARN, KR, "middle")

d.legend(LEG, [("쓰기 분산", ACC), ("읽기 조회", INFO), ("결과 합산", OK), ("관리 부담", WARN)])
d.save("07-02.hot-key.svg")
