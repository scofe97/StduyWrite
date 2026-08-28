# 09-03 §3 — 키가 파일 이름이 된다
# configMap 볼륨과 "거의 같다"는 것이 본문의 전제라, 다른 점만 도드라져야 한다 —
# 볼륨 타입 이름, 참조 필드 이름, 그리고 tmpfs 에 놓인다는 것.
# 타입 스펙: type-architecture.md — Secret 경계 상자에서 secret 볼륨을 거쳐 컨테이너 경계 상자로 키가 파일이 되어 건너간다.
#           configMap 볼륨과 같은 골격이라 다른 점만 도드라지는 구성도다.
#           type-data-flow 는 역할 레인 1~4 × 단계 열 × 타입 있는 페이로드 칩이 입력 계약인
#           데이터 플랫폼 전용 타입이라 여기엔 맞지 않는다. type-architecture 의 Best for 에
#           "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 640, "KUBERNETES IN ACTION · 09-03",
      "키가 파일 이름이 되고, 값이 내용이 된다",
      "secret 볼륨은 configMap 볼륨과 붙이는 방법이 거의 같다. 볼륨 타입이 secret 이고 참조가 "
      "secretName 이라는 점, 그리고 파일이 메모리에 놓인다는 점만 다르다.",
      "kiada-tls Secret 의 인증서·개인 키를 envoy 에 파일로")

d.box(60, 176, 380, 216, PAPER, RULE, 0.9, 8)
d.t(250, 204, "Secret  kiada-tls", 11, SOFT, KR)
for i, (k, v) in enumerate((("tls.crt", "…인증서 바이트…"), ("tls.key", "…개인 키 바이트…"))):
    y = 254 + i * 66
    d.box(84, y - 24, 332, 52, PAPER2, INFO, 1.0, 5)
    d.t(104, y - 2, k, 12, INFO, MONO, "start", 600)
    d.t(104, y + 18, v, 10, MUTED, KR, "start")

d.o.append(f'<rect x="{610-140}" y="248" width="280" height="76" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(610, 278, "secret 볼륨", 13, ACC, KR, "middle", 600)
d.t(610, 302, "secretName: kiada-tls", 10, MUTED, MONO)
d.path("M 444 286 L 462 286", MUTED, 1.4, m="ar")

d.box(780, 176, 380, 216, PAPER, RULE, 0.9, 8)
d.t(970, 204, "envoy 컨테이너  /etc/certs", 11, SOFT, KR)
for i, (nm, mode) in enumerate((("tls.crt", "-rw-r--r--"), ("tls.key", "-rw-r-----"))):
    y = 254 + i * 66
    d.box(804, y - 24, 332, 52, PAPER2, OK, 1.0, 5)
    d.t(824, y - 2, nm, 12, OK, MONO, "start", 600)
    d.t(824, y + 18, mode, 10, MUTED, MONO, "start")
d.path("M 758 286 L 776 286", ACC, 1.4, m="acc")

ddx.focal_tag(d, 610, 424, "파일은 tmpfs — 메모리에 놓인다", 320)

d.t(24, 500, "configMap 볼륨과 다른 점은 셋이다 — 볼륨 타입이 secret, 참조 필드가 secretName, "
             "그리고 파일이 디스크가 아니라 메모리에 놓인다.", 11, MUTED, KR, "start")
d.t(24, 522, "그래서 노드가 꺼지면 남지 않는다. 다만 기본 권한은 0644 라, 개인 키처럼 좁혀야 하는 파일은 "
             "defaultMode 나 items 로 따로 지정한다.", 11, MUTED, KR, "start")
d.legend(552, [("Secret 의 엔트리", INFO), ("투영하는 볼륨", ACC), ("컨테이너의 파일", OK)])
d.save("09-03-secret-volume-projection.svg")
print("ok")
