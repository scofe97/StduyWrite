# 12-01 §1 클러스터를 하나의 메시로 묶는 세 전제 — 원문 그림 12.1.
# 본문(원문 12.2): 교차 클러스터 워크로드 발견(컨트롤 플레인이 상대 클러스터의 워크로드를 발견해야 하며,
#       그러려면 상대 클러스터의 API 서버에 닿아야 한다), 교차 클러스터 연결성(워크로드끼리 연결이 서야 하고,
#       엔드포인트를 아는 것만으로는 쓸모가 없다), 클러스터 간 공통 신뢰(교차 클러스터 워크로드가 상호
#       인증할 수 있어야 Istio 의 보안 기능이 산다).
# 셋 다 채워야 성립하므로 교집합으로 그린다. 둘만 채운 자리에 무엇이 빠지는지가 이 그림의 요점이다.
# 타입 스펙: type-venn — 집합의 교집합이 논점이다. 원 셋, 라벨은 원 밖, 교집합 라벨은 겹침 안,
#           focal 은 교집합 한 곳, 중심·반지름은 4의 배수.
#           축약: 세 원의 중앙 교집합은 세 호로 둘러싸인 좁은 영역이라, 그 안에 완전히 들어가는 원을 하나
#           그려 focal 로 표시한다(반지름 40 < 영역의 내접 반지름 44). 없는 면적을 만들지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, KR, MONO

W, H = 1000, 720
d = D(W, H, "ISTIO IN ACTION · 12-01 §1",
      "셋을 다 채워야 하나의 메시가 된다",
      "저자가 든 전제 셋을 집합으로 놓았다. 둘만 채운 자리에는 각각 다른 것이 빠지고, 색이 붙은 "
      "가운데에서만 메시가 성립한다. 셋은 순서가 아니라 조건이다.",
      "엔드포인트를 아는 것만으로는 쓸모가 없다는 저자의 문장이 이 그림의 출발점입니다")

AX, AY = 500, 268
BX, BY = 412, 424
CX, CY = 588, 424
R = 148
GX, GY = 500, 372

for cx, cy, col in ((AX, AY, MUTED), (BX, BY, SOFT), (CX, CY, INK)):
    d.o.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{col}0A" stroke="{col}" stroke-width="1"/>')
d.o.append(f'<circle cx="{GX}" cy="{GY}" r="40" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
d.t(GX, GY + 4, "메시 성립", 11, ACC, KR, "middle", 600)

d.t(AX, 100, "CROSS-CLUSTER DISCOVERY", 8, SOFT, MONO, "middle")
d.t(AX, 118, "워크로드 발견", 14, MUTED, KR, "middle", 600)
d.t(244, 452, "워크로드 연결성", 14, SOFT, KR, "middle", 600)
d.path("M 244 464 L 244 512 L 320 512", SOFT, 0.8, m="soft")
d.t(756, 452, "공통 신뢰", 14, INK, KR, "middle", 600)
d.path("M 756 464 L 756 512 L 680 512", INK, 0.8, m="ar")

d.t(AX, 180, "상대의 API 서버를 읽는다", 11, MUTED, KR, "middle")
d.t(AX, 200, "서비스와 엔드포인트", 11, MUTED, MONO, "middle")
d.t(332, 470, "IP 로 닿는다", 11, SOFT, KR, "middle")
d.t(332, 490, "또는 동서 게이트웨이", 11, SOFT, KR, "middle")
d.t(668, 470, "같은 뿌리의 인증서", 11, INK, KR, "middle")
d.t(668, 490, "상호 인증이 선다", 11, INK, KR, "middle")

d.t(392, 328, "알고 닿지만", 11, MUTED, KR, "middle")
d.t(392, 346, "서로를 못 믿는다", 11, MUTED, KR, "middle")
d.t(608, 328, "알고 믿지만", 11, MUTED, KR, "middle")
d.t(608, 346, "닿지 못한다", 11, MUTED, KR, "middle")
d.t(500, 468, "닿고 믿지만", 11, MUTED, KR, "middle")
d.t(500, 486, "있는 줄 모른다", 11, MUTED, KR, "middle")

d.t(28, 604, "저자가 못 박는 문장 — 워크로드 엔드포인트를 아는 것은 그리로 연결을 걸 수 없으면 쓸모가 없다", 11, SOFT, KR, "start")
d.t(28, 628, "셋을 채우는 일은 대부분 istioctl 이 자동화한다 — 어려운 것은 조직이 그 권한을 허용하느냐다", 11, MUTED, KR, "start")
d.legend(652, [("셋이 모두 채워진 자리", ACC), ("하나가 빠진 자리", MUTED)])
d.save("12-01.three-preconditions.svg")
