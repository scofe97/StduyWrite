# 04-01 §1 — 사용자와 프로세스와 파일이 서로에게 하는 일.
# 원문("Resources and Ownership"): "Each user account is associated with a user ID that can be given
#       access to executables, files, devices, and other Linux assets. A human user can log in with a
#       user account, and a process can run as a user account."
#       Users: "Launch processes and own files. A process is a program (executable file) that the kernel
#              has loaded into main memory and runs."
#       Files: "Have owners; by default, the user who creates the file owns it."
#       Processes: "Use files for communication and persistency. Of course, users indirectly also use
#                  files, but they need to do so via processes."
#       저자는 이 그림이 매우 단순한 관점이지만 행위자와 그 관계를 이해하게 해 준다고 적는다.
# 타입 스펙: type-architecture — 구성요소와 그 사이의 연결. accent 는 저자가 "간접적으로만" 이라고
#           단서를 붙인 한 경로.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 616
d = D(W, H, "LEARNING MODERN LINUX · 04-01 §1",
      "사용자는 프로세스를 띄우고 파일을 소유한다",
      "원서가 접근 관점에서 그린 세 행위자와 그 관계. 사용자가 파일에 직접 닿는 길은 없고 "
      "언제나 프로세스를 거친다는 것이 이 그림의 논점이다.",
      "프로세스는 사용자 계정으로 실행됩니다")

UX, UY, BW, BH = 60, 176, 280, 112
PX, PY = 300, 356
FX, FY = 540, 176

d.box(UX, UY, BW, BH, PAPER2, INFO, 1.2, 8)
d.t(UX + BW / 2, UY + 40, "사용자", 17, INFO, KR, "middle", 600)
d.t(UX + BW / 2, UY + 66, "UID 로 식별되고", 12, MUTED, KR)
d.t(UX + BW / 2, UY + 86, "로그인하거나 프로세스를 돌린다", 12, MUTED, KR)

d.box(FX, FY, BW, BH, PAPER2, OK, 1.2, 8)
d.t(FX + BW / 2, FY + 40, "파일", 17, OK, KR, "middle", 600)
d.t(FX + BW / 2, FY + 66, "소유자가 있고", 12, MUTED, KR)
d.t(FX + BW / 2, FY + 86, "기본은 만든 사람이 갖는다", 12, MUTED, KR)

d.box(PX, PY, BW, BH, PAPER2, MUTED, 1.2, 8)
d.t(PX + BW / 2, PY + 40, "프로세스", 17, INK, KR, "middle", 600)
d.t(PX + BW / 2, PY + 66, "커널이 주기억장치에 올려 돌리는", 12, MUTED, KR)
d.t(PX + BW / 2, PY + 86, "실행 파일", 12, MUTED, KR)

# 사용자 -> 프로세스
d.path(f"M {UX + 140} {UY + BH} L {UX + 140} {PY + 40} L {PX - 10} {PY + 40}",
       INFO, 1.5, m="info")
d.t(UX + 152, PY + 30, "띄운다", 12, INFO, KR, "start")

# 사용자 -> 파일 (소유)
d.path(f"M {UX + BW} {UY + 44} L {FX - 10} {FY + 44}", INFO, 1.5, m="info")
d.t((UX + BW + FX) / 2, UY + 34, "소유한다", 12, INFO, KR)

# 프로세스 -> 파일 (사용)
d.path(f"M {PX + BW} {PY + 40} L {FX + 140} {PY + 40} L {FX + 140} {FY + BH + 8}",
       OK, 1.5, m="ok")
d.t(FX + 152, PY + 30, "쓴다 — 통신과 지속성", 12, OK, KR, "start")

# 사용자 -> 파일 (간접) — 저자가 단서를 붙인 경로
d.path(f"M {UX + BW} {UY + 84} L {FX - 10} {FY + 84}", ACC, 1.5, m="acc", dash="6 5")
d.t((UX + BW + FX) / 2, UY + 104, "간접적으로만", 12, ACC, KR, "middle", 600)
d.t((UX + BW + FX) / 2, UY + 124, "프로세스를 거쳐야 한다", 12, ACC, KR)

d.tone(28, 496, W - 32 - 16, 60, INFO)
d.t(48, 524, "저자는 이 그림이 아주 단순한 관점이라고 밝힙니다", 13, INK, KR, "start", 600)
d.t(48, 544, "그래도 행위자와 관계를 잡아 두면 뒤에서 상호작용을 자세히 볼 때 도움이 된다고 적습니다.",
    12, MUTED, KR, "start")

d.legend(572, [("사용자가 하는 일", INFO), ("프로세스가 하는 일", OK), ("직접 길이 없는 곳", ACC)])
d.save("04-01.users-files.svg")
print("ok 04-01.users-files")
