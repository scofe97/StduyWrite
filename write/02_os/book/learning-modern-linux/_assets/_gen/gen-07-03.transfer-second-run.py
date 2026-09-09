# 07-03 §5 — 두 번째로 보낼 때 무엇이 달라지는가.
# 원문("File Transfer"): "Synchronizing files with rsync is much more convenient and faster than scp."
#       "rsync ... can be told to copy only files that have been added or changed, making it a good
#       tool for backing up directories as well."  저자는 여기까지만 적는다.
# 노트의 읽기: *무엇을 근거로* 바뀌었다고 판단하는지가 실무에서 문제가 되는 자리인데 원서에 없다.
#       형제 도식 07-03.file-transfer.svg 는 "무엇을 옮기느냐"로 도구를 고르는 갈래를 그리므로,
#       이 도식은 축을 달리해 "같은 것을 두 번 보낼 때"만 본다. 2026-09-07 학습 세션 요청.
#   rsync(1) — "Rsync finds files that need to be transferred using a \"quick check\" algorithm
#       (by default) that looks for files that have changed in size or in last-modified time."
#   scp 에는 그런 비교가 없다 — scp(1) 은 파일을 복사할 뿐 두 쪽을 견주지 않는다.
# 타입 스펙: type-swimlane — 레인 하나에 도구 하나를 두고 왼→오른쪽으로 같은 절차를 두 번 흘린다.
#       레인을 가르는 것은 액터(도구)이고 열을 가르는 것은 회차다. 하이라이트는 두 레인이
#       갈리는 그 한 칸. coral 은 하나뿐이다.
#       축약: 파일 개수는 설명을 위한 예시 숫자다 — 원서 출력의 값이 아니라 그렇게 표시한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 880, 652
d = D(W, H, "LEARNING MODERN LINUX · 07-03 §5",
      "첫 전송은 같고 두 번째에서 갈린다",
      "받는 쪽이 비어 있는 첫 회차에는 둘 다 전부 보낸다. 두 번째부터 scp 는 여전히 통째로 "
      "보내고 rsync 는 양쪽을 견주어 바뀐 것만 보낸다.",
      "파일 개수는 설명을 위한 예시입니다")

LABX, LABW = 24, 150
C1X, CW, GAPX = 190, 323, 20
C2X = C1X + CW + GAPX
LANE_Y, LANE_H, LANE_GAP = 172, 128, 24

d.t(C1X + CW / 2, 150, "1차 전송", 12, MUTED, KR, "middle", 600)
d.t(C2X + CW / 2, 150, "2차 전송 — 파일 3개만 고쳤다", 12, MUTED, KR, "middle", 600)

lanes = [
    # (도구, 부제, 색, 1차 (큰 글자, 설명), 2차 (큰 글자, 설명), 2차가 초점인가)
    ("scp", "복사할 뿐이다", INFO,
     ("100개 전부", "받는 쪽이 비어 있다"),
     ("100개 전부", "견주지 않으니 통째로 다시"), False),
    ("rsync", "견주고 나서 보낸다", OK,
     ("100개 전부", "받는 쪽이 비어 있다"),
     ("바뀐 3개만", "크기나 수정 시각이 다른 것만"), True),
]

for i, (name, sub, col, first, second, focal) in enumerate(lanes):
    y = LANE_Y + i * (LANE_H + LANE_GAP)
    cy = y + LANE_H / 2
    d.box(LABX, y, LABW, LANE_H, PAPER2, col, 1.2, 8)
    d.t(LABX + LABW / 2, y + 52, name, 16, col, MONO, "middle", 600)
    d.t(LABX + LABW / 2, y + 76, sub, 11.5, MUTED, KR)

    for x, (big, note), hot in ((C1X, first, False), (C2X, second, focal)):
        if hot:
            d.tone(x, y, CW, LANE_H, ACC, 8, "12", 1.5)
        else:
            d.box(x, y, CW, LANE_H, PAPER2, RULE, 1.0, 8)
        c = ACC if hot else col
        d.t(x + 24, y + 54, big, 19, c, KR, "start", 600)
        d.t(x + 24, y + 84, note, 12, MUTED, KR, "start")

    # 회차 사이의 흐름 — 레인 안에서 왼쪽에서 오른쪽으로
    d.arrow([(C1X + CW + 3, cy), (C2X - 4, cy)], SOFT, "soft", 1.4)

d.line(LABX, LANE_Y + LANE_H + LANE_GAP / 2, W - 24, LANE_Y + LANE_H + LANE_GAP / 2, RULE, 1.0)

BY = LANE_Y + 2 * LANE_H + LANE_GAP + 22
d.tone(24, BY, W - 48, 96, ACC)
d.t(44, BY + 28, "견주는 기준이 무엇인가", 13, INK, KR, "start", 600)
d.t(44, BY + 52, "기본은 quick check 입니다. 크기나 최종 수정 시각이 달라진 파일을 찾고 둘 다 그대로면 건너뜁니다.",
    12, MUTED, KR, "start")
d.t(44, BY + 74, "-c 를 켜면 크기가 같은 파일의 체크섬까지 견주는데, 그러려면 양쪽이 파일 전체를 읽어야 합니다.",
    12, MUTED, KR, "start")

d.legend(BY + 118, [("복사만 한다", INFO), ("견주고 보낸다", OK), ("두 회차가 갈리는 자리", ACC)])
d.save("07-03.transfer-second-run.svg")
print("ok 07-03.transfer-second-run")
