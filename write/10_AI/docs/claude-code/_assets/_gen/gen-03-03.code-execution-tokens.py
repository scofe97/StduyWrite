"""도구 직접 호출과 코드 실행 방식의 토큰 소비 비교.

# 타입 스펙: type-bar
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, WARN, OK, INK, MUTED, SOFT, PAPER, RULE, KR, MONO

W, H = 920, 420
d = D(
    W, H,
    "CONTEXT EXPANSION VS CODE EXECUTION",
    "도구 직접 호출과 코드 실행 방식의 토큰 소비 비교",
    "중간 데이터 모델 통과 방식과 샌드박스 격리 오케스트레이션 방식 간 토큰 소모량 비교",
    lead="Google Drive → Salesforce 한 사례 기준, 코드로 실행하면 토큰 소모가 98% 이상 줄었습니다"
)

PX0, PX1 = 232, 856
PY0, PY1 = 100, 236
VMAX = 160000
SCALE = (PX1 - PX0) / float(VMAX)

# 선형 눈금선 (0, 40k, 80k, 120k, 160k)
for v in (0, 40000, 80000, 120000, 160000):
    x = PX0 + v * SCALE
    d.line(x, PY0, x, PY1, RULE, 0.8)
    d.t(x, PY1 + 18, f"{v // 1000}k" if v else "0", 11, SOFT, MONO, "middle")

d.t((PX0 + PX1) / 2, PY1 + 38, "토큰 소모량 (Tokens) · 선형 눈금", 12, SOFT, KR, "middle")

def bar(y, tokens, c, name, sub_txt, val_txt, focal=False):
    w = max(round(tokens * SCALE / 4) * 4, 8)
    d.tone(PX0, y, w, 40, c, 4, "22" if focal else "16", 1.4 if focal else 1.0)
    # 레이블 (좌측)
    d.t(PX0 - 16, y + 17, name, 13, INK, KR, "end", 600)
    d.t(PX0 - 16, y + 33, sub_txt, 12, MUTED, KR, "end")
    # 값 레이블: 긴 막대는 막대 내부 우측, 짧은 막대는 막대 외부 우측
    tx = PX0 + w + 12
    if tx > PX1 - 180:
        d.t(PX0 + w - 12, y + 25, val_txt, 13, INK, KR, "end", 600)
    else:
        d.t(tx, y + 25, val_txt, 13, c, KR, "start", 600)

# 1. 도구 직접 호출 방식 (~150,000 토큰)
bar(116, 150000, WARN, "도구 직접 호출 방식", "전체 정의 · 중간 데이터 경유", "~150,000 토큰 (컨텍스트 팽창)")

# 2. 코드 실행 샌드박스 방식 (~2,000 토큰, focal)
bar(176, 2000, ACC, "코드 실행 샌드박스", "필요한 정의만 · 중간 데이터 비경유", "~2,000 토큰 (98.7% 절감)", focal=True)

# 절감 효과 칩
d.chip((PX0 + PX1) / 2, 310, "98.7% 절감 (필요한 도구 정의만 로드 + 중간 데이터 모델 비경유)", OK, 12)

d.legend(360, [
    ("코드 실행 샌드박스 (Focal)", ACC),
    ("도구 직접 호출 (비용 발생)", WARN),
    ("컨텍스트 절감 효과", OK)
])

d.save("03-03.code-execution-tokens.svg")
