# 07-01 §3 — 요청은 단계마다 이벤트를 만들고, 정책에서 첫 번째로 맞는 규칙이 수준을 정하며, 수준에 따라 로그에 남는 내용이 늘어난다.
# 본문 근거: 이 노트 ### 3 「감사 로그로 접근 기록하기」.
# 검증 근거: kind v1.35.0 에서 정답 3 의 정책으로 ConfigMap·Secret 은 Metadata(본문 없음), Service 는 Request(요청 본문만), 파드는 RequestResponse(요청·응답 본문)로 남고
#            nodes·namespaces 요청은 이벤트가 없으며 RequestReceived 이벤트도 없음. 128개 이벤트의 단계는 ResponseStarted 와 ResponseComplete 뿐.
# 공식 근거: kubernetes.io 감사 문서의 Audit policy·Audit backends 절, apiserver-audit.v1 의 Policy.
# 타입 스펙: type-swimlane — 처리 흐름 레인과 수준별 내용 레인.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "CKS STUDY GUIDE · 07-01 §3",
      "요청이 단계와 정책을 거쳐 감사 로그에 남는 길과 수준별 내용",
      "위 레인은 API 요청이 단계별 이벤트가 되고 정책의 첫 일치 규칙이 수준을 정해 로그 백엔드나 웹훅 백엔드로 가는 흐름이고, "
      "아래 레인은 None 에서 RequestResponse 로 갈수록 이벤트에 메타데이터, 요청 본문, 응답 본문이 차례로 더해지는 흐름이다.",
      "첫 번째로 맞는 규칙이 수준을 정하고, 수준이 높을수록 로그에 남는 내용이 늘어납니다")

BW, BH, PITCH, X0 = 190, 76, 212, 24
LANE_X, LANE_W, LANE_H = 12, 856, 132
A_Y, S_Y = 96, 244


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def lane_steps(y, items):
    by = y + 40
    for i, (title, sub, c) in enumerate(items):
        x = X0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
        d.t(x + BW / 2, by + 32, title, 13, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 11, MUTED, MONO)
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "요청이 기록되기까지")
lane_steps(A_Y, [
    ("API 요청", "kubectl create configmap", INFO),
    ("단계별 이벤트", "omitStages: RequestReceived", INFO),
    ("정책의 첫 일치 규칙", "level 이 정해짐", ACC),
    ("백엔드", "log 파일 · webhook", SOFT),
])
lane(S_Y, "수준이 로그에 더하는 내용")
lane_steps(S_Y, [
    ("None", "기록 없음", SOFT),
    ("Metadata", "사용자 · 동사 · 리소스", INFO),
    ("Request", "+ 요청 본문", WARN),
    ("RequestResponse", "+ 응답 본문", BAD),
])

d.legend(392, [("요청과 기록", INFO), ("수준이 정해지는 자리", ACC), ("본문이 더해지는 수준", WARN), ("응답 본문까지", BAD), ("결과", SOFT)])
d.save("07-01.audit-level-path.svg")
