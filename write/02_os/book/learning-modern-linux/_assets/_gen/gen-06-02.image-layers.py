# 06-02 §6 — Dockerfile 지시어 일곱이 층 일곱이 되는 과정.
# 원문("Container Images") 지시어 범주 다섯 — Base images(FROM), Metadata(LABEL),
#       Arguments and environment variables(ARGS, ENV),
#       Build-time specifications("COPY, RUN, etc., which define how the image is constructed, layer for
#       layer"), Runtime specifications("CMD and ENTRYPOINT, which define how the container can be run").
# 원문("Example: containerized greeter") Dockerfile 축자 —
#       FROM ubuntu:20.04 / LABEL org.opencontainers.image.authors="Michael Hausenblas" /
#       COPY greeter.sh /app/ / WORKDIR /app / RUN chown -R 1001:1 /app / USER 1001 /
#       ENTRYPOINT ["/app/greeter.sh"]
#       USER 줄에 붙은 저자 설명 — "This and the next line define the user running the app. If you don't
#       do this, it will unnecessarily run as root."
#       빌드 출력의 이미지 크기 — greeter:1 이 72.8MB, ubuntu:20.04 도 72.8MB.
# 주의: 저자의 빌드 출력 Step 7/7 은 CMD 로 찍혀 있어 목록의 ENTRYPOINT 와 어긋난다. 도식은 목록을
#       따르고 그 어긋남을 별도 띠로 표시한다 — 조용히 한쪽으로 맞추지 않는다.
# 타입 스펙: type-layers — 아래에서 위로 쌓이는 층과 그 사이의 계약. accent 는 4장의 최소 권한이
#           Dockerfile 두 줄로 착지하는 자리. 축약: 각 층의 실제 다이제스트는 논점이 아니라 뺐다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 700
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §6",
      "지시어 일곱이 층 일곱이 된다",
      "Dockerfile 의 각 줄이 이미지의 층 하나를 만든다. 빌드 시점의 지시어와 런타임의 지시어가 "
      "성격이 갈리고, 층으로 남는 것은 앞쪽이다.",
      "USER 를 쓰지 않으면 불필요하게 root 로 돕니다")

LX, LW, LH, GAP = 32, 560, 48, 8
Y0 = 168
layers = [
    ("FROM ubuntu:20.04", "베이스 이미지 — 명시적 태그로", INFO, 0),
    ("LABEL org.opencontainers...", "메타데이터 — 계보를 남긴다", MUTED, 0),
    ("COPY greeter.sh /app/", "빌드 시점 — 바이너리나 JAR 일 수도", OK, 0),
    ("WORKDIR /app", "빌드 시점 — 작업 디렉토리", OK, 0),
    ("RUN chown -R 1001:1 /app", "빌드 시점 — 소유를 옮긴다", OK, 0),
    ("USER 1001", "이 줄이 없으면 root 로 돈다", ACC, 1),
    ("ENTRYPOINT [\"/app/greeter.sh\"]", "런타임 — 인자를 덧붙일 수 있다", WARN, 0),
]
for i, (cmd, note, col, focal) in enumerate(layers):
    y = Y0 + i * (LH + GAP)
    if focal:
        d.o.append(f'<rect x="{LX}" y="{y}" width="{LW}" height="{LH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.5"/>')
    else:
        d.box(LX, y, LW, LH, PAPER2, col, 1.2, 6)
    d.t(LX + 16, y + 22, cmd, 12.5, col, MONO, "start", 600)
    d.t(LX + 16, y + 42, note, 11.5, MUTED, KR, "start")
    d.t(LX - 8, y + LH / 2 + 5, f"{i + 1}", 12, SOFT, MONO, "end")

RX = 624
d.box(RX, Y0, 224, 148, PAPER2, OK, 1.2, 8)
d.t(RX + 112, Y0 + 30, "docker images", 13, OK, MONO, "middle", 600)
d.line(RX + 16, Y0 + 44, RX + 208, Y0 + 44, RULE, 1)
for i, (name, size) in enumerate([("greeter:1", "72.8MB"), ("ubuntu:20.04", "72.8MB")]):
    d.t(RX + 20, Y0 + 72 + i * 26, name, 11.5, INK, MONO, "start")
    d.t(RX + 204, Y0 + 72 + i * 26, size, 11.5, MUTED, MONO, "end")
d.t(RX + 112, Y0 + 132, "더해서 145.6MB 가 아닙니다", 11.5, OK, KR)

d.o.append(f'<rect x="{RX}" y="{Y0 + 168}" width="224" height="120" rx="8" '
           f'fill="{ACC}06" stroke="{ACC}" stroke-width="1.2" stroke-dasharray="7 6"/>')
d.t(RX + 20, Y0 + 198, "5장의 CoW 가", 12.5, ACC, KR, "start", 600)
d.t(RX + 20, Y0 + 218, "여기에서 관측됩니다", 12.5, ACC, KR, "start", 600)
d.t(RX + 20, Y0 + 244, "greeter 가 베이스의 층을", 11.5, MUTED, KR, "start")
d.t(RX + 20, Y0 + 262, "공유하고 자기 층만 얹었기", 11.5, MUTED, KR, "start")
d.t(RX + 20, Y0 + 280, "때문입니다.", 11.5, MUTED, KR, "start")

WY = 572
d.tone(LX, WY, W - 64, 56, WARN)
d.t(LX + 20, WY + 26, "원문 정오 — 목록은 ENTRYPOINT 인데 빌드 출력은 CMD 입니다",
    12.5, INK, KR, "start", 600)
d.t(LX + 20, WY + 46,
    "ENTRYPOINT 는 인자를 덧붙이고 CMD 는 명령 자체를 대체합니다. 저자의 설명은 ENTRYPOINT 를 전제합니다.",
    11.5, MUTED, KR, "start")

d.legend(WY + 76, [("베이스", INFO), ("빌드 시점 — 층이 된다", OK),
                   ("런타임", WARN), ("4장의 최소 권한이 착지한 줄", ACC)])
d.save("06-02.image-layers.svg")
print("ok 06-02.image-layers")
