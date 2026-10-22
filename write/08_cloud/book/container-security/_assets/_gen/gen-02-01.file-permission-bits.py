# 타입 스펙: type-dp-security-matrix — 묶음(소유자·그룹·그 외) × 비트(r·w·x) 행렬. 위쪽 아홉 글자를 셋씩 끊어 아래 행으로 내리고, 열 아래에 그 동작을 할 수 있는 쪽을 적는다. focal 은 소유자의 w.
# 사실 출처: 노트 L76~L82(셋씩 세 묶음, liz 소유·staff 그룹 myapp, 쓰기는 소유자만·실행은 소유자와 staff·읽기는 세 묶음 모두), L84(원문 서술로 복원한 예), L74(DAC)
# Layout conventions: 아홉 글자 띠 칸 44, stride 48, 묶음 간격 24(x=36·200·364). 행렬 라벨 칸 x=36 w=272, 열 x=316·512·708 w=188, 행 y=244 stride 64 h=56. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, KR, MONO

W, H = 960, 548


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "MATRIX · 02-01 §2",
      "권한 아홉 글자는 셋씩 끊어 소유자·그룹·그 외의 읽기·쓰기·실행으로 읽습니다",
      "myapp 파일의 권한 rwx r-x r-- 를 소유자 liz, 그룹 staff, 그 외 모두 세 행으로 나눈 3 × 3 행렬. "
      "읽기는 세 묶음 모두, 쓰기는 소유자만, 실행은 소유자와 staff 그룹이 할 수 있다. 원문 서술로 복원한 예다.",
      lead="대시는 그 비트가 꺼져 있다는 표시이고, 이 방식 전체를 임의 접근 제어(DAC)라고 부릅니다.")

GROUPS = [("rwx", "소유자 liz"), ("r-x", "그룹 staff"), ("r--", "그 외 모두")]
GX = [36, 200, 364]

# 위쪽 띠: 아홉 글자
for g, (bits, name) in enumerate(GROUPS):
    for k, ch in enumerate(bits):
        x = GX[g] + k * 48
        d.box(x, 100, 44, 44)
        d.t(x + 22, 130, ch, 18, INK if ch != "-" else SOFT, MONO, "middle", 600)
    d.line(GX[g], 156, GX[g] + 140, 156, MUTED, 1.2)
    d.line(GX[g], 152, GX[g], 156, MUTED, 1.2)
    d.line(GX[g] + 140, 152, GX[g] + 140, 156, MUTED, 1.2)
    d.t(GX[g] + 70, 176, name, 12, MUTED, KR, "middle", 600)

d.t(556, 116, "myapp · 소유자 liz · 그룹 staff", 12, INK, MONO, "start")
d.t(556, 140, "원문 서술로 복원한 예", 12, MUTED, KR, "start")

# 행렬
LX, LW = 36, 272
CX = [316, 512, 708]
CW = 188
d.box(LX, 204, LW, 32, "#161B22")
d.t(LX + 16, 225, "묶음", 12, MUTED, KR, "start", 600)
for j, (bit, word) in enumerate((("r", "읽기"), ("w", "쓰기"), ("x", "실행"))):
    d.box(CX[j], 204, CW, 32, "#161B22")
    d.t(CX[j] + CW / 2, 225, f"{bit} {word}", 13, INK, KR, "middle", 600)

ROW_Y, ROW_S, ROW_H = 244, 64, 56
for i, (bits, name) in enumerate(GROUPS):
    y = ROW_Y + i * ROW_S
    fit(name, 13, LW - 100)
    d.box(LX, y, LW, ROW_H)
    d.t(LX + 16, y + 34, bits, 16, INK, MONO, "start", 600)
    d.t(LX + 88, y + 34, name, 13, INK, KR, "start", 600)
    for j, ch in enumerate(bits):
        x = CX[j]
        on = ch != "-"
        focal = (i == 0 and j == 1)
        if focal:
            d.tone(x, y, CW, ROW_H, ACC, 6, "1F", 1.6)
            d.t(x + CW / 2, y + 26, "w", 16, ACC, MONO, "middle", 600)
            d.t(x + CW / 2, y + 45, "쓰기는 여기뿐", 12, MUTED, KR, "middle")
        elif on:
            d.tone(x, y, CW, ROW_H, OK, 6, "14", 1.1)
            d.t(x + CW / 2, y + 34, ch, 16, OK, MONO, "middle", 600)
        else:
            d.box(x, y, CW, ROW_H)
            d.t(x + CW / 2, y + 34, "-", 16, SOFT, MONO, "middle")

# 아래: 열별로 그 동작을 할 수 있는 쪽
FY = 444
d.line(LX, FY, 904, FY, SOFT, 1.0)
d.t(LX + 16, FY + 28, "할 수 있는 쪽", 12, MUTED, KR, "start", 600)
for j, (txt, c) in enumerate((("세 묶음 모두", INK), ("소유자만", ACC), ("소유자 · staff", INK))):
    d.t(CX[j] + CW / 2, FY + 28, txt, 13, c, KR, "middle", 600)

d.legend(504, [("켜짐", OK), ("쓰기는 소유자만", ACC)])
d.save(str(ASSETS / "02-01.file-permission-bits.svg"))
print("ok 02-01 file-permission-bits")
