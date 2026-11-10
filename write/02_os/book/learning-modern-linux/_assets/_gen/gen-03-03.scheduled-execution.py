# 03-03 §8 — cron 과 systemd timer 의 실행 흐름 및 실패 격리 비교
# 타입 스펙: type-swimlane — 두 스케줄링 경로(cron vs systemd timer)의 단계별 대조
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 520
d = D(W, H, "LEARNING MODERN LINUX · 03-03 §8",
      "예약 실행의 두 경로 — cron 과 systemd timer",
      "주기 실행 스크립트가 실행 환경과 로깅을 다루는 두 방식 비교. "
      "cron 은 최소 환경과 침묵 위험이 따르고, systemd timer 는 저널 로깅과 상태 가시성을 제공한다.",
      "핵심 대비: 최소 환경·수동 로깅(cron) vs 통합 저널·중복 방지(systemd timer)")

LANE_X, LANE_W = 16, 172
TRACK_X = LANE_X + LANE_W + 12
LANE_H, LANE_GAP, LANE_Y0 = 136, 16, 116
SLOT_W, SLOT_GAP, SLOT_H = 154, 12, 108

lanes = [
    ("cron", "기존 주기 실행", WARN),
    ("systemd timer", "현대적 스케줄링", OK),
]

cron_steps = [
    ("스케줄 정의", "crontab 5자리", ["30 2 * * *", "분 시 일 월 요일"], WARN),
    ("실행 환경", "최소 PATH 환경", ["PATH=/usr/bin:/bin", "절대 경로 필수"], BAD),
    ("동시성 제어", "도구 직접 연동", ["flock -n 필요", "미적용 시 중복 실행"], WARN),
    ("로깅·확인", "명시적 리다이렉션", [">> backup.log 2>&1", "누락 시 침묵 실패"], BAD),
]

timer_steps = [
    ("스케줄 정의", "*.timer 유닛", ["OnCalendar=*-*-*", "Persistent=true"], OK),
    ("실행 환경", "*.service 유닛", ["Type=oneshot", "환경 변수 명시 제어"], OK),
    ("동시성 제어", "유닛 자체 억제", ["중복 실행 방지 내장", "의존성(After=) 관리"], OK),
    ("로깅·확인", "journald & 상태", ["systemctl list-timers", "journalctl -u 조회"], OK),
]

def slot_x(i):
    return TRACK_X + i * (SLOT_W + SLOT_GAP)

for li, (name, sub, c) in enumerate(lanes):
    y = LANE_Y0 + li * (LANE_H + LANE_GAP)
    d.box(LANE_X, y, LANE_W, LANE_H, PAPER2, c, 1.0, 6)
    d.t(LANE_X + 16, y + 48, name, 15, c, KR, "start", 600)
    d.t(LANE_X + 16, y + 74, sub, 12, MUTED, KR, "start")

for li, (step_list, is_timer) in enumerate([(cron_steps, False), (timer_steps, True)]):
    y = LANE_Y0 + li * (LANE_H + LANE_GAP) + 14
    for si, (title, sub_title, lines, c) in enumerate(step_list):
        x = slot_x(si)
        d.box(x, y, SLOT_W, SLOT_H, PAPER, c, 1.0, 6)
        d.t(x + SLOT_W / 2, y + 24, title, 13, INK, KR, "middle", 600)
        d.t(x + SLOT_W / 2, y + 42, sub_title, 11, c, KR, "middle")
        for k, line in enumerate(lines):
            d.t(x + SLOT_W / 2, y + 66 + k * 18, line, 11, MUTED,
                MONO if any(ch in "*/=." for ch in line) else KR, "middle")

for li in range(2):
    y_center = LANE_Y0 + li * (LANE_H + LANE_GAP) + 14 + SLOT_H / 2
    for si in range(3):
        x_from = slot_x(si) + SLOT_W
        x_to = slot_x(si + 1)
        c = OK if li == 1 else MUTED
        mk = "ok" if li == 1 else "ar"
        d.path(f"M {x_from + 2} {y_center} L {x_to - 6} {y_center}", c, 1.2, m=mk)

d.t(20, 442, "cron: 최소 PATH 와 로그 누락 주의 — systemd timer: 통합 로깅과 중복 실행 방지 보장",
    12, MUTED, KR, "start")

d.legend(464, [("안전 / 통합 관리", OK), ("주의 / 수동 설정", WARN), ("조용한 실패 위험 지점", BAD)])
d.save("03-03.scheduled-execution.svg")
print("ok 03-03.scheduled-execution")
