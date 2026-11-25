# 타입 스펙: type-flowchart
# 2절 helm lint 와 렌더 테스트의 오류 검출 분기 (Paired policy-evaluation traces)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, PAPER, PAPER2, KR, MONO

W, H = 904, 472

d = D(W, H, "HELM · LINT VS RENDER TEST",
      "helm lint 와 렌더 테스트의 오류 검출 분기",
      "위험한 Role 권한이 든 ./t3/demo 사본이 helm lint --strict 는 종료 코드 0 으로 통과하고 render-test.sh 에서 차단되는 두 경로",
      lead="동일 차트 사본(./t3/demo) 입력 · lint 는 형식만 확인해 통과하고, 렌더 테스트는 값 단언에서 차단(Helm v4.1.4 실측)")

# ── 상단 입력 차트 ──────────────────────────────────────────────────────
IN_X, IN_Y, IN_W, IN_H = 132, 92, 640, 44
d.box(IN_X, IN_Y, IN_W, IN_H, PAPER2, RULE, 1.1, 6)
d.t(452, IN_Y + 18, "입력 차트 사본: ./t3/demo", 13, INK, KR, "middle", 600)
d.t(452, IN_Y + 35, 'Role verbs: ["*"]  ·  (YAML 형식은 정상)', 12, MUTED, MONO, "middle")

# 레인 좌표 (모두 4의 배수)
LX, RX = 220, 684
LANE_W = 328
LX0 = LX - LANE_W // 2  # 56
RX0 = RX - LANE_W // 2  # 520

# 입력 -> 양쪽 레인 분기 화살표 (직각 꺾임)
d.arrow([(452, IN_Y + IN_H), (452, 144), (LX, 144), (LX, 156)], MUTED, "ar", 1.2)
d.arrow([(452, IN_Y + IN_H), (452, 144), (RX, 144), (RX, 156)], MUTED, "ar", 1.2)

# ── 레인 헤더 ────────────────────────────────────────────────────────────
HDR_Y, HDR_H = 156, 40
d.box(LX0, HDR_Y, LANE_W, HDR_H, PAPER2, RULE, 1.0, 6)
d.t(LX, HDR_Y + 25, "helm lint ./t3/demo --strict", 13, INK, MONO, "middle", 600)

d.box(RX0, HDR_Y, LANE_W, HDR_H, PAPER2, RULE, 1.0, 6)
d.t(RX, HDR_Y + 25, "./render-test.sh ./t3/demo", 13, INK, MONO, "middle", 600)

# ── 1행: 첫 분기점 ──────────────────────────────────────────────────────
Y1, ROW_H = 216, 56
d.arrow([(LX, HDR_Y + HDR_H), (LX, Y1)], MUTED, "ar", 1.2)
d.arrow([(RX, HDR_Y + HDR_H), (RX, Y1)], MUTED, "ar", 1.2)

d.tone(LX0, Y1, LANE_W, ROW_H, OK, 6, "12", 1.1)
d.t(LX0 + 16, Y1 + 22, "차트 형식 · 값의 의미는 점검 밖", 12, MUTED, KR, "start")
d.t(LX0 + 16, Y1 + 42, "통과 · Role 의 * 도 올바른 YAML", 13, OK, KR, "start", 600)

# 중앙 첫 분기점 마커 (Focal)
d.tone(400, Y1 + 4, 104, 48, ACC, 6, "16", 1.4)
d.t(452, Y1 + 24, "첫 분기점", 13, ACC, KR, "middle", 600)
d.t(452, Y1 + 42, "값 의미 검사", 12, INK, KR, "middle")
d.line(384, Y1 + 28, 400, Y1 + 28, ACC, 1.2, "3 3")
d.line(504, Y1 + 28, 520, Y1 + 28, ACC, 1.2, "3 3")

d.tone(RX0, Y1, LANE_W, ROW_H, BAD, 6, "14", 1.3)
d.t(RX0 + 16, Y1 + 22, "단언 1 · Role verbs 가 get,list 인가", 12, MUTED, KR, "start")
d.t(RX0 + 16, Y1 + 42, "FAIL · Role verbs: *,get,list", 13, BAD, KR, "start", 600)

# ── 2행: fail 로 막은 mode 값 ───────────────────────────────────────────
Y2 = 288
d.arrow([(LX, Y1 + ROW_H), (LX, Y2)], WARN, "warn", 1.2)
d.arrow([(RX, Y1 + ROW_H), (RX, Y2)], BAD, "bad", 1.2, "4 4")

d.tone(LX0, Y2, LANE_W, ROW_H, WARN, 6, "12", 1.1)
d.t(LX0 + 16, Y2 + 22, "fail 로 막아 둔 잘못된 mode 값", 12, MUTED, KR, "start")
d.t(LX0 + 16, Y2 + 42, "lint 는 통과시킴 (실측)", 13, WARN, KR, "start", 600)

d.box(RX0, Y2, LANE_W, ROW_H, PAPER2, RULE, 1.0, 6)
d.t(RX0 + 16, Y2 + 22, "단언 4 · --set mode=weird 는 렌더 실패인가", 12, MUTED, KR, "start")
d.t(RX0 + 16, Y2 + 42, "NOT REACHED · 앞 단언에서 중단", 13, SOFT, KR, "start", 600)

# ── 최종 결과 ────────────────────────────────────────────────────────────
Y4, OUT_H = 360, 44
d.arrow([(LX, Y2 + ROW_H), (LX, Y4)], WARN, "warn", 1.3)
d.arrow([(RX, Y2 + ROW_H), (RX, Y4)], BAD, "bad", 1.3)

d.tone(LX0, Y4, LANE_W, OUT_H, WARN, 6, "14", 1.2)
d.t(LX, Y4 + 27, "종료 코드 0 · 위험 매니페스트 통과 (실측)", 13, WARN, KR, "middle", 600)

d.tone(RX0, Y4, LANE_W, OUT_H, BAD, 6, "14", 1.2)
d.t(RX, Y4 + 27, "종료 코드 1 · FAIL 차단 (실측)", 13, BAD, KR, "middle", 600)

# ── 범례 ────────────────────────────────────────────────────────────────
LEG_Y = 424
d.legend(LEG_Y, [
    ("형식 점검 통과", OK),
    ("값 의미를 못 거름", WARN),
    ("실패 차단 (FAIL)", BAD),
    ("첫 분기점", ACC),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm 렌더 테스트.lint-vs-render-test.svg")
d.save(out_path)
print("ok gen-Helm 렌더 테스트.lint-vs-render-test")
