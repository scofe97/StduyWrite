# 08-01 §8 Kiali 가 세는 단위.
# 본문(저자 정의 그대로): "A workload is a running binary that can be deployed as a set of identical
#       running replicas ... in Kubernetes, this would be the Pods part of a deployment."
#       "An application is a grouping of workloads and associated constructs like services and configuration."
# 예제 애플리케이션에서는 둘이 사실상 같아 차이가 드러나지 않는다. 그런데 화면의 메뉴가 이 두 단위로 갈려 있다.
# 타입 스펙: type-nested — 포함으로 표현하는 계층. 링 3(3~5), 안쪽으로 갈수록 획이 진해지고 채움이 짙어진다.
#           링 라벨은 왼쪽 위 종이색 마스크 위 mono eyebrow, coral 은 가장 안쪽 초점 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 1000, 620
d = D(W, H, "ISTIO IN ACTION · 08-01 §8",
      "Kiali 는 두 단위로 세고 화면도 그렇게 갈린다",
      "워크로드는 동일한 복제본으로 배포되는 바이너리 하나이고, 애플리케이션은 그런 워크로드들과 서비스·설정을 "
      "묶은 것이다. 예제에서는 둘이 사실상 같아 보이지만 왼쪽 메뉴가 이 두 단위로 나뉘어 있다.",
      "그래프의 노드도 이 단위 위에 놓입니다 — 무엇을 세는지가 무엇이 보이는지를 정합니다")

def ring(x, y, w, h, tag, sub, stroke, fill, focal=False):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{1.4 if focal else 1.0}"/>')
    tw = len(tag) * 6 + 16
    d.o.append(f'<rect x="{x + 20}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 28, y + 3, tag, 8, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 28, y + 30, sub, 11, ACC if focal else MUTED, KR, "start")

ring(84, 128, 828, 372, "NAMESPACE · ISTIOINACTION", "개요 화면이 세는 가장 바깥 단위", f"{INK}30", f"{INK}04")
ring(124, 184, 752, 280, "APPLICATION", "워크로드들 + 서비스 · 설정을 묶은 것", MUTED, f"{INK}07")
ring(164, 240, 672, 184, "WORKLOAD", "동일한 복제본으로 배포되는 바이너리 하나", ACC, f"{ACC}0E", focal=True)

# 워크로드의 내용물 — 디플로이먼트에 속한 파드들
for i in range(3):
    x = 232 + i * 232
    d.o.append(f'<rect x="{x}" y="{316}" width="200" height="60" rx="6" fill="{ACC}10" stroke="{ACC}66" stroke-width="1"/>')
    d.t(x + 100, 342, f"webapp-{i + 1}", 12, INK, KR, "middle", 600)
    d.t(x + 100, 362, "2/2 · app + istio-proxy", 9, MUTED, MONO)

d.t(28, 522, "저자의 예제에서는 애플리케이션과 워크로드가 사실상 같아 차이가 드러나지 않는다", 11, SOFT, KR, "start")
d.t(28, 544, "그럼에도 구분을 적어 두는 이유는 왼쪽 메뉴와 검증 대상이 이 단위 위에 놓이기 때문이다", 11, MUTED, KR, "start")
d.legend(572, [("저자가 정의로 못 박은 단위", ACC), ("그 위를 감싸는 단위", MUTED)])
d.save("08-01.kiali-units.svg")
