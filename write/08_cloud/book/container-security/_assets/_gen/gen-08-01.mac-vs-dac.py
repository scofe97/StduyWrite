# 타입 스펙: type-flowchart — 접근 요청은 DAC 마름모와 MAC 마름모를 차례로 지나야 수행되고, 어느 쪽에서든 아니오면 거부다. 아래에 DAC 의 판정 주체, MAC 안 두 LSM(AppArmor · SELinux)의 판정 축을 단다. focal 은 MAC.
# 사실 출처: 노트 L98(AppArmor 프로파일 · capability · 파일 접근), L106~L110(MAC 중앙 관리자 · DAC 소유자 재량), L128~L137(SELinux 도메인 · 타입 · 사용자 신원 무관 · 양쪽 모두 허용해야 수행)
# Layout conventions: 요청 타원 x=48 w=120 · DAC 마름모 중심 x=316 · MAC 마름모 중심 x=612(폭 208 h=112, y=176~288) · 수행 타원 x=800 w=140 · 거부 상자 y=100 h=40, 아래 카드 y=316~480. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, BAD, INFO, KR, MONO

W, H = 984, 560


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "FLOWCHART · 08-01 §3",
      "접근 요청은 DAC 와 MAC 를 차례로 통과해야 수행됩니다",
      "접근 요청이 DAC 마름모와 MAC 마름모를 차례로 지나는 흐름. 어느 쪽에서든 허용이 아니면 거부이고 둘 다 허용이어야 수행된다. "
      "DAC 의 판정 주체는 파일 소유자의 재량이다. MAC 는 중앙 관리자가 설정하며 AppArmor 는 실행 파일 프로파일의 capability 와 파일 접근으로, "
      "SELinux 는 프로세스 도메인과 파일 타입 라벨로 판정한다.",
      lead="두 판정은 서로를 대신하지 않고 함께 작동하므로, 한쪽이 허용해도 다른 쪽이 막으면 접근은 거부됩니다.")

CY = 232
# 요청 타원
d.o.append(f'<rect x="48" y="{CY - 18}" width="120" height="36" rx="18" fill="#161B22" stroke="#BFC0C038" stroke-width="0.9"/>')
d.t(108, CY + 5, "접근 요청", 13, INK, KR, "middle", 600)

# 거부 상자(위)
d.tone(408, 100, 112, 40, BAD, 6, "14", 1.2)
d.t(464, 125, "거부", 13, BAD, KR, "middle", 600)

# 마름모
def diamond(cx, col, l1, l2, focal=False):
    d.o.append(f'<polygon points="{cx},176 {cx + 104},{CY} {cx},288 {cx - 104},{CY}" fill="{col}{"1F" if focal else "14"}" stroke="{col}" stroke-width="{1.6 if focal else 1.2}"/>')
    d.t(cx, CY - 2, l1, 13, col if focal else INK, MONO, "middle", 600)
    d.t(cx, CY + 16, l2, 12, INK, KR, "middle", 600)

# 화살표(도형보다 먼저)
d.arrow([(170, CY), (208, CY)], SOFT, "soft", 1.3)
d.arrow([(422, CY), (504, CY)], SOFT, "soft", 1.3)
d.t(463, CY - 10, "예", 12, MUTED, KR, "middle", 600)
d.arrow([(718, CY), (796, CY)], SOFT, "soft", 1.3)
d.t(757, CY - 10, "예", 12, MUTED, KR, "middle", 600)
d.arrow([(316, 174), (316, 120), (404, 120)], BAD, "bad", 1.3)
d.t(328, 156, "아니오", 12, MUTED, KR, "start", 600)
d.arrow([(612, 174), (612, 120), (524, 120)], BAD, "bad", 1.3)
d.t(624, 156, "아니오", 12, MUTED, KR, "start", 600)

diamond(316, INFO, "DAC", "허용?")
diamond(612, ACC, "MAC", "허용?", True)

# 수행 타원
d.o.append(f'<rect x="800" y="{CY - 18}" width="140" height="36" rx="18" fill="{OK}14" stroke="{OK}" stroke-width="1.2"/>')
d.t(870, CY + 5, "수행", 13, OK, KR, "middle", 600)

# 아래: DAC 카드
d.arrow([(316, 290), (316, 312)], INFO, "info", 1.3)
d.tone(168, 316, 296, 164, INFO, 6, "14", 1.2)
d.t(316, 344, "DAC — 임의 접근 제어", 13, INFO, KR, "middle", 600)
for i, s in enumerate(["판정 주체: 파일 소유자의 재량", "남에게 접근을 넘길 수 있음", "내 계정도 막을 수 있음"]):
    fit(s, 12, 280)
    d.t(316, 380 + 28 * i, s, 12, MUTED, KR, "middle")

# 아래: MAC 묶음
d.arrow([(612, 290), (612, 312)], ACC, "acc", 1.6)
d.tone(492, 316, 448, 164, ACC, 8, "0F", 1.6)
d.t(508, 344, "MAC — 강제 접근 제어", 13, ACC, KR, "start", 600)
d.t(924, 344, "중앙 관리자가 설정", 12, MUTED, KR, "end")
CARDS = [
    (508, "AppArmor", ["축: 실행 파일 프로파일", "capability · 파일 접근"]),
    (724, "SELinux", ["축: 도메인 × 파일 타입", "사용자 신원 무관"]),
]
for x, t, subs in CARDS:
    d.box(x, 364, 208, 100)
    d.t(x + 104, 392, t, 13, INK, MONO, "middle", 600)
    for i, s in enumerate(subs):
        fit(s, 12, 196)
        d.t(x + 104, 420 + 22 * i, s, 12, MUTED, kr(s), "middle")

d.legend(H - 44, [("DAC", INFO), ("MAC", ACC), ("수행", OK), ("거부", BAD)])
d.save(str(ASSETS / "08-01.mac-vs-dac.svg"))
print("ok 08-01 mac-vs-dac")
