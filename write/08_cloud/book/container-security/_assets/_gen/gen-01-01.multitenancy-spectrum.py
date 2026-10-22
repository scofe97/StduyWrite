# 타입 스펙: type-dp-security-matrix — 격리가 약한 쪽(공유 머신)에서 강한 쪽(베어메탈)으로 다섯 행을 세우고, 커널과 물리 머신을 공유하는지를 칸마다 상태색으로 보인다. 1차원 스펙트럼 공백(visual-diagram-selection 「알려진 공백」)의 대체이며, 컨테이너와 가상머신 사이에 focal 점선 경계를 긋는다.
# 사실 출처: 노트 L134(한 물리 머신 위 여러 VM, 이웃을 알 수 없음), L138~L140(공유 머신: Linux 접근 제어, 같은 커널, docker 명령은 사실상 root), L146~L152(VM 격리, 시끄러운 이웃), L156(자기 고객만 있는 VM 옵션, 베어메탈 임대), L160(컨테이너 격리 < VM 격리)
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, KR, MONO

W, H = 984, 652


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "DP-SECURITY-MATRIX · 01-01 §4",
      "공유하는 것이 많을수록 격리가 약하고, 컨테이너와 가상머신 사이가 이 책의 경계입니다",
      "다섯 가지 배치를 격리가 약한 쪽에서 강한 쪽으로 세웠다. 공유 머신과 컨테이너는 커널과 물리 머신을 함께 쓰고, 가상머신부터 커널이 분리되며, "
      "전용 VM 과 베어메탈에서 물리 머신까지 분리된다.",
      lead="칸 색은 그 자원을 이웃과 공유하는지를 뜻합니다. 위쪽일수록 약한 격리입니다.")

AX = 36
LX, LW = 96, 184
COLS = [(296, 148, "커널"), (460, 164, "물리 머신"), (640, 296, "비고")]
HY, HH = 100, 40
RY0, RH, RST = 156, 48, 88

ROWS = [
    ("공유 머신", "대학 서버", ("공유", BAD), ("공유", BAD), "사용자끼리 서로 믿지 않음"),
    ("컨테이너", "같은 호스트", ("공유", BAD), ("공유", BAD), "docker 명령 = 사실상 root"),
    ("가상머신", "이웃 VM 모름", ("분리", OK), ("공유", BAD), "시끄러운 이웃"),
    ("전용 VM", "클라우드 옵션", ("분리", OK), ("자기 고객만", WARN), "시끄러운 이웃 없음"),
    ("베어메탈", "임대", ("분리", OK), ("전용", OK), "시끄러운 이웃 없음"),
]

# 머리 행
d.t(LX + 12, HY + 26, "배치", 12, MUTED, KR, "start", 600)
for cx, cw, name in COLS:
    d.t(cx + 12 if name == "비고" else cx + cw / 2, HY + 26, name, 12, MUTED, KR,
        "start" if name == "비고" else "middle", 600)
d.line(AX, HY + HH, 948, HY + HH, "rgba(191,192,192,0.22)", 0.8)

# 왼쪽 축: 약함 → 강함
ay1, ay2 = RY0 + 8, RY0 + 4 * RST + RH - 8
d.arrow([(AX + 8, ay1), (AX + 8, ay2)], SOFT, "soft", 1.3)
d.t(AX + 8, HY + 26, "격리", 11, SOFT, KR, "middle")

for i, (name, sub, kern, phys, note) in enumerate(ROWS):
    y = RY0 + i * RST
    fit(name, 14, LW - 24)
    fit(sub, 12, LW - 24)
    fit(note, 12, 296 - 24)
    d.box(LX, y, LW, RH)
    d.t(LX + 12, y + 21, name, 14, INK, KR, "start", 600)
    d.t(LX + 12, y + 39, sub, 12, MUTED, KR, "start")
    for (cx, cw, _), (val, c) in zip(COLS[:2], (kern, phys)):
        fit(val, 13, cw - 16)
        d.tone(cx, y, cw, RH, c, 6, "1F" if c == BAD else "14", 1.1)
        d.t(cx + cw / 2, y + 30, val, 13, c, KR, "middle", 600)
    cx, cw, _ = COLS[2]
    d.box(cx, y, cw, RH)
    d.t(cx + 12, y + 30, note, 12, MUTED, kr(note), "start")

# 컨테이너 | 가상머신 경계
by = RY0 + 2 * RST - (RST - RH) // 2
d.line(AX, by, 948, by, ACC, 1.6, "6 5")
d.chip(490, by, "이 책이 반복해서 따지는 경계", ACC, 12)

d.legend(H - 56, [("공유", BAD), ("자기 고객만", WARN), ("분리 · 전용", OK), ("경계", ACC)])
d.save(str(ASSETS / "01-01.multitenancy-spectrum.svg"))
print("ok 01-01 multitenancy-spectrum")
