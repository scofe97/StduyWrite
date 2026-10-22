# 타입 스펙: type-swimlane — 가로 레인 셋(전통적 머신 · 컨테이너 · 비root 컨테이너) × 단계 넷(침투 · 권한 상승 · 탈출 · 얻는 권한). 컨테이너 레인의 권한 상승 칸이 건너뛴 칸이다. focal 은 그 칸.
# 사실 출처: 노트 L188(비특권 침투·root 앱의 알려진 취약점), L190(컨테이너는 기본 root·탈출·호스트 root·추가 상승 불필요), L192(침투 후 권한 상승 단계가 이미 완료), L194~L197(비root 여도 남는 setuid 바이너리·추가 capability)
# Layout conventions: 레인 라벨 x=36 w=156, 단계 열 x=204·384·564·744 w=152(간격 28), 머리 y=96 h=32, 레인 y=140·244·348(높이 88·88·132). 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, WARN, BAD, KR, MONO

W, H = 960, 552


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "SWIMLANE · 02-01 §5",
      "전통적 머신은 침투 뒤 권한 상승이 따로 필요하지만, 컨테이너는 그 단계가 이미 끝나 있습니다",
      "가로 레인 셋과 단계 넷. 전통적 머신은 비특권 사용자로 침투해 root 로 도는 앱의 취약점을 이용해 root 를 얻는다. "
      "컨테이너는 이미 root 라 권한 상승 칸을 건너뛰고 탈출만 하면 호스트 root 다. 비root 컨테이너에도 setuid 바이너리와 추가 capability 두 경로가 남는다.",
      lead="컨테이너는 기본이 root 라서 탈출만 하면 호스트에서도 root 이고 더 올릴 권한이 없습니다.")

CX = [204, 384, 564, 744]
CW, CH = 152, 64
LX, LW = 36, 156

# 머리 행
for j, (num, name) in enumerate((("1", "침투"), ("2", "권한 상승"), ("3", "탈출"), ("4", "얻는 권한"))):
    d.box(CX[j], 96, CW, 32, "#161B22")
    d.t(CX[j] + 14, 117, num, 11, SOFT, MONO, "start")
    d.t(CX[j] + CW / 2 + 6, 117, name, 13, INK, KR, "middle", 600)

LANES = [(140, 88, "전통적 머신", ""), (244, 88, "컨테이너", "기본이 root"), (348, 132, "비root 컨테이너", "그래도 남는 경로")]
for y, h, name, sub in LANES:
    fit(name, 13, LW - 24)
    d.box(LX, y, LW, h)
    d.t(LX + 16, y + h / 2 + (0 if sub else 5), name, 13, INK, KR, "start", 600)
    if sub:
        d.t(LX + 16, y + h / 2 + 20, sub, 12, MUTED, KR, "start")


def cell(j, y, title, sub=None, c=None, dashed=False, h=CH):
    x = CX[j]
    fit(title, 13, CW - 16)
    if sub:
        fit(sub, 12, CW - 16)
    col = c or INK
    if dashed:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{h}" rx="6" fill="{c or SOFT}1F" stroke="{c or SOFT}" stroke-width="{1.6 if c == ACC else 1.0}" stroke-dasharray="6 5"/>')
    elif c:
        d.tone(x, y, CW, h, c, 6, "14", 1.1)
    else:
        d.box(x, y, CW, h)
    ty = y + h / 2 - (4 if sub else -5)
    d.t(x + CW / 2, ty, title, 13, c or INK, kr(title), "middle", 600)
    if sub:
        d.t(x + CW / 2, ty + 20, sub, 12, MUTED, kr(sub), "middle")


def harrow(j, y, c=SOFT, mk="soft", dash=None):
    d.arrow([(CX[j] + CW + 2, y), (CX[j + 1] - 4, y)], c, mk, 1.3, dash)


# 레인 1: 전통적 머신
y1 = 140 + 12
cell(0, y1, "비특권 사용자", "코드 실행 확보")
cell(1, y1, "root 앱 찾기", "알려진 취약점 이용")
cell(2, y1, "해당 없음", None, None, True)
cell(3, y1, "root", "상승 성공", BAD)
for j in range(3):
    harrow(j, y1 + CH / 2, dash="4 4" if j >= 1 else None)

# 레인 2: 컨테이너
y2 = 244 + 12
cell(0, y2, "컨테이너 안", "이미 root 로 실행")
cell(1, y2, "건너뜀", "이미 root", ACC, True)
cell(2, y2, "컨테이너 탈출", "여전히 필요")
cell(3, y2, "호스트 root", "추가 상승 불필요", BAD)
for j in range(3):
    harrow(j, y2 + CH / 2)

# 레인 3: 비root 컨테이너 — 권한 상승 칸에 두 경로
ya, yb = 348, 420
cell(0, 384, "비root 로 실행")
cell(1, ya, "setuid 바이너리", "이미지 속 s 비트", WARN)
cell(1, yb, "추가 capability", "필요 이상 부여", WARN)
mid = 384 + CH / 2
d.line(CX[0] + CW + 2, mid, 370, mid, SOFT, 1.3)
d.line(370, ya + CH / 2, 370, yb + CH / 2, SOFT, 1.3)
d.arrow([(370, ya + CH / 2), (CX[1] - 4, ya + CH / 2)], SOFT, "soft", 1.3)
d.arrow([(370, yb + CH / 2), (CX[1] - 4, yb + CH / 2)], SOFT, "soft", 1.3)

d.legend(508, [("건너뛴 단계", ACC), ("얻는 root", BAD), ("남는 경로", WARN)])
d.save(str(ASSETS / "02-01.privilege-escalation.svg"))
print("ok 02-01 privilege-escalation")
