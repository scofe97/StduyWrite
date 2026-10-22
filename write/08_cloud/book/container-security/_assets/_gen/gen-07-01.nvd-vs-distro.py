# 타입 스펙: type-flowchart — bash 4.2-2ubuntu2.2 한 값이 NVD 범위 검사에서는 취약으로 판정되고, 배포판 권고 검사에서 안전으로 뒤집힌다. NVD 판정에서 멈추면 오탐이다. focal 은 배포판 권고의 분기.
# 사실 출처: 노트 L62~L70(NVD 목록만으로는 부족 · Ubuntu 12.04 bash 4.2-2ubuntu2.2 · CVE-2014-6271 취약 버전 1.14.0~4.3 · 패치만 적용한 버전 · 배포판 권고 병행).
# Layout conventions: 중심 열 cx=360, 상자 폭 360 · 높이 56, 마름모 폭 280 · 높이 88, 세로 stride 4의 배수. 오른쪽 열은 막다른 길·주석. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, RULE

W, H = 960, 804
CX = 360


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "CONTAINER SECURITY · 07-01 §2",
      "같은 bash 가 NVD 에서는 취약, 배포판 권고에서는 안전으로 갈립니다",
      "Ubuntu 12.04 의 bash 4.2-2ubuntu2.2 는 CVE-2014-6271 의 NVD 영향 버전 1.14.0~4.3 안에 들어 취약으로 판정된다. "
      "Ubuntu 보안 권고에서는 그 버전에 수정이 적용돼 있어 안전이고, NVD 판정에서 멈추면 오탐이 된다.",
      "NVD 는 버전 번호만 봅니다. 배포판은 마이너 버전을 올리지 않고 패치만 적용해 배포할 수 있습니다.")


def oval(cx, y, w, h, title, sub=None, c=None):
    fit(title, 13, w - 24)
    if c:
        d.tone(cx - w / 2, y, w, h, c, h / 2, "14", 1.1)
    else:
        d.box(cx - w / 2, y, w, h, r=h / 2)
    if sub:
        fit(sub, 12, w - 24)
        d.t(cx, y + h / 2 - 3, title, 13, c or INK, kr(title), "middle", 600)
        d.t(cx, y + h / 2 + 15, sub, 12, MUTED, kr(sub), "middle")
    else:
        d.t(cx, y + h / 2 + 5, title, 13, c or INK, kr(title), "middle", 600)


def step(cx, y, title, sub, c=None, w=360, h=56, focal=False):
    fit(title, 13, w - 24)
    fit(sub, 12, w - 24)
    if focal:
        d.tone(cx - w / 2, y, w, h, ACC, 6, "1F", 1.4)
    elif c:
        d.tone(cx - w / 2, y, w, h, c, 6, "14", 1.1)
    else:
        d.box(cx - w / 2, y, w, h)
    d.t(cx, y + 24, title, 13, ACC if focal else (c or INK), kr(title), "middle", 600)
    d.t(cx, y + 44, sub, 12, MUTED, kr(sub), "middle")


def diamond(cx, cy, w, h, text, focal=False):
    c = ACC if focal else MUTED
    pts = f"{cx} {cy - h / 2} L {cx + w / 2} {cy} L {cx} {cy + h / 2} L {cx - w / 2} {cy} Z"
    fill = f'{ACC}1F' if focal else "#161B22"
    d.o.append(f'<path d="M {pts}" fill="{fill}" stroke="{c}" stroke-width="{1.4 if focal else 1.0}"/>')
    fit(text, 13, w - 100)
    d.t(cx, cy + 5, text, 13, ACC if focal else INK, kr(text), "middle", 600)


# 시작
oval(CX, 100, 360, 44, "Ubuntu 12.04 · bash 4.2-2ubuntu2.2")
d.arrow([(CX, 144), (CX, 172)], MUTED, "ar")
# NVD 조회
step(CX, 176, "NVD · CVE-2014-6271", "취약 버전 1.14.0 ~ 4.3")
d.arrow([(CX, 232), (CX, 256)], MUTED, "ar")
# 분기 1: 버전이 범위 안인가
diamond(CX, 300, 280, 88, "4.2 가 범위 안?")
d.arrow([(CX - 140, 300), (176, 300)], MUTED, "ar")
d.t(CX - 152, 290, "아니오", 12, MUTED, KR, "end", 600)
oval(112, 278, 128, 44, "해당 없음")
d.arrow([(CX, 344), (CX, 372)], WARN, "warn", 1.6)
d.t(CX + 10, 364, "예", 12, WARN, KR, "start", 600)
# NVD 판정
step(CX, 376, "NVD 판정 · 취약", "버전 번호만으로 내린 결론", c=WARN)
# 여기서 멈추면 오탐
d.line(CX + 180, 404, 572, 404, WARN, 1.2, "4 4")
d.tone(576, 380, 328, 48, WARN, 6, "0F", 1.0)
d.t(740, 402, "여기서 멈추면 오탐", 13, WARN, KR, "middle", 600)
d.t(740, 420, "배포판이 이미 패치했을 수 있음", 12, MUTED, KR, "middle")
d.arrow([(CX, 432), (CX, 460)], MUTED, "ar")
d.t(CX + 10, 452, "배포판 권고까지", 12, MUTED, KR, "start", 600)
# 권고 조회
step(CX, 464, "Ubuntu 보안 권고 조회", "같은 CVE · 같은 패키지 버전")
d.arrow([(CX, 520), (CX, 548)], MUTED, "ar")
# 분기 2 (focal)
diamond(CX, 592, 280, 88, "이 버전에 수정?", focal=True)
d.arrow([(CX + 140, 592), (584, 592)], BAD, "bad", 1.5)
d.t(CX + 152, 582, "아니오", 12, BAD, KR, "start", 600)
oval(692, 570, 160, 44, "취약 확정", c=BAD)
d.arrow([(CX, 636), (CX, 668)], OK, "ok", 1.6)
d.t(CX + 10, 658, "예", 12, OK, KR, "start", 600)
oval(CX, 672, 280, 64, "안전 · 백포트", "패치만 적용한 버전", c=OK)
d.t(CX + 156, 708, "마이너 버전을 올리지 않고 패치만 배포", 12, MUTED, KR, "start")

d.legend(764, [("NVD 판정", WARN), ("배포판 권고에서 안전", OK), ("배포판 권고에서 취약", BAD), ("배포판 권고 분기", ACC)])
d.save(str(ASSETS / "07-01.nvd-vs-distro.svg"))
print("ok 07-01 nvd-vs-distro")
