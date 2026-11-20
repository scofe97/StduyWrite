# 타입 스펙: type-radar
# 사실 출처: review-findings.md, internal/runtime/manager.go:426, internal/core/service.go:109,1376,
#   internal/runtime/protocol.go:29, internal/qjs/runtime.go:21, README.md:38,
#   internal/core/service.go:2341, internal/app/serve.go:330, go test ./... (32 패키지 통과)
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 510
d = D(W, H,
      "FLATS · QUALITY ATTRIBUTES EVALUATION",
      "flats 6속성 품질 평가",
      "가용성·성능·확장성·변경용이성·유지보수성·테스트용이성 6대 아키텍처 품질 속성 실측 평가",
      lead="격리 경계와 시계 주입 기반 테스트는 우수하나 core 대형 파일과 단일 호스트 자원 집중이 관측됩니다")

# 축 매개변수
x_start = 180
plot_w = 480  # 96px per score unit (0..5)
y_top = 96
y_bot = 406

# X축 눈금선 (0..5)
for score in range(6):
    gx = x_start + int(score * (plot_w / 5))
    is_base = (score == 0)
    d.line(gx, y_top, gx, y_bot, c=RULE if not is_base else MUTED, sw=1.0 if is_base else 0.6, dash=None if is_base else "3 4")
    d.t(gx, y_bot + 18, f"{score}", 10, MUTED, fam=MONO, anchor="middle")

d.t(x_start + plot_w // 2, y_bot + 34, "EVALUATION SCORE (0 - 5)", 9, SOFT, fam=MONO, anchor="middle")

# 6대 속성 데이터 (속성명, 점수, 대표 근거 칩, 포컬 여부)
items = [
    ("가용성", 4, "지수 백오프·CAS 배포", False),
    ("성능", 4, "VM 풀·컴파일 캐시", False),
    ("확장성", 3, "단일 프로세스 메모리", True),
    ("변경용이성", 3, "core 대형 파일 집중", True),
    ("유지보수성", 3, "120줄 초과 함수 18개", True),
    ("테스트용이성", 5, "시계 주입·32패키지 통과", False),
]

y0 = 108
pitch = 48
bar_h = 24

for i, (name, score, chip_txt, is_focal) in enumerate(items):
    y = y0 + i * pitch
    bar_w = int((score / 5.0) * plot_w)
    stroke_c = ACC if is_focal else INFO
    fill_c = f"{ACC}28" if is_focal else f"{INFO}18"

    # 카테고리 레이블 (우측 정렬)
    d.t(x_start - 16, y + 16, name, 12, INK if is_focal else MUTED, fam=KR, anchor="end", weight=600 if is_focal else 500)

    # 막대 배경 마스크 & 본체
    d.box(x_start, y, bar_w, bar_h, fill=fill_c, stroke=stroke_c, sw=1.3 if is_focal else 0.9, r=4)

    # 점수 수치 (막대 우측)
    d.t(x_start + bar_w + 14, y + 17, f"{score} / 5", 11, stroke_c, fam=MONO, anchor="start", weight=600)

    # 대표 근거 칩 (고정 열)
    chip_x = 835
    chip_stroke = ACC if is_focal else MUTED
    d.chip(chip_x, y + 12, chip_txt, c=chip_stroke, size=11, pad=8)

# 범례
d.legend(456, [
    ("우수 영역 (4~5 / 5)", INFO),
    ("개선 검토 영역 (3 / 5, Focal)", ACC),
    ("대표 관측 근거", MUTED),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "06-02-quality-radar.svg"))
d.save(out)
print(f"saved: {out}")
