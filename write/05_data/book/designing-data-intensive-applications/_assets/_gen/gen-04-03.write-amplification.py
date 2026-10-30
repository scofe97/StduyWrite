# 04-03 §4 — 애플리케이션의 1회 쓰기 요청이 B-tree와 LSM에서 디스크 쓰기로 불어나는 write amplification 데이터 흐름.
# 바이트 수·배수는 본문·원서에 없어 넣지 않는다(10-30 검증에서 100 Byte·수십 배 제거).
# 사실 출처: 04-03 본문 §4(L64~L72) — B-tree WAL+페이지 최소 2회 쓰기 및 소규모 변경 시 4~16 KiB 전체 페이지 쓰기, LSM WAL+memtable flush+compaction, 청크 압축으로 낮은 증폭, SSD 마모 완화.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY1 = 104
LH = 148
PY2 = PY1 + LH + 20
LEG = PY2 + LH + 28
H = LEG + 56

d = D(W, H, "04-03 · WRITE AMPLIFICATION DATA FLOW", "B-tree와 LSM 디스크 쓰기 증폭 경로",
      "애플리케이션 쓰기 하나가 두 저장 엔진에서 디스크 쓰기 여러 번으로 늘어나는 경로를 따라간다.",
      "애플리케이션 요청 → WAL 기록 → 디스크 페이지 덮어쓰기 / SSTable 압축 플러시 → 증폭 결과")

# === 1. 상단 레인: B-tree 제자리 덮어쓰기 경로 ===
d.box(24, PY1, 832, LH, PAPER, WARN, 1.1)
d.t(40, PY1 + 24, "B-tree 경로 — 고정 페이지 덮어쓰기", 13, INK, KR, "start", 600)
d.chip(460, PY1 + 22, "최소 2회 쓰기 · 페이지 단위 증폭", WARN, 11)

XS = [40, 234, 436, 642]
WS = [164, 172, 176, 198]
Y_BOX1 = PY1 + 44
BH = 80
YM1 = Y_BOX1 + BH / 2

# B-1: 앱 쓰기
d.box(XS[0], Y_BOX1, WS[0], BH, PAPER2, INFO, 1.0)
d.t(XS[0] + WS[0] / 2, Y_BOX1 + 26, "앱 쓰기 요청", 12, INK, KR, "middle", 600)
d.t(XS[0] + WS[0] / 2, Y_BOX1 + 46, "몇 바이트 키 갱신", 12, INK, KR, "middle")
d.t(XS[0] + WS[0] / 2, Y_BOX1 + 64, "단일 레코드 수정", 11, MUTED, KR, "middle")

# B-2: WAL 기록
d.box(XS[1], Y_BOX1, WS[1], BH, PAPER2, OK, 1.1)
d.t(XS[1] + WS[1] / 2, Y_BOX1 + 26, "1. WAL 선행 기록", 12, OK, KR, "middle", 600)
d.t(XS[1] + WS[1] / 2, Y_BOX1 + 46, "로그에 한 번 append", 12, INK, KR, "middle")
d.t(XS[1] + WS[1] / 2, Y_BOX1 + 64, "디스크 fsync 1회", 11, MUTED, KR, "middle")

# B-3: 디스크 페이지 덮어쓰기
d.tone(XS[2], Y_BOX1, WS[2], BH, WARN, 6, "18", 1.2)
d.t(XS[2] + WS[2] / 2, Y_BOX1 + 26, "2. 페이지 제자리 덮어쓰기", 12, WARN, KR, "middle", 600)
d.t(XS[2] + WS[2] / 2, Y_BOX1 + 46, "4~16 KiB 전체 페이지", 12, INK, MONO, "middle")
d.t(XS[2] + WS[2] / 2, Y_BOX1 + 64, "소규모 수정도 전체 쓰기", 11, MUTED, KR, "middle")

# B-4: 증폭 결과
d.box(XS[3], Y_BOX1, WS[3], BH, PAPER2, WARN, 1.3)
d.t(XS[3] + WS[3] / 2, Y_BOX1 + 26, "최소 두 번 디스크 쓰기", 12, WARN, KR, "middle", 600)
d.t(XS[3] + WS[3] / 2, Y_BOX1 + 46, "몇 바이트에도 전체 페이지", 12, INK, KR, "middle")
d.t(XS[3] + WS[3] / 2, Y_BOX1 + 64, "분할 시 추가 페이지 덮어쓰기", 11, MUTED, KR, "middle")

# 화살표 3개
for i in range(3):
    x1 = XS[i] + WS[i]
    x2 = XS[i + 1]
    d.arrow([(x1 + 4, YM1), (x2 - 4, YM1)], MUTED, "ar", 1.3)


# === 2. 하단 레인: LSM 순차 압축 쓰기 경로 (FOCAL) ===
d.box(24, PY2, 832, LH, PAPER, ACC, 1.3)
d.t(40, PY2 + 24, "LSM 경로 — 불변 파일 압축 순차 쓰기", 13, ACC, KR, "start", 600)
d.chip(460, PY2 + 22, "압축 청크 순차 기록 · 낮은 증폭", ACC, 11)

Y_BOX2 = PY2 + 44
YM2 = Y_BOX2 + BH / 2

# L-1: 앱 쓰기
d.box(XS[0], Y_BOX2, WS[0], BH, PAPER2, INFO, 1.0)
d.t(XS[0] + WS[0] / 2, Y_BOX2 + 26, "앱 쓰기 요청", 12, INK, KR, "middle", 600)
d.t(XS[0] + WS[0] / 2, Y_BOX2 + 46, "키 하나 쓰기", 12, INK, KR, "middle")
d.t(XS[0] + WS[0] / 2, Y_BOX2 + 64, "단일 레코드 추가", 11, MUTED, KR, "middle")

# L-2: WAL 기록
d.box(XS[1], Y_BOX2, WS[1], BH, PAPER2, OK, 1.1)
d.t(XS[1] + WS[1] / 2, Y_BOX2 + 26, "1. WAL 선행 기록", 12, OK, KR, "middle", 600)
d.t(XS[1] + WS[1] / 2, Y_BOX2 + 46, "로그에 한 번 append", 12, INK, KR, "middle")
d.t(XS[1] + WS[1] / 2, Y_BOX2 + 64, "디스크 순차 플러시", 11, MUTED, KR, "middle")

# L-3: Memtable 누적 후 플러시 & Compaction
d.box(XS[2], Y_BOX2, WS[2], BH, PAPER2, INFO, 1.0)
d.t(XS[2] + WS[2] / 2, Y_BOX2 + 26, "2. SSTable 순차 플러시", 12, INFO, KR, "middle", 600)
d.t(XS[2] + WS[2] / 2, Y_BOX2 + 46, "청크 압축 일괄 쓰기", 12, INK, KR, "middle")
d.t(XS[2] + WS[2] / 2, Y_BOX2 + 64, "compaction 마다 다시 쓰기", 11, MUTED, KR, "middle")

# L-4: 증폭 결과 (FOCAL)
d.tone(XS[3], Y_BOX2, WS[3], BH, ACC, 6, "20", 1.4)
d.t(XS[3] + WS[3] / 2, Y_BOX2 + 26, "상대적 낮은 디스크 증폭", 12, ACC, KR, "middle", 600)
d.t(XS[3] + WS[3] / 2, Y_BOX2 + 46, "청크 압축으로 공간 절감", 12, INK, KR, "middle")
d.t(XS[3] + WS[3] / 2, Y_BOX2 + 64, "SSD 마모 덜함", 11, ACC, KR, "middle")

# 화살표 3개
for i in range(3):
    x1 = XS[i] + WS[i]
    x2 = XS[i + 1]
    d.arrow([(x1 + 4, YM2), (x2 - 4, YM2)], ACC if i == 2 else MUTED, "acc" if i == 2 else "ar", 1.3)

d.legend(LEG, [
    ("LSM 압축 완화", ACC),
    ("B-tree 페이지 증폭", WARN),
    ("WAL 선행 기록", OK),
    ("정상 쓰기 경로", INFO)
])

d.save("04-03.write-amplification.svg")
