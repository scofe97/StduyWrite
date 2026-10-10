# 타입 스펙: type-dp-security-matrix — 배정된 comparison 타입이 스펙 목록에 없어 암호화 전·후 tcpdump 관측 항목을 비교하는 type-dp-security-matrix 로 전환. 셀 1개 focal.
# 사실 출처: Cilium Up and Running 14장 cil14.txt 줄 339-420(비암호화 캡처), 421-487(암호화 캡처), 495-528(hostNetwork) / docs.cilium.io v1.20 security/network/encryption-wireguard/
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 436
d = D(W, H, "CILIUM UP AND RUNNING · 14-01 §5", "암호화 설정 전·후 패킷 캡처 비교",
      "WireGuard 활성화 시 애플리케이션 평문과 Pod IP 가 UDP 51871 암호문으로 은폐된다",
      "WireGuard 활성화 시 애플리케이션 평문과 Pod IP 가 UDP 51871 암호문으로 은폐된다")

LP = 16
C1_W, C2_W, C3_W, C4_W = 170, 224, 230, 240
GAP = 10
X1 = LP
X2 = X1 + C1_W + GAP
X3 = X2 + C2_W + GAP
X4 = X3 + C3_W + GAP

HDR_Y, HDR_H = 100, 46

headers = [
    (X1, C1_W, "관측 항목", "field"),
    (X2, C2_W, "암호화 해제 (false)", "unencrypted"),
    (X3, C3_W, "WireGuard 암호화 (true)", "wireguard"),
    (X4, C4_W, "감청자 관측 결과", "visibility")
]

for x, w, nm, sub in headers:
    d.box(x, HDR_Y, w, HDR_H, PAPER2, SOFT, 1.0)
    d.t(x + w / 2, HDR_Y + 20, nm, 12, INK, KR, "middle", 600)
    d.t(x + w / 2, HDR_Y + 36, sub, 11, MUTED, MONO)

rows = [
    ("Bearer 토큰", "HTTP 인증 헤더", [
        ("MYSECRETTOKEN 노출", "grep Bearer 로 즉시 검출", BAD),
        ("바이트 스트림 은폐", "UDP 51871 암호 페이로드", "focal"),
        ("평문 토큰 미관측", "캡처에서 Bearer 문자열 사라짐", OK)
    ]),
    ("애플리케이션 본문", "HTTP 요청·응답", [
        ("HTTP/1.1 200 OK 평문", "텍스트 본문 그대로 노출", BAD),
        ("ChaCha20-Poly1305 암호화", "0x0000 덤프만 관측", OK),
        ("데이터 기밀성 유지", "복호화 키 없이 판독 불가", OK)
    ]),
    ("Pod 통신 식별", "L3 IP 주소", [
        ("출발·도착 Pod IP 노출", "Pod IP 가 그대로 보임", BAD),
        ("WireGuard 헤더로 은폐", "노드 IP 10.89.0.x 만 관측", OK),
        ("서비스 토폴로지 은폐", "어느 Pod 간 통신인지 불명", OK)
    ]),
    ("호스트 네임스페이스", "hostNetwork 트래픽", [
        ("평문 통신 유지", "노드 프로세스 트래픽", WARN),
        ("WireGuard 터널 미적용", "Pod-노드 구간 암호화 제외", WARN),
        ("예외 구간 노출 주의", "L7 보안·정책 검토", WARN)
    ])
]

ROW_Y0, ROW_H, STRIDE = 158, 58, 66

for i, (name, hint, cells) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(X1, y, C1_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(X1 + C1_W / 2, y + 24, name, 12, INK, KR, "middle", 600)
    d.t(X1 + C1_W / 2, y + 44, hint, 12, MUTED, KR)

    for j, (val, sub, tone) in enumerate(cells):
        x, w = [X2, X3, X4][j], [C2_W, C3_W, C4_W][j]
        if tone == "focal":
            d.tone(x, y, w, ROW_H, ACC, r=4, op="14", sw=1.4)
            col = ACC
        elif tone == BAD:
            d.tone(x, y, w, ROW_H, BAD, r=4, op="12", sw=1.1)
            col = BAD
        elif tone == WARN:
            d.tone(x, y, w, ROW_H, WARN, r=4, op="10", sw=1.0)
            col = WARN
        elif tone == OK:
            d.tone(x, y, w, ROW_H, OK, r=4, op="10", sw=1.0)
            col = OK
        else:
            d.box(x, y, w, ROW_H, PAPER2, RULE, 0.7, r=4)
            col = INK

        d.t(x + w / 2, y + 24, val, 12, col, KR, "middle", 600)
        d.t(x + w / 2, y + 44, sub, 12, MUTED, KR)

d.save("14-01.testing-viewing.svg")
