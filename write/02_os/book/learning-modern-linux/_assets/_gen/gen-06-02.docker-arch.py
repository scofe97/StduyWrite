# 06-02 §5 — docker run 한 줄이 호스트 안에서 실제로 지나는 자리: CLI → 데몬 → (레지스트리에서 당겨 온)
#           로컬 이미지 → 컨테이너, 그리고 데몬이 커널에 만들어 달라는 네임스페이스·cgroups.
# 원문("Docker"): "What's so unique about Docker is not the building blocks (namespaces, cgroups, CoW
#       filesystems, and bind mounts). These existed a while before Docker came into being. What's so
#       special is that Docker combined these building blocks in a way that makes them easy to use by
#       hiding the complexity of managing the low-level bits like namespaces and cgroups."
#   The container image: "A compressed archive file that contains metadata in JSON files and the layers,
#       which are effectively directories. The Docker daemon pulls the container images as needed from a
#       container registry."
#   The container as the runtime artifact: "You can start, stop, kill, and remove it. You interact with
#       the Docker daemon using a client CLI tool (docker). This CLI tool sends commands to the daemon,
#       which in turn executes the respective operation, such as building or running a container."
# 원문("Running containers"): "The docker run command takes a container image and a set of runtime
#       inputs, such as environment variables, ports to expose, and volumes to mount. With this
#       information, Docker creates the necessary namespaces and cgroups and launches the application
#       defined in the container image (CMD or ENTRYPOINT)."
# 값: 명령 `docker run -d --rm nginx:1.21` 과 레지스트리 경로 `public.ecr.aws/some:tag` 는 본문 명령 표의 예다.
#       컨테이너의 정의(프로세스 그룹)는 본문 핵심 요약의 것이다.
# 축약: 이미지 안의 층 셋은 개수가 출력에 없는 예라 점선으로 그렸다. 데몬과 커널 사이의 런타임
#       (containerd·runc)은 §5 본문이 Docker 의 내부로 말하지 않아 그리지 않았다. 레지스트리 인증도 뺐다.
# 타입 스펙: type-architecture — 호스트 경계 안팎의 구성요소와 연결. accent 는 데몬이 대신 만들어 주는
#           네임스페이스·cgroups 한 묶음.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 612
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §5",
      "docker run 한 줄이 호스트 안에서 지나는 자리",
      "사용자가 docker CLI 로 docker run -d --rm nginx:1.21 을 치면 명령이 Docker 데몬으로 간다. 데몬은 "
      "필요하면 레지스트리에서 이미지를 당겨 오는데, 이미지는 JSON 메타데이터와 디렉토리인 층을 담은 "
      "압축 아카이브다. 데몬은 런타임 입력을 받아 커널에 네임스페이스와 cgroups 를 만들고 그 안에서 "
      "이미지에 정의된 앱을 프로세스 그룹으로 띄운다. 커널의 네 재료는 Docker 이전부터 있었다.",
      "Docker 가 새로 만든 것은 커널 아래가 아니라 위의 사용 방식입니다")

HX0, HX1, HY0 = 24, 640, 104          # 호스트 경계
GX0, GX1 = 680, 856                   # 레지스트리
AY, AH = 136, 60                      # 1행: CLI · 데몬 · 레지스트리
BY_, BH = 268, 120                    # 2행: 컨테이너 · 이미지
SEG = BY_ + BH + 24                   # 데몬 → 커널 가로 구간
KY, KH = SEG + 36, 80                 # 커널 띠
HY1 = KY + KH + 16
CX0, CX1 = 44, 300                    # 왼쪽 열
DX0, DX1 = 384, 620                   # 오른쪽 열
IX1 = 580                             # 이미지 상자 오른쪽(데몬 → 커널 선이 지나갈 자리)

d.o.append(f'<rect x="{HX0}" y="{HY0}" width="{HX1 - HX0}" height="{HY1 - HY0}" rx="10" fill="none" '
           f'stroke="{RULE}" stroke-width="1.2"/>')
d.t(HX0 + 12, HY0 + 18, "호스트", 12, SOFT, KR, "start", 600)

# 연결선 먼저
d.arrow([(CX1, AY + AH / 2), (DX0 - 4, AY + AH / 2)], INFO, "info", 1.5)
d.arrow([(GX0, AY + AH / 2), (DX1 + 4, AY + AH / 2)], MUTED, "ar", 1.4)
d.arrow([(480, AY + AH), (480, BY_ - 4)], OK, "ok", 1.4)
d.arrow([(DX0, BY_ + BH / 2), (CX1 + 4, BY_ + BH / 2)], OK, "ok", 1.4)
d.arrow([(604, AY + AH), (604, SEG), (172, SEG), (172, KY + 4)], ACC, "acc", 1.5)

# 1행
d.box(CX0, AY, CX1 - CX0, AH, PAPER2, INFO, 1.2, 8)
d.t(CX0 + 14, AY + 24, "docker", 14, INFO, MONO, "start", 600)
d.t(CX0 + 84, AY + 24, "CLI", 12, MUTED, MONO, "start")
d.t(CX0 + 14, AY + 46, "$ docker run -d --rm nginx:1.21", 11.5, INK, MONO, "start")
d.t((CX1 + DX0) / 2, AY + AH / 2 - 10, "명령", 12, INFO, KR)

d.box(DX0, AY, DX1 - DX0, AH, PAPER2, INFO, 1.2, 8)
d.t((DX0 + DX1) / 2, AY + 26, "Docker 데몬", 14, INFO, KR, "middle", 600)
d.t((DX0 + DX1) / 2, AY + 46, "빌드 · 실행을 수행", 12, MUTED, KR)

d.box(GX0, AY, GX1 - GX0, AH, PAPER2, MUTED, 1.2, 8)
d.t((GX0 + GX1) / 2, AY + 26, "컨테이너 레지스트리", 13, INK, KR, "middle", 600)
d.t((GX0 + GX1) / 2, AY + 46, "public.ecr.aws/some:tag", 11, MUTED, MONO)
d.t((HX1 + GX0) / 2, AY + AH / 2 - 10, "pull", 12, MUTED, MONO)

# 런타임 입력 칩 (docker run 이 함께 받는 것)
RY = AY + AH + 28
d.t(CX0, RY + 4, "런타임 입력", 12, SOFT, KR, "start")
for cx, c in ((196, "환경 변수"), (264, "포트"), (316, "볼륨")):
    d.chip(cx, RY, c, MUTED, 11)

# 2행 — 컨테이너
d.box(CX0, BY_, CX1 - CX0, BH, PAPER2, OK, 1.2, 8)
d.t(CX0 + 14, BY_ + 26, "컨테이너", 14, OK, KR, "start", 600)
d.t(CX1 - 14, BY_ + 26, "런타임 산출물", 11, SOFT, KR, "end")
d.box(CX0 + 14, BY_ + 40, CX1 - CX0 - 28, 36, PAPER, MUTED, 1.0, 6)
d.t((CX0 + CX1) / 2, BY_ + 63, "nginx 프로세스 그룹", 12, INK, KR)
d.t((CX0 + CX1) / 2, BY_ + 102, "start · stop · kill · rm", 12, MUTED, MONO)
d.t((DX0 + CX1) / 2, BY_ + BH / 2 - 10, "앱 실행", 12, OK, KR)

# 2행 — 로컬 이미지
d.box(DX0, BY_, IX1 - DX0, BH, PAPER2, OK, 1.2, 8)
d.t(DX0 + 14, BY_ + 26, "nginx:1.21", 13, OK, MONO, "start", 600)
d.t(IX1 - 14, BY_ + 26, "이미지", 11, SOFT, KR, "end")
d.box(DX0 + 14, BY_ + 40, 64, 64, PAPER, MUTED, 1.0, 4)
d.t(DX0 + 46, BY_ + 68, "JSON", 12, INK, MONO, "middle", 600)
d.t(DX0 + 46, BY_ + 86, "메타", 11, MUTED, KR)
LX0_ = DX0 + 92
for i in range(3):
    y = BY_ + 40 + i * 22
    d.o.append(f'<rect x="{LX0_}" y="{y}" width="{IX1 - 14 - LX0_}" height="18" rx="3" fill="{OK}14" '
               f'stroke="{OK}" stroke-width="0.9" stroke-dasharray="4 3"/>')
d.t((LX0_ + IX1 - 14) / 2, BY_ + 40 + 13, "층 = 디렉토리 (예)", 11, INK, KR)
d.t(488, BY_ - 22, "당겨 둔 이미지", 11, OK, KR, "start")

# 데몬 → 커널 구간 라벨
d.t(320, SEG + 20, "네임스페이스 · cgroups 생성", 12, ACC, KR, "start", 600)

# 커널 띠
d.box(CX0, KY, DX1 - CX0, KH, PAPER2, MUTED, 1.0, 8)
d.t(CX0 + 14, KY + 22, "리눅스 커널 — Docker 이전부터 있던 재료", 12, SOFT, KR, "start", 600)
FX0, FX1 = CX0 + 12, CX1 + 12
d.o.append(f'<rect x="{FX0}" y="{KY + 32}" width="{FX1 - FX0}" height="36" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.chip(FX0 + 74, KY + 50, "네임스페이스", ACC, 12)
d.chip(FX0 + 196, KY + 50, "cgroups", ACC, 12)
d.chip(DX1 - 12 - 98 - 12 - 67, KY + 50, "CoW 파일시스템", MUTED, 12)
d.chip(DX1 - 12 - 49, KY + 50, "바인드 마운트", MUTED, 12)

d.legend(HY1 + 20, [("클라이언트 · 데몬", INFO), ("이미지 · 컨테이너", OK), ("데몬이 대신 만드는 것", ACC)])
d.save("06-02.docker-arch.svg")
print("ok 06-02.docker-arch", HY1 + 20)
