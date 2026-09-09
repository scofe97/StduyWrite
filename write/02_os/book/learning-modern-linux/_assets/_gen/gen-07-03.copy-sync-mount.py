# 07-03 §6 — 사본이 어디에 있느냐가 세 모델을 가른다.
# 원문("Mounting Remote Filesystems"): "NFS is a widely supported and used way to share files over a
#       network from a central place." 저자는 마운트를 "복사해 오는 대신" 이라고만 소개하고
#       그 선택이 무엇을 바꾸는지는 적지 않는다. sshfs 는 원서에 없다.
# 노트의 읽기: 셋을 가르는 축은 *사본이 어디에 있는가* 다. 2026-09-07 학습 세션 요청 도식.
#       복사(scp)는 사본을 만들고 끝, 동기화(rsync)는 사본을 두고 실행할 때마다 맞추고,
#       마운트는 사본이 아예 없어 매 접근이 왕복이다. 오프라인이 그 차이를 드러낸다 —
#       사본이 있는 쪽은 그대로 읽히고 마운트는 디렉토리가 통째로 멈춘다.
# 타입 스펙: type-architecture — 구성요소와 데이터가 *어디에 사는가* 를 그리는 형태. 점선 경계로
#       세 모델을 나누고 각 경계 안에 로컬·원격 상자를 둔다. coral 은 하나뿐이며 사본이 없어
#       오프라인에 멈추는 마운트다.
#       축약: NFS 의 캐시 일관성(close-to-open)은 본문 표가 맡으므로 여기서는 그리지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 654
d = D(W, H, "LEARNING MODERN LINUX · 07-03 §6",
      "사본이 어디에 있느냐가 세 모델을 가른다",
      "복사와 동기화는 양쪽에 사본을 두고 마운트는 사본을 두지 않는다. "
      "그 차이가 오프라인에서 드러난다 — 사본이 있으면 읽히고 없으면 멈춘다.",
      "구글 드라이브 같은 동기화와 마운트는 다른 모델입니다")

PX, PW, PGAP, PY, PH = 24, 266, 16, 148, 330
panels = [
    ("복사", "scp", INFO, "사본 하나", "한 번 받아 온다", "그대로 읽힙니다"),
    ("동기화", "rsync", OK, "사본 하나", "실행할 때마다 맞춘다", "그대로 읽힙니다"),
    ("마운트", "NFS · sshfs", ACC, "사본 없음", "읽을 때마다 건너온다", "통째로 멈춥니다"),
]

for i, (name, tools, col, local, arrow_note, offline) in enumerate(panels):
    x = PX + i * (PW + PGAP)
    focal = (col is ACC)
    if focal:
        d.tone(x, PY, PW, PH, ACC, 8, "10", 1.5)
    else:
        d.box(x, PY, PW, PH, "rgba(245,245,245,0.02)", col, 1.2, 8)
    d.t(x + 20, PY + 30, name, 15, col, KR, "start", 600)
    d.t(x + PW - 20, PY + 30, tools, 11.5, MUTED, MONO, "end")

    # 로컬 — 사본이 있는가 없는가가 여기서 갈린다
    d.box(x + 20, PY + 52, PW - 40, 52, PAPER2, col if focal else RULE, 1.1, 6)
    d.t(x + 34, PY + 76, "내 기계", 11, MUTED, KR, "start")
    d.t(x + PW - 34, PY + 78, local, 13.5, col, KR, "end", 600)

    # 두 상자 사이 — 무엇이 오가는가
    d.arrow([(x + PW / 2, PY + 176), (x + PW / 2, PY + 122)], SOFT, "soft", 1.4)
    d.t(x + PW / 2, PY + 154, arrow_note, 11.5, MUTED, KR)

    # 원격 — 어느 모델에서든 원본은 저쪽에 있다
    d.box(x + 20, PY + 184, PW - 40, 52, PAPER2, RULE, 1.0, 6)
    d.t(x + 34, PY + 208, "원격", 11, MUTED, KR, "start")
    d.t(x + PW - 34, PY + 210, "원본", 13.5, MUTED, KR, "end", 600)

    d.line(x + 20, PY + 258, x + PW - 20, PY + 258, RULE, 1.0, "4 5")
    d.t(x + 20, PY + 282, "망이 끊기면", 11, SOFT, KR, "start")
    d.t(x + 20, PY + 306, offline, 13, ACC if focal else MUTED, KR, "start", 600)

BY = PY + PH + 22
d.tone(24, BY, W - 48, 74, INFO)
d.t(44, BY + 28, "사본이 없다는 것이 값이자 대가입니다", 13, INK, KR, "start", 600)
d.t(44, BY + 52, "용량을 차지하지 않고 언제나 최신인 대신, 접근 하나하나가 네트워크 왕복입니다.",
    12, MUTED, KR, "start")

d.legend(BY + 96, [("사본을 만든다", INFO), ("사본을 맞춘다", OK), ("사본이 없다", ACC)])
d.save("07-03.copy-sync-mount.svg")
print("ok 07-03.copy-sync-mount")
