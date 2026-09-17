# §5.4.2 원문 밖 보강 · 라우트 리플렉션 — 되비춘 경로가 돌아왔을 때 두 자리에서 걸러진다.
# 출처: RFC 4456 §8 Avoiding Routing Information Loops (ORIGINATOR_ID 는 Type 9, CLUSTER_LIST 는 Type 10)
# 논지는 "AS-PATH 가 못 막는 자리를 무엇이 막는가"라 검사 두 개를 위에서 아래로 놓고
# 걸린 경로가 빠지는 곳을 오른쪽에 둔다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 통과와 폐기가 색으로 갈린다.
#           type-sequence 는 주체 간 메시지 순서가 아니라 한 라우터 안의 검사라 기각.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 1000, 592
d = D(W, H, "RFC 4456 §8 · LOOP AVOIDANCE",
      "AS 안에서는 AS-PATH 가 길어지지 않아 다른 표식이 필요합니다",
      "iBGP 로 도는 동안 AS-PATH 는 그대로이므로 되비춘 경로가 돌아와도 자기 번호로는 알아볼 수 없습니다. "
      "리플렉터는 되비출 때 경로를 처음 낸 라우터의 식별자를 ORIGINATOR_ID 로 붙이고 자기 CLUSTER_ID 를 CLUSTER_LIST 앞에 더합니다. "
      "받는 쪽은 그 두 값에서 자기 것을 발견하면 그 광고를 버립니다.",
      lead="되비출 때 표식을 붙이고, 받을 때 그 표식에서 자기 것을 찾습니다")

X, BW, BH, STRIDE, Y0 = 72, 448, 76, 104, 116
DX, DW = 616, 312

STEPS = [
    ("되비출 때 표식을 붙인다", "ORIGINATOR_ID · Type 9 · 4바이트", INFO, MONO,
     INFO, "경로를 처음 낸 라우터", "그 라우터의 BGP Identifier"),
    ("ORIGINATOR_ID 검사", "받은 값이 내 BGP Identifier", ACC, KR,
     BAD, "일치하면 무시", "내가 낸 경로가 돌아온 것"),
    ("CLUSTER_LIST 검사", "되비출 때 CLUSTER_ID 를 앞에 더함", ACC, KR,
     BAD, "내 CLUSTER_ID 가 목록에 있으면 무시", "같은 클러스터로 돌아온 것"),
    ("남은 경로를 표에 올린다", "동점이면 CLUSTER_LIST 가 짧은 쪽", OK, KR,
     None, None, None),
]

for i, (title, sub, c, fam, rc, out, why) in enumerate(STEPS):
    y = Y0 + i * STRIDE
    if i:
        d.arrow([(X + BW // 2, y - STRIDE + BH), (X + BW // 2, y)], MUTED, "ar", 1.4)
    if c is ACC:
        d.tone(X, y, BW, BH, ACC, 6)
    else:
        d.box(X, y, BW, BH, PAPER2, RULE, 0.9, 6)
    d.t(X + 24, y + 30, title, 14, c, KR, "start", 600)
    d.t(X + 24, y + 54, sub, 12, MUTED, fam, "start")

    if out:
        d.arrow([(X + BW, y + BH // 2), (DX, y + BH // 2)], rc,
                "info" if rc is INFO else "bad", 1.5)
        d.box(DX, y, DW, BH, PAPER, RULE, 0.9, 6)
        d.t(DX + 24, y + 30, out, 13, rc, KR, "start", 600)
        d.t(DX + 24, y + 54, why, 12, MUTED, KR, "start")

d.legend(536, [("되비출 때 붙는 표식", INFO), ("자기 것을 찾는 검사", ACC),
               ("버려지는 광고", BAD), ("표에 오르는 경로", OK)])
d.save(str(pathlib.Path(__file__).resolve().parent.parent / "05-02.rr-loop-guard.svg"))
print("ok")
