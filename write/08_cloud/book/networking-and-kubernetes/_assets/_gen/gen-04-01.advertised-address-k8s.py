# 04-01.advertised-address-k8s — IP-per-Pod 에서는 같은 세 단계가 전부 성공한다
# 본문 요구: "같은 세 단계인데 결과가 전부 성공 … 1단계가 쓴 주소와 2단계가 말한 주소가 같은 값"
# 타입 스펙: type-sequence — docker 짝과 같은 레인·stride. 갈리는 값은 노드 레인의 주소 교체 여부 하나.
#           손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다. 골격은 _cc_04_01_advertise.py.
import _cc_04_01_advertise as cc

cc.draw("k8s").save("04-01.advertised-address-k8s.svg")
print("ok advertised-address-k8s")
