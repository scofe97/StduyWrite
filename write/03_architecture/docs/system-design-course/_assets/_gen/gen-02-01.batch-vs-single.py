# 타입 스펙: type-bar — 1,000건 저장 시 단건 순차 쓰기와 단일 파티션 묶음 쓰기의 소요 시간 비교 (가정 수치).
# 사실 출처: 요약 §4.13, 조사 보고서 행 20·21·22, 본문 5절(가정 수치: 단건 쓰기 1건 5ms × 1,000건 = 5,000ms, 단일 파티션 묶음 쓰기 = 50ms, 다중 파티션 배치는 5KiB 경고/50KiB 실패로 금지).
# Layout conventions: 가로 막대 2행(Y0=144, PITCH=72, BH=32), PX0=280, PX1=880 (5,000ms 기준 선형 눈금, 1,000ms당 120px). 모든 좌표 4의 배수.
import sys, pathlib
ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS_DIR))
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, SOFT, RULE, KR, MONO

W, H = 960, 460
PX0, PX1 = 280, 880
VMAX = 5000
Y0, PITCH, BH = 144, 72, 32

d = D(W, H, "SYSTEM DESIGN COURSE · 02-01 §5",
      "1,000건 저장 시간: 한 건씩 5,000ms 대 묶어서 50ms",
      "건당 5ms 기준 1,000건 순차 쓰기는 5.0초가 걸리지만, 단일 파티션으로 묶으면 50ms 로 단축됩니다.",
      "1,000건 저장 소요 시간 비교 (단일 파티션 묶음 vs 단건 순차)")


def px(v):
    return PX0 + round((v / VMAX) * (PX1 - PX0))


# 눈금선 및 축 라벨
ybot = Y0 + PITCH + BH
for k in range(6):
    v = k * 1000
    x = px(v)
    d.line(x, Y0 - 16, x, ybot + 8, RULE, 0.8 if k else 1.0)
    d.t(x, ybot + 24, f"{v:,} ms" if v else "0", 12, SOFT, MONO, "middle")

d.t((PX0 + PX1) // 2, ybot + 44, "소요 시간 (밀리초 · 선형 눈금)", 13, SOFT, KR, "middle")

# 데이터 행
rows = [
    {
        "label": "단건 순차 쓰기",
        "sub": "건당 5ms (가정) × 1,000건",
        "val": 5000,
        "disp": "5,000 ms (5.0초)",
        "color": BAD,
        "focal": False,
    },
    {
        "label": "단일 파티션 묶음",
        "sub": "약 100배 속도 향상",
        "val": 50,
        "disp": "50 ms (가정 · 0.05초)",
        "color": ACC,
        "focal": True,
    },
]

for i, r in enumerate(rows):
    y = Y0 + i * PITCH
    col = r["color"]
    is_focal = r["focal"]

    # 라벨 (Y축 카테고리)
    d.t(PX0 - 16, y + 14, r["label"], 14, INK, KR, "end", 600)
    d.t(PX0 - 16, y + 30, r["sub"], 12, col if is_focal else MUTED, KR, "end")

    # 막대
    w = max(round((r["val"] / VMAX) * (PX1 - PX0)), 8)
    d.tone(PX0, y, w, BH, col, 4, "20" if is_focal else "12", 1.4 if is_focal else 1.0)

    # 수치 표시
    if r["val"] > 1000:
        d.t(PX0 + w - 16, y + 21, r["disp"], 13, INK, MONO, "end", 600)
    else:
        d.t(PX0 + w + 14, y + 21, r["disp"], 13, ACC, KR, "start", 600)

# 단서 및 주의 박스 (다중 파티션 배치 한계)
box_y = 312
d.tone(24, box_y, W - 48, 52, WARN, 6, "10", 1.0)
d.t(40, box_y + 22, "단일 파티션(channel_id) 묶음 기준 · 다중 파티션 배치: 5KiB 경고 · 50KiB 실패", 13, WARN, KR, "start", 600)
d.t(40, box_y + 40, "대안: 비동기 병렬 쓰기 (다중 파티션 코디네이터 노드 병목 방지)", 12, MUTED, KR, "start")

d.legend(H - 44, [
    ("단건 순차 쓰기 (가정)", BAD),
    ("단일 파티션 묶음 쓰기 (초점)", ACC),
    ("배치 크기 제약 (주의)", WARN),
])

out_path = str(ASSETS_DIR / "02-01.batch-vs-single.svg")
d.save(out_path)
print(f"saved: {out_path}")
