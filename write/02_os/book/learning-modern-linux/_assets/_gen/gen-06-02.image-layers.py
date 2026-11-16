# 06-02 §6 — greeter Dockerfile 일곱 줄이 빌드되며 쌓인 실제 모양: Step 마다 이미지 ID 가 하나씩 생기고,
#           태그 greeter:1 은 맨 위 ID 를, ubuntu:20.04 는 맨 아래 ID 를 가리킨다.
# 원문("Container Images") 지시어 범주 다섯 — Base images(FROM), Metadata(LABEL),
#       Arguments and environment variables(ARGS, ENV),
#       Build-time specifications("COPY, RUN, etc., which define how the image is constructed, layer for
#       layer"), Runtime specifications("CMD and ENTRYPOINT, which define how the container can be run").
# 원문("Example: containerized greeter") Dockerfile 축자 —
#       FROM ubuntu:20.04 / LABEL org.opencontainers.image.authors="Michael Hausenblas" /
#       COPY greeter.sh /app/ / WORKDIR /app / RUN chown -R 1001:1 /app / USER 1001 /
#       ENTRYPOINT ["/app/greeter.sh"]
#       USER 줄에 붙은 저자 설명 — "If you don't do this, it will unnecessarily run as root."
# 값: 본문 `sudo docker build -t greeter:1 .` 출력 그대로 — build context 3.072kB, Step 1~7 의 ID
#       (fb52e22af1b0 · def717e3352b · 5f3eb160fea3 · d73572886c13 · 42c35a6db6e2 · b6e0e27f253b ·
#       433a5f10d84e). `docker images` 출력 — greeter 1 433a5f10d84e 72.8MB, ubuntu 20.04 fb52e22af1b0 72.8MB.
#       ubuntu:20.04 의 IMAGE ID 가 Step 1 의 ID 와 같다는 것이 "베이스의 층을 공유" 의 실제 모습이다.
# 주의: 빌드 출력 Step 7/7 은 CMD 로 찍혀 있어 목록의 ENTRYPOINT 와 어긋난다(본문 원문 정오). 도식은 목록을
#       따르고 그 줄에 "출력엔 CMD" 칩을 단다 — 조용히 한쪽으로 맞추지 않는다.
# 색: 본문이 범주를 준 줄만 범주색을 쓴다(FROM 베이스, COPY·RUN 빌드 시점, ENTRYPOINT 런타임). LABEL 은
#       메타데이터, WORKDIR 은 본문이 범주를 말하지 않아 둘 다 중립색. USER 는 4장의 최소 권한이 착지한
#       자리라 accent.
# 타입 스펙: type-layers — 아래(베이스)에서 위(마지막 지시어)로 쌓이는 층. accent 는 USER 1001 한 줄.
# 축약: 층마다의 실제 크기와 어느 줄이 파일시스템 내용을 바꾸는지는 본문에 없어 그리지 않았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 624
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §6",
      "Step 마다 ID 가 하나씩 쌓이고 태그는 그 ID 를 가리킨다",
      "docker build 가 Dockerfile 일곱 줄을 차례로 처리하며 Step 마다 이미지 ID 를 하나씩 남긴다. "
      "맨 아래 Step 1 의 fb52e22af1b0 은 ubuntu:20.04 의 IMAGE ID 와 같고, 맨 위 433a5f10d84e 에 "
      "greeter:1 태그가 붙는다. 두 이미지가 각각 72.8MB 로 나와도 아래 층은 디스크에 한 벌이다. "
      "USER 1001 줄이 없으면 컨테이너는 불필요하게 root 로 돈다.",
      "greeter:1 은 ubuntu:20.04 위에 여섯 단계를 얹은 것입니다")

SX0, SX1 = 56, 600            # 층 띠
Y7, RH, RS = 116, 42, 50      # 맨 위(Step 7) y, 높이, stride
steps = [  # (step, 지시어, ID, 색, 칩)
    (1, "FROM ubuntu:20.04", "fb52e22af1b0", INFO, None),
    (2, "LABEL org.opencontainers.image.authors", "def717e3352b", MUTED, None),
    (3, "COPY greeter.sh /app/", "5f3eb160fea3", OK, None),
    (4, "WORKDIR /app", "d73572886c13", MUTED, None),
    (5, "RUN chown -R 1001:1 /app", "42c35a6db6e2", OK, None),
    (6, "USER 1001", "b6e0e27f253b", ACC, None),
    (7, "ENTRYPOINT [\"/app/greeter.sh\"]", "433a5f10d84e", WARN, "출력엔 CMD"),
]


def ry(n):
    return Y7 + (7 - n) * RS


# 빌드 순서 화살표(왼쪽 여백)
d.t(24, Y7 - 12, "빌드 순서", 11, SOFT, KR, "start")
d.arrow([(36, ry(1) + RH), (36, Y7 + 4)], SOFT, "soft", 1.2)

# 오른쪽 태그 — 연결선 먼저
TX0, TX1 = 640, 856
for n in (7, 1):
    y = ry(n) + RH / 2
    d.arrow([(TX0 - 2, y), (SX1 + 6, y)], ACC if n == 7 else INFO, "acc" if n == 7 else "info", 1.3)

for n, ins, iid, c, chip in steps:
    y = ry(n)
    if c is ACC:
        d.o.append(f'<rect x="{SX0}" y="{y}" width="{SX1 - SX0}" height="{RH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(SX0, y, SX1 - SX0, RH, PAPER2, c, 1.1, 6)
    by = y + RH / 2 + 5
    d.t(SX0 + 12, by, f"{n}/7", 11, SOFT, MONO, "start")
    d.t(SX0 + 56, by, ins, 12.5, INK if c is MUTED else c, MONO, "start", 600)
    d.t(SX1 - 12, by, iid, 12, INFO, MONO, "end")
    if chip:
        d.chip(SX0 + 380, y + RH / 2, chip, WARN, 11)

# 태그 상자
for n, tag, iid, c in ((7, "greeter:1", "433a5f10d84e", ACC), (1, "ubuntu:20.04", "fb52e22af1b0", INFO)):
    y = ry(n)
    d.box(TX0, y, TX1 - TX0, RH, PAPER, c, 1.2, 6)
    d.t(TX0 + 14, y + 18, tag, 13, c, MONO, "start", 600)
    d.t(TX0 + 14, y + 35, "72.8MB", 11, MUTED, MONO, "start")
    d.t(TX1 - 14, y + 35, "태그", 11, SOFT, KR, "end")

# 가운데: 크기 합산과 디스크
NY0, NY1 = ry(6) + 12, ry(2) + RH - 12
d.o.append(f'<rect x="{TX0}" y="{NY0}" width="{TX1 - TX0}" height="{NY1 - NY0}" rx="8" fill="none" '
           f'stroke="{OK}" stroke-width="1.1" stroke-dasharray="5 4"/>')
cx = (TX0 + TX1) / 2
d.t(cx, NY0 + 30, "docker images", 12, SOFT, MONO)
d.t(cx, NY0 + 62, "72.8MB + 72.8MB", 13, INK, MONO, "middle", 600)
d.t(cx, NY0 + 86, "합산 145.6MB 가 아님", 12, MUTED, KR)
d.line(TX0 + 24, NY0 + 108, TX1 - 24, NY0 + 108, RULE, 1)
d.t(cx, NY0 + 136, "fb52e22af1b0 은", 12, INFO, MONO)
d.t(cx, NY0 + 158, "디스크에 한 벌", 12, INK, KR, "middle", 600)
d.t(cx, NY0 + 182, "5장 CoW · 층 공유", 12, OK, KR)

# 아래: 빌드 입력
BY = ry(1) + RH + 32
d.arrow([(SX0 + 120, BY - 2), (SX0 + 120, ry(1) + RH + 4)], MUTED, "ar", 1.3)
d.box(SX0, BY, SX1 - SX0, 48, PAPER, MUTED, 1.0, 6)
d.t(SX0 + 14, BY + 20, "$ sudo docker build -t greeter:1 .", 12.5, INK, MONO, "start", 600)
d.t(SX0 + 14, BY + 38, "build context 3.072kB → Docker daemon", 11.5, MUTED, MONO, "start")

d.legend(BY + 48 + 24, [("베이스", INFO), ("빌드 시점 명세", OK), ("런타임 명세", WARN),
                        ("root 를 피하는 줄", ACC)])
d.save("06-02.image-layers.svg")
print("ok 06-02.image-layers", BY + 72)
