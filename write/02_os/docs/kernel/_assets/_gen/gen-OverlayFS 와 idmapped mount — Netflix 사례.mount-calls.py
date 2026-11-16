# 컨테이너 하나가 뜰 때 마운트 호출이 몇 번 쌓이는가 — 기존 방식과 containerd PR #12092 이후.
# 값이 단계마다 움직인다: 101 → 202 → 20,200, 그리고 5,000 → 100.
# 타입 스펙: type-flowchart — 왼쪽에서 오른쪽으로 흐르는 두 줄(기존·변경 후), 줄마다 값이 불어나거나 줄어든다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, PAPER2, RULE, KR, MONO

W, H = 880, 520
d = D(W, H, "OVERLAYFS · IDMAPPED MOUNT",
      "컨테이너 하나가 뜰 때 쌓이는 마운트 호출",
      "레이어 50개 이미지로 컨테이너 100개를 띄울 때, 기존 방식은 호출이 101회에서 202회, 20,200회로 불어난다. "
      "containerd PR 12092 는 부모 디렉터리를 한 번만 idmap 해서 레이어 수와 호출 수를 떼어 놓는다.",
      lead="호출 수는 레이어 수 곱하기 컨테이너 수로 자란다")

BX = [40, 332, 624]; BW = 216; BH = 64

# ---- 기존: 레이어마다 ----
d.t(40, 112, "기존 — 레이어마다 idmap", 14, BAD, KR, "start", 600)
top = [("idmapped bind mount", "× 50  레이어마다 1번"),
       ("overlay mount", "× 1  lowerdir 50개 병합"),
       ("umount", "× 50  임시 마운트 정리")]
for (x, (a, b)) in zip(BX, top):
    d.box(x, 128, BW, BH, PAPER2, RULE, 0.9, 6)
    d.t(x + 16, 154, a, 13, INK, MONO, "start", 600)
    d.t(x + 16, 176, b, 12, MUTED, KR, "start")
for i in range(2):
    d.arrow([(BX[i] + BW, 160), (BX[i + 1] - 4, 160)], MUTED, "ar", 1.3)

vals = [("101회", "컨테이너 1개, 1번 실행", False),
        ("202회", "× 2  containerd 가 두 번 수행", False),
        ("20,200회", "× 100  컨테이너 동시 기동", True)]
for (x, (n, s, focal)) in zip(BX, vals):
    if focal:
        d.tone(x, 236, BW, BH, ACC, 6)
    else:
        d.box(x, 236, BW, BH, PAPER2, RULE, 0.9, 6)
    d.t(x + 16, 262, n, 16, ACC if focal else INK, MONO, "start", 600)
    d.t(x + 16, 284, s, 12, MUTED, KR, "start")
for i in range(2):
    d.arrow([(BX[i] + BW, 268), (BX[i + 1] - 4, 268)], MUTED, "ar", 1.3)
for x in BX:
    d.arrow([(x + BW / 2, 192), (x + BW / 2, 232)], SOFT, "soft", 1.0, "3 3")

# ---- 변경 후: 부모 디렉터리 한 번 ----
d.line(40, 332, W - 40, 332, RULE, 0.8)
d.t(40, 364, "변경 후 — 부모 디렉터리 한 번 idmap", 14, OK, KR, "start", 600)
d.box(40, 380, 276, BH, PAPER2, RULE, 0.9, 6)
d.t(56, 406, "idmapped bind mount", 13, INK, MONO, "start", 600)
d.t(56, 428, "× 1  레이어 50개의 부모 디렉터리", 12, MUTED, KR, "start")
d.box(364, 380, 216, BH, PAPER2, RULE, 0.9, 6)
d.t(380, 406, "overlay mount", 13, INK, MONO, "start", 600)
d.t(380, 428, "× 1  이후 레이어 수와 무관", 12, MUTED, KR, "start")
d.tone(628, 380, 212, BH, OK, 6)
d.t(644, 406, "5,000 → 100", 16, OK, MONO, "start", 600)
d.t(644, 428, "bind mount 호출, PR 작성자 계산", 12, MUTED, KR, "start")
d.arrow([(316, 412), (360, 412)], MUTED, "ar", 1.3)
d.arrow([(580, 412), (624, 412)], MUTED, "ar", 1.3)

d.legend(H - 56, [("기존: 레이어 수에 비례", BAD), ("변경 후: 상수", OK), ("논점: 동시 기동의 총합", ACC)])
d.save(os.path.join(os.path.dirname(__file__), "..", "OverlayFS 와 idmapped mount — Netflix 사례.mount-calls.svg"))
print("ok mount-calls")
