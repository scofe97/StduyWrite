# 타입 스펙: type-architecture — 사용자 · 소스 관리 · 클러스터 세 구역. 사용자는 Git 에만 체크인하고, 클러스터는 오퍼레이터만 고치며, 오퍼레이터의 배포 요청은 어드미션 컨트롤러의 다섯 검사를 지나야 컨테이너가 돈다. 사용자의 직접 접근은 점선으로 끊는다. focal 은 어드미션 컨트롤러.
# 사실 출처: 노트 L161~L171(어드미션 컨트롤 · 다섯 검사 · 실패하면 실행 안 됨), L175~L177(GitOps · 오퍼레이터 · 자격증명 · 감사 추적). 오퍼레이터의 요청이 어드미션을 지나는 배치는 노트가 적지 않은 도식 구성이다.
# Layout conventions: 흐름 중심선 y=282, 흐름 노드 h=64, 어드미션 h=164, 존 y=148 h=308, 직접 접근 우회선 y=116, 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, RULE

W, H = 1000, 532
CY = 282


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "CONTAINER SECURITY · 06-02 §5",
      "어드미션은 배포 직전에 막고 GitOps 는 직접 접근을 없앱니다",
      "사용자는 Git 에만 체크인하고 오퍼레이터가 클러스터를 고친다. 배포 요청은 어드미션 컨트롤러의 다섯 검사를 통과해야 컨테이너로 실행된다.",
      "스캔을 건너뛴 이미지를 가리키는 배포도 어드미션에서 멈춥니다.")


def zone(x, y, w, h, name):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#F5F5F308" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="6 5"/>')
    d.t(x + 16, y + 22, name, 12, MUTED, KR, "start", 600)


def node(x, y, w, h, title, sub, c=None, focal=False):
    fit(title, 14, w - 16)
    if sub:
        fit(sub, 12, w - 16)
    if c:
        d.tone(x, y, w, h, c, 6, "1F" if focal else "14", 1.4 if focal else 1.1)
    else:
        d.box(x, y, w, h, "#161B22", RULE, 1.0)
    ty = y + h / 2 - (4 if sub else -5)
    d.t(x + w / 2, ty, title, 14, c if c and not focal else INK, kr(title), "middle", 600)
    if sub:
        d.t(x + w / 2, y + h / 2 + 18, sub, 12, MUTED, kr(sub), "middle")


zone(212, 148, 180, 308, "소스 관리")
zone(440, 148, 536, 308, "클러스터")

# 직접 접근 우회선 — 사용자 위쪽에서 클러스터 존 위쪽으로, 점선
d.arrow([(86, 250), (86, 116), (704, 116), (704, 146)], BAD, "bad", 1.5, "6 5")
d.chip(396, 116, "직접 접근 (불필요)", BAD, 12)

# 흐름 화살표
d.arrow([(150, CY), (224, CY)], MUTED, "ar", 1.5)
d.t(186, CY - 10, "체크인", 12, MUTED, KR, "middle", 600)
d.arrow([(378, CY), (452, CY)], MUTED, "ar", 1.5)
d.t(414, CY - 10, "반영", 12, MUTED, KR, "middle", 600)
d.arrow([(594, CY), (628, CY)], MUTED, "ar", 1.5)
d.arrow([(818, CY), (852, CY)], OK, "ok", 1.5)
d.t(835, CY - 10, "통과", 12, OK, KR, "middle", 600)
d.arrow([(724, 364), (724, 392)], BAD, "bad", 1.5)
d.t(738, 382, "실패", 12, BAD, KR, "start", 600)

# 노드
node(24, 250, 124, 64, "사용자", "Git 접근만")
node(228, 250, 148, 64, "Git", "원하는 상태 코드")
node(456, 250, 136, 64, "오퍼레이터", "GitOps")
d.tone(632, 200, 184, 164, ACC, 6, "1F", 1.4)
d.t(724, 228, "어드미션 컨트롤러", 14, INK, KR, "middle", 600)
d.line(648, 240, 800, 240, ACC, 0.8)
for i, chk in enumerate(["스캔 여부", "신뢰 레지스트리", "서명", "승인", "root 실행 여부"]):
    d.t(652, 262 + i * 22, chk, 12, INK, kr(chk), "start")
node(856, 250, 104, 64, "컨테이너", "실행", OK)
node(632, 396, 184, 40, "실행 안 됨", None, BAD)

# 이점 칩
d.line(302, 314, 302, 344, SOFT, 1.0)
node(228, 344, 148, 36, "감사 추적", None, OK)
d.line(524, 314, 524, 344, SOFT, 1.0)
node(456, 344, 136, 36, "수정 권한 보유", None, OK)

d.legend(484, [("집행 지점", ACC), ("이점 · 통과", OK), ("차단 · 실패", BAD)])
d.save(str(ASSETS / "06-02.admission-gitops.svg"))
print("ok 06-02 admission-gitops")
