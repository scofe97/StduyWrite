# a0-03 §7 검증된 것이 쌓이고 그것으로 판정한다.
# 본문(부록 C.3, C.3.2): JWT 인증 필터가 클레임을 뽑아 filter metadata 에 넣고, PeerAuthentication
#       필터가 피어 신원을 뽑아 넣으며, 인가 필터가 그것을 읽어 판정한다. 인가 필터의 순서는
#       커스텀 -> 거부 -> 허용 -> catch-all.
# 타입 스펙: type-data-flow — 데이터가 단계를 지나며 쌓이고 마지막에 소비되는 것이 논점이다.
#           흐름 칸과 그 사이에 쌓이는 저장소를 함께 그린다.
#           축약: 인가 필터 넷은 한 칸 안에 순서대로 적어 흐름 칸 수를 늘리지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 620
d = D(W, H, "ISTIO IN ACTION · A0-03 §7",
      "인가 필터는 아무것도 검증하지 않는다",
      "앞선 두 필터가 검증해 남긴 것만 인가 필터가 읽는다. 그래서 정책이 맞아도 메타데이터가 비면 "
      "걸릴 근거가 없다. 색이 붙은 저장소가 요청 신원이 쌓이는 자리다.",
      "인가가 기대대로 안 걸리면 정책보다 이 저장소를 먼저 봅니다")

BW, BH, BY = 268, 72, 148
def stage(x, label, sub):
    d.box(x, BY, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + BW / 2, BY + 30, label, 12, INK, KR, "middle", 600)
    d.t(x + BW / 2, BY + 52, sub, 11, MUTED, MONO, "middle")

stage(28, "JWT 인증 필터", "jwt_authn")
stage(364, "PeerAuthentication 필터", "peer authn")
d.arrow([(296, BY + BH / 2), (360, BY + BH / 2)], MUTED, "ar", 1.4)

# 쌓이는 저장소
SY = 300
d.o.append(f'<rect x="28" y="{SY}" width="604" height="140" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(48, SY + 26, "filter metadata", 13, ACC, MONO, "start", 600)
META = [
    ("Principal", "워크로드 신원", "PeerAuthentication"),
    ("Namespace", "워크로드 네임스페이스", "PeerAuthentication"),
    ("Request principal", "최종 사용자 주체", "RequestAuthentication"),
    ("Request auth claims", "최종 사용자 클레임", "RequestAuthentication"),
]
for i, (k, what, who) in enumerate(META):
    y = SY + 52 + i * 22
    d.t(48, y, k, 11, INK, MONO, "start", 600)
    d.t(216, y, what, 11, MUTED, KR, "start")
    d.t(400, y, who, 11, SOFT, MONO, "start")

for x in (162, 498):
    d.arrow([(x, BY + BH), (x, SY - 2)], ACC, "acc", 1.4)
d.t(180, 250, "뽑아서 넣는다", 11, ACC, KR, "start", 600)

# 소비하는 쪽
AX = 692
d.o.append(f'<rect x="{AX}" y="{BY}" width="280" height="292" rx="6" '
           f'fill="{INFO}12" stroke="{INFO}" stroke-width="1.2"/>')
d.t(AX + 20, BY + 28, "인가 필터", 13, INFO, KR, "start", 600)
d.t(AX + 20, BY + 50, "읽기만 한다", 11, MUTED, KR, "start")
ORDER = ["1. 커스텀", "2. 거부", "3. 허용", "4. catch-all"]
for i, o in enumerate(ORDER):
    y = BY + 92 + i * 44
    d.box(AX + 20, y, 240, 34, PAPER2, RULE, 1.0, 4)
    d.t(AX + 36, y + 22, o, 12, INK, KR, "start", 600)
    if i < len(ORDER) - 1:
        d.arrow([(AX + 140, y + 34), (AX + 140, y + 42)], MUTED, "ar", 1.2)
# 꺾어 두면 세로 구간이 라벨을 관통한다. 두 상자의 y 가 겹치므로 직선으로 잇는다.
d.path(f"M 632 {SY + 70} L {AX - 2} {SY + 70}", INFO, 1.4, m="info")
d.t(636, SY + 54, "읽는다", 11, INFO, KR, "start", 600)

d.t(28, 484, "catch-all 은 앞의 어느 필터도 요청을 처리하지 않았을 때만 실행된다 — 9 장 §5 의 평가 순서와 같은 것이다", 11, SOFT, KR, "start")
d.t(28, 508, "메타데이터를 보려면 로거 레벨을 올린다 — istioctl proxy-config log ... --level rbac:debug", 11, MUTED, MONO, "start")
d.legend(532, [("요청 신원이 쌓이는 자리", ACC), ("그것을 읽기만 하는 쪽", INFO)])
d.save("a0-03.filter-metadata.svg")
