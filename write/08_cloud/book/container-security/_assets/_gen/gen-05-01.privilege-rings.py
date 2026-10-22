# 타입 스펙: type-dp-security-matrix — 행 = 권한 링(Ring -1 · 0 · 1 · 3), 열 = 일반 구성 · 하이퍼바이저 · 하드웨어 가상화. 셀 = 그 링에 앉는 것. 커널이 Ring 0 → Ring 1 → Ring 0 으로 옮겨 가고 하이퍼바이저가 Ring 0 → Ring -1 로 올라가는 이동이 격자에서 대각선으로 읽힌다. focal 은 Ring 1 으로 내려온 게스트 커널.
# 사실 출처: 노트 L59(일반 구성 커널 Ring 0 · 유저 공간 Ring 3), L97~L99(하이퍼바이저 Ring 0 · 게스트 커널 Ring 1), L137(VT-x · VMX root mode · Ring -1 · 게스트 커널 Ring 0)
# Layout conventions: 스펙 §2 공식. left_pad 36 · comp_col_w 160 · gap 12 · role_col_w 220 · role_gap 16 · header_h 52 · row_h 52 · row_stride 60. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, PAPER, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, KR, MONO

W, H = 936, 472
LP, CW, GAP, RW, RG = 36, 160, 12, 220, 16
HEAD_Y, HEAD_H = 96, 52
ROW_Y0, ROW_H, ROW_STRIDE = 164, 52, 60


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


def rx(j):
    return LP + CW + GAP + j * (RW + RG)


def ry(k):
    return ROW_Y0 + k * ROW_STRIDE


d = D(W, H, "MATRIX · 05-01 §1 · §3 · §4",
      "하이퍼바이저가 들어오면 커널은 Ring 1 로 내려가고, VT-x 가 Ring 0 을 돌려줍니다",
      "권한 링 넷(Ring -1, 0, 1, 3) 과 구성 셋(일반 구성, 하이퍼바이저, 하드웨어 가상화) 의 격자. 일반 구성에서 커널은 Ring 0 이고 유저 공간은 Ring 3 이다. "
      "하이퍼바이저가 Ring 0 을 차지하면 게스트 커널은 Ring 1 로 내려간다. VT-x 는 하이퍼바이저를 Ring -1 인 VMX root mode 로 올려 게스트 커널이 Ring 0 을 되찾게 한다.",
      lead="같은 커널이 구성에 따라 Ring 0, Ring 1, Ring 0 으로 옮겨 앉고, 하이퍼바이저는 Ring 0 에서 Ring -1 로 올라갑니다.")

# 머리 행
d.box(LP, HEAD_Y, CW, HEAD_H, "#161B22")
d.t(LP + CW / 2, HEAD_Y + 24, "권한 수준", 13, INK, KR, "middle", 600)
d.t(LP + CW / 2, HEAD_Y + 42, "링", 12, MUTED, KR, "middle")
COLS = [("일반 구성", "VM 없음"), ("하이퍼바이저", "Type 1"), ("하드웨어 가상화", "Intel VT-x")]
for j, (name, code) in enumerate(COLS):
    fit(name, 13, RW - 16)
    d.box(rx(j), HEAD_Y, RW, HEAD_H, "#161B22")
    d.t(rx(j) + RW / 2, HEAD_Y + 24, name, 13, INK, KR, "middle", 600)
    d.t(rx(j) + RW / 2, HEAD_Y + 42, code, 12, MUTED, kr(code), "middle")

# 행 라벨
ROWS = [("Ring -1", "VMX root mode"), ("Ring 0", "특권 명령 실행"), ("Ring 1", None), ("Ring 3", "가장 낮음")]
for k, (name, hint) in enumerate(ROWS):
    y = ry(k)
    d.box(LP, y, CW, ROW_H)
    if hint:
        fit(hint, 12, CW - 24)
        d.t(LP + 12, y + 22, name, 13, INK, MONO, "start", 600)
        d.t(LP + 12, y + 40, hint, 12, MUTED, kr(hint), "start")
    else:
        d.t(LP + 12, y + 31, name, 13, INK, MONO, "start", 600)


def cell(k, j, value, sub=None, c=None, focal=False):
    x, y = rx(j), ry(k)
    fit(value, 13, RW - 16)
    if sub:
        fit(sub, 12, RW - 16)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{RW}" height="{ROW_H}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
        col = ACC
    elif c:
        d.tone(x, y, RW, ROW_H, c, 6, "14", 1.1)
        col = c
    else:
        d.box(x, y, RW, ROW_H)
        col = INK
    if sub:
        d.t(x + RW / 2, y + 22, value, 13, col, kr(value), "middle", 600)
        d.t(x + RW / 2, y + 40, sub, 12, MUTED, kr(sub), "middle")
    else:
        d.t(x + RW / 2, y + 31, value, 13, col, kr(value), "middle", 600)


def empty(k, j):
    x, y = rx(j), ry(k)
    d.o.append(f'<rect x="{x}" y="{y}" width="{RW}" height="{ROW_H}" rx="6" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="6 5"/>')
    d.t(x + RW / 2, y + 31, "—", 13, SOFT, KR, "middle")


# Ring -1
empty(0, 0)
empty(0, 1)
cell(0, 2, "하이퍼바이저", None, WARN)
# Ring 0
cell(1, 0, "커널", None, INFO)
cell(1, 1, "하이퍼바이저", None, WARN)
cell(1, 2, "게스트 커널", "Ring 0 를 되찾음", INFO)
# Ring 1
empty(2, 0)
cell(2, 1, "게스트 커널", "하이퍼바이저보다 낮은 권한", focal=True)
empty(2, 2)
# Ring 3
cell(3, 0, "유저 공간 코드")
cell(3, 1, "유저 공간 코드")  # 원서 그림 5-3: 하이퍼바이저 아래에서도 User space 는 Ring 3
empty(3, 2)

d.legend(428, [("커널", INFO), ("하이퍼바이저", WARN), ("권한이 낮아진 커널", ACC)])
d.save(str(ASSETS / "05-01.privilege-rings.svg"))
print("ok 05-01 privilege-rings")
