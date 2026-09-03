# 13-01 §1 쿠버네티스와 VM 이 같은 여섯 항목을 각각 어떻게 처리하는가.
# 본문(원문 표 13.1): Installing proxy / Configuring proxy / Bootstrap workload identity /
#       Health checking / Registration / DNS resolution 여섯 행을 쿠버네티스 구현과 VM 구현으로 나눠 적는다.
#       쿠버네티스: 웹훅 또는 istioctl 로 주입 · 주입 때 함께 설정 · 토큰을 쿠버네티스 메커니즘이 주입 ·
#       준비성과 생존성을 쿠버네티스가 수행 · 등록은 쿠버네티스가 처리 · 클러스터 안 DNS 서버로 해석(DNS 프록시는 선택).
#       VM: 내려받아 손으로 설치 · WorkloadGroup 에서 istioctl 로 생성해 전송 · 토큰을 손으로 전송 ·
#       준비성은 WorkloadGroup 에 설정 · WorkloadGroup 멤버로 자동 등록 · DNS 프록시가 istiod 에게 설정받아 해석.
# 원문 13.1.3 이 이름 해석을 VM 편입의 "마지막 이정표" 라고 부르므로 그 칸을 accent 한다.
# 타입 스펙: type-swimlane — 같은 여섯 단계를 두 주체가 나눠 맡는 것이 논점이다.
#           레인마다 왼쪽 여백에 mono eyebrow, 레인 구분선 1px, accent 는 칸 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 520
d = D(W, H, "ISTIO IN ACTION · 13-01 §1",
      "오른쪽 여섯 칸이 모두 누군가의 일이 된다",
      "저자가 장을 닫으며 놓는 표를 그대로 옮겼다. 왼쪽은 대개 플랫폼의 이름이고 오른쪽은 전부 사람이나 "
      "새 리소스의 이름이다. 색이 붙은 칸이 저자가 마지막 이정표라 부른 자리다.",
      "이 장의 나머지는 오른쪽 레인의 여섯 칸을 하나씩 채우는 일입니다")

LABEL_W, LANE_H, LANE_Y0 = 140, 116, 128
HDR_Y = LANE_Y0 - 26
SLOT = (W - LABEL_W - 32) / 6
CW, CH = SLOT - 12, 72

stages = ["설치", "설정", "신원", "헬스", "등록", "이름"]
lanes = [("KUBERNETES", "플랫폼이 처리한다"), ("VIRTUAL MACHINE", "운영자와 새 리소스가 나눈다")]
cells = [
    [("웹훅 또는", "istioctl"), ("주입할 때", "함께"), ("쿠버네티스가", "파드에 주입"),
     ("쿠버네티스가", "준비성 · 생존성"), ("쿠버네티스가", "처리"), ("클러스터 안", "DNS 서버")],
    [("내려받아", "직접 설치"), ("WorkloadGroup", "에서 생성 · 전송"), ("토큰을", "손으로 옮긴다"),
     ("WorkloadGroup", "의 준비성만"), ("그룹 멤버로", "자동 등록"), ("사이드카의", "DNS 프록시")],
]
FOCAL = (1, 5)

def slot_x(j): return LABEL_W + j * SLOT + (SLOT - CW) / 2
def lane_top(k): return LANE_Y0 + k * LANE_H

for j, name in enumerate(stages):
    d.t(LABEL_W + j * SLOT + SLOT / 2, HDR_Y, name, 10, SOFT, MONO, "middle", 600)
for k, (name, sub) in enumerate(lanes):
    top = lane_top(k)
    d.line(0, top, W, top, RULE, 0.8)
    d.t(16, top + 48, name, 9, SOFT, MONO, "start", 600)
    d.t(16, top + 68, sub, 11, MUTED, KR, "start")
d.line(0, lane_top(2), W, lane_top(2), RULE, 0.8)
d.line(LABEL_W - 16, lane_top(0), LABEL_W - 16, lane_top(2), RULE, 1.0)

for k in range(2):
    for j in range(6):
        x, y = slot_x(j), lane_top(k) + 22
        focal = (k, j) == FOCAL
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        else:
            d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 6)
        a, b = cells[k][j]
        d.t(x + CW / 2, y + 30, a, 11, ACC if focal else INK, KR, "middle", 600)
        d.t(x + CW / 2, y + 50, b, 11, ACC if focal else MUTED, KR, "middle")

d.t(24, 400, "쿠버네티스에서도 같은 셋이 필요하다 — 프록시 설치 · istiod 에 붙는 설정 · 신원 토큰. 다만 플랫폼이 대신한다", 11, SOFT, KR, "start")
d.t(24, 424, "저자가 못 박는 문장 — 이 편의는 쿠버네티스 밖의 워크로드로 확장되지 않는다", 11, MUTED, KR, "start")
d.t(24, 448, "설치 한 줄만은 쿠버네티스에서도 istioctl 로 손수 주입하는 선택지가 웹훅과 나란히 적혀 있다", 11, SOFT, KR, "start")
d.legend(468, [("마지막 이정표", ACC), ("플랫폼이 대신하는 자리", MUTED)])
d.save("13-01.who-does-what.svg")
