# 02-02 §2.이미지 빌드 — docker build 가 실제로 시키는 일
# 본문 근거(02-02 §2 '이미지 빌드'):
#   "docker build -t kiada:latest ." · "-t 는 이미지 이름:태그, 마지막 . 은 빌드 컨텍스트(현재 디렉터리)"
#   "빌드 과정에서 Docker 는 베이스 이미지(node:23-alpine)를 로컬에 없으면 pull 하고, 그 이미지로
#    컨테이너를 만들어 Dockerfile 의 다음 지시문을 차례로 실행합니다. 각 지시문이 새 이미지 레이어
#    하나를 만들고, 마지막 이미지에 -t 로 지정한 태그가 붙습니다."
#   Dockerfile 지시문 4줄: FROM · COPY app.js · COPY html/ · ENTRYPOINT
# 타입 스펙: 주체가 넷(개발자·CLI·daemon·레지스트리)이고 순서가 논지다 → type-sequence.
#   focal 은 '지시문 하나 = 레이어 하나' 한 곳 — 본문이 레이어 구조로 넘어가는 지점이다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, INFO, OK, WARN, MUTED, SOFT, INK, KR, MONO
import ddx

d = Seq(1120, 714, "KUBERNETES IN ACTION · 02-02",
        "docker build 가 실제로 시키는 일",
        "docker build 는 CLI 가 직접 이미지를 만드는 것이 아니라 빌드 컨텍스트를 daemon 에 넘기고 "
        "결과를 돌려받는 절차다. 지시문 하나가 레이어 하나를 만들고, 마지막 이미지에 태그가 붙는다.",
        "docker build -t kiada:latest .  ·  베이스 이미지 node:23-alpine")

ddx.lanes(d, [("개발자", "터미널"),
              ("docker CLI", "docker build"),
              ("Docker daemon", "빌드 실행 주체"),
              ("레지스트리", "베이스 이미지 출처")], y0=110, lane_w=230)
d.rails(590)

ddx.msg(d, "개발자", "docker CLI", "docker build -t kiada:latest .", 206, INFO,
        sub="마지막 . 이 빌드 컨텍스트다")
ddx.msg(d, "docker CLI", "Docker daemon", "빌드 컨텍스트 전송", 262, INFO,
        sub="현재 디렉터리를 통째로 넘긴다")
ddx.msg(d, "Docker daemon", "레지스트리", "베이스 이미지 pull", 318, WARN, mk="warn",
        sub="로컬에 없을 때만 일어난다")
ddx.msg(d, "레지스트리", "Docker daemon", "node:23-alpine", 374, WARN, mk="warn", dash="6 5")
ddx.selfmsg(d, "Docker daemon", "지시문마다 레이어 하나", 430,
            sub="FROM · COPY 두 줄 · ENTRYPOINT")
ddx.state(d, "Docker daemon", "레이어가 쌓여 이미지가 된다", 486, ACC)
ddx.msg(d, "Docker daemon", "docker CLI", "이미지 ID + 태그", 538, INFO, dash="6 5")

d.t(24, 630, "CLI 는 빌드를 하지 않는다 — 컨텍스트를 넘기고 결과를 받을 뿐이다. "
             "그래서 컨텍스트에 불필요한 파일이 있으면 그만큼 전송 비용이 든다.", 11, MUTED, KR, "start")
d.legend(646, [("빌드가 만들어 내는 것", ACC), ("주고받는 호출", INFO),
               ("조건부로만 일어나는 것", WARN)])
d.save("02-02-image-build-sequence.svg")
print("ok image-build-sequence")
