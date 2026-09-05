# 06-02 §5 — Docker 의 두 개념과, docker run 한 줄이 실제로 시키는 일.
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
# 타입 스펙: type-architecture — 구성요소와 그 사이의 연결. accent 는 이 절의 논점, 곧 데몬이 대신
#           불러 주는 커널 기능들. 축약: 레지스트리 인증과 이미지 서명 경로는 원문에 없어 그리지 않았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 620
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §5",
      "명령 한 줄이 커널 기능 둘을 대신 불러 준다",
      "Docker 의 개념은 이미지와 컨테이너 둘뿐이다. 그 사이에서 데몬이 하는 일이 "
      "이 장 전체의 논점이다.",
      "특별한 것은 재료가 아니라 복잡함을 숨긴 조합입니다")

CX, CY, CW_, CH_ = 32, 168, 216, 76
d.box(CX, CY, CW_, CH_, PAPER2, INFO, 1.2, 8)
d.t(CX + 16, CY + 30, "docker", 15, INFO, MONO, "start", 600)
d.t(CX + 16, CY + 54, "클라이언트 CLI 도구", 11.5, MUTED, KR, "start")

DX, DY, DW, DH = 320, 168, 240, 76
d.box(DX, DY, DW, DH, PAPER2, INFO, 1.2, 8)
d.t(DX + DW / 2, DY + 30, "Docker 데몬", 15, INFO, KR, "middle", 600)
d.t(DX + DW / 2, DY + 54, "명령을 받아 연산을 수행한다", 11.5, MUTED, KR)

RX, RY_, RW, RH_ = 632, 168, 216, 76
d.box(RX, RY_, RW, RH_, PAPER2, MUTED, 1.2, 8)
d.t(RX + RW / 2, RY_ + 30, "컨테이너 레지스트리", 14, INK, KR, "middle", 600)
d.t(RX + RW / 2, RY_ + 54, "필요할 때 데몬이 당겨 온다", 11.5, MUTED, KR)

d.path(f"M {CX + CW_} {CY + 38} L {DX - 8} {DY + 38}", INFO, 1.5, m="info")
d.t((CX + CW_ + DX) / 2, CY + 26, "명령", 11.5, INFO, KR)
d.path(f"M {DX + DW} {DY + 38} L {RX - 8} {RY_ + 38}", MUTED, 1.5, m="ar")
d.t((DX + DW + RX) / 2, DY + 26, "pull", 11.5, MUTED, MONO)

IX, IY, IW, IH = 320, 296, 240, 96
d.box(IX, IY, IW, IH, PAPER2, OK, 1.2, 8)
d.t(IX + IW / 2, IY + 30, "컨테이너 이미지", 14.5, OK, KR, "middle", 600)
d.t(IX + IW / 2, IY + 56, "압축된 아카이브 파일", 11.5, MUTED, KR)
d.t(IX + IW / 2, IY + 76, "JSON 메타데이터 + 층", 11.5, MUTED, MONO)
d.path(f"M {DX + DW / 2} {DY + DH} L {IX + IW / 2} {IY - 2}", OK, 1.4, m="ok")

KX, KY, KW, KH = 632, 296, 216, 96
d.o.append(f'<rect x="{KX}" y="{KY}" width="{KW}" height="{KH}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
d.t(KX + KW / 2, KY + 28, "커널에 시키는 일", 14, ACC, KR, "middle", 600)
d.t(KX + KW / 2, KY + 52, "필요한 네임스페이스와", 11.5, ACC, KR)
d.t(KX + KW / 2, KY + 72, "cgroups 를 만든다", 11.5, ACC, KR)
d.path(f"M {DX + DW} {DY + 60} L {KX + KW / 2} {DY + 60} L {KX + KW / 2} {KY - 2}",
       ACC, 1.4, m="acc")

TX, TY, TW, TH = 32, 296, 240, 96
d.box(TX, TY, TW, TH, PAPER2, MUTED, 1.2, 8)
d.t(TX + TW / 2, TY + 28, "런타임 입력", 14, INK, KR, "middle", 600)
d.t(TX + TW / 2, TY + 52, "환경 변수 · 노출할 포트", 11.5, MUTED, KR)
d.t(TX + TW / 2, TY + 72, "마운트할 볼륨", 11.5, MUTED, KR)
d.path(f"M {TX + TW} {TY + 48} L {DX + DW / 2} {TY + 48} L {DX + DW / 2} {DY + DH + 2}",
       MUTED, 1.3, m="ar", dash="6 5")

BX, BY, BW, BH = 320, 428, 240, 76
d.box(BX, BY, BW, BH, PAPER2, OK, 1.2, 8)
d.t(BX + BW / 2, BY + 30, "컨테이너", 15, OK, KR, "middle", 600)
d.t(BX + BW / 2, BY + 54, "start · stop · kill · rm", 11.5, MUTED, MONO)
d.path(f"M {IX + IW / 2} {IY + IH} L {BX + BW / 2} {BY - 2}", OK, 1.4, m="ok")

d.tone(32, 428, 240, 76, MUTED)
d.t(52, 456, "재료는 Docker 이전에도 있었습니다", 12, INK, KR, "start", 600)
d.t(52, 478, "네임스페이스 · cgroups", 11.5, MUTED, MONO, "start")
d.t(52, 496, "CoW 파일시스템 · 바인드 마운트", 11.5, MUTED, KR, "start")

d.legend(536, [("클라이언트와 데몬", INFO), ("두 개념", OK), ("데몬이 대신 부르는 것", ACC)])
d.save("06-02.docker-arch.svg")
print("ok 06-02.docker-arch")
