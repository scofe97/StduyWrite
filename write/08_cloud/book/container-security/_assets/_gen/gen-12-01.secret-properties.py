# 타입 스펙: type-architecture — 시크릿 값이 저장 중 · 이동 중 · 사용 중 세 구간을 지나며 암호문에서 평문이 되고, 평문으로 풀려면 복호화 키가 필요한데 그 키도 시크릿이라 원래 질문으로 되돌아온다. 아래 띠는 수명과 노출 성질. focal 은 되돌아오는 화살표.
# 사실 출처: 노트 L42~L60(구간별 요구, 복호화 키가 또 하나의 시크릿), L62~L78(폐기 · 순환 · 독립된 생애주기 · 최소 노출)
# Layout conventions: 구역 폭 264 · 간격 48(x=36·348·660), 구역 y=100 높이 176, 노드 216x64(y=148), 아래 띠 상자 폭 204 stride 228(y=404). 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, KR, MONO


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


W, H = 960, 564
d = D(W, H, "ARCHITECTURE · 12-01 §1",
      "시크릿은 세 구간에서 비밀이어야 하고, 암호화는 문제를 한 칸 미룰 뿐입니다",
      "시크릿 값은 저장 중과 이동 중에 암호문이고 사용 중에만 평문이 된다. 평문으로 풀려면 복호화 키가 필요한데 그 키도 시크릿이라 원래 질문으로 되돌아온다. "
      "아래 띠는 폐기, 순환, 독립된 생애주기, 최소 노출 네 가지 성질이다.",
      lead="구간마다 요구가 다르고, 복호화 키 자체가 또 하나의 시크릿입니다")

ZW, ZH, ZY = 264, 176, 100
ZX = [36, 348, 660]
NW, NH, NY = 216, 64, 148

ZONES = [
    ("저장 중", "시크릿 저장소", "암호문", OK, ["암호화된 형태로 저장", "접근자 전원 열람 불가"]),
    ("이동 중", "네트워크", "암호문", OK, ["암호화한 채 이동", "네트워크에서 엿볼 수 없음"]),
    ("사용 중", "애플리케이션", "평문 · 메모리", WARN, ["디스크에 쓰지 않음", "메모리에만 둠"]),
]

# 구역 → 되돌아오는 화살표 → 노드 순으로 그린다
for zx in ZX:
    d.o.append(f'<rect x="{zx}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="rgba(245,245,245,0.02)" '
               f'stroke="{RULE}" stroke-width="1" stroke-dasharray="6 5"/>')

# 노드 사이 이동
d.arrow([(ZX[0] + 24 + NW + 2, NY + 32), (ZX[1] + 24 - 2, NY + 32)], MUTED, "ar", 1.4)
d.arrow([(ZX[1] + 24 + NW + 2, NY + 32), (ZX[2] + 24 - 2, NY + 32)], MUTED, "ar", 1.4)

# 되돌아오는 화살표: 사용 중 → 저장소 (focal)
BX_FROM, BX_TO, BY = ZX[2] + 132, ZX[0] + 132, 332
d.arrow([(BX_FROM, ZY + ZH + 2), (BX_FROM, BY), (BX_TO, BY), (BX_TO, ZY + ZH + 4)], ACC, "acc", 1.6)
d.t(BX_FROM + 12, 308, "복호화 키 필요", 12, ACC, KR, "start")
d.t(BX_TO + 12, 308, "원래 질문으로", 12, ACC, KR, "start")
fit("복호화 키도 또 하나의 시크릿", 13, 260)
d.chip(480, BY, "복호화 키도 또 하나의 시크릿", ACC, 13, 16)

for zx, (zone, name, form, c, reqs) in zip(ZX, ZONES):
    fit(name, 14, NW - 16)
    fit(form, 12, NW - 16)
    d.t(zx + 16, ZY + 24, zone, 12, MUTED, KR, "start", 600)
    d.box(zx + 24, NY, NW, NH)
    d.t(zx + 132, NY + 28, name, 14, INK, KR, "middle", 600)
    d.t(zx + 132, NY + 50, form, 12, c, kr(form), "middle", 600)
    for i, r in enumerate(reqs):
        fit(r, 12, ZW - 24)
        d.t(zx + 132, 240 + i * 20, r, 12, MUTED, KR, "middle")

# 아래 띠: 수명과 노출
d.t(36, 388, "수명 · 노출", 12, MUTED, KR, "start", 600)
d.line(120, 384, 924, 384, RULE, 0.8)
PROPS = [
    ("폐기", "침해 의심 · 퇴사"),
    ("순환", "주기적으로 변경"),
    ("독립 생애주기", "재빌드 · 재배포 없이 교체"),
    ("최소 노출", "쓰기 전용 · 필요한 곳만"),
]
for i, (title, sub) in enumerate(PROPS):
    x = 36 + i * 228
    fit(title, 14, 188)
    fit(sub, 12, 188)
    d.box(x, 404, 204, 64)
    d.t(x + 102, 404 + 26, title, 14, INK, KR, "middle", 600)
    d.t(x + 102, 404 + 48, sub, 12, MUTED, KR, "middle")

d.legend(H - 56, [("암호문", OK), ("평문", WARN), ("미뤄진 문제", ACC)])
d.save(str(ASSETS / "12-01.secret-properties.svg"))
print("ok 12-01 secret-properties")
