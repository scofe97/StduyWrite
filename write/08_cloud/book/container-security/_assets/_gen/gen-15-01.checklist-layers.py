# 타입 스펙: type-layers — 체크리스트 열아홉 항목을 안쪽에서 바깥으로 다섯 계층(실행 권한 · 이미지·공급망 · 커널 격리 · 컴포넌트 사이 통신 · 호스트·클라우드)으로 묶고, 어느 층에도 속하지 않고 전부를 가로지르는 런타임 축 하나를 옆에 세운다. focal 은 런타임 축.
# 사실 출처: 노트 L62~L78(다섯 계층의 항목·베이스 이미지 선택지·Docker 기본 프로파일→앱별 프로파일·mTLS 수단 무관·CIS 벤치마크·런타임 축)
# Layout conventions: 층 h=72, stride 84(y=100+84i), 폭 712(x=60), 오른쪽 런타임 축 x=796 w=120, 왼쪽 방향 화살표 x=36. 각 층은 왼쪽 인덱스 태그 · 층 이름 · 칩 목록 · 값 한 줄. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, PAPER, KR, MONO


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def tw(t, size):
    return sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)


W, H = 960, 580
BX, BW, BH, STRIDE, Y0 = 60, 712, 72, 84, 100
RX, RW = 796, 120

d = D(W, H, "CONTAINER SECURITY · 15-01 §2",
      "열아홉 항목은 안쪽에서 바깥으로 다섯 계층이고 런타임이 전부를 가로지른다",
      "컨테이너 실행 권한, 이미지와 공급망, 커널 격리, 컴포넌트 사이 통신, 호스트와 클라우드 순으로 묶고, "
      "런타임 보호와 드리프트 방지는 어느 계층에도 속하지 않고 다섯 계층을 모두 가로지른다.",
      "체크리스트를 평평한 목록이 아니라 심층 방어의 순서로 다시 묶은 배치")

LAYERS = [
    ("L1", "컨테이너 실행 권한",
     ["비root", "--privileged", "capability", "읽기 전용", "자원 한계"],
     "목록 맨 앞 · 항목 다섯"),
    ("L2", "이미지 · 공급망",
     ["베이스 이미지", "스캔 + 재빌드", "불변성", "어드미션 컨트롤"],
     "scratch · distroless · Alpine · RHEL minimal"),
    ("L3", "커널 격리",
     ["seccomp", "AppArmor", "SELinux"],
     "Docker 기본 프로파일 → 애플리케이션별 프로파일"),
    ("L4", "컴포넌트 사이 통신",
     ["상호 TLS", "네트워크 정책", "시크릿 관리"],
     "상호 TLS 는 애플리케이션 코드든 서비스 메시든"),
    ("L5", "호스트 · 클라우드",
     ["컨테이너 전용 호스트", "보안 릴리스", "CSPM", "CIS 벤치마크"],
     "Linux · Docker · Kubernetes 용 CIS 벤치마크"),
]
CHIP_X = BX + 188
for i, (tag, name, chips, sub) in enumerate(LAYERS):
    y = Y0 + i * STRIDE
    assert tw(name, 16) <= 152, name
    d.tone(BX, y, BW, BH, INFO, 6, "12", 1.0)
    d.t(BX + 16, y + 28, tag, 11, SOFT, MONO, "start")
    d.t(BX + 16, y + 52, name, 16, INK, KR, "start", 600)
    x = CHIP_X
    for c in chips:
        w = tw(c, 12) + 16
        d.o.append(f'<rect x="{x}" y="{y + 12}" width="{w:.1f}" height="24" rx="4" fill="{PAPER}" stroke="{INFO}" stroke-width="0.9"/>')
        d.t(x + w / 2, y + 28, c, 12, INK, kr(c))
        x += w + 8
    assert x - 8 <= BX + BW - 12, (name, x)
    assert tw(sub, 12) <= BX + BW - 12 - CHIP_X, sub
    d.t(CHIP_X, y + 58, sub, 12, MUTED, kr(sub), "start")

# 런타임 축: 모든 계층을 옆에서 가로지른다
bar_h = 4 * STRIDE + BH
d.tone(RX, Y0, RW, bar_h, ACC, 6, "1F", 1.4)
mid = Y0 + bar_h // 2
d.t(RX + RW / 2, mid - 72, "런타임 축", 15, INK, KR, "middle", 600)
d.t(RX + RW / 2, mid - 48, "지금 벌어지는 일", 12, MUTED, KR, "middle")
for k, c in enumerate(["런타임 보호", "드리프트 방지"]):
    w = tw(c, 12) + 16
    assert w <= RW - 12, (c, w)
    yy = mid - 20 + k * 40
    d.o.append(f'<rect x="{RX + (RW - w) / 2:.1f}" y="{yy}" width="{w:.1f}" height="24" rx="4" fill="{PAPER}" stroke="{ACC}" stroke-width="0.9"/>')
    d.t(RX + RW / 2, yy + 16, c, 12, INK, KR)
for i in range(5):
    cy = Y0 + i * STRIDE + BH // 2
    d.line(BX + BW, cy, RX, cy, ACC, 1.2, "3 4")
    d.o.append(f'<circle cx="{BX + BW}" cy="{cy}" r="3" fill="{ACC}"/>')

# 왼쪽 방향 화살표: 안쪽 → 바깥쪽
d.t(36, Y0 + 12, "안쪽", 12, MUTED, KR, "middle", 600)
d.arrow([(36, Y0 + 24), (36, Y0 + bar_h - 24)], SOFT, "soft", 1.4)
d.t(36, Y0 + bar_h - 4, "바깥", 12, MUTED, KR, "middle", 600)

d.legend(Y0 + bar_h + 24, [("계층 · 미리 막아 둔 것", INFO), ("런타임 축 · 지금 벌어지는 일", ACC)])
d.save(str(ASSETS / "15-01.checklist-layers.svg"))
print("ok 15-01 checklist-layers")
