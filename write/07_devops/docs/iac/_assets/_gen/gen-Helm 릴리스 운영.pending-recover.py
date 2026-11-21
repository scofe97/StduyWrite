# 타입 스펙: type-state
# 6절 pending 으로 멈춘 릴리스 — 릴리스 상태 전이와 복구 경로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 424

d = D(W, H, "HELM · RELEASE RECOVERY",
      "pending-upgrade 고착과 롤백 및 Secret 삭제 복구 전이",
      "비정상 중단으로 인한 릴리스 잠금 상태와 두 가지 복구 경로(롤백 vs Secret 삭제)의 이력 전이",
      lead="kill -9 로 멈춘 pending-upgrade 해제 경로 · 롤백(Rev 7 잔존) vs Secret 삭제(Rev 9 재사용)")

# ── 시작점 ──────────────────────────────────────────────
d.o.append(f'<circle cx="24" cy="220" r="6" fill="{INK}"/>')
d.arrow([(30, 220), (88, 220)], MUTED, "ar", 1.2)

# ── 상태 1: deployed (Rev 6) ───────────────────────────
N1_X, N1_Y, N1_W, N1_H = 90, 172, 168, 96
d.tone(N1_X, N1_Y, N1_W, N1_H, OK, 8, "14", 1.2)
d.t(N1_X + N1_W // 2, N1_Y + 28, "deployed", 15, OK, MONO, "middle", 600)
d.t(N1_X + N1_W // 2, N1_Y + 48, "리비전 6 · 정상 운영", 12, INK, KR, "middle")
d.line(N1_X + 16, N1_Y + 60, N1_X + N1_W - 16, N1_Y + 60, RULE, 0.8)
d.t(N1_X + N1_W // 2, N1_Y + 80, "hl-rel-chart (1.25.0)", 11, MUTED, MONO, "middle")

# ── 전이 1 -> 2: kill -9 중단 ──────────────────────────
d.arrow([(N1_X + N1_W + 2, 220), (370, 220)], ACC, "acc", 1.4)
d.t(315, 208, "upgrade 중 중단", 11, ACC, KR, "middle", 600)
d.t(315, 236, "kill -9 강제 종료", 11, MUTED, MONO, "middle")

# ── 상태 2: pending-upgrade (Rev 7) [Focal] ────────────
N2_X, N2_Y, N2_W, N2_H = 372, 172, 196, 96
d.tone(N2_X, N2_Y, N2_W, N2_H, ACC, 8, "14", 1.4)
d.t(N2_X + N2_W // 2, N2_Y + 28, "pending-upgrade", 15, ACC, MONO, "middle", 600)
d.t(N2_X + N2_W // 2, N2_Y + 48, "리비전 7 · 비정상 중단", 12, INK, KR, "middle")
d.line(N2_X + 16, N2_Y + 60, N2_X + N2_W - 16, N2_Y + 60, RULE, 0.8)
d.t(N2_X + N2_W // 2, N2_Y + 80, "Preparing upgrade", 11, MUTED, MONO, "middle")

# ── 상태 2 자체 루프: upgrade 재시도 거절 ───────────────
d.arrow([(420, N2_Y), (420, 128), (520, 128), (520, N2_Y - 4)], BAD, "bad", 1.3)
d.t(470, 104, "helm upgrade 재시도", 11, MUTED, KR, "middle")
d.t(470, 120, "another operation in progress", 10, BAD, MONO, "middle")

# ── 복구 경로 1 (상단): helm rollback ──────────────────
d.arrow([(N2_X + N2_W + 2, 204), (646, 204), (646, 148), (722, 148)], INFO, "info", 1.3)
d.t(607, 194, "직전 6 복구", 11, MUTED, KR, "middle")
d.t(670, 136, "helm rollback", 11, INFO, MONO, "middle", 600)

# ── 상태 3A: deployed (Rev 8) ──────────────────────────
N3A_X, N3A_Y, N3A_W, N3A_H = 724, 100, 196, 96
d.tone(N3A_X, N3A_Y, N3A_W, N3A_H, OK, 8, "14", 1.2)
d.t(N3A_X + N3A_W // 2, N3A_Y + 24, "deployed", 15, OK, MONO, "middle", 600)
d.t(N3A_X + N3A_W // 2, N3A_Y + 44, "리비전 8 · 롤백 완료", 12, INK, KR, "middle")
d.line(N3A_X + 16, N3A_Y + 54, N3A_X + N3A_W - 16, N3A_Y + 54, RULE, 0.8)
d.t(N3A_X + N3A_W // 2, N3A_Y + 68, "Rev 7 pending 이력 잔존", 11, ACC, KR, "middle")
d.t(N3A_X + N3A_W // 2, N3A_Y + 84, "Rollback to 6", 11, MUTED, MONO, "middle")

# 3A 종료 표지
d.line(N3A_X + N3A_W, 148, 930, 148, MUTED, 1.2)
d.o.append(f'<circle cx="938" cy="148" r="8" fill="none" stroke="{INK}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="938" cy="148" r="5" fill="{INK}"/>')

# ── 복구 경로 2 (하단): delete secret + upgrade ────────
d.arrow([(N2_X + N2_W + 2, 236), (646, 236), (646, 292), (722, 292)], INFO, "info", 1.3)
d.t(607, 226, "Secret 삭제", 11, INFO, KR, "middle", 600)
d.t(670, 306, "upgrade 재시도", 11, MUTED, KR, "middle")

# ── 상태 3B: deployed (Rev 9) ──────────────────────────
N3B_X, N3B_Y, N3B_W, N3B_H = 724, 244, 196, 96
d.tone(N3B_X, N3B_Y, N3B_W, N3B_H, OK, 8, "14", 1.2)
d.t(N3B_X + N3B_W // 2, N3B_Y + 24, "deployed", 15, OK, MONO, "middle", 600)
d.t(N3B_X + N3B_W // 2, N3B_Y + 44, "리비전 9 · 재배포 완료", 12, INK, KR, "middle")
d.line(N3B_X + 16, N3B_Y + 54, N3B_X + N3B_W - 16, N3B_Y + 54, RULE, 0.8)
d.t(N3B_X + N3B_W // 2, N3B_Y + 68, "Secret v7·v9 삭제", 11, INFO, KR, "middle")
d.t(N3B_X + N3B_W // 2, N3B_Y + 84, "리비전 번호 9 재사용", 11, MUTED, KR, "middle")

# 3B 종료 표지
d.line(N3B_X + N3B_W, 292, 930, 292, MUTED, 1.2)
d.o.append(f'<circle cx="938" cy="292" r="8" fill="none" stroke="{INK}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="938" cy="292" r="5" fill="{INK}"/>')

# ── 범례 ────────────────────────────────────────────────
LEG_Y = 376
d.legend(LEG_Y, [
    ("정상 배포 (deployed)", OK),
    ("고착 상태 (pending)", ACC),
    ("재시도 거절", BAD),
    ("복구 조치", INFO),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm 릴리스 운영.pending-recover.svg")
d.save(out_path)
print("ok gen-Helm 릴리스 운영.pending-recover")
