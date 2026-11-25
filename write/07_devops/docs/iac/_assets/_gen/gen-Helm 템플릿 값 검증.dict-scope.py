# 타입 스펙: type-architecture
# 2절 dict 로 헬퍼 템플릿에 값 전달 — 호출 범위와 $·. 치환 경로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 456

d = D(W, H, "HELM · NAMED TEMPLATE DICT SCOPE",
      "dict 로 헬퍼 템플릿에 값을 넘길 때 범위 변화",
      "named template 호출 시 dict 가 . 과 $ 를 대체하고 root 키로 최상위 컨텍스트에 닿는 경로",
      lead="헬퍼 안의 . 과 $ 는 모두 전달된 dict 를 가리킴 · .Values 를 읽으려면 root 키로 $ 전달 필요")


def zone(x, y, w, h, label, c=RULE):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="0.9" stroke-dasharray="5 4"/>')
    lw = int(len(label) * 7.5) + 20
    d.o.append(f'<rect x="{x + 16}" y="{y + 4}" width="{lw}" height="14" rx="2" fill="{PAPER}"/>')
    d.t(x + 16 + lw // 2, y + 15, label, 12, SOFT, KR, "middle")


# ── 존 1: 호출 템플릿 (최상위 컨텍스트) ─────────────────────────────
Z1_X, Z1_Y, Z1_W, Z1_H = 24, 96, 260, 224
zone(Z1_X, Z1_Y, Z1_W, Z1_H, "호출부 템플릿", RULE)

C1_X, C1_Y, C1_W, C1_H = 40, 128, 228, 72
d.tone(C1_X, C1_Y, C1_W, C1_H, INFO, 6, "14", 1.2)
d.t(C1_X + 14, C1_Y + 23, "최상위 컨텍스트 ($)", 13, INFO, KR, "start", 600)
d.t(C1_X + 14, C1_Y + 43, ".Values · .Release · .Chart", 11, INK, MONO, "start")
d.t(C1_X + 14, C1_Y + 62, "렌더 시작 시점 루트 객체", 13, MUTED, KR, "start")

C2_X, C2_Y, C2_W, C2_H = 40, 228, 228, 76
d.tone(C2_X, C2_Y, C2_W, C2_H, ACC, 6, "14", 1.4)
d.t(C2_X + 14, C2_Y + 23, "dict 인자 생성", 13, ACC, KR, "start", 600)
d.t(C2_X + 14, C2_Y + 44, 'dict "root" $ "name" "web"', 11, INK, MONO, "start")
d.t(C2_X + 14, C2_Y + 64, "root 키에 $ 를 담아 전달", 13, MUTED, KR, "start")

d.arrow([(C1_X + C1_W // 2, C1_Y + C1_H + 2), (C2_X + C2_W // 2, C2_Y - 2)], INFO, "info", 1.2)


# ── 존 2: 헬퍼 템플릿 (_helpers.tpl) ────────────────────────────────
Z2_X, Z2_Y, Z2_W, Z2_H = 352, 96, 584, 224
zone(Z2_X, Z2_Y, Z2_W, Z2_H, "헬퍼 내부 (define demo.fullimage)", ACC)

H1_X, H1_Y, H1_W, H1_H = 368, 128, 228, 176
d.box(H1_X, H1_Y, H1_W, H1_H, PAPER, RULE, 1.0, 6)
d.t(H1_X + 14, H1_Y + 24, "헬퍼가 받은 범위 (. = $)", 13, INK, KR, "start", 600)
d.t(H1_X + 14, H1_Y + 45, "전달된 dict 가 . 과 $ 를 덮음", 13, MUTED, KR, "start")
d.box(H1_X + 14, H1_Y + 66, 200, 40, PAPER2, INFO, 1.0, 4)
d.t(H1_X + 24, H1_Y + 90, '"root" -> 최상위 $', 12, INFO, MONO, "start", 600)
d.box(H1_X + 14, H1_Y + 118, 200, 40, PAPER2, RULE, 1.0, 4)
d.t(H1_X + 24, H1_Y + 142, '"name" -> "web"', 12, INK, MONO, "start")

# 우측 결과 카드 2개 (실패 vs 성공)
R1_X, R1_Y, R1_W, R1_H = 632, 128, 288, 76
d.tone(R1_X, R1_Y, R1_W, R1_H, BAD, 6, "14", 1.2)
d.t(R1_X + 14, R1_Y + 23, ".Values.image (root 누락)", 12, BAD, MONO, "start", 600)
d.t(R1_X + 14, R1_Y + 44, "dict 안에 Values 키 없음", 13, INK, KR, "start")
d.t(R1_X + 14, R1_Y + 64, "nil pointer evaluating error", 11, BAD, MONO, "start")

R2_X, R2_Y, R2_W, R2_H = 632, 228, 288, 76
d.tone(R2_X, R2_Y, R2_W, R2_H, OK, 6, "14", 1.2)
d.t(R2_X + 14, R2_Y + 23, ".root.Values.image", 12, OK, MONO, "start", 600)
d.t(R2_X + 14, R2_Y + 44, "root 키로 최상위 $ 참조", 13, INK, KR, "start")
d.t(R2_X + 14, R2_Y + 64, '"nginx:1.27@web" 렌더 성공', 11, OK, MONO, "start")


# ── 화살표 연결 (직각 경로) ─────────────────────────────────────────
AY_CALL = C2_Y + C2_H // 2
d.arrow([(C2_X + C2_W + 2, AY_CALL), (H1_X - 2, AY_CALL)], ACC, "acc", 1.4)
d.t((Z1_X + Z1_W + Z2_X) // 2, AY_CALL - 10, "include", 11, ACC, MONO, "middle", 600)

AY_BAD = R1_Y + R1_H // 2
d.arrow([(H1_X + H1_W + 2, AY_BAD), (R1_X - 2, AY_BAD)], BAD, "bad", 1.2)

AY_OK = R2_Y + R2_H // 2
d.arrow([(H1_X + H1_W + 2, AY_OK), (R2_X - 2, AY_OK)], OK, "ok", 1.4)


# ── 하단 요약 ───────────────────────────────────────────────────────
SUMM_Y, SUMM_H = 336, 52
d.box(Z1_X, SUMM_Y, 912, SUMM_H, PAPER2, RULE, 0.9, 6)
d.t(Z1_X + 16, SUMM_Y + 21, "헬퍼 내부에서 with·range 를 써도 $ 는 여전히 전달된 dict", 13, INK, KR, "start", 600)
d.t(Z1_X + 16, SUMM_Y + 41, "최상위 객체는 .root 로 꺼내고 · nindent 파이프에는 include 사용", 13, MUTED, KR, "start")


# ── 범례 ────────────────────────────────────────────────────────────
d.legend(408, [
    ("dict 인자 전달", ACC),
    ("최상위 $ 참조", INFO),
    ("정상 렌더", OK),
    ("nil 포인터 오류", BAD),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm 템플릿 값 검증.dict-scope.svg")
d.save(out_path)
print("ok gen-Helm 템플릿 값 검증.dict-scope")
