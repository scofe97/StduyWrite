# 타입 스펙: type-layers
# 03-01.dockershim-vs-containerd-path — dockershim 경로와 containerd 직접 경로의 호출 단수
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dd import D, INK, MUTED, SOFT, ACC, INFO, OK, BAD, KR, MONO

W, H = 1000, 548
ROW_H, ROW_GAP, Y0 = 52, 20, 134
STACK_W = 420
LX, RX = 40, 540

d = D(W, H, "CALL DEPTH · 03-01",
      "컨테이너가 뜨기까지 건너는 층 비교",
      "dockershim 경로는 Docker Engine 을 한 번 더 거치고 containerd 직접 경로는 거치지 않는 차이",
      lead="두 경로 모두 컨테이너의 부모 프로세스는 containerd-shim 입니다")

LEFT = [("L1", "kubelet · dockershim", "CRI 를 Docker API 로 변환", INFO),
        ("L2", "Docker Engine", "내부에서 containerd 에 위임", BAD),
        ("L3", "containerd", "네임스페이스 moby", INFO),
        ("L4", "containerd-shim", "컨테이너의 부모", INFO),
        ("L5", "컨테이너 프로세스", "nginx", OK)]
RIGHT = [("L1", "kubelet", "CRI 로 직접 호출", INFO),
         ("L2", "containerd", "CRI 플러그인 · 네임스페이스 k8s.io", ACC),
         ("L3", "containerd-shim", "컨테이너의 부모", INFO),
         ("L4", "컨테이너 프로세스", "nginx", OK)]


def stack(x, rows, title, dashed_color=None):
    d.t(x, Y0 - 16, title, 14, INK, KR, "start", 600)
    for i, (tag, name, sub, c) in enumerate(rows):
        y = Y0 + (ROW_H + ROW_GAP) * i
        if c == dashed_color:
            d.o.append(f'<rect x="{x}" y="{y}" width="{STACK_W}" height="{ROW_H}" rx="6" '
                       f'fill="{c}10" stroke="{c}" stroke-width="1.4" stroke-dasharray="6 4"/>')
        else:
            d.tone(x, y, STACK_W, ROW_H, c, 6, "10", 1.4 if c == ACC else 1.0)
        d.t(x + 14, y + 31, tag, 10, SOFT, MONO, "start")
        d.t(x + 50, y + 31, name, 14, c, MONO if name.startswith(("kubelet", "containerd", "Docker")) else KR,
            "start", 600)
        d.t(x + STACK_W - 14, y + 31, sub, 12, MUTED, KR, "end")
        if i < len(rows) - 1:
            d.arrow([(x + STACK_W / 2, y + ROW_H + 2), (x + STACK_W / 2, y + ROW_H + ROW_GAP - 3)],
                    MUTED, "ar", 1.4)


stack(LX, LEFT, "dockershim 경로 — 건너는 경계 4개", BAD)
stack(RX, RIGHT, "containerd 직접 경로 — 건너는 경계 3개")

d.legend(504, [("두 경로가 공유하는 층", INFO), ("dockershim 경로에만 있는 층", BAD),
               ("현재 경로의 중심", ACC), ("컨테이너", OK)])
d.save(str(Path(__file__).resolve().parent.parent / "03-01.dockershim-vs-containerd-path.svg"))
print("ok 03-01.dockershim-vs-containerd-path")
