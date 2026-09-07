# 타입 스펙: type-architecture — 무엇이 경계에 서고 무엇이 안팎으로 갈리는가.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.9 도입 + §8.9.1 (책 614~615쪽) —
#   목표 셋과 세 갈래 분류는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 1000, 576
d = D(W, H, "SECTION 8.9.1 · FIREWALL PLACEMENT",
      "관문을 하나로 모아야 정책을 강제할 수 있습니다",
      "성의 도개교와 사무 빌딩의 보안 데스크와 같은 자리다. 드나드는 모든 것이 한 곳을 지난다.",
      "목표 셋과 세 갈래 분류는 원문 §8.9.1 의 것입니다")

d.tone(24, 148, 300, 160, OK, 8, "12", 1.2)
d.t(174, 190, "조직의 망", 13, OK, KR, "middle", 600)
d.t(174, 218, "비교적 자유롭게", 11, MUTED, KR)
d.t(174, 240, "자원에 접근합니다", 11, MUTED, KR)

d.tone(404, 148, 192, 160, ACC, 8, "20", 1.5)
d.t(500, 190, "방화벽", 13, ACC, KR, "middle", 600)
d.t(500, 218, "검사 · 기록", 11, MUTED, KR)
d.t(500, 240, "버림 · 전달", 11, MUTED, KR)

d.tone(676, 148, 300, 160, BAD, 8, "12", 1.2)
d.t(826, 190, "나머지 전부", 13, BAD, KR, "middle", 600)
d.t(826, 218, "접근을 꼼꼼히", 11, MUTED, KR)
d.t(826, 240, "살펴야 합니다", 11, MUTED, KR)

d.arrow([(328, 212), (400, 212)], MUTED, "ar", 1.4)
d.arrow([(672, 244), (600, 244)], MUTED, "ar", 1.4)

GY = 336
d.box(24, GY, 470, 152, PAPER2, RULE, 1.0)
d.t(44, GY + 28, "방화벽의 목표 셋", 12, INK, KR, "start", 600)
d.line(44, GY + 40, 474, GY + 40, RULE, 0.8)
for i, (n, ln) in enumerate([("1", "모든 트래픽이 방화벽을 지납니다"),
                             ("2", "정책이 허용한 것만 통과합니다"),
                             ("3", "방화벽 자신이 뚫리지 않습니다")]):
    d.t(44, GY + 68 + i * 26, n, 11, SOFT, MONO, "start", 600)
    d.t(66, GY + 68 + i * 26, ln, 11, MUTED if i < 2 else ACC, KR, "start")
d.t(44, GY + 146, "셋째가 깨지면 잘못된 안전감만 남습니다 — 없느니만 못합니다.", 11, ACC, KR, "start")

d.box(514, GY, 462, 152, PAPER2, RULE, 1.0)
d.t(534, GY + 28, "세 갈래", 12, INK, KR, "start", 600)
d.line(534, GY + 40, 956, GY + 40, RULE, 0.8)
# 세 갈래는 같은 축의 세 단계라 한 색으로 둔다. OK/WARN 을 섞으면 범례의
# 내부·바깥 색과 뜻이 겹쳐 같은 색이 두 가지를 가리키게 된다.
KINDS = [("전통 패킷 필터", "헤더만 · 하나씩 따로", INFO),
         ("상태 필터", "연결을 기억합니다", INFO),
         ("응용 게이트웨이", "응용 데이터까지", INFO)]
for i, (k, v, c) in enumerate(KINDS):
    d.t(534, GY + 68 + i * 26, k, 11, c, KR, "start", 600)
    d.t(700, GY + 68 + i * 26, v, 11, MUTED, KR, "start")
d.t(534, GY + 146, "볼 수 있는 깊이가 막을 수 있는 것을 정합니다.", 11, SOFT, KR, "start")

d.legend(508, [("내부", OK), ("경계", ACC), ("바깥", BAD), ("보는 깊이", INFO)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-05.firewall-placement.svg"
d.save(out); print("→", out.name)
