# 타입 스펙: type-flowchart
# 7절 차트 변경 검증 순서 — 관문별 오류 차단 및 통과 흐름
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 554

d = D(W, H, "HELM · VERIFICATION GATES",
      "차트 변경 검증 순서와 오류 검출 범위",
      "문법 오류, 렌더 오류, 필드 형식 오류가 4단계 검증 관문에서 차단되거나 통과하는 흐름",
      lead="가벼운 점검부터 순차 검증 · 필드 형식 오류는 API 서버 dry-run=server 에서만 차단")

CX = 240
BOX_X = 520
BOX_W = 410
BOX_H = 50

# ── 시작 노드: 차트 매니페스트 변경 ─────────────────────────────────────
Y0 = 96
d.o.append(f'<rect x="{CX - 80}" y="{Y0 - 15}" width="160" height="30" rx="15" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
d.t(CX, Y0 + 4, "차트 매니페스트 변경", 12, INK, KR, "middle")

# ── 관문 1: helm lint (문법 점검) ────────────────────────────────────────
Y1 = 154
d.arrow([(CX, Y0 + 15), (CX, Y1 - 22)], MUTED, "ar", 1.2)

d.o.append(f'<path d="M {CX} {Y1 - 22} L {CX + 95} {Y1} L {CX} {Y1 + 22} L {CX - 95} {Y1} Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
d.t(CX, Y1 + 4, "helm lint (문법 점검)", 12, INK, KR, "middle")

# 관문 1 문법 오류 -> 차단 박스
d.arrow([(CX + 95, Y1), (BOX_X - 2, Y1)], BAD, "bad", 1.4)
d.t(426, Y1 - 8, "문법 오류", 11, BAD, KR, "middle", 600)
d.tone(BOX_X, Y1 - BOX_H // 2, BOX_W, BOX_H, BAD, 6, "12", 1.2)
d.t(BOX_X + 16, Y1 - 6, "helm lint 실패 (차단)", 12, BAD, KR, "start", 600)
d.t(BOX_X + 16, Y1 + 14, "Chart.yaml 메타데이터 누락 · 템플릿 기본 문법 위반", 11, MUTED, KR, "start")

# 관문 1 통과 -> 관문 2로
Y2 = 236
d.arrow([(CX, Y1 + 22), (CX, Y2 - 22)], MUTED, "ar", 1.2)
d.t(CX + 14, (Y1 + 22 + Y2 - 22) // 2 + 4, "통과", 11, MUTED, KR, "start")

# ── 관문 2: helm template (로컬 YAML 렌더링) ─────────────────────────────
d.o.append(f'<path d="M {CX} {Y2 - 22} L {CX + 95} {Y2} L {CX} {Y2 + 22} L {CX - 95} {Y2} Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
d.t(CX, Y2 + 4, "helm template (YAML 렌더)", 12, INK, KR, "middle")

# 관문 2 렌더 오류 -> 차단 박스
d.arrow([(CX + 95, Y2), (BOX_X - 2, Y2)], BAD, "bad", 1.4)
d.t(426, Y2 - 8, "렌더 오류", 11, BAD, KR, "middle", 600)
d.tone(BOX_X, Y2 - BOX_H // 2, BOX_W, BOX_H, BAD, 6, "12", 1.2)
d.t(BOX_X + 16, Y2 - 6, "helm template 실패 (차단)", 12, BAD, KR, "start", 600)
d.t(BOX_X + 16, Y2 + 14, "required 빈 값 · 템플릿 실행 오류", 11, MUTED, KR, "start")

# 관문 2 통과 -> 관문 3으로
Y3 = 318
d.arrow([(CX, Y2 + 22), (CX, Y3 - 22)], MUTED, "ar", 1.2)
d.t(CX + 14, (Y2 + 22 + Y3 - 22) // 2 + 4, "통과", 11, MUTED, KR, "start")

# ── 관문 3: dry-run=server (Helm 서버 시뮬레이션) ─────────────────────────
d.o.append(f'<path d="M {CX} {Y3 - 22} L {CX + 95} {Y3} L {CX} {Y3 + 22} L {CX - 95} {Y3} Z" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>')
d.t(CX, Y3 + 4, "dry-run=server (Helm)", 12, INK, KR, "middle")

# 관문 3 필드 형식 오류 -> 미감지 통과 (위험)
d.arrow([(CX + 95, Y3), (BOX_X - 2, Y3)], WARN, "warn", 1.4)
d.t(426, Y3 - 8, "필드 오류", 11, WARN, KR, "middle", 600)
d.tone(BOX_X, Y3 - BOX_H // 2, BOX_W, BOX_H, WARN, 6, "12", 1.2)
d.t(BOX_X + 16, Y3 - 6, "오류 없이 통과 (미감지)", 12, WARN, KR, "start", 600)
d.t(BOX_X + 16, Y3 + 14, "Helm 4.1.4 스키마 미검증 · ConfigMap.data 맵 삽입 통과", 11, MUTED, KR, "start")

# 관문 3 통과 -> 관문 4로 (API 서버 검증 전달)
Y4 = 400
d.arrow([(CX, Y3 + 22), (CX, Y4 - 26)], MUTED, "ar", 1.2)
d.t(CX + 14, (Y3 + 22 + Y4 - 26) // 2 + 4, "전달", 11, MUTED, KR, "start")

# ── 관문 4: kubectl apply --dry-run=server (API 서버 검증, Focal) ─────────
DIA_W = 108
DIA_H = 26
d.o.append(f'<path d="M {CX} {Y4 - DIA_H} L {CX + DIA_W} {Y4} L {CX} {Y4 + DIA_H} L {CX - DIA_W} {Y4} Z" fill="{PAPER2}" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX, Y4 - 4, "kubectl apply", 12, ACC, MONO, "middle", 600)
d.t(CX, Y4 + 12, "--dry-run=server", 11, ACC, MONO, "middle", 600)

# 관문 4 필드 형식 오류 -> 차단 박스 (Focal)
d.arrow([(CX + DIA_W, Y4), (BOX_X - 2, Y4)], ACC, "acc", 1.4)
d.t(426, Y4 - 8, "필드 형식 오류", 11, ACC, KR, "middle", 600)
d.tone(BOX_X, Y4 - BOX_H // 2, BOX_W, BOX_H, ACC, 6, "16", 1.4)
d.t(BOX_X + 16, Y4 - 6, "BadRequest 400 거절 (차단)", 12, ACC, KR, "start", 600)
d.t(BOX_X + 16, Y4 + 14, "ConfigMap.data string 필드 형식 위반 차단", 11, INK, KR, "start")

# 관문 4 통과 -> 최종 정상 배포 승인
Y5 = 464
d.arrow([(CX, Y4 + DIA_H), (CX, Y5 - 20)], OK, "ok", 1.4)
d.t(CX + 14, (Y4 + DIA_H + Y5 - 20) // 2 + 4, "통과", 11, OK, KR, "start")

d.tone(130, 444, 220, 40, OK, 6, "14", 1.2)
d.t(CX, 461, "배포 승인: helm upgrade", 12, OK, KR, "middle", 600)
d.t(CX, 476, "클러스터 배포 안전 확인", 11, MUTED, KR, "middle")

# ── 범례 ────────────────────────────────────────────────────────────────
LEG_Y = 502
d.legend(LEG_Y, [
    ("API 서버 차단", ACC),
    ("안전 배포 승인", OK),
    ("오류 미감지 통과 위험", WARN),
    ("문법·렌더 오류 차단", BAD),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm 차트 작성.verify-gates.svg")
d.save(out_path)
print("ok gen-Helm 차트 작성.verify-gates")
