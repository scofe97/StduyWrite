# 03-01 §1 — API 서버는 요청을 인증 → 인가 → 어드미션 순서로 거르고, 단계마다 거절 자리가 따로 있다.
# 본문 근거: 이 노트 §1 「API 서버는 요청을 인증, 인가, 어드미션 컨트롤 순서로 거릅니다」.
# 공식 근거: kubernetes.io/docs/concepts/security/controlling-access/ — 인증 실패 401, 인가 거부 403,
#            어드미션은 쓰기·연결 요청에만 적용되고 컨트롤러 하나의 거절로 즉시 중단, 통과 후 검증과 저장.
#            익명 신원은 kubernetes.io/docs/reference/access-authn-authz/authentication/ (system:anonymous).
# 타입 스펙: type-flowchart — 단계마다 통과/거절로 갈리는 순차 절차가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 392
d = D(W, H, "CKS STUDY GUIDE · 03-01 §1",
      "요청이 거치는 세 관문",
      "클라이언트 요청이 kube-apiserver 에서 인증, 인가, 어드미션 컨트롤을 차례로 통과해 검증을 거친 뒤 etcd 에 저장되는 순서와 "
      "각 관문에서 거절될 때의 결과를 그린 흐름도다.",
      "어느 관문에서 막혀도 요청은 저장소에 닿지 못합니다")

BW, BH, GAP, X0, Y0 = 140, 92, 30, 30, 110


def stage(i, title, subs, c=INK, tone=None):
    x = X0 + i * (BW + GAP)
    if tone:
        d.tone(x, Y0, BW, BH, tone, 8, "12", 1.4)
    else:
        d.box(x, Y0, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(x + BW / 2, Y0 + 30, title, 15, c, KR, "middle", 600)
    for j, (txt, fam) in enumerate(subs):
        d.t(x + BW / 2, Y0 + 54 + j * 18, txt, 12, MUTED, fam)
    return x


xs = [
    stage(0, "클라이언트 요청", [("TLS 연결", KR), ("기본 포트 6443", MONO)], INFO),
    stage(1, "1 인증", [("인증기 순차 시도", KR), ("system:anonymous", MONO)], ACC, ACC),
    stage(2, "2 인가", [("RBAC 등 모듈", KR), ("하나라도 허용", KR)], ACC, ACC),
    stage(3, "3 어드미션", [("쓰기·연결 요청", KR), ("읽기 요청은 제외", KR)], ACC, ACC),
    stage(4, "검증 후 저장", [("etcd", MONO), ("오브젝트 기록", KR)], OK),
]

for i in range(4):
    xa = xs[i] + BW
    d.path(f"M {xa} {Y0 + BH / 2} L {xa + GAP - 2} {Y0 + BH / 2}", MUTED, 1.5, m="ar")

# 거절 자리 — 인증·인가·어드미션 아래
RY, RH = 250, 74


def reject(i, code, sub):
    x = xs[i]
    d.arrow([(x + BW / 2, Y0 + BH), (x + BW / 2, RY - 2)], BAD, "bad", 1.4)
    d.tone(x, RY, BW, RH, BAD, 8, "12", 1.2)
    d.t(x + BW / 2, RY + 30, code, 12 if code[0].isdigit() else 14, BAD, MONO if code[0].isdigit() else KR, "middle", 600)
    d.t(x + BW / 2, RY + 54, sub, 12, MUTED)


reject(1, "401 Unauthorized", "잘못된 자격 증명")
reject(2, "403 Forbidden", "모든 모듈 거부")
reject(3, "즉시 거절", "컨트롤러 하나의 거부")

d.legend(352, [("요청이 거치는 관문", ACC), ("거절", BAD), ("저장", OK), ("진입", INFO)])
d.save("03-01.request-stages.svg")
