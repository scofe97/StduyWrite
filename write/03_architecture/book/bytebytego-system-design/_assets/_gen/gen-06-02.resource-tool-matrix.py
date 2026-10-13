# 타입 스펙: type-dp-security-matrix — 자원 다섯 행 × 도구 범위 세 열의 대응 격자(격자 문법을 비교 행렬로 사용). 초점 칸 하나는 디스크의 %util 로, 직렬 장치에서만 포화 신호라는 점.
# 사실 출처: man7.org 의 vmstat(8)·iostat(1)·pidstat(1)·ps(1)·top(1)·lsof(8)·ss(8) 와 netstat(8) 쪽
#   · vmstat: 필드 r·us·sy·wa·st·si·so(vmstat(8) FIELD DESCRIPTION FOR VM MODE) · iostat -x: aqu-sz·r_await·w_await·%util, await 는 -s 와 함께일 때(iostat(1) REPORTS, sysstat v12.8.0 iostat.c, %util 은 요청을 보낸 시간의 비율이며 병렬 장치에서는 한계를 보이지 않음)
#   · pidstat: -u CPU · -r 메모리(RSS) · -d 입출력(kB_rd/s) · ps: pcpu 정렬 · lsof: -p 로 프로세스 지정, 출력 열 FD·TYPE·NAME · ss: -s 요약, -p 프로세스, TCP 상태 목록.
# Layout conventions: §2 공식 — left_pad 12, comp_col_w 176, 열 폭 216·간격 12, header_h 36, header_y 96, row_h 48 · stride 56. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LEFT, COMP_W, GAP0, COL_W, COL_GAP = 12, 176, 12, 216, 12
HDR_Y, HDR_H, ROW0, ROW_H, STRIDE = 96, 36, 144, 48, 56
cols = ["시스템 전체", "프로세스별", "먼저 볼 값"]
rows = [
    ("CPU", "쓰는 쪽과 기다리는 쪽", "vmstat · top", "pidstat -u · ps", "r · us · sy · wa · st"),
    ("메모리", "남은 양과 스왑", "vmstat · top", "pidstat -r", "si · so · RSS"),
    ("디스크 IO", "대기열과 대기 시간", "iostat -x", "pidstat -d", "aqu-sz · r_await · %util"),
    ("네트워크", "소켓과 연결", "ss -s", "ss -p", "TCP 상태"),
    ("열린 파일", "파일과 소켓 목록", "lsof", "lsof -p PID", "FD · TYPE · NAME"),
]
FOCAL = (2, 2)

W = LEFT + COMP_W + GAP0 + 3 * COL_W + 2 * COL_GAP + 48
H = ROW0 + (len(rows) - 1) * STRIDE + ROW_H + 20 + 44
d = D(W, H, "BYTEBYTEGO · 06-02 §4",
      "자원마다 열어야 하는 창",
      "자원 하나에 시스템 전체 도구와 프로세스별 도구가 짝으로 있고 볼 값이 정해져 있습니다",
      "자원이 정해지면 도구와 필드가 따라옵니다")


def cx(j):
    return LEFT + COMP_W + GAP0 + j * (COL_W + COL_GAP)


d.box(LEFT, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LEFT + COMP_W / 2, HDR_Y + 23, "자원 × 범위", 12, INK, KR, "middle", 600)
for j, nm in enumerate(cols):
    d.box(cx(j), HDR_Y, COL_W, HDR_H, PAPER2, "rgba(191,192,192,0.45)", 0.9, 6)
    d.t(cx(j) + COL_W / 2, HDR_Y + 23, nm, 12, INK, KR, "middle", 600)

for i, (name, sub, a, b, c3) in enumerate(rows):
    y = ROW0 + i * STRIDE
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LEFT + 12, y + 20, name, 13, INK, KR, "start", 600)
    d.t(LEFT + 12, y + 38, sub, 12, MUTED, KR, "start")
    for j, txt in enumerate((a, b, c3)):
        x = cx(j)
        if (i, j) == FOCAL:
            d.tone(x, y, COL_W, ROW_H, ACC, 4, "14", 1.4)
            col = ACC
        else:
            col = INFO if j < 2 else OK
            d.tone(x, y, COL_W, ROW_H, col, 4, "10", 0.9)
        d.t(x + COL_W / 2, y + 29, txt, 12, col, MONO, "middle", 600)

d.legend(H - 44, [("도구", INFO), ("먼저 볼 값", OK), ("해석에 주의", ACC)])
d.save("06-02.resource-tool-matrix.svg")
