# 타입 스펙: type-dp-security-matrix — 행 = 설치 방법 셋(Cilium CLI · Helm 직접 실행 · Helm + GitOps), 열 = 재현성·적용 주체·드리프트와 복구의 비교 행렬. 배정된 비교 타입 이름이 스펙 목록에 없어 비교 행렬 문법을 가진 이 타입으로 바꿨다. 셀 1개만 focal.
# 사실 출처: 추출본 cil16.txt 줄 40-62(CLI 대 Helm), 66-90(노트북·bastion), 94-166(Argo CD·Flux, 교착 경고)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W = 920
H = 444
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 200, 12, 204, 16
HDR_Y, HDR_H = 96, 52
ROW_Y0, ROW_H, STRIDE = 168, 56, 68
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(3)]

d = D(W, H, "CILIUM UP AND RUNNING · 16-01 §1", "설치 방법 세 가지의 재현성과 권한",
      "Helm 위에 GitOps 를 얹되 같은 클러스터를 관리하는 교착에 대비합니다",
      "누가 적용하고 값이 어디에 남는지로 세 방법을 가른다")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 24, "설치 방법", 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HDR_Y + 42, "method", 11, MUTED, MONO)
for j, (nm, code) in enumerate([("재현성", "repro"), ("적용 주체", "actor"), ("드리프트·복구", "drift")]):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 24, nm, 13, INK, KR, "middle", 600)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 42, code, 11, MUTED, MONO)

rows = [
    ("Cilium CLI", "cilium install", [
        ("명령형 실행", "값이 추상화됨", None),
        ("작업자 워크스테이션", "", None),
        ("GitOps 와 안 맞음", "선언형 흐름 밖", None)]),
    ("Helm 직접 실행", "노트북 · bastion", [
        ("값 관리 수단 없음", "업그레이드도 수동", None),
        ("cluster-admin", "~/.kube/config", WARN),
        ("값 파일 유실 위험", "데모에만 적합", None)]),
    ("Helm + GitOps", "Argo CD · Flux", [
        ("Git 이 단일 진실 원천", "커밋 메시지가 이유", OK),
        ("클러스터의 GitOps 도구", "클러스터 간 같은 값", OK),
        ("Git 과 자동 동기화", "교착 대비 복구 잡", "focal")]),
]

def fam(s): return KR if any("가" <= c <= "힣" for c in s) else MONO

for i, (name, hint, cells) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LP + 12, y + 24, name, 13, INK, fam(name), "start", 600)
    d.t(LP + 12, y + 44, hint, 12 if fam(hint) == KR else 11, MUTED, fam(hint), "start")
    for j, (val, sub, tone) in enumerate(cells):
        x = RX[j]
        if tone == "focal":
            d.tone(x, y, ROLE_W, ROW_H, ACC, r=4, op="14", sw=1.4)
        elif tone == OK:
            d.tone(x, y, ROLE_W, ROW_H, OK, r=4, op="10", sw=0.9)
        elif tone == WARN:
            d.tone(x, y, ROLE_W, ROW_H, WARN, r=4, op="10", sw=0.9)
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 0.7, r=4)
        col = ACC if tone == "focal" else (OK if tone == OK else (WARN if tone == WARN else INK))
        if sub:
            d.t(x + ROLE_W / 2, y + 24, val, 12, col, fam(val), "middle", 600)
            d.t(x + ROLE_W / 2, y + 44, sub, 12 if fam(sub) == KR else 11, MUTED, fam(sub))
        else:
            d.t(x + ROLE_W / 2, y + 34, val, 12, col, fam(val), "middle", 600)

LEG_Y = ROW_Y0 + 2 * STRIDE + ROW_H + 28
d.legend(LEG_Y, [("재현 가능한 원천", OK), ("넓은 권한", WARN), ("교착 대비 지점", ACC)])
d.save("16-01.install-tools-matrix.svg")
