# 04-01 §2 — 인메모리 해시 인덱스 구조와 네 가지 설계 한계.
# 키를 로그 파일의 바이트 offset에 매핑해 1회 seek 로 읽기를 가속하되, 디스크 고갈·RAM 적재·비영속·범위 쿼리 한계를 갖는다.
# 사실 출처: 04-01 §2(L59~L75), 원서 Ch.4 §Log-Structured Storage Figure 4-1(p.4: 12→0, 42→60).
# offset 125 는 원서 `cat database` 출력의 앞 두 줄 바이트 길이(60+65)로 계산한 값이다.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, BAD, KR, MONO

W = 880
PY1 = 104
PH1 = 196
PY2 = 332
PH2 = 84
LEG = 444
H = LEG + 56

d = D(W, H, "04-01 · HASH INDEX", "인메모리 해시 인덱스 구조와 네 가지 한계",
      "인메모리 해시 맵이 각 키를 디스크 로그 파일의 바이트 offset에 매핑해 seek 한 번으로 값을 읽지만, 메모리 적재와 비영속의 구조적 한계를 갖는다.",
      "인메모리 바이트 offset 매핑 · 1회 디스크 seek 조회 · 네 가지 구조적 제약")

# --- 1. 인메모리 해시 맵 (RAM) ---
d.box(24, PY1, 316, PH1, PAPER2, RULE, 1.0)
d.t(36, PY1 + 22, "인메모리 해시 맵 (RAM)", 13, INK, KR, "start", 600)
d.t(36, PY1 + 42, "키를 바이트 offset에 매핑", 12, SOFT, KR, "start")

d.box(36, PY1 + 56, 292, 28, PAPER, RULE, 0.8)
d.t(96, PY1 + 74, "키 (key)", 12, SOFT, KR, "middle", 600)
d.t(240, PY1 + 74, "바이트 offset", 12, SOFT, KR, "middle", 600)

# Memory Row 1
d.box(36, PY1 + 88, 292, 36, PAPER, RULE, 0.8)
d.t(96, PY1 + 110, "12", 12, INK, MONO, "middle")
d.t(240, PY1 + 110, "0", 12, MUTED, MONO, "middle")

# Memory Row 2 (Focal)
d.tone(36, PY1 + 128, 292, 56, ACC, 6, "20", 1.4)
d.t(96, PY1 + 152, "42", 13, ACC, MONO, "middle", 600)
d.t(240, PY1 + 152, "125", 13, ACC, MONO, "middle", 600)
d.t(182, PY1 + 172, "최신 쓰기 반영 (60 → 125 갱신)", 12, ACC, KR, "middle")

# --- 2. append-only 로그 파일 (디스크) ---
d.box(468, PY1, 388, PH1, PAPER2, RULE, 1.0)
d.t(480, PY1 + 22, "append-only 로그 파일 (디스크)", 13, INK, KR, "start", 600)
d.t(480, PY1 + 42, "database 파일 끝에 레코드 누적", 12, SOFT, KR, "start")

# Disk Row 0
d.box(480, PY1 + 56, 364, 36, PAPER, RULE, 0.8)
d.chip(532, PY1 + 74, "offset 0", INFO, 11)
d.t(580, PY1 + 78, "12,{\"name\":\"London\",...}", 11, MUTED, MONO, "start")

# Disk Row 1
d.box(480, PY1 + 96, 364, 36, PAPER, RULE, 0.8)
d.chip(536, PY1 + 114, "offset 60", WARN, 11)
d.t(584, PY1 + 118, "42,{...[\"Golden Gate Bridge\"]}", 11, MUTED, MONO, "start")
d.t(832, PY1 + 118, "옛 값", 12, WARN, KR, "end")

# Disk Row 2 (Focal)
d.tone(480, PY1 + 136, 364, 48, ACC, 6, "20", 1.4)
d.chip(540, PY1 + 160, "offset 125", ACC, 11)
d.t(588, PY1 + 164, "42,{...[\"Exploratorium\"]}", 11, INK, MONO, "start")
d.t(832, PY1 + 164, "최신값", 12, ACC, KR, "end")

# --- 3. 1회 seek 연결 화살표 ---
d.arrow([(328, PY1 + 160), (476, PY1 + 160)], ACC, "acc", 1.5)
d.t(402, PY1 + 148, "1회 seek 직접 읽기", 12, ACC, KR, "middle", 600)
d.t(402, PY1 + 176, "캐시 적재 시 I/O 0", 12, MUTED, KR, "middle")

# --- 4. 인메모리 해시 인덱스의 4가지 구조적 한계 ---
d.t(24, PY2 - 12, "해시 인덱스의 4가지 구조적 한계", 13, INK, KR, "start", 600)

CW = 196
GAP = 16
X0 = 24

cards = [
    ("1. 디스크 공간 고갈", "덮어써진 옛 항목", "디스크 공간 미회수", "계속 쓰면 고갈", WARN),
    ("2. 해시 맵 비영속", "재시작 시 RAM 맵 소실", "전체 로그 재스캔 필수", "재시작 지연", WARN),
    ("3. RAM 용량 한계", "모든 키가 메모리에 적재", "디스크 해시는 I/O·충돌 비용", "대용량 키 제약", BAD),
    ("4. 범위 쿼리 비효율", "10000~19999 일괄 스캔 불가", "키마다 따로 조회", "SSTable·B-tree 대안", BAD),
]

for i, (title, l1, l2, tag, col) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    d.tone(x, PY2, CW, PH2, col, 6, "18", 1.0)
    d.t(x + 12, PY2 + 20, title, 12, col, KR, "start", 600)
    d.t(x + 12, PY2 + 38, l1, 12, MUTED, KR, "start")
    d.t(x + 12, PY2 + 54, l2, 12, MUTED, KR, "start")
    d.t(x + CW - 12, PY2 + 72, tag, 12, col, KR, "end")

d.legend(LEG, [("최신 offset (focal)", ACC), ("해시·로그 구조", INFO), ("공간·복구 한계", WARN), ("메모리·쿼리 제약", BAD)])
d.save("04-01.log-hash-index.svg")
