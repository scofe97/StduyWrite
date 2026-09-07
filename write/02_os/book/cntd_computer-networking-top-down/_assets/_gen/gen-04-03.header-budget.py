# 타입 스펙: type-treemap — 면적 = 헤더 바이트 수. 20바이트를 필드 묶음으로 분해한다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §4.3.1 Figure 4.17 + 이 기계의 실측 헤더
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, WARN, KR, MONO, esc

W, H = 940, 560
d = D(W, H, "IPV4 HEADER · 20 BYTES",
      "헤더 20바이트를 무엇이 차지하나",
      "IPv4 헤더 20바이트를 필드 묶음별 면적으로 나눈 트리맵. 주소 두 개가 8바이트로 40%를 차지하고, 포워딩이 실제로 읽는 것은 목적지 4바이트다.",
      "면적 = 바이트 수 · 주소 두 개가 8바이트로 헤더의 40%를 차지합니다")

# 플롯: x 40→900 (860), y 100→444 (344). 두 행, 4px 거터.
X0, Y0 = 40, 100
R1_H, R2_H, G = 204, 136, 4
R2_Y = Y0 + R1_H + G                       # 308
W1 = (860 - 2 * G) / 3                     # 284
W2 = (860 - 3 * G) / 4                     # 212

# (이름, 바이트, 참값 share, 부제, 누가 만지나, 잉크 농도)
row1 = [
    ("목적지 주소", 4, 20.0, "16-19", "포워딩이 읽는 유일한 필드", "fwd"),
    ("출발지 주소", 4, 20.0, "12-15", "출발지가 적고 끝까지 그대로", "fix"),
    ("식별자·플래그·오프셋", 4, 20.0, "4-7", "단편화용. IPv6 가 버린 자리", "fix"),
]
row2 = [
    ("헤더 체크섬", 2, 10.0, "10-11", "TTL 이 바뀌면 다시 계산", "hop"),
    ("TTL · 프로토콜", 2, 10.0, "8-9", "TTL 만 홉마다 1씩 줄어듭니다", "hop"),
    ("전체 길이", 2, 10.0, "2-3", "최대 65,535바이트", "fix"),
    ("버전·길이·서비스유형", 2, 10.0, "0-1", "실측 덤프의 45 00 이 이 자리", "fix"),
]

drawn = []


TINT = {"fwd": (ACC, "1E", 1.5), "hop": (WARN, "16", 1.3), "fix": (INK, "0E", 1.0)}


def cell(x, y, w, h, name, nbytes, share, off, note, kind):
    col, op, sw = TINT[kind]
    fill = f"{col}{op}"
    stroke = col if kind != "fix" else f"{INK}4D"
    d.o.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="2" '
               f'data-share="{share:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    d.t(x + 16, y + 30, name, 13, col if kind != "fix" else INK, KR, "start", 600)
    d.t(x + 16, y + 50, f"{nbytes} B · {share:.0f}% · byte {off}", 10, MUTED, MONO, "start")
    d.t(x + 16, y + 72, note, 11, MUTED, KR, "start")
    drawn.append((name, share, w * h))


for i, (nm, nb, sh, off, note, op) in enumerate(row1):
    cell(X0 + i * (W1 + G), Y0, W1, R1_H, nm, nb, sh, off, note, op)
for i, (nm, nb, sh, off, note, op) in enumerate(row2):
    cell(X0 + i * (W2 + G), R2_Y, W2, R2_H, nm, nb, sh, off, note, op)

d.legend(478, [("포워딩이 읽는 필드", ACC), ("홉마다 바뀌는 필드", WARN), ("출발지가 적고 그대로 가는 필드", INK)])
d.t(900, 500, "AREA = HEADER BYTES · RFC 791 · 20B, NO OPTIONS", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "04-03.header-budget.svg"
d.save(out)

total = sum(a for _, _, a in drawn)
print("면적 검산 (참 share 대비 상대 오차)")
for nm, sh, a in drawn:
    got = a / total * 100
    print(f"  {nm:<22}참 {sh:5.2f}%  그린 {got:5.2f}%  상대오차 {(got - sh) / sh * 100:+.2f}%")
print("합계", f"{sum(sh for _, sh, _ in drawn):.1f}%", "→", out)
