# 01-01 §6 — 마이크로 프론트엔드가 마이크로서비스와 함께 놓였을 때의 전경 (원문 Figure 1-3).
# 도메인 이름은 지어내지 않고 저자가 프론트엔드 도메인 예시로 든 check-out · search · profile 을 쓴다.
# 타입 스펙: type-architecture — 신뢰 경계(브라우저 / 서버)로 묶은 구성요소와 그 사이 연결.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1240, 608
d = D(W, H, "BUILDING MICRO-FRONTENDS · 01-01 §6",
      "마이크로 프론트엔드와 마이크로서비스가 함께 놓인 전경",
      "UI 조각이 런타임에 합쳐지고 각 조각이 자기 도메인의 서비스와 짝을 이룬다. 세로 띠 하나가 한 팀이 끝까지 소유하는 범위다.",
      "가로로는 신뢰 경계, 세로로는 팀의 소유 범위입니다. 두 경계가 직각으로 만납니다")

BW, BH, GAP = 280, 88, 72
X0 = (W - (3 * BW + 2 * GAP)) / 2                 # 128
ZX, ZW = 88, 1064
domains = [("검색", "search", "카탈로그 조회"), ("체크아웃", "check-out", "주문 · 결제"), ("프로필", "profile", "계정 · 설정")]

def cx(i): return X0 + i * (BW + GAP) + BW / 2

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" stroke="{RULE}" stroke-width="0.8"/>')
    lw = len(label) * 7 + 16
    d.o.append(f'<rect x="{x + 16}" y="{y - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw / 2, y + 3, label, 7.5, SOFT, MONO)

zone(ZX, 100, ZW, 200, "BROWSER · RUNTIME COMPOSITION")
zone(ZX, 360, ZW, 168, "SERVER SIDE")

# 팀 소유 범위 — 두 신뢰 경계를 세로로 가로지른다 (accent 1개)
d.o.append(f'<rect x="{cx(1) - BW / 2 - 16}" y="180" width="{BW + 32}" height="316" rx="8" fill="{ACC}0A" stroke="{ACC}" stroke-width="1.3" stroke-dasharray="5 4"/>')
d.o.append(f'<rect x="{cx(1) - 66}" y="174" width="132" height="12" rx="2" fill="{PAPER}"/>')
d.t(cx(1), 183, "ONE TEAM · END TO END", 7.5, ACC, MONO)

# 애플리케이션 셸
d.box(X0, 132, 3 * BW + 2 * GAP, 36, PAPER2, RULE, 1.0, 6)
d.t(W / 2, 155, "애플리케이션 셸 — 조각을 런타임에 합친다", 12, INK, KR, "middle", 600)

# 연결선 먼저
for i in range(3):
    d.arrow([(cx(i), 284), (cx(i), 390)], MUTED, "ar", 1.3)
    d.t(cx(i) + 10, 340, "자기 도메인 API", 9, MUTED, MONO, "start")

for i, (ko, en, sub) in enumerate(domains):
    x = X0 + i * (BW + GAP)
    d.box(x, 196, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, 224, f"{ko} 마이크로 프론트엔드", 13, INK, KR, "start", 600)
    d.t(x + 20, 246, en, 9, SOFT, MONO, "start")
    d.t(x + 20, 268, "독립 개발 · 테스트 · 배포", 10, MUTED, KR, "start")

    d.box(x, 392, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, 420, f"{ko} 마이크로서비스", 13, INK, KR, "start", 600)
    d.t(x + 20, 442, sub, 10, MUTED, KR, "start")
    d.t(x + 20, 464, "자체 저장소 · 공유 안 함", 10, MUTED, KR, "start")

d.legend(560, [("한 팀이 끝까지 소유하는 범위", ACC)])
d.save("01-01.combined-microarchitectures.svg")
print("h 필요:", 560 + 22 + 16, " 실제:", H, " 우측끝:", X0 + 3 * BW + 2 * GAP)
