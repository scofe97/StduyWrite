# 04-06 §1 다차원 인덱스 — 위도·경도 2차원 범위 쿼리에서 연결 인덱스와 R-tree의 탐색 방식 비교.
# 사실 출처: 04-06 본문 §1 L33~L44, 원서 PDF 34쪽(위도 51.4946~51.5 쿼리, R-tree 는 가까운 점을 같은 서브트리에 묶음)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 96, 316
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "04-06 · §1 MULTIDIMENSIONAL INDEX", "연결 인덱스와 R-tree의 2차원 범위 검색",
      "연결 인덱스는 위도만 좁힐 뿐 경도는 전체 띠를 훑어야 하지만, R-tree는 가까운 점을 같은 서브트리에 묶어 위도와 경도를 함께 좁힌다.",
      "왼쪽은 위도 정렬에 따른 1차원 띠 스캔 낭비, 오른쪽은 가까운 점을 묶은 서브트리 단위 탐색입니다.")

PANEL_W = 416
# 좌측 패널: 연결 인덱스 (위도, 경도)
d.box(16, PY, PANEL_W, PH, PAPER, RULE, 1.0)
d.t(32, PY + 26, "연결 인덱스 — (위도, 경도) 단일 축 정렬", 14, INK, KR, "start", 600)
d.t(32, PY + 46, "위도 구간을 좁혀도 해당 띠의 경도를 전부 스캔", 12, MUTED, KR, "start")

# 우측 패널: R-tree 2차원 공간 분할 (Focal ACC)
d.tone(448, PY, PANEL_W, PH, ACC, 6, "10", 1.4)
d.t(464, PY + 26, "R-tree — 가까운 점을 서브트리로 묶음", 14, ACC, KR, "start", 600)
d.t(464, PY + 46, "공간을 나눠 가까운 점을 같은 서브트리에 둠", 12, MUTED, KR, "start")

# === 좌측 패널 내용: 연결 인덱스 ===
# 질의 영역 표시: 위도 51.49~51.50 띠
BOX_LX, BOX_LY, BOX_LW, BOX_LH = 36, PY + 64, 376, 176
d.box(BOX_LX, BOX_LY, BOX_LW, BOX_LH, PAPER2, RULE, 0.8)

# 2D 좌표축 약식 표시 (위도 Y축, 경도 X축)
d.line(BOX_LX + 32, BOX_LY + 144, BOX_LX + 356, BOX_LY + 144, RULE, 0.8)
d.t(BOX_LX + 356, BOX_LY + 162, "경도 축", 12, SOFT, KR, "end")
d.line(BOX_LX + 32, BOX_LY + 144, BOX_LX + 32, BOX_LY + 16, RULE, 0.8)
d.t(BOX_LX + 38, BOX_LY + 28, "위도 축", 12, SOFT, KR, "start")

# 위도 검색 띠 (전체 폭에 걸침)
STRIP_Y, STRIP_H = BOX_LY + 48, 56
d.tone(BOX_LX + 36, STRIP_Y, 324, STRIP_H, WARN, 4, "16", 1.0)
d.t(BOX_LX + 46, STRIP_Y + 18, "위도 일치 띠 (51.4946 ~ 51.5)", 12, WARN, KR, "start")

# 띠 내부 점들
# 점 1 (불일치)
d.box(BOX_LX + 84, STRIP_Y + 28, 8, 8, WARN, WARN, 1.0)
d.t(BOX_LX + 88, STRIP_Y + 48, "경도 벗어남", 12, WARN, KR, "middle")

# 점 2 (질의 사각형 내부 - 실제 일치)
d.box(BOX_LX + 188, STRIP_Y + 22, 92, 26, PAPER, OK, 1.2)
d.box(BOX_LX + 198, STRIP_Y + 31, 8, 8, OK, OK, 1.2)
d.t(BOX_LX + 244, STRIP_Y + 39, "목표 식당", 12, OK, KR, "middle")

# 점 3 (불일치)
d.box(BOX_LX + 314, STRIP_Y + 28, 8, 8, WARN, WARN, 1.0)
d.t(BOX_LX + 318, STRIP_Y + 48, "경도 벗어남", 12, WARN, KR, "middle")

# 좌측 하단 해설
d.box(BOX_LX, PY + 252, BOX_LW, 48, PAPER2, WARN, 0.9)
d.t(BOX_LX + BOX_LW / 2, PY + 270, "위도 인덱스는 위도 띠 전체 레코드를 반환", 12, INK, KR, "middle")
d.t(BOX_LX + BOX_LW / 2, PY + 288, "경도 필터링을 위해 무관한 행까지 전부 검사", 12, WARN, KR, "middle")


# === 우측 패널 내용: R-tree ===
BOX_RX = 468
d.box(BOX_RX, BOX_LY, BOX_LW, BOX_LH, PAPER2, RULE, 0.8)

# R-tree 경계 상자들
# 상자 A (북서쪽 - 완전 제외)
d.box(BOX_RX + 28, BOX_LY + 20, 136, 56, PAPER, RULE, 1.0)
d.t(BOX_RX + 96, BOX_LY + 42, "서브트리 A", 12, SOFT, KR, "middle")
d.t(BOX_RX + 96, BOX_LY + 60, "질의 영역 밖 · 건너뜀", 12, MUTED, KR, "middle")

# 상자 B (중앙 질의 영역 포함)
d.tone(BOX_RX + 180, BOX_LY + 36, 172, 92, ACC, 6, "14", 1.4)
d.t(BOX_RX + 266, BOX_LY + 54, "서브트리 B", 12, ACC, KR, "middle", 600)

# 질의 사각형 (상자 B 내부 교집합)
d.box(BOX_RX + 196, BOX_LY + 64, 140, 54, PAPER, OK, 1.2)
d.t(BOX_RX + 266, BOX_LY + 82, "지도 검색 사각형", 12, OK, KR, "middle")
d.box(BOX_RX + 216, BOX_LY + 92, 8, 8, OK, OK, 1.2)
d.t(BOX_RX + 270, BOX_LY + 100, "목표 식당 일치", 12, OK, KR, "middle")

# 상자 C (남서쪽 - 완전 제외)
d.box(BOX_RX + 28, BOX_LY + 88, 136, 56, PAPER, RULE, 1.0)
d.t(BOX_RX + 96, BOX_LY + 110, "서브트리 C", 12, SOFT, KR, "middle")
d.t(BOX_RX + 96, BOX_LY + 128, "질의 영역 밖 · 건너뜀", 12, MUTED, KR, "middle")

# 우측 하단 해설
d.box(BOX_RX, PY + 252, BOX_LW, 48, PAPER2, ACC, 0.9)
d.t(BOX_RX + BOX_LW / 2, PY + 270, "질의 사각형과 겹치지 않는 서브트리는 건너뜀", 12, INK, KR, "middle")
d.t(BOX_RX + BOX_LW / 2, PY + 288, "위도와 경도 두 차원을 함께 좁힘", 12, ACC, KR, "middle")

d.legend(LEG, [("질의 사각형 일치", OK), ("R-tree 서브트리 탐색", ACC), ("단일 축 낭비 스캔", WARN), ("검색 제외 서브트리", SOFT)])
d.save("04-06.multidimensional-index.svg")
