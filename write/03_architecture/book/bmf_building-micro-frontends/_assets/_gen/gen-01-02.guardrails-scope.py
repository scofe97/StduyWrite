# 01-02 §3 — 분산화가 "각자 알아서"가 아닌 이유. 자율은 가드레일 안에서만 성립한다.
# 원문 두 곳을 겹쳐 읽는다: 마이크로서비스 쪽 "로깅·모니터링 같은 핵심 결정 외에는 공통 표준이 필요 없다"와
# 프론트엔드 쪽 "기술 리더십이 현장 관행과 함께 가드레일을 제공한다".
# 타입 스펙: type-nested — 바깥이 넓은 범위, 안으로 갈수록 구체. 포함 관계가 곧 결정 권한의 범위다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, KR, MONO

W, H = 1000, 560
d = D(W, H, "BUILDING MICRO-FRONTENDS · 01-02 §3",
      "가드레일 안의 자율 — 결정 권한의 세 겹",
      "바깥 고리일수록 넓은 범위의 결정이고 안쪽 고리가 팀이 스스로 정하는 영역이다. 저자는 자율을 무제한이 아니라 울타리 안의 자율로 정의한다.",
      "안으로 들어갈수록 결정하는 주체가 좁아지고, 가장 안쪽이 팀의 몫입니다")

rings = [
    (60, 100, 880, 372, "SYSTEM-WIDE STANDARD", "시스템 공통 표준", "로깅 · 모니터링처럼 전체가 맞춰야 하는 핵심 결정만 남긴다", f"{INK}4D", 1.0, f"{INK}04"),
    (100, 156, 800, 260, "GUARDRAILS", "기술 리더십이 세운 가드레일", "아키텍트 · 프린시펄 엔지니어 · CTO가 현장 관행과 함께 정한다", MUTED, 1.1, f"{INK}06"),
]
for x, y, w, h, eyebrow, name, desc, stroke, sw, fill in rings:
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    lw = len(eyebrow) * 6.4 + 16
    d.o.append(f'<rect x="{x + 24}" y="{y - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
    d.t(x + 24 + lw / 2, y + 3, eyebrow, 7.5, SOFT, MONO)
    d.t(x + 24, y + 30, name, 14, INK, KR, "start", 600)
    d.t(x + 24, y + 50, desc, 11, MUTED, KR, "start")

# 가장 안쪽 — 팀의 자율 (accent 하나)
IX, IY, IW, IH = 140, 212, 720, 148
d.o.append(f'<rect x="{IX}" y="{IY}" width="{IW}" height="{IH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
lw = len("TEAM AUTONOMY") * 6.4 + 16
d.o.append(f'<rect x="{IX + 24}" y="{IY - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
d.t(IX + 24 + lw / 2, IY + 3, "TEAM AUTONOMY", 7.5, ACC, MONO)
d.t(IX + 24, IY + 32, "팀이 스스로 정하는 영역", 15, ACC, KR, "start", 600)
for i, line in enumerate(["도메인에 맞는 도구와 접근을 고른다",
                          "중앙 결정을 기다리지 않고 배포한다",
                          "도메인 전문성이 쌓이므로 팀이 가장 잘 판단한다"]):
    d.t(IX + 24, IY + 60 + i * 24, "· " + line, 12, MUTED, KR, "start")

d.legend(512, [("팀의 몫", ACC)])
d.save("01-02.guardrails-scope.svg")
print("h 필요:", 512 + 22 + 16, " 실제:", H)
