# 타입 스펙: type-dp-security-matrix — 배정된 comparison 타입이 스펙 목록에 없어 4가지 Ingress 한계와 결과·대응을 행렬로 비교하는 type-dp-security-matrix 로 전환. 셀 1개 focal.
# 사실 출처: Cilium Up and Running 7장 cil7.txt 줄 514-554(Single shared configuration role, Poor multitenancy support, Nonportable annotations, Hard to extend)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 430
d = D(W, H, "CILIUM UP AND RUNNING · 07-01 §4", "Ingress 의 4가지 한계와 Gateway API 대응",
      "표현력과 역할 분리의 태생적 한계로 인해 비표준 어노테이션 누더기가 발생한다",
      "Ingress 의 구조적 제약은 표준화된 Gateway API 로 해결한다")

LP = 16
C1_W, C2_W, C3_W, C4_W = 170, 224, 230, 240
GAP = 10
X1 = LP
X2 = X1 + C1_W + GAP
X3 = X2 + C2_W + GAP
X4 = X3 + C3_W + GAP

HDR_Y, HDR_H = 100, 46

headers = [
    (X1, C1_W, "한계 항목", "limitation"),
    (X2, C2_W, "원인 구조", "cause"),
    (X3, C3_W, "운영상 결과", "impact"),
    (X4, C4_W, "Gateway API 대응", "solution")
]

for x, w, nm, sub in headers:
    d.box(x, HDR_Y, w, HDR_H, PAPER2, SOFT, 1.0)
    d.t(x + w / 2, HDR_Y + 20, nm, 12, INK, KR, "middle", 600)
    d.t(x + w / 2, HDR_Y + 36, sub, 11, MUTED, MONO)

rows = [
    ("단일 설정 역할", "공유 컨트롤러", [
        ("클러스터 전역 단일 감시", "역할 위임 불가능", None),
        ("플랫폼 엔지니어 병목", "전체 라우팅 승인 필요", WARN),
        ("GatewayClass / Gateway 분리", "역할 기반 리소스 계층화", OK)
    ]),
    ("멀티테넌시 부재", "격리 범위 없음", [
        ("네임스페이스 경계 제어 결여", "자체 격리 장치 부재", None),
        ("팀 간 설정 충돌 위험", "공유 클러스터 위험", WARN),
        ("네임스페이스 첨부 제어", "안전한 셀프 서비스 허용", OK)
    ]),
    ("비표준 어노테이션", "벤더 종속", [
        ("기능 확장을 주석에 의존", "구현체별 문법 파편화", None),
        ("컨트롤러 교체 시 파손", "이식성 상실 및 락인", BAD),
        ("표준 필드 및 확장 필터", "규격화된 코어 API 제공", OK)
    ]),
    ("확장성 한계", "기본 HTTP 국한", [
        ("단순 호스트·경로 매칭", "L7 세부 제어 불가", None),
        ("트래픽 분할·가중치 불가", "어노테이션 누더기화", "focal"),
        ("HTTPRoute · 가중치 99/1", "헤더 제어 · gRPC 지원", OK)
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

d.save("07-01.ingress-limitations.svg")
