# 타입 스펙: type-gantt — 한 줄 버퍼 위에서 길이가 제각각인 항목을 막대로 그리고, 같은 링의 두 상태를 위아래로 쌓는다(원형 대신 가로 펴기).
# 사실 출처: 추출본 ebpf2.txt 477~506행(읽기·쓰기 포인터, 길이 헤더, 앞지르면 기록 안 하고 드롭 카운터 증가).
#   칸 수·길이는 개념 예시이며 실제 바이트 값이 아니다. 드롭 규칙은 perf 쪽: PERF_RECORD_LOST 의 lost 필드(linux v7.2 include/uapi/linux/perf_event.h 줄 914).
# Layout conventions: 칸 폭 48, 칸 높이 40, 행 간격 160, 라벨 열 x=24~172, 타임라인 x=180~948. 좌표는 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 460
d = D(W, H, "LEARNING EBPF · 02-02 §1",
      "링 버퍼는 읽기 지점 뒤로 쓰기를 못 넘긴다",
      "길이가 다른 항목이 쓰기 지점에서 이어 붙고 읽기 지점이 뒤따라간다. 새 항목이 남은 칸보다 길면 쓰지 않고 드롭 카운터만 올린다.",
      "같은 16칸 버퍼의 두 시점")

X0, CW, CH, N = 180, 48, 40, 16
def cx(i): return X0 + i * CW

def strip(y, used):
    # 항목이 차지하지 않은 칸만 칸 상자로 그린다(막대와 상자가 겹치지 않게)
    for i in range(N):
        if i not in used:
            d.box(cx(i), y, CW, CH, PAPER2, RULE, 0.8, 0)
        d.t(cx(i) + CW/2, y - 6, str(i), 11, SOFT, MONO)

def rec(i0, n, y, label, c=MUTED, dash=False):
    x, w = cx(i0), n * CW
    d.o.append(f'<rect x="{x+2}" y="{y+2}" width="{w-4}" height="{CH-4}" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.2"' + (' stroke-dasharray="5 4"' if dash else '') + '/>')
    if label:
        d.t(x + w/2, y + 25, label, 12, INK if not dash else c, KR, "middle", 600)

def ptr(i, y, name, c, mk):
    x = cx(i)
    d.line(x, y - 4, x, y + CH + 4, c, 2.0)
    d.chip(x, y + CH + 22, name, c, 12)

def wrap(y):
    xe, xs = cx(N) - 24, cx(0) + 36
    yb = y + CH + 56
    d.arrow([(xe, y + CH + 2), (xe, yb), (xs, yb), (xs, y + CH + 6)], SOFT, "soft", 1.2, "5 4")
    d.chip((xe + xs) / 2, yb, "끝 → 처음", SOFT, 12)

# 행 A — 읽을 항목 3개
YA = 116
d.t(24, YA + 24, "읽을 항목 3개", 13, INK, KR, "start", 600)
d.t(24, YA + 44, "읽기 0 · 쓰기 10", 12, MUTED, MONO, "start")
strip(YA, set(range(0, 10)))
rec(0, 3, YA, "항목 1 · 3칸", INFO)
rec(3, 5, YA, "항목 2 · 5칸", INFO)
rec(8, 2, YA, "항목 3 · 2칸", INFO)
ptr(0, YA, "읽기", INFO, "info")
ptr(10, YA, "쓰기", OK, "ok")
wrap(YA)

# 행 B — 항목 1 을 읽고 항목 4 를 쓴 뒤
YB = 268
d.t(24, YB + 24, "항목 4 쓴 뒤", 13, INK, KR, "start", 600)
d.t(24, YB + 44, "읽기 3 · 쓰기 15", 12, MUTED, MONO, "start")
d.chip(98, YB + 76, "드롭 0 → 1", BAD, 12)
strip(YB, set(range(0, 15)) | {15})
rec(3, 5, YB, "항목 2 · 5칸", INFO)
rec(8, 2, YB, "항목 3 · 2칸", INFO)
rec(10, 5, YB, "항목 4 · 5칸", INFO)
# 거부된 새 항목 5칸: 빈 칸 15·0·1·2 네 칸으로는 1칸이 모자란다
rec(15, 1, YB, "", BAD, True)
rec(0, 3, YB, "", BAD, True)
d.t(cx(0) + 1.5 * CW, YB + 18, "새 항목 5칸", 12, BAD, KR, "middle", 600)
d.t(cx(0) + 1.5 * CW, YB + 34, "1칸 부족", 12, BAD, KR, "middle", 400)
ptr(3, YB, "읽기", INFO, "info")
ptr(15, YB, "쓰기", OK, "ok")
wrap(YB)

d.legend(H - 56, [("남은 항목", INFO), ("쓰기 지점", OK), ("거부된 쓰기", BAD)])
d.save("02-02.ring-buffer.svg")
