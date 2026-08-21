# 16-03 §4 — 사용자가 만지는 것은 하나뿐이다
# 캡션의 마지막 절("사용자는 커스텀 오브젝트만 다룹니다")이 요점이라, 만들어지는 오브젝트를
# 나열하는 데서 그치면 안 되고 사용자 손이 닿는 경계가 그어져 있어야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 640, "KUBERNETES IN ACTION · 16-03",
      "사용자가 만지는 것은 하나뿐이다",
      "Operator 는 CRD 로 API 에 오브젝트 타입을 더하고, 그 타입의 인스턴스가 만들어지면 "
      "StatefulSet·Service·Secret 을 알아서 만들고 관리한다.",
      "MongoDB Operator · 앱을 만든 조직이 관리법을 안다")

ddx.node(d, 170, 232, "CustomResourceDefinition", "API 에 타입을 더한다", 260, 84, INFO)
d.o.append(f'<rect x="{500-140}" y="190" width="280" height="84" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(500, 220, "MongoDB 오브젝트", 13, ACC, KR, "middle", 600)
d.t(500, 244, "사용자가 만드는 것", 11, MUTED, KR)
d.path("M 302 232 L 354 232", MUTED, 1.5, m="ar")
d.t(328, 214, "타입이 생겨야", 10, SOFT, KR)

ddx.node(d, 830, 232, "Operator", "커스텀 컨트롤러", 220, 84, OK)
d.path("M 642 232 L 716 232", ACC, 1.5, m="acc")
d.t(679, 214, "감시한다", 10, ACC, KR)

d.box(60, 340, 1080, 152, PAPER, RULE, 0.9, 8)
d.t(600, 366, "Operator 가 만들고 관리하는 것 — 사용자는 건드리지 않는다", 11, SOFT, KR)
for i, (nm, s) in enumerate((("StatefulSet", "파드와 PVC"), ("Service", "headless · 신원"),
                             ("Secret", "자격 증명"))):
    ddx.node(d, 320 + i * 280, 434, nm, s, 240, 68, INFO)
    d.path(f"M 830 280 L {320 + i*280} 396", OK, 1.3, m="ok")

ddx.bracket(d, 40, 190, 276, "사용자 손이 닿는 곳", ACC)

d.t(24, 546, "StatefulSet 은 신원과 볼륨을 되돌려 주지만, 리플리카 셋 초기화나 노드 장애 시 강제 삭제 판단은 "
             "여전히 사람 몫이었다. Operator 는 그 도메인 지식을 코드로 옮긴다.", 11, MUTED, KR, "start")
d.t(24, 568, "쿠버네티스에 기본 포함되지 않아 별도 설치해야 하고, 보통 앱을 만든 조직이 개발한다.",
     11, MUTED, KR, "start")
d.legend(592, [("선언과 산출물", INFO), ("사용자가 만드는 것", ACC), ("자동화하는 주체", OK)])
d.save("16-03-operator-crd.svg")
print("ok")
