# 08-01 §1 — 두 자리가 따로 있어 한쪽만 바꿀 수 있다
# 본문의 요점은 "명령은 그대로 두고 인자만 바꾸거나 그 반대가 모두 가능하다"이다. 그러니
# 조합 셋을 나열하는 데서 그치면 안 되고, 실제로 실행되는 줄이 결과 열로 서 있어야 한다.
# 타입 스펙: type-dp-security-matrix.md — 행은 조합 셋, 열은 무엇을 덮었나와 실제로 실행되는 줄이다. 실행되는 줄이 결과 열로 서 있어
#           한쪽만 바꿔도 된다는 논지가 칸으로 드러난다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, KR
import ddx

# 좌표는 행렬 아래끝에서 산출한다 — y=556 은 4 행 행렬의 마지막 행(472~560) 안이라
# 산문이 마지막 행의 글자를 관통했다.
MTOP, ROW_H, GAP, NROWS = 148, 88, 12, 4
MBOT = MTOP + 24 + NROWS * (ROW_H + GAP) - GAP   # 560
NOTE_Y, LEG_Y = MBOT + 28, MBOT + 56
d = D(1240, LEG_Y + 40, "KUBERNETES IN ACTION · 08-01",
      "이미지를 다시 빌드하지 않고 바꾼다",
      "Dockerfile 의 ENTRYPOINT 와 CMD 가 Pod 매니페스트의 command 와 args 로 각각 이어진다. "
      "두 자리가 나뉘어 있어 한쪽만 덮어쓸 수 있다.",
      "ENTRYPOINT [\"/kiada\"]  ·  CMD [\"--port\", \"8080\"]")

ddx.matrix(
    d, x0=24, hdr_y=MTOP, row_h=ROW_H, gap=GAP, focal_col=3,
    cols=[(250, "매니페스트에 적은 것"), (280, "command"), (280, "args"), (350, "실제로 실행되는 것")],
    rows=[
        ([("아무것도 안 적으면", "기본값 그대로"), ("이미지의 ENTRYPOINT", "/kiada"),
          ("이미지의 CMD", "--port 8080"), ("/kiada --port 8080", "이미지가 정한 대로")], INFO),
        ([("command 만", "실행 파일을 바꾼다"), ("매니페스트 값", "/kiada-profiler"),
          ("이미지의 CMD", "--port 8080"), ("/kiada-profiler --port 8080", "인자는 그대로 따라간다")], OK),
        ([("args 만", "인자를 바꾼다"), ("이미지의 ENTRYPOINT", "/kiada"),
          ("매니페스트 값", "--port 9090"), ("/kiada --port 9090", "실행 파일은 그대로")], OK),
        ([("둘 다", "통째로 바꾼다"), ("매니페스트 값", "/bin/sh"),
          ("매니페스트 값", "-c 'sleep 3600'"), ("/bin/sh -c 'sleep 3600'", "이미지 기본값이 다 밀린다")], ACC),
    ])

d.t(24, NOTE_Y, "명령과 인자가 두 디렉티브·두 필드로 나뉘어 있어 이 조합이 가능하다. "
             "프로파일링을 켜려고 이미지를 다시 빌드할 필요가 없다.", 11, MUTED, KR, "start")
d.legend(LEG_Y, [("기본값", INFO), ("한쪽만 덮음", OK), ("둘 다 덮음", ACC)])
d.save("08-01-command-args-override.svg")
print("ok")
