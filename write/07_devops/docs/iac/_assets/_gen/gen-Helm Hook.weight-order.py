# 타입 스펙: type-sequence
# 3절 Hook 여러 개의 실행 순서 — hook-weight 오름차순 순차 실행
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 600

d = D(W, H, "HELM · HOOK WEIGHT ORDER",
      "Hook 여러 개의 실행 순서와 weight 기반 오름차순 제어",
      "동일 시점 Hook 여러 개가 있을 때 hook-weight 오름차순으로 순차 실행되는 과정 및 본 리소스 적용 순서",
      lead="이름 순과 반대로 weight -5 인 b-backup 이 먼저 돌고, 완료 후 weight 5 인 a-migrate 가 실행됩니다")

# 4개 레인 좌표: x = 120, 352, 584, 816 (모두 4의 배수, 간격 232px)
LANES = [
    ("Helm", "helm upgrade (rev 3)"),
    ("hl-hokv-app-b-backup", "weight: \"-5\" · 사전 백업"),
    ("hl-hokv-app-a-migrate", "weight: \"5\" · 마이그레이션"),
    ("hl-hokv-app-app", "Deployment · 본 리소스"),
]

LX = {}
LANE_W = 192
Y0 = 96
LANE_H = 44

for i, (nm, sub) in enumerate(LANES):
    x = 120 + i * 232
    LX[nm] = x
    d.box(x - LANE_W // 2, Y0, LANE_W, LANE_H, PAPER2, RULE, 1.0)
    d.t(x, Y0 + 19, nm, 13, INK, KR if any("가" <= c <= "힣" for c in nm) else MONO, "middle", 600)
    d.t(x, Y0 + 35, sub, 11, MUTED, KR if any("가" <= c <= "힣" for c in sub) else MONO)

# 수직 레일
Y_TOP = Y0 + LANE_H
Y_BOT = 516
for x in LX.values():
    d.line(x, Y_TOP + 6, x, Y_BOT, RULE, 1.0, "3 6")


def msg(a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
    x1, x2 = LX[a], LX[b]
    dr = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
    mx = (x1 + x2) // 2
    w = sum(13.0 if "가" <= ch <= "힣" else 7.5 for ch in label) + 24
    d.o.append(f'<rect x="{mx - w / 2}" y="{y - 18}" width="{w}" height="16" rx="2" fill="{PAPER}"/>')
    d.t(mx, y - 6, label, 13, c, KR if any("가" <= ch <= "힣" for ch in label) else MONO, "middle", 600)
    if sub:
        sw = sum(12.0 if "가" <= ch <= "힣" else 7.2 for ch in sub) + 20
        d.o.append(f'<rect x="{mx - sw / 2}" y="{y + 6}" width="{sw}" height="16" rx="2" fill="{PAPER}"/>')
        d.t(mx, y + 18, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


def state_chip(key, txt, y, c):
    x = LX[key]
    w = sum(13.0 if "가" <= ch <= "힣" else 7.8 for ch in txt) + 28
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 14}" width="{w}" height="28" rx="4" fill="{PAPER}"/>')
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 14}" width="{w}" height="28" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 5, txt, 13, c, KR if any("가" <= ch <= "힣" for ch in txt) else MONO, "middle", 600)


# 1. Helm -> b-backup: weight -5 우선 실행
msg("Helm", "hl-hokv-app-b-backup", "1. Job 생성 (weight -5)", 176, ACC, "acc")
state_chip("hl-hokv-app-b-backup", "START: 19:54:09Z", 212, INFO)
state_chip("hl-hokv-app-b-backup", "DONE: 19:54:14Z (성공)", 252, OK)

# 2. b-backup -> Helm: 완료 감지
msg("hl-hokv-app-b-backup", "Helm", "2. 완료 감지 (Wait 완료)", 292, MUTED, "ar", dash="4 4")

# 3. Helm -> a-migrate: weight 5 후속 실행
msg("Helm", "hl-hokv-app-a-migrate", "3. Job 생성 (weight 5)", 336, INFO, "info")
state_chip("hl-hokv-app-a-migrate", "START: 19:54:14Z", 372, INFO)
state_chip("hl-hokv-app-a-migrate", "DONE: 19:54:17Z (성공)", 412, OK)

# 4. a-migrate -> Helm: 완료 감지
msg("hl-hokv-app-a-migrate", "Helm", "4. 완료 감지 (Hook 종료)", 452, MUTED, "ar", dash="4 4")

# 5. Helm -> Deployment: 본 리소스 매니페스트 적용
msg("Helm", "hl-hokv-app-app", "5. 본 리소스 매니페스트 적용", 492, OK, "ok")
state_chip("hl-hokv-app-app", "STATUS: deployed (rev 3)", 528, OK)

# 범례
LEG_Y = 552
d.legend(LEG_Y, [
    ("우선 실행 (weight -5)", ACC),
    ("후속 실행 (weight 5)", INFO),
    ("작업 완료 및 배포", OK),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm Hook.weight-order.svg")
d.save(out_path)
print("ok gen-Helm Hook.weight-order")
