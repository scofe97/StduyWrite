# 타입 스펙: type-flowchart
# 7절 직접 고친 값과 upgrade 충돌 — 버전별 적용 방식과 충돌 흐름
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 480

d = D(W, H, "HELM · SSA CONFLICT FLOWCHART",
      "설치 및 upgrade 도구 버전에 따른 replicas 값 갱신 및 충돌 흐름",
      "kubectl scale 로 바꾼 replicas=3 에 대해 Helm 3(CSA) 와 Helm 4(SSA) 가 처리하는 덮어쓰기 및 소유권 충돌 분기",
      lead="릴리스 설치 도구(Helm 3 vs 4)와 upgrade 방식(CSA vs SSA)에 따른 replicas 값 보존 및 충돌 오류 분기")

# ── 시작: kubectl scale ────────────────────────────────
d.o.append(f'<rect x="348" y="90" width="264" height="34" rx="17" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
d.t(480, 112, "kubectl scale --replicas=3", 12, INK, MONO, "middle", 600)

# 시작 -> 분기 1
d.arrow([(480, 124), (480, 154)], MUTED, "ar", 1.2)

# ── 분기 1: 릴리스 설치 도구 ───────────────────────────
d.o.append(f'<path d="M 480 154 L 576 176 L 480 198 L 384 176 Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
d.t(480, 180, "릴리스 설치 도구?", 12, INK, KR, "middle")

# ── 왼쪽 가지: Helm 3 (CSA) ────────────────────────────
d.arrow([(384, 176), (240, 176), (240, 222)], INFO, "info", 1.3)
d.t(312, 168, "Helm 3 설치", 11, INFO, KR, "middle")

# 분기 2A: Helm 3 설치 후 upgrade 도구
d.o.append(f'<path d="M 240 222 L 336 244 L 240 266 L 144 244 Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
d.t(240, 248, "upgrade 실행 도구?", 12, INK, KR, "middle")

# 2A-1: Helm 3 upgrade
d.arrow([(144, 244), (122, 244), (122, 294)], OK, "ok", 1.3)
d.t(112, 268, "Helm 3", 11, OK, MONO, "end")

# 카드 1: Helm 3 -> Helm 3
d.tone(24, 296, 196, 108, OK, 6, "14", 1.2)
d.t(122, 318, "Helm 3 upgrade", 13, OK, MONO, "middle", 600)
d.t(122, 336, "CSA 전략적 병합", 11, MUTED, KR, "middle")
d.line(36, 346, 208, 346, RULE, 0.8)
d.t(122, 366, "차트 값으로 덮어씀", 12, INK, KR, "middle")
d.t(122, 388, "replicas: 3 → 2", 12, OK, MONO, "middle", 600)

# 2A-2: Helm 4 (auto) upgrade
d.arrow([(336, 244), (362, 244), (362, 294)], OK, "ok", 1.3)
d.t(372, 268, "Helm 4 (auto)", 11, OK, MONO, "start")

# 카드 2: Helm 3 -> Helm 4
d.tone(260, 296, 204, 108, OK, 6, "14", 1.2)
d.t(362, 318, "Helm 4 upgrade", 13, OK, MONO, "middle", 600)
d.t(362, 336, "직전 CSA 방식 계승", 11, MUTED, KR, "middle")
d.line(272, 346, 452, 346, RULE, 0.8)
d.t(362, 366, "차트 값으로 덮어씀", 12, INK, KR, "middle")
d.t(362, 388, "replicas: 3 → 2", 12, OK, MONO, "middle", 600)

# ── 오른쪽 가지: Helm 4 (SSA) ───────────────────────────
d.arrow([(576, 176), (720, 176), (720, 222)], ACC, "acc", 1.3)
d.t(648, 168, "Helm 4 설치 (SSA)", 11, ACC, KR, "middle")

# 분기 2B: Helm 4 설치 후 충돌 옵션
d.o.append(f'<path d="M 720 222 L 820 244 L 720 266 L 620 244 Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
d.t(720, 248, "--force-conflicts?", 12, INK, MONO, "middle")

# 2B-1: 미지정 (기본값) -> 충돌 실패 [Focal]
d.arrow([(620, 244), (598, 244), (598, 294)], BAD, "bad", 1.3)
d.t(588, 268, "기본값 (미지정)", 11, BAD, KR, "end")

# 카드 3: 충돌 오류
d.tone(496, 296, 204, 108, BAD, 6, "16", 1.4)
d.t(598, 318, "소유권 충돌 오류", 13, BAD, KR, "middle", 600)
d.t(598, 336, "UPGRADE FAILED", 11, BAD, MONO, "middle")
d.line(508, 346, 688, 346, RULE, 0.8)
d.t(598, 366, "소유권 충돌 발생", 11, INK, KR, "middle")
d.t(598, 388, "conflict: .spec.replicas", 11, BAD, MONO, "middle", 600)

# 2B-2: --force-conflicts 지정 -> 덮어씀
d.arrow([(820, 244), (834, 244), (834, 294)], WARN, "warn", 1.3)
d.t(824, 284, "--force-conflicts", 11, WARN, MONO, "end")

# 카드 4: 강제 덮어쓰기
d.tone(732, 296, 204, 108, WARN, 6, "14", 1.2)
d.t(834, 318, "소유권 강제 탈환", 13, WARN, KR, "middle", 600)
d.t(834, 336, "SSA 강제 덮어쓰기", 11, MUTED, KR, "middle")
d.line(744, 346, 924, 346, RULE, 0.8)
d.t(834, 366, "차트 값으로 덮어씀", 12, INK, KR, "middle")
d.t(834, 388, "replicas: 3 → 1", 12, WARN, MONO, "middle", 600)

# ── 범례 ────────────────────────────────────────────────
LEG_Y = 436
d.legend(LEG_Y, [
    ("덮어씀 (CSA)", OK),
    ("충돌 오류 (SSA)", BAD),
    ("강제 덮어쓰기", WARN),
    ("설치 분기", ACC),
    ("도구 분기", INFO),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm 릴리스 운영.ssa-conflict.svg")
d.save(out_path)
print("ok gen-Helm 릴리스 운영.ssa-conflict")
