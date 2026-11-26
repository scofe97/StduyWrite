# 01-01 학습 목표 뒤 전체 지도 — 절 여섯을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 핵심)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(저장소 chapter-overview 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 560
d = D(W, H, "02_OS · FILESYSTEM · 01-01",
      "FHS 두 축에서 불변 OS·컨테이너 배치까지",
      "1절의 배치 충돌에서 시작해 2절의 FHS 두 축을 딛고 관리 주체, /opt 번들, OSTree 불변 OS, 컨테이너·Kubernetes 경계로 이어지는 전체 흐름 지도.",
      "2절의 두 분류 축이 나머지 절의 경로 판단 기준을 떠받칩니다")

CW, CH, GAP, X0 = 400, 108, 24, 28
ROWS = [104, 240, 376]
cards = [
    ("§1", "폴더 규칙이 없을 때의 충돌", "업그레이드 덮어쓰기와 루트 비대화"),
    ("§2", "FHS 3.0 두 분류 축", "공유 가능성 × 변경 여부로 /usr·/etc·/var 분리"),
    ("§3", "관리 주체별 설치 경로", "/usr · /usr/local · /opt · /srv 네 갈래"),
    ("§4", "대형 제품과 /opt 번들", "의존성 격리와 OS 패치 사각지대"),
    ("§5", "불변 OS 와 OSTree 배치", "읽기 전용 /usr · /var 링크 · /etc 병합"),
    ("§6", "컨테이너·Kubernetes 경계", "이미지 rootfs FHS · 호스트 마운트 · PVC"),
]

def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]

for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH // 2), (x2 - 2, y2 + CH // 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW // 2} {y1 + CH} L {x1 + CW // 2} {bus} L {x2 + CW // 2} {bus} L {x2 + CW // 2} {y2 - 2}",
               MUTED, 1.4, m="ar")

for i, (num, title, sub) in enumerate(cards):
    x, y = pos(i); focal = (i == 1)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, y + 28, num, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 20, y + 58, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, y + 86, sub, 13, MUTED, KR, "start")

d.legend(512, [("나머지 절의 기준 축", ACC)])
d.save("01-01.chapter-overview.svg")
