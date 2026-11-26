# 01-01 §4 대형 제품과 /opt 번들의 의존성 격리 및 OS 패치 사각지대.
# 타입 스펙: type-architecture — Secure paved road 패턴(공유 라이브러리 패치 도달 vs 번들 격리 경계 대조).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 540
d = D(W, H, "FHS 3.0 · /USR VS /OPT BUNDLE",
      "/opt 번들의 의존성 격리와 OS 패치 사각지대",
      "왼쪽 배포판 패키지는 /usr/lib 공유 라이브러리를 통해 OS 보안 패치를 일괄 반영받고, 오른쪽 /opt 번들은 자체 라이브러리로 충돌을 피하는 대신 공유 라이브러리 패치가 전파되지 않아 제품 별도 업그레이드가 필요하다.",
      "자체 번들은 /usr/lib 버전 충돌을 피하는 대신 공유 라이브러리 보안 패치 경로에서 벗어납니다")

LX, LW, RX, RW = 24, 408, 528, 408
ZY, ZH = 104, 360
for zx, zw, label in [(LX, LW, "DISTRO MANAGED · /USR"), (RX, RW, "/OPT BUNDLE · SELF-CONTAINED")]:
    d.o.append(f'<rect x="{zx}" y="{ZY}" width="{zw}" height="{ZH}" rx="8" fill="#F5F5F305" stroke="{RULE}" stroke-width="1.0" stroke-dasharray="4 4"/>')
    lw_mask = len(label) * 6.5 + 16
    d.o.append(f'<rect x="{zx + 16}" y="{ZY - 6}" width="{lw_mask}" height="14" rx="2" fill="{PAPER}"/>')
    d.t(zx + 24, ZY + 4, label, 8, SOFT, MONO, "start", 500)

LCX, RCX = LX + LW // 2, RX + RW // 2

# 왼쪽: OS 패키지 관리자 → /usr/lib (OK)
d.arrow([(LCX, 200), (LCX, 250)], OK, "ok", 1.6)
d.t(LCX + 16, 230, "보안 패치 일괄 반영", 13, OK, KR, "start", 500)

# 왼쪽: /usr/lib → 앱 A · 앱 B (직각 버스)
d.path(f"M {LCX} 316 L {LCX} 340", MUTED, 1.3)
d.path(f"M 132 340 L 324 340", MUTED, 1.3)
d.arrow([(132, 340), (132, 366)], MUTED, "ar", 1.3)
d.arrow([(324, 340), (324, 366)], MUTED, "ar", 1.3)

# 존 경계 차단선: /usr/lib 공유 라이브러리 패치 → 오른쪽 /opt 번들 경계 앞 정지 (BAD)
d.arrow([(372, 284), (500, 284)], BAD, "bad", 1.6, dash="5 4")
d.line(506, 276, 520, 292, BAD, 2.0)
d.line(506, 292, 520, 276, BAD, 2.0)
d.t(480, 264, "공유 패치 미전파", 13, BAD, KR, "middle", 600)

# 오른쪽: 제품 별도 업그레이드 → /opt/<pkg> 번들 (WARN)
d.arrow([(RCX, 200), (RCX, 250)], WARN, "warn", 1.6)
d.t(RCX + 16, 230, "제품 별도 패치 필수", 13, WARN, KR, "start", 500)

# 오른쪽: /opt/<pkg> 번들 → /etc/opt · /var/opt (점선 직각 버스)
d.path(f"M {RCX} 320 L {RCX} 344", MUTED, 1.2, dash="4 3")
d.path(f"M 636 344 L 828 344", MUTED, 1.2, dash="4 3")
d.arrow([(636, 344), (636, 366)], MUTED, "ar", 1.2, dash="4 3")
d.arrow([(828, 344), (828, 366)], MUTED, "ar", 1.2, dash="4 3")

# 왼쪽 노드
d.tone(100, 144, 256, 56, OK, r=6, op="12", sw=1.2)
d.t(LCX, 168, "OS 패키지 관리자", 14, OK, KR, "middle", 600)
d.t(LCX, 188, "apt · dnf", 12, MUTED, MONO)

d.box(84, 252, 288, 64, PAPER2, RULE, 1.0, 6)
d.t(LCX, 278, "공유 라이브러리 · 단일 버전 정렬", 13, INK, KR, "middle", 600)
d.t(LCX, 300, "/usr/lib", 12, MUTED, MONO)

for ax, nm, path in [(48, "배포판 앱 A", "/usr/bin/appA"), (240, "배포판 앱 B", "/usr/bin/appB")]:
    d.box(ax, 368, 168, 68, PAPER2, RULE, 1.0, 6)
    d.t(ax + 84, 396, nm, 14, INK, KR, "middle", 600)
    d.t(ax + 84, 420, path, 12, MUTED, MONO)

# 오른쪽 노드
d.tone(604, 144, 256, 56, WARN, r=6, op="12", sw=1.2)
d.t(RCX, 168, "공급자 패키지 업그레이드", 14, WARN, KR, "middle", 600)
d.t(RCX, 190, "OS 패치와 독립 주기", 13, MUTED, KR)

# FOCAL 노드
d.o.append(f'<rect x="564" y="252" width="336" height="68" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(RCX, 278, "/opt/<pkg> 자체 번들", 15, ACC, KR, "middle", 600)
d.t(RCX, 302, "/opt/<pkg>/bin · 번들 라이브러리", 13, INK, KR)

for bx, nm, path in [(552, "호스트 설정", "/etc/opt/<pkg>"), (744, "가변 데이터", "/var/opt/<pkg>")]:
    d.box(bx, 368, 168, 68, PAPER2, RULE, 1.0, 6)
    d.t(bx + 84, 396, nm, 14, INK, KR, "middle", 600)
    d.t(bx + 84, 420, path, 12, MUTED, MONO)

d.legend(492, [("번들 격리 (충돌 회피)", ACC), ("OS 패치 도달", OK), ("공유 패치 차단", BAD), ("제품 별도 패치", WARN)])
d.save("01-01.opt-bundle-patch.svg")
