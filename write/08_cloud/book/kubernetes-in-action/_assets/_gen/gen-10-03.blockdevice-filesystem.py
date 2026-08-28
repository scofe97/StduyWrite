# 10-03 §1 — 벽과 대장은 다른 층이다
# 캡션이 "번호 매긴 사물함 벽과 그 위의 관리 대장"이라는 비유를 준다. 그 비유를 그림으로
# 옮기되, 두 층이 각각 무엇을 아는지가 함께 보여야 리사이즈 2 층 구조로 이어진다.
# 타입 스펙: type-architecture.md — 블록 디바이스라는 칸의 벽과 그 위 파일시스템 대장 두 구성 요소, 그리고 대장이 벽을
#           가리키는 화살표로 이뤄진다. 층 이야기는 짝 도식(filesystem-resize-layers)이 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 620, "KUBERNETES IN ACTION · 10-03",
      "번호 붙은 칸과 그 위의 대장",
      "블록 디바이스는 같은 크기의 칸이 번호 순으로 늘어선 벽이다. 파일시스템은 그 위에 얹힌 대장으로, "
      "어느 파일이 몇 번 칸에 있는지를 적어 둔다.",
      "리사이즈가 두 층으로 나뉘는 이유가 여기 있다")

d.box(60, 300, 500, 172, PAPER, RULE, 0.9, 8)
d.t(310, 328, "블록 디바이스 — 번호 붙은 칸의 벽", 11, SOFT, KR)
for i in range(10):
    x = 90 + i * 46
    d.box(x, 366, 38, 62, PAPER2, INFO, 1.0, 4)
    d.t(x + 19, 402, str(i), 11, INFO, MONO)
d.t(310, 452, "칸이 몇 개인지만 안다 — 안에 무엇이 있는지는 모른다", 10, MUTED, KR)

d.box(660, 176, 480, 172, PAPER, RULE, 0.9, 8)
d.t(900, 204, "파일시스템 — 그 위의 관리 대장", 11, SOFT, KR)
for i, (f, blocks) in enumerate((("app.conf", "3, 4"), ("data.db", "5, 6, 7"), ("(빈 칸)", "8, 9"))):
    y = 244 + i * 30
    d.t(700, y, f, 11, ACC if i < 2 else SOFT, MONO, "start")
    d.t(900, y, f"블록 {blocks}", 11, MUTED, MONO, "start")
d.t(900, 332, "어느 파일이 몇 번 칸에 있는지 적어 둔다", 10, MUTED, KR)

d.path("M 900 356 L 900 392 L 570 392", ACC, 1.5, m="acc")
d.t(760, 374, "대장이 벽을 가리킨다", 10, ACC, KR)

d.t(24, 520, "그래서 벽에 칸을 더 붙여도 대장이 모르면 그 칸을 쓰지 못한다. 리사이즈가 블록 디바이스 확장과 "
             "파일시스템 확장 두 단계로 나뉘는 이유다.", 11, MUTED, KR, "start")
d.legend(548, [("칸", INFO), ("대장의 기록", ACC)])
d.save("10-03-blockdevice-filesystem.svg")
print("ok")
