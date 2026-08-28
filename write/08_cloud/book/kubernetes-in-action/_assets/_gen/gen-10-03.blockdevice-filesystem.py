# 10-03 §1 — 벽과 대장은 다른 층이다
# 캡션이 "번호 매긴 사물함 벽과 그 위의 관리 대장"이라는 비유를 준다. 그 비유를 그림으로
# 옮기되, 두 층이 각각 무엇을 아는지가 함께 보여야 리사이즈 2 층 구조로 이어진다.
# 타입 스펙: type-layers.md — 본문이 "그 사물함 벽 *위에* 얹은 관리 대장" 이라고 위아래로 말하므로
#           그대로 두 층으로 쌓는다. 왼쪽 여백의 방향 표시가 정본이 요구하는 direction indicator 다.
#           정본은 전폭 띠 4~6 겹이 계약인데 여기는 두 겹이다 — 본문이 두 층뿐이라 못박으므로
#           겹을 늘리지 않는다. 짝 도식(filesystem-resize-layers)이 같은 두 층을 그대로 이어받는다.
#           2026-08-29 재작성: 처음에는 벽을 왼쪽 아래, 대장을 오른쪽 위에 두고 화살표로 이어
#           architecture 로 적었다. 그러면 본문이 말하는 '위에 얹혔다'가 그림에 없다 —
#           본문이 도식의 규격을 적어 두었으므로 형태를 본문에 맞춘다.
#           예시 파일명도 본문 그대로 맞춘다(이력서.pdf 는 5·6·7 번 칸 · 빈 칸은 9 번부터).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

W, H = 1200, 640
d = D(W, H, "KUBERNETES IN ACTION · 10-03",
      "번호 붙은 칸의 벽과 그 위에 얹힌 대장",
      "블록 디바이스는 같은 크기의 칸이 번호 순으로 늘어선 벽이다. 파일시스템은 그 위에 얹힌 "
      "대장으로, 어느 파일이 몇 번 칸에 있는지를 적어 둔다.",
      "리사이즈가 두 층으로 나뉘는 이유가 여기 있다")

BX, BW = 200, 936
# 두 층 사이를 62px 열어 둔다 — 18px 로 두었더니 층을 잇는 화살표가 4px 로 줄고
# 그 설명이 아래 층 상자를 파고들었다.
FS_Y, BD_Y, LH = 182, 372, 128

# ddx 기본 밴드 폭(24~976)은 1000px 캔버스용이라 1200px 에서는 층이 밴드를 뚫는다.
ddx.band(d, 104, 578, "벽에 칸을 더 붙여도 대장이 모르면 그 칸을 쓰지 못한다", x=24, w=1152)

# 위 층 — 파일시스템(관리 대장)
d.o.append(f'<rect x="{BX}" y="{FS_Y}" width="{BW}" height="{LH}" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(BX + 24, FS_Y + 34, "파일시스템 — 관리 대장", 14, ACC, KR, "start", 600)
d.t(BX + 24, FS_Y + 66, "이력서.pdf 는 5 · 6 · 7 번 칸에 나눠 들어 있다", 12, MUTED, KR, "start")
d.t(BX + 24, FS_Y + 94, "빈 칸은 9 번부터다", 12, MUTED, KR, "start")
d.t(BX + BW - 24, FS_Y + 80, "이름으로 다룬다", 11, SOFT, KR, "end")

# 아래 층 — 블록 디바이스(번호 붙은 칸의 벽)
d.box(BX, BD_Y, BW, LH, PAPER2, INFO, 1.2, 6)
d.t(BX + 24, BD_Y + 32, "블록 디바이스 — 번호 붙은 칸의 벽", 14, INFO, KR, "start", 600)
CW, CG = 74, 10
for i in range(10):
    x = BX + 24 + i * (CW + CG)
    used = i in (5, 6, 7)
    c = ACC if used else INFO
    if used:
        d.o.append(f'<rect x="{x}" y="{BD_Y+52}" width="{CW}" height="54" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, BD_Y + 52, CW, 54, PAPER, RULE, 1.0, 4)
    d.t(x + CW // 2, BD_Y + 85, str(i), 13, c if used else SOFT, MONO)
d.t(BX + BW - 24, BD_Y + 32, "칸이 몇 개인지만 안다", 11, SOFT, KR, "end")

# 층 사이 — 대장이 벽을 가리킨다
d.path(f"M {BX+300} {FS_Y+LH+6} L {BX+300} {BD_Y-10}", ACC, 1.5, m="acc")
d.t(BX + 316, FS_Y + LH + 30, "5 · 6 · 7 번 칸을 가리킨다", 10, ACC, KR, "start")

# 정본의 방향 표시 — 스택 바깥 왼쪽 여백
d.t(BX - 24, FS_Y + 74, "이름", 11, ACC, KR, "end", 600)
d.t(BX - 24, BD_Y + 74, "번호", 11, INFO, KR, "end", 600)
d.path(f"M {BX-64} {BD_Y+40} L {BX-64} {FS_Y+94}", MUTED, 1.2, m="ar")
d.t(BX - 78, (FS_Y + BD_Y) // 2 + 74, "추상 ↑", 10, SOFT, KR, "end")

d.t(24, 540, "그래서 벽에 칸을 더 붙여도 대장이 모르면 그 칸을 쓰지 못한다. 리사이즈가 블록 디바이스 확장과 "
             "파일시스템 확장 두 단계로 나뉘는 이유다.", 11, MUTED, KR, "start")
d.legend(600, [("대장이 아는 것 — 이름과 그 자리", ACC), ("벽이 아는 것 — 칸 번호", INFO)])
d.save("10-03-blockdevice-filesystem.svg")
print("ok")
