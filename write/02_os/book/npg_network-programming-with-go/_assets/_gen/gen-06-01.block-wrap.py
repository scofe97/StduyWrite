# 타입 스펙: type-line
# 06-01 TFTP 블록 번호 오버플로 톱니 곡선
# 사실 출처: NPG Ch.6 p.10-11 (Data Packets, 65,535 x 512B ≈ 33.5MB 오버플로)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 460
d = D(W, H, "NPG CH.6 — TFTP BLOCK OVERFLOW",
      "블록 번호 증가와 33.5MB 오버플로 톱니",
      "전송 누적 바이트에 따른 uint16 블록 번호 순환",
      "65,535 블록 도달 시 0 으로 떨어지는 톱니 곡선")

# 플롯 영역 좌표
x0, x1 = 100, 800
y_top, y_bot = 120, 350
x_mid = 450

# Y축 그리드선 (5개)
grids = [
    (y_top, "65,535"),
    (y_top + (y_bot - y_top) * 0.25, "49,152"),
    (y_top + (y_bot - y_top) * 0.50, "32,768"),
    (y_top + (y_bot - y_top) * 0.75, "16,384"),
    (y_bot, "0"),
]

for gy, glab in grids:
    d.line(x0, gy, x1, gy, RULE, 0.7, dash="3 3")
    d.t(x0 - 12, gy + 4, glab, 11, SOFT, MONO, "end")

# 축 선
d.line(x0, y_top, x0, y_bot, RULE, 1.2)
d.line(x0, y_bot, x1, y_bot, RULE, 1.2)

# X축 눈금 레이블
d.t(x0, y_bot + 22, "0 MB", 11, SOFT, MONO, "middle")
d.t(x_mid, y_bot + 22, "33.5 MB", 11, INK, MONO, "middle", 600)
d.t(x1, y_bot + 22, "67.0 MB", 11, SOFT, MONO, "middle")

# 축 제목
d.t(x0 - 12, y_top - 12, "블록 번호", 11, MUTED, KR, "end")
d.t(x1, y_bot + 36, "누적 전송량 (MB)", 11, MUTED, KR, "end")

# 사이클 1 톱니선 (0MB -> 33.5MB)
d.line(x0, y_bot, x_mid, y_top, ACC, 2.2)
# 오버플로 수직 낙하
d.line(x_mid, y_top, x_mid, y_bot, BAD, 1.6, dash="4 3")

# 사이클 2 톱니선 (33.5MB -> 67MB)
d.line(x_mid, y_bot, x1, y_top, ACC, 2.2)
# 두 번째 오버플로 수직 낙하
d.line(x1, y_top, x1, y_bot, BAD, 1.6, dash="4 3")

# 정점 마커 (33.5MB, 65,535)
d.o.append(f'<circle cx="{x_mid}" cy="{y_top}" r="5" fill="{ACC}"/>')
d.t(x_mid, y_top - 10, "65,535 도달", 11, ACC, KR, "middle", 600)

# 두 번째 정점 마커 (67.0MB, 65,535)
d.o.append(f'<circle cx="{x1}" cy="{y_top}" r="5" fill="{ACC}"/>')
d.t(x1 - 10, y_top - 10, "65,535 도달", 11, ACC, KR, "end", 600)

# 오버플로 설명 콜아웃 (x_mid 오른쪽)
d.box(x_mid + 16, y_top + 70, 160, 48, fill=PAPER2, stroke=BAD, r=6)
d.t(x_mid + 96, y_top + 90, "uint16 오버플로", 11, BAD, KR, "middle", 600)
d.t(x_mid + 96, y_top + 107, "0 으로 강제 순환", 11, SOFT, KR, "middle")
d.arrow([(x_mid + 16, y_top + 94), (x_mid + 4, y_top + 94)], BAD, "bad", 1.2)

# 바닥 계산 근거 콜아웃 (그래프 왼쪽 위 0~15MB x 49,152 이상 빈 영역)
d.box(x0 + 30, 127, 170, 44, fill=PAPER2, stroke=RULE, r=6)
d.t(x0 + 115, 145, "65,535 × 512B", 11, INK, MONO, "middle", 600)
d.t(x0 + 115, 161, "= 약 33.5 MB 한도", 11, MUTED, KR, "middle")

# Legend
d.legend(H - 42, [("블록 번호 증가", ACC), ("오버플로 낙하", BAD), ("전송 기준선", RULE)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "06-01.block-wrap.svg"))
d.save(out)
print(f"saved: {out}")
