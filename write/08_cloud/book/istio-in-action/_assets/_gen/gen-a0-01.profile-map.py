# a0-01 §3 프로파일 여덟이 갈리는 축.
# 본문(부록 A.2 의 코드 주석 여덟 개 그대로): default 는 운영 출발점, demo 는 시연용,
#       empty 는 전부 끔, external 은 컨트롤 플레인을 관리 대상 밖에, minimal 은 default 에서
#       인그레스 뺀 것, openshift 는 default + Istio CNI, preview 는 default + 실험 기능,
#       remote 는 현재 default 와 동일한 자리 표시자.
# 타입 스펙: type-tree — 넷이 default 를 부모로 두는 계보라 계층이 논점이다. 루트 하나에서
#           가지를 내리고 잎에 한 줄 설명을 단다.
#           축약: 계열이 아닌 셋은 위 행에 형제로 띄워 두어 아래 계보와 섞이지 않게 한다.
#           default 를 잎 넷의 가운데 위에 놓아야 버스가 다른 루트 밑을 지나지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 580
d = D(W, H, "ISTIO IN ACTION · A0-01 §3",
      "넷은 default 의 변주이고 셋은 따로 선다",
      "여덟 중 minimal · openshift · preview · remote 는 default 에서 한 가지만 바꾼 것이다. "
      "위 행의 셋은 그 계보 밖에 선다. 색이 붙은 것이 다음 절에서 쓰이는 프로파일이다.",
      "책 전체가 demo 로 돌아갔다는 사실을 저자가 여기서 못 박습니다")

BW, BH = 216, 64
def box(x, y, name, sub, focal=False, root=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif root:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{INK}0A" stroke="{INK}55" stroke-width="1.2"/>')
    else:
        d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, y + 26, name, 13, ACC if focal else INK, MONO, "start", 600)
    d.t(x + 16, y + 46, sub, 11, MUTED, KR, "start")

# 1 행 — 계보 밖에 서는 셋
SY = 128
box(32, SY, "demo", "시연용 · 자원을 끝까지 낮춘 것", root=True)
box(392, SY, "external", "컨트롤 플레인을 밖에 둘 때", root=True)
box(752, SY, "empty", "전부 끈다", focal=True)
d.t(860, SY + BH + 22, "다음 절이", 11, ACC, KR, "middle", 600)
d.t(860, SY + BH + 42, "쓰는 것", 11, ACC, KR, "middle", 600)

# 2 행 — 계열의 부모. 잎 넷의 가운데 위에 둔다.
RY = 252
box(392, RY, "default", "운영 배포의 출발점", root=True)

# 3 행 — default 의 잎 넷
LY = 372
LEAVES = [
    (32, "minimal", "인그레스 게이트웨이가 없다"),
    (264, "openshift", "Istio CNI 플러그인이 켜진다"),
    (496, "preview", "실험적 기능이 켜진다"),
    (728, "remote", "지금은 default 와 같다"),
]
for x, name, sub in LEAVES:
    d.box(x, LY, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, LY + 26, name, 13, INK, MONO, "start", 600)
    d.t(x + 16, LY + 46, sub, 11, MUTED, KR, "start")

# default 한 줄기가 내려와 버스에서 넷으로 갈라진다
BUS = 332
d.path(f"M 500 {RY + BH} L 500 {BUS}", MUTED, 1.3)
d.path(f"M 140 {BUS} L 836 {BUS}", MUTED, 1.3)
for x, _, _ in LEAVES:
    d.arrow([(x + BW / 2, BUS), (x + BW / 2, LY - 2)], MUTED, "ar", 1.3)
d.t(620, BUS - 6, "한 가지만 바꾼 변주", 11, SOFT, KR, "start")   # default 상자(392~608) 오른쪽으로

d.t(28, 464, "istioctl profile list 가 이 여덟을 내놓고, istioctl profile dump <이름> 이 그 정의를 그대로 편다", 11, INK, MONO, "start")
d.t(28, 488, "책 전체가 demo 로 돌아갔다 — 복제본이 하나씩인 것도 운영에서 다중 복제인 것도 여기서 나온다", 11, SOFT, KR, "start")
d.t(28, 512, "remote 는 원격 클러스터 설정이 갈라질 경우를 대비해 남겨 둔 자리 표시자다", 11, MUTED, KR, "start")
d.legend(536, [("다음 절이 쓰는 프로파일", ACC), ("계열의 부모와 계보 밖의 셋", MUTED)])
d.save("a0-01.profile-map.svg")
