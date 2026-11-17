# 04-01 §1 — 사용자와 프로세스와 파일이 서로에게 하는 일.
# 원서 「Resources and Ownership」의 세 행위자 관계(사실 확인용 요약): 사용자는 프로세스를 띄우고
#       파일을 소유한다. 파일에는 소유자가 있고 기본은 만든 사용자다. 프로세스는 통신과 보존을 위해
#       파일을 쓰고, 사용자가 파일을 쓰는 길은 프로세스를 거치는 간접 경로뿐이다.
#       credentials(7): "These IDs determine who owns the process."
# 타입 스펙: type-architecture — 구성요소와 그 사이의 연결. accent 는 간접 경로 한 줄.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 548
d = D(W, H, "LEARNING MODERN LINUX · 04-01 §1",
      "사용자는 프로세스를 띄우고 파일을 소유한다",
      "접근 관점에서 본 세 행위자와 그 관계. 사용자가 파일에 직접 닿는 길은 없고 "
      "언제나 프로세스를 거친다.",
      "프로세스는 사용자 계정으로 실행됩니다")

UX, UY, BW, BH = 60, 176, 280, 112
PX, PY = 300, 356
FX, FY = 540, 176

d.box(UX, UY, BW, BH, PAPER2, INFO, 1.2, 8)
d.t(UX + BW / 2, UY + 40, "사용자", 17, INFO, KR, "middle", 600)
d.t(UX + BW / 2, UY + 66, "UID 로 식별", 12, MUTED, KR)
d.t(UX + BW / 2, UY + 86, "로그인 · 프로세스 실행", 12, MUTED, KR)

d.box(FX, FY, BW, BH, PAPER2, OK, 1.2, 8)
d.t(FX + BW / 2, FY + 40, "파일", 17, OK, KR, "middle", 600)
d.t(FX + BW / 2, FY + 66, "소유자 하나", 12, MUTED, KR)
d.t(FX + BW / 2, FY + 86, "기본은 만든 사용자", 12, MUTED, KR)

d.box(PX, PY, BW, BH, PAPER2, MUTED, 1.2, 8)
d.t(PX + BW / 2, PY + 40, "프로세스", 17, INK, KR, "middle", 600)
d.t(PX + BW / 2, PY + 66, "실행 중인 프로그램", 12, MUTED, KR)
d.t(PX + BW / 2, PY + 86, "사용자의 UID 를 지님", 12, MUTED, KR)

d.path(f"M {UX + 140} {UY + BH} L {UX + 140} {PY + 40} L {PX - 10} {PY + 40}",
       INFO, 1.5, m="info")
d.t(UX + 152, PY + 30, "띄움", 12, INFO, KR, "start")

d.path(f"M {UX + BW} {UY + 44} L {FX - 10} {FY + 44}", INFO, 1.5, m="info")
d.t((UX + BW + FX) / 2, UY + 34, "소유", 12, INFO, KR)

d.path(f"M {PX + BW} {PY + 40} L {FX + 140} {PY + 40} L {FX + 140} {FY + BH + 8}",
       OK, 1.5, m="ok")
d.t(FX + 152, PY + 30, "사용 — 통신과 보존", 12, OK, KR, "start")

d.path(f"M {UX + BW} {UY + 84} L {FX - 10} {FY + 84}", ACC, 1.5, m="acc", dash="6 5")
d.t((UX + BW + FX) / 2, UY + 104, "간접 사용뿐", 12, ACC, KR, "middle", 600)
d.t((UX + BW + FX) / 2, UY + 124, "프로세스를 거침", 12, ACC, KR)

d.legend(500, [("사용자가 하는 일", INFO), ("프로세스가 하는 일", OK), ("직접 길이 없는 곳", ACC)])
d.save("04-01.users-files.svg")
print("ok 04-01.users-files")
