# 개념 노트 「힙 밖에서 쌓이는 메모리」 · arena 가 쌓이는 다섯 걸음.
# 논지는 "해제한 메모리가 프로세스 안에 남고 운영체제로는 돌아가지 않는다"이다.
# 타입 스펙: type-flowchart — 위에서 아래로 흐르는 단계, 오른쪽에 그때 관측되는 값.
#           type-loop 은 링 기하와 호 연결선을 요구하는데 이 폴더 프리미티브에 호가 없어 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, BAD, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 676
d = D(W, H, "TROUBLESHOOTING CONCEPT · MALLOC ARENA",
      "해제해도 운영체제로는 돌아가지 않습니다",
      "C 라이브러리는 큰 덩이를 미리 받아 두고 그 안에서 잘라 준다. 그 덩이가 arena 이고, 스레드가 락을 다투면 새 덩이를 연다. "
      "개수 상한은 코어 수에서 유도되고, 한 번 연 덩이는 거의 비어도 반납되지 않는다.",
      lead="살아 있는 할당 몇 개가 64 MB 덩이 하나를 통째로 붙잡습니다")

X, BW, BH, STRIDE, Y0 = 56, 456, 76, 100, 112
DX, DW = 592, 352

STEPS = [
    ("스레드가 malloc 을 부른다", "빈 덩이가 없으면 새 arena 를 연다", INFO, INFO,
     "arena 수 증가", "락 경쟁이 방아쇠"),
    ("개수 상한은 코어 수에서 나온다", "64비트 기본값은 코어 수의 8 배", ACC, ACC,
     "40 코어 노드 → 최대 320", "컨테이너 CPU 한도와 무관"),
    ("객체를 해제한다", "메모리는 그 arena 의 빈칸 목록으로", INFO, OK,
     "프로세스는 다시 쓸 수 있음", "재사용은 정상 동작"),
    ("운영체제에는 반납되지 않는다", "덩이가 거의 비어도 그대로 점유", BAD, BAD,
     "RSS 그대로", "커널이 보기에는 사용 중"),
    ("덩이 수 × 64 MB 가 RSS 로 남는다", "살아 있는 할당 몇 개가 덩이를 붙잡음", BAD, BAD,
     "NMT 합계 밖", "힙 대시보드에도 안 보임"),
]

for i, (title, sub, c, rc, out, why) in enumerate(STEPS):
    y = Y0 + i * STRIDE
    if i:
        d.arrow([(X + BW // 2, y - STRIDE + BH), (X + BW // 2, y)], MUTED, "ar", 1.4)
    if c is ACC:
        d.tone(X, y, BW, BH, ACC, 6)
    else:
        d.box(X, y, BW, BH, PAPER2, RULE, 0.9, 6)
    d.t(X + 24, y + 30, title, 13, c, KR, "start", 600)
    d.t(X + 24, y + 54, sub, 12, MUTED, KR, "start")

    d.line(X + BW, y + BH // 2, DX, y + BH // 2, RULE, 0.8, "4,3")
    d.box(DX, y, DW, BH, PAPER, RULE, 0.9, 6)
    d.t(DX + 24, y + 30, out, 13, rc, KR, "start", 600)
    d.t(DX + 24, y + 54, why, 12, MUTED, KR, "start")

d.legend(620, [("여는 계기", INFO), ("코어 수에서 유도되는 상한", ACC),
               ("정상 동작", OK), ("돌려주지 않는 몫", BAD)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-21.arena-retention.svg"))
print("ok")
