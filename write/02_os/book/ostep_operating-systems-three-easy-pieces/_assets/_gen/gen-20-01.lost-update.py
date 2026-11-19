# 20-01 「카운터 갱신 하나가 사라지는 순서」 — 두 스레드가 같은 카운터에 1 을 더하는데, 첫 스레드가 쓰기 전에 전환이 끼어들면 결과가 52 가 아니라 51 이다.
# 본문 근거: 이 노트 「4. 공유 카운터와 경쟁 상태」.
# 값 근거: OSTEP 26장 그림 26.7 의 아홉 행(PC·eax·counter). 카운터는 50 에서 시작한다.
# 공식 근거: OSTEP 26장 §26.3 — 코드는 두 번 실행됐지만 카운터는 50 에서 51 로만 늘었다. 올바른 값은 52 다.
# 타입 스펙: type-sequence 의 표 변형 — 세로가 시간, 가로 세 열이 운영체제·스레드 1·스레드 2, 오른쪽에 PC·eax·counter 를 명령 직후 값으로 붙인다.
#             (dd.Seq 의 레이블이 영문 고정이라 한글 열 머리를 쓰려고 D 위에서 직접 그린다.)
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, PAPER2, ACC, OK, WARN, INFO, BAD, KR, MONO

W, H = 984, 640
d = D(W, H, "SEQUENCE · 20-01 §4",
      "읽은 값을 쓰기 전에 전환이 끼어들면 두 번 더해도 한 번만 반영된다",
      "카운터가 50 일 때 스레드 1 이 값을 eax 로 읽고 1 을 더해 eax 가 51 이 된 뒤 전환이 일어난다. "
      "스레드 2 도 50 을 읽고 51 을 만들어 카운터에 51 을 쓴다. "
      "스레드 1 이 다시 돌면서 자기 eax 51 을 카운터에 쓰므로 최종 값은 52 가 아니라 51 이다.",
      lead="가로 세 열은 누가 실행하는지, 오른쪽 세 열은 그 명령이 끝난 직후의 값입니다.")

OSX, T1X, T2X = 12, 196, 460
CW = 236
VX = (700, 780, 868)
ROWH = 40
TOP = 148

for x, n in ((OSX, "운영체제"), (T1X, "스레드 1"), (T2X, "스레드 2")):
    d.box(x, 100, CW if x != OSX else 168, 28, PAPER2, RULE, 1.0, 4)
    d.t(x + (CW if x != OSX else 168) / 2, 119, n, 13, INK, KR, "middle", 600)
for x, n in zip(VX, ("PC", "eax", "counter")):
    d.t(x + 28, 119, n, 13, INK, MONO, "middle", 600)

rows = [
    ("t1", "임계 구역 직전", "100", "0", "50"),
    ("t1", "mov 8049a1c,%eax", "105", "50", "50"),
    ("t1", "add $0x1,%eax", "108", "51", "50"),
    ("os", "인터럽트: T1→T2", "100", "0", "50"),
    ("t2", "mov 8049a1c,%eax", "105", "50", "50"),
    ("t2", "add $0x1,%eax", "108", "51", "50"),
    ("t2", "mov %eax,8049a1c", "113", "51", "51"),
    ("os", "인터럽트: T2→T1", "108", "51", "51"),
    ("t1", "mov %eax,8049a1c", "113", "51", "51"),
]
for i, (who, txt, pc, eax, cnt) in enumerate(rows):
    y = TOP + i * ROWH
    x, w, c = {"os": (OSX, 168, MUTED), "t1": (T1X, CW, INFO), "t2": (T2X, CW, OK)}[who]
    d.tone(x, y, w, 32, c, 4, "16", 1.0)
    d.t(x + w / 2, y + 21, txt, 13, c, MONO if txt[0] in "madi" and who != "os" and "·" not in txt else KR, "middle")
    d.line(VX[0] - 8, y + 36, W - 48, y + 36, RULE, 0.5)
    last = i == len(rows) - 1
    lost = i == 8
    for vx, v in zip(VX, (pc, eax, cnt)):
        col = ACC if (vx == VX[2] and (i == 6 or i == 8)) else MUTED
        d.t(vx + 28, y + 21, v, 13, col, MONO, "middle", 600 if col == ACC else 400)

# 결과 줄
yy = TOP + len(rows) * ROWH + 8
d.tone(T1X, yy, 504, 36, ACC, 6, "1e", 1.4)
d.t(T1X + 252, yy + 23, "기대값 52, 실제 counter 51", 13, ACC, KR, "middle", 600)

d.legend(H - 40, [("스레드 1", INFO), ("스레드 2", OK), ("운영체제", MUTED), ("갱신이 사라진 값", ACC)])
d.save("20-01.lost-update.svg")
print("ok 20-01 lost-update")
