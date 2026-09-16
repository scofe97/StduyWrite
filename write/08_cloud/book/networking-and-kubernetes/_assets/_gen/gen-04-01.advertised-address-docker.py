# 04-01.advertised-address-docker — 포트 매핑 뒤에서 광고 주소가 어긋나는 세 단계
# 본문 요구: "사람이 설정에 적어 준 주소로 붙은 1단계는 성공 … 2단계에서 브로커가 172.17.0.5 를
#           알려 주고 … 3단계에서 그 주소로 붙으면 타임아웃"
# 타입 스펙: type-sequence — 참여자 셋 사이의 시간순 메시지 세 개. 2번은 응답이라 점선.
#           손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다. k8s 짝과 골격은 _cc_04_01_advertise.py.
import _cc_04_01_advertise as cc

cc.draw("docker").save("04-01.advertised-address-docker.svg")
print("ok advertised-address-docker")
