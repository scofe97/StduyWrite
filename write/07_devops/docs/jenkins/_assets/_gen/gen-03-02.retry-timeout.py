# 타입 스펙: type-gantt
# 1절 재시도와 타임아웃의 중첩 순서 — retry 와 timeout 의 중첩 순서에 따른 시간축 막대 비교
# 본문 사실 출처: 03-02.병렬·승인·재시도와 실행기 점유.md 35~55행
#   37행: 전체 상한을 거는 timeout 안에 일시적 오류를 복구하는 retry 를 감싸야 의도치 않은 대기 시간 팽창을 막습니다.
#   41행: retry 가 바깥이고 timeout 이 안쪽이면 시도마다 타임아웃이 새로 시작됩니다... retry(3) 안에 10분 타임아웃을 두면 최악의 경우 30분 동안 실행기(Executor)를 붙잡습니다.
#   43행: 안전한 구성은 전체 상한인 timeout 을 바깥에 두고 그 안에서 retry 를 수행하는 형태입니다.
#   46~50행: timeout(time: 10, unit: 'MINUTES') { retry(3) { sh 'curl --max-time 30 -f http://api.example.com/deploy' } }
#   53행: 세 번의 재시도를 모두 합친 총시간이 10분을 넘지 않습니다. 개별 명령어에도 자체 제한(--max-time 30)을 두어 단일 시도가 전체 예산을 독점하지 않도록 방어합니다.
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 352
d = D(
    W,
    H,
    "JENKINS · RETRY & TIMEOUT",
    "재시도와 타임아웃의 중첩 순서",
    "retry 와 timeout 의 중첩 순서에 따른 실행기 점유 시간 비교. 바깥 retry 는 시도마다 10분이 새로 시작되어 최악의 경우 30분 동안 실행기를 점유하고, 바깥 timeout 은 세 번의 재시도를 합친 총시간을 10분 상한으로 제한합니다.",
    lead="바깥 retry 는 최악 30분 누적 점유(상단) vs 바깥 timeout 은 전체 10분 상한 준수(하단)",
)

LP = 16
LABEL_W = 216
AX = 240
TOTAL_MIN = 30
TIMELINE_W = 660  # 22px per minute
PX_PER_MIN = 22
AY = 132

# 시간축 눈금선 및 라벨 (0분, 10분, 20분, 30분)
for m in (0, 10, 20, 30):
    x = AX + m * PX_PER_MIN
    d.line(x, AY - 4, x, AY + 132, RULE, 0.8, "2 4")
    d.t(x, AY - 12, f"{m}분", 13, MUTED, KR, "middle")

# ── 1. 바깥 retry · 안쪽 timeout (위험: 최악 30분 점유) ──────────────────
R1_Y = 140
R1_H = 44

d.box(LP, R1_Y, LABEL_W, R1_H, PAPER2, RULE, 0.9, 4)
d.t(LP + 12, R1_Y + 18, "retry(3) { timeout(10m) }", 13, INK, MONO, "start", 600)
d.t(LP + 12, R1_Y + 34, "시도마다 10분 타임아웃 재시작", 13, WARN, KR, "start")

# 시도 1 (0~10분)
x1_start = AX
x1_w = 10 * PX_PER_MIN
d.tone(x1_start, R1_Y, x1_w, R1_H, WARN, 4, "18", 1.0)
d.t(x1_start + x1_w // 2, R1_Y + 18, "시도 1 (10분)", 13, INK, KR, "middle", 600)
d.t(x1_start + x1_w // 2, R1_Y + 34, "타임아웃 발생", 13, WARN, KR, "middle")

# 시도 2 (10~20분)
x2_start = x1_start + x1_w
x2_w = 10 * PX_PER_MIN
d.tone(x2_start, R1_Y, x2_w, R1_H, WARN, 4, "18", 1.0)
d.t(x2_start + x2_w // 2, R1_Y + 18, "시도 2 (10분)", 13, INK, KR, "middle", 600)
d.t(x2_start + x2_w // 2, R1_Y + 34, "타임아웃 발생", 13, WARN, KR, "middle")

# 시도 3 (20~30분)
x3_start = x2_start + x2_w
x3_w = 10 * PX_PER_MIN
d.tone(x3_start, R1_Y, x3_w, R1_H, BAD, 4, "20", 1.2)
d.t(x3_start + x3_w // 2, R1_Y + 18, "시도 3 (10분)", 13, INK, KR, "middle", 600)
d.t(x3_start + x3_w // 2, R1_Y + 34, "최악 30분 실행기 점유", 13, BAD, KR, "middle", 600)

# 시도별 타임아웃 한도선
d.line(x2_start, R1_Y - 4, x2_start, R1_Y + R1_H + 4, WARN, 1.4)
d.line(x3_start, R1_Y - 4, x3_start, R1_Y + R1_H + 4, WARN, 1.4)
d.line(x3_start + x3_w, R1_Y - 4, x3_start + x3_w, R1_Y + R1_H + 4, BAD, 1.8)

# ── 2. 바깥 timeout · 안쪽 retry (안전: 전체 10분 상한) ──────────────────
R2_Y = 212
R2_H = 44

d.box(LP, R2_Y, LABEL_W, R2_H, PAPER2, RULE, 0.9, 4)
d.t(LP + 12, R2_Y + 18, "timeout(10m) { retry(3) }", 13, INK, MONO, "start", 600)
d.t(LP + 12, R2_Y + 34, "전체 상한 10분 강제", 13, ACC, KR, "start")

# 10분 전체 예산 (0~10분)
d.tone(AX, R2_Y, 10 * PX_PER_MIN, R2_H, ACC, 4, "18", 1.4)
d.t(AX + (10 * PX_PER_MIN) // 2, R2_Y + 18, "시도 1·2·3 합쳐 10분 이내", 13, INK, KR, "middle", 600)
d.t(AX + (10 * PX_PER_MIN) // 2, R2_Y + 34, "시도마다 --max-time 30", 13, ACC, MONO, "middle")

# 10분 상한선
lim_x = AX + 10 * PX_PER_MIN
d.line(lim_x, R2_Y - 6, lim_x, R2_Y + R2_H + 6, ACC, 2.0)

# 10~30분 보호 구간
save_w = 20 * PX_PER_MIN
d.tone(lim_x, R2_Y, save_w, R2_H, OK, 4, "0A", 1.0)
d.t(lim_x + save_w // 2, R2_Y + 27, "10분에서 끝남 — 실행기 점유 없음", 13, OK, KR, "middle", 600)

# 범례
LEG_Y = 296
d.legend(
    LEG_Y,
    [
        ("시도별 10분 점유", WARN),
        ("최악 30분 점유", BAD),
        ("전체 10분 상한", ACC),
        ("10분 뒤 점유 없음", OK),
    ],
)

out_path = pathlib.Path(__file__).resolve().parent.parent / "03-02.retry-timeout.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
