# 타입 스펙: type-data-flow — 이미지가 개발자 데스크톱 → 빌드 직후 → 레지스트리 → 어드미션 컨트롤 네 지점을 지나며 지점마다 잡는 것과 막다른 길(빌드 실패 · 배포 거부)이 다르다. 취약점이 나오면 개발자가 이미지를 재빌드해 왼쪽으로 되돌아간다. focal 은 빌드 직후 게이트.
# 사실 출처: 노트 L174(이른 시점에 걷어내는 편이 빠르고 쌈), L182~L184(이미지마다 의존성 · 개발자가 재빌드 · 보안팀 수작업 불필요), L186~L197(네 지점 표 · 빌드 실패 · 24시간 재스캔), L201(스캔 통과 이미지만 배포), L295(하나만 고르면 빌드 직후), L180(전통 방식은 보안팀이 호스트 패키지를 갱신, 파이프라인 한참 오른쪽).
# Layout conventions: 카드 폭 200 · 칸 사이 36(x=28·264·500·736), 카드 h=148 · 결과 상자 h=48. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, RULE

W, H = 960, 536
X = [28, 264, 500, 736]
CW = 200


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "CONTAINER SECURITY · 07-01 §5",
      "스캔은 빌드 직후 게이트부터 걸고, 걸린 취약점은 개발자가 재빌드해 고칩니다",
      "이미지가 개발자 데스크톱, 빌드 직후, 레지스트리, 어드미션 컨트롤 네 지점을 지나며 각 지점에서 스캔한다. "
      "빌드 직후에는 심각도가 기준을 넘으면 빌드가 실패하고, 어드미션 컨트롤은 스캔 안 된 이미지의 배포를 거부한다. "
      "취약점이 나오면 개발자가 패치된 버전으로 이미지를 다시 빌드한다.",
      "왼쪽에서 걷어낼수록 수정이 빠르고 쌉니다.")

# 위쪽 축 — 코드 작성에서 운영 배포로
AY = 112
d.arrow([(28, AY), (932, AY)], SOFT, "soft", 1.3)
d.t(28, 96, "코드 작성", 13, INK, KR, "start", 600)
d.t(932, 96, "운영 배포", 13, INK, KR, "end", 600)
d.chip(480, AY, "늦을수록 수정 비용 증가", MUTED, 12)
d.chip(176, AY, "컨테이너: 개발자 재빌드", OK, 12)
d.chip(820, AY, "전통: 보안팀 수작업", MUTED, 12)

CY, CH = 136, 148
STAGES = [
    ("개발자 데스크톱", "로컬 빌드를 직접 스캔", "푸시하기 전에", "스스로 고칠 기회", False),
    ("빌드 직후", "이미지 빌드 직후 스캔 단계", "심각도가 기준을 넘으면", "빌드를 실패시킴", True),
    ("레지스트리", "푸시된 이미지 재스캔", "재빌드 없이 묵은 이미지의", "새 취약점 (24시간 주기)", False),
    ("어드미션 컨트롤", "스캔 통과 이미지만 배포", "이 검사가 없으면", "스캐너 우회가 쉬움", False),
]
for j, (name, act, r1, r2, focal) in enumerate(STAGES):
    x = X[j]
    fit(name, 14, CW - 24)
    fit(act, 12, CW - 24)
    fit(r1, 12, CW - 24)
    fit(r2, 12, CW - 24)
    if focal:
        d.tone(x, CY, CW, CH, ACC, 6, "1F", 1.4)
    else:
        d.box(x, CY, CW, CH, "#161B22", RULE, 1.0)
    d.t(x + 16, CY + 30, name, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, CY + 54, act, 12, MUTED, kr(act), "start")
    d.line(x + 16, CY + 72, x + CW - 16, CY + 72, RULE, 0.8)
    d.t(x + 16, CY + 98, r1, 12, MUTED, kr(r1), "start")
    d.t(x + 16, CY + 120, r2, 12, INK, kr(r2), "start", 600)
    if j < 3:
        d.arrow([(x + CW + 2, CY + 52), (X[j + 1] - 4, CY + 52)], SOFT, "soft", 1.3)

# 지점마다의 결과
OY, OH = 316, 48
OUTS = [
    ("소스 저장소에 푸시", None, INFO),
    ("빌드 실패", "배포 자체를 막음", BAD),
    ("새 취약점 발견", "정기 재스캔", WARN),
    ("배포 거부", "스캔 안 된 이미지", BAD),
]
for j, (t1, t2, c) in enumerate(OUTS):
    x = X[j]
    fit(t1, 13, CW - 24)
    d.tone(x, OY, CW, OH, c, 6, "14", 1.1)
    d.arrow([(x + CW / 2, CY + CH + 2), (x + CW / 2, OY - 4)], c, {INFO: "info", BAD: "bad", WARN: "warn"}[c], 1.4)
    if t2:
        fit(t2, 12, CW - 24)
        d.t(x + CW / 2, OY + 20, t1, 13, c, kr(t1), "middle", 600)
        d.t(x + CW / 2, OY + 38, t2, 12, MUTED, kr(t2), "middle")
    else:
        d.t(x + CW / 2, OY + 29, t1, 13, c, kr(t1), "middle", 600)

# 재빌드 띠 — 막힌 세 곳에서 내려와 왼쪽 끝으로 되돌아간다
BY = 404
d.tone(28, BY, 908, 48, OK, 6, "12", 1.1)
d.t(480, BY + 30, "취약점 발견 → 개발자가 의존성을 올려 이미지 재빌드", 14, OK, KR, "middle", 600)
for j in (1, 2, 3):
    d.arrow([(X[j] + CW / 2, OY + OH + 2), (X[j] + CW / 2, BY - 4)], MUTED, "ar", 1.3)
d.arrow([(28, BY + 24), (12, BY + 24), (12, CY + 74), (24, CY + 74)], OK, "ok", 1.4)

d.legend(476, [("소스 푸시", INFO), ("차단", BAD), ("재스캔 결과", WARN), ("재빌드", OK), ("빌드 직후 게이트", ACC)])
d.save(str(ASSETS / "07-01.shift-left-pipeline.svg"))
print("ok 07-01 shift-left-pipeline")
