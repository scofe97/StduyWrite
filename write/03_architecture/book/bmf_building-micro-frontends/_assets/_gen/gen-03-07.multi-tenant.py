# 03-07 §4 — 조각 하나가 서로 다른 프론트엔드 스택에 그대로 꽂힌다.
# 저자의 고객 지원 솔루션 예다. 프레임워크 이름은 저자가 "웹 컴포넌트를 만들 수 있다"고 든 셋만 쓴다.
# 타입 스펙: type-architecture — 논리 경계(고객사별 애플리케이션)로 묶은 구성요소와 그 사이 연결.
#           accent 는 여러 경계에 같은 모습으로 들어가는 조각 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1160
MX, MY_, MW, MH = 40, 200, 300, 96
ZX, ZW, ZH = 480, 640, 92
ZYS = (108, 224, 340)
LEGEND_Y = ZYS[2] + ZH + 34
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-07 §4",
      "같은 조각이 서로 다른 스택에 그대로 꽂힌다",
      "왼쪽 조각 하나를 오른쪽 세 고객사 애플리케이션이 각자의 프레임워크 위에서 그대로 쓴다. 웹 표준이라 다시 만들지 않는다.",
      "화살표는 같은 산출물이 각 애플리케이션에 실린다는 뜻입니다")

d.tone(MX, MY_, MW, MH, ACC, 8, "12", 1.4)
d.t(MX + 20, MY_ + 32, "채팅 조각", 15, ACC, KR, "start", 600)
d.t(MX + 20, MY_ + 56, "커스텀 요소로 감싼 하나의 산출물", 10.5, MUTED, KR, "start")
d.t(MX + 20, MY_ + 78, "custom element + shadow DOM", 9.5, ACC, MONO, "start")

tenants = [("고객사 A", "React"), ("고객사 B", "Angular"), ("고객사 C", "Vue")]
for (name, fw), zy in zip(tenants, ZYS):
    d.o.append(f'<rect x="{ZX}" y="{zy}" width="{ZW}" height="{ZH}" rx="8" '
               f'fill="{INK}03" stroke="{INK}30" stroke-width="1.0" stroke-dasharray="4 4"/>')
    lab = f"TENANT · {fw.upper()}"
    tw = len(lab) * 5.6 + 14
    d.o.append(f'<rect x="{ZX + 14}" y="{zy - 8}" width="{tw}" height="16" fill="{PAPER}"/>')
    d.t(ZX + 20, zy + 4, lab, 8, SOFT, MONO, "start")
    d.box(ZX + 28, zy + 22, ZW - 56, 52, PAPER2, RULE, 1.0, 6)
    d.t(ZX + 46, zy + 44, name, 12.5, INK, KR, "start", 600)
    d.t(ZX + 46, zy + 62, f"{fw} 로 만든 자기 애플리케이션", 9.5, MUTED, KR, "start")

# 연결 — 조각 오른쪽 변 부착점을 20px 씩 벌린다
base = (MX + MW + ZX) / 2
for zy, ay, dx in zip(ZYS, (MY_ + 24, MY_ + 48, MY_ + 72), (-28, 0, 28)):
    ty = zy + 48
    mid = base + dx
    d.arrow([(MX + MW, ay), (mid, ay), (mid, ty), (ZX + 28, ty)], MUTED, "ar", 1.4)

d.legend(LEGEND_Y, [("여러 스택에 그대로 들어가는 조각", ACC), ("같은 산출물이 실린다", MUTED)])
d.save("03-07.multi-tenant.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
