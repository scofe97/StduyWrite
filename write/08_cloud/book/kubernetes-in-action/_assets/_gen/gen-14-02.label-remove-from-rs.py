# 14-02 §4 — label 하나로 세트에서 빼낸다
# 14-01 의 '무시한다' 성질을 도구로 쓰는 장면이다. 전후를 나란히 놓아야 "빼는 순간 대체가
# 만들어진다"는 인과가 보인다. 조사 대상이 살아남는 것이 이 수의 목적이므로 그쪽이 focal.
# 타입 스펙: type-dp-security-matrix.md — 열이 바꾸기 전과 뒤 두 벌, 행이 파드. 뒤쪽에 한 줄이 늘어난 것이 판정이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 640, "KUBERNETES IN ACTION · 14-02",
      "label 을 바꾸면 세트에서 빠진다",
      "selector 에 맞는 파드 수를 컨트롤러가 늘 맞추므로, 문제 파드의 label 을 바꿔 selector 에서 빼면 "
      "컨트롤러가 대체 파드를 만든다. 문제 파드는 남아 있어 느긋하게 조사할 수 있다.",
      "kubectl label po kiada-78j7m rel=debug --overwrite")

def scene(x0, w, label, pods, note, note_c):
    ddx.band(d, 100, 452, label, x=x0, w=w)
    d.t(x0 + w / 2, 168, "selector: app=kiada, rel=stable", 10, SOFT, MONO)
    for i, (nm, lab, c, focal) in enumerate(pods):
        cy = 214 + i * 62
        if focal:
            d.o.append(f'<rect x="{x0+w/2-190}" y="{cy-24}" width="380" height="48" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x0 + w / 2 - 168, cy + 4, f"{nm}   {lab}", 11, ACC, MONO, "start")
        else:
            d.box(x0 + w / 2 - 190, cy - 24, 380, 48, PAPER2, c, 1.1, 6)
            d.t(x0 + w / 2 - 168, cy + 4, f"{nm}   {lab}", 11, c, MONO, "start")
    d.t(x0 + w / 2, 428, note, 11, note_c, KR)

scene(24, 570, "바꾸기 전 — 3 벌이 모두 세트 안", [
    ("kiada-78j7m", "rel=stable   1/2 Running", WARN, False),
    ("kiada-98lmx", "rel=stable   2/2 Running", OK, False),
    ("kiada-wk99p", "rel=stable   2/2 Running", OK, False),
], "컨테이너 하나가 죽었지만 개수는 3 이라 컨트롤러는 가만히 있다", WARN)

scene(626, 570, "바꾼 뒤 — 빠진 자리를 컨트롤러가 채운다", [
    ("kiada-78j7m", "rel=debug    selector 밖", None, True),
    ("kiada-98lmx", "rel=stable   2/2 Running", OK, False),
    ("kiada-wk99p", "rel=stable   2/2 Running", OK, False),
    ("kiada-xtxcl", "rel=stable   방금 만들어짐", INFO, False),
], "세트 안이 다시 3 벌 · 문제 파드는 살아서 남는다", ACC)

d.t(24, 504, "빼낸 파드는 더 이상 ReplicaSet 이 관리하지 않으므로, 조사가 끝나면 직접 지워야 한다. "
             "ownerReferences 에서도 ReplicaSet 참조가 제거된다.", 11, MUTED, KR, "start")
d.t(24, 526, "개수는 맞는데 서비스가 반쪽인 상태를 쿠버네티스가 스스로 알아채지 못하는 것이 왼쪽 장면이다 — "
             "그 공백은 availableReplicas 를 지켜보는 관측이 메운다.", 11, MUTED, KR, "start")
d.legend(556, [("정상 파드", OK), ("문제 파드", WARN), ("대체 파드", INFO), ("빼낸 파드", ACC)])
d.save("14-02-label-remove-from-rs.svg")
print("ok")
