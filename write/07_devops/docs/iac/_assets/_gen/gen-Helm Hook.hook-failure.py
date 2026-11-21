# 타입 스펙: type-state
# 5절 Hook 이 실패하면 배포는 어떻게 되는가 — 실패 상태 전이 및 복구 경로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 460

d = D(W, H, "HELM · HOOK FAILURE RECOVERY",
      "Hook 실패 시 릴리스 상태 전이와 복구 경로",
      "pre-upgrade Hook 실패로 인한 failed 상태 전이 및 helm rollback 과 --rollback-on-failure 두 가지 복구 경로",
      lead="Hook 실패 시 릴리스는 failed 로 남으며, 직접 수동 롤백하거나 플래그로 자동 롤백해 정상 복구합니다")

# 시작점 (fill dot) — 연결선 38px 로 short advice 방지
START_X, START_Y = 18, 170
d.o.append(f'<circle cx="{START_X}" cy="{START_Y}" r="6" fill="{INK}"/>')
d.arrow([(START_X + 8, START_Y), (64, START_Y)], MUTED, "ar", 1.2)

# 상태 1: deployed (초기 릴리스)
S1_X, S1_Y, S1_W, S1_H = 66, 126, 196, 88
d.box(S1_X, S1_Y, S1_W, S1_H, PAPER, OK, 1.2, 8)
d.t(S1_X + S1_W // 2, S1_Y + 26, "STATUS: deployed", 13, OK, MONO, "middle", 600)
d.t(S1_X + S1_W // 2, S1_Y + 46, "REVISION: 9 (1.0.0)", 12, INK, MONO, "middle")
d.chip(S1_X + S1_W // 2, S1_Y + 68, "정상 릴리스", OK, 11)

# 전이 1 -> 2: helm upgrade failure (S1 우측 262 -> S2 좌측 412, 간격 150px, 중심 337)
T1_Y = 170
d.arrow([(S1_X + S1_W + 2, T1_Y), (410, T1_Y)], BAD, "bad", 1.4)
d.t(337, T1_Y - 18, "helm upgrade (2.0.0)", 11, BAD, MONO, "middle", 600)
d.t(337, T1_Y - 5, "Hook 실패 (exit 1)", 11, BAD, KR, "middle")
d.t(337, T1_Y + 16, "failed: 1/1", 11, MUTED, MONO, "middle")

# 상태 2: failed (Hook 실패로 인한 릴리스 상태) — FOCAL
S2_X, S2_Y, S2_W, S2_H = 412, 126, 196, 88
d.box(S2_X, S2_Y, S2_W, S2_H, PAPER, BAD, 1.4, 8)
d.t(S2_X + S2_W // 2, S2_Y + 26, "STATUS: failed", 13, BAD, MONO, "middle", 600)
d.t(S2_X + S2_W // 2, S2_Y + 46, "REVISION: 10 (1.0.0)", 12, BAD, KR, "middle")
d.chip(S2_X + S2_W // 2, S2_Y + 68, "배포 중단 (파드 미적용)", BAD, 11)

# ── 분기 A: 수동 롤백 (helm rollback) (S2 우측 608 -> S3A 좌측 720, 간격 112px, 중심 664)
TA_Y = 150
d.arrow([(S2_X + S2_W + 2, TA_Y), (718, TA_Y)], ACC, "acc", 1.4)
d.t(664, TA_Y - 14, "helm rollback", 11, ACC, MONO, "middle", 600)
d.t(664, TA_Y + 14, "직접 롤백 (rev 9)", 11, MUTED, KR, "middle")

# 상태 3A: deployed (수동 롤백 완료)
S3A_X, S3A_Y, S3A_W, S3A_H = 720, 106, 204, 88
d.box(S3A_X, S3A_Y, S3A_W, S3A_H, PAPER, OK, 1.2, 8)
d.t(S3A_X + S3A_W // 2, S3A_Y + 26, "STATUS: deployed", 13, OK, MONO, "middle", 600)
d.t(S3A_X + S3A_W // 2, S3A_Y + 46, "rev 11 (Rollback to 9)", 12, INK, MONO, "middle")
d.chip(S3A_X + S3A_W // 2, S3A_Y + 68, "수동 복구 완료", OK, 11)

# 종료점 A (ringed dot)
END_A_X, END_A_Y = 940, 150
d.o.append(f'<circle cx="{END_A_X}" cy="{END_A_Y}" r="8" fill="none" stroke="{OK}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="{END_A_X}" cy="{END_A_Y}" r="5" fill="{OK}"/>')
d.line(S3A_X + S3A_W + 2, END_A_Y, END_A_X - 10, END_A_Y, OK, 1.2)

# ── 분기 B: 자동 롤백 (--rollback-on-failure) ─────────────────────────
TB_Y = 300
d.path(f"M {S2_X + S2_W // 2} {S2_Y + S2_H + 2} L {S2_X + S2_W // 2} {TB_Y} L 718 {TB_Y}", INFO, 1.4, m="info")
d.t(616, TB_Y - 14, "--rollback-on-failure", 11, INFO, MONO, "middle", 600)
d.t(616, TB_Y + 14, "다시 upgrade · rev 12 failed → 자동 롤백", 11, MUTED, KR, "middle")

# 상태 3B: deployed (자동 롤백 완료)
S3B_X, S3B_Y, S3B_W, S3B_H = 720, 256, 204, 88
d.box(S3B_X, S3B_Y, S3B_W, S3B_H, PAPER, OK, 1.2, 8)
d.t(S3B_X + S3B_W // 2, S3B_Y + 26, "STATUS: deployed", 13, OK, MONO, "middle", 600)
d.t(S3B_X + S3B_W // 2, S3B_Y + 46, "rev 13 (Rollback to 11)", 12, INK, MONO, "middle")
d.chip(S3B_X + S3B_W // 2, S3B_Y + 68, "자동 복구 완료", OK, 11)

# 종료점 B (ringed dot)
END_B_X, END_B_Y = 940, 300
d.o.append(f'<circle cx="{END_B_X}" cy="{END_B_Y}" r="8" fill="none" stroke="{OK}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="{END_B_X}" cy="{END_B_Y}" r="5" fill="{OK}"/>')
d.line(S3B_X + S3B_W + 2, END_B_Y, END_B_X - 10, END_B_Y, OK, 1.2)

# 범례
LEG_Y = 404
d.legend(LEG_Y, [
    ("정상 배포 (deployed)", OK),
    ("배포 실패 (failed)", BAD),
    ("수동 롤백 경로", ACC),
    ("자동 롤백 경로", INFO),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm Hook.hook-failure.svg")
d.save(out_path)
print("ok gen-Helm Hook.hook-failure")
