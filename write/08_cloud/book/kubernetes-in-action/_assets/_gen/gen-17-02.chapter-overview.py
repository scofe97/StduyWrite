# 17-02 전체 지도 — 무엇을 열어 줄 것인가
# 본문이 "2×2 로 압축한 지도"이고 "네 영역은 각각 독립한다"고 못박는다. 그러니 체인이나
# 띠가 아니라 격자여야 하고, 순서를 암시하는 화살표를 두면 안 된다.
# 타입 스펙: type-dp-security-matrix.md — 본문이 "네 영역은 각각 독립한다"고 못박아 화살표를 두지 않았다 — 순서 없는 2×2 격자다.
#           13-03 chapter-overview 와 같은 형태이고, 단계 체인으로 그린 다른 편 개요와 일부러 다르다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1180, 620, "KUBERNETES IN ACTION · 17-02",
      "무엇을 열어 줄 것인가",
      "노드 에이전트는 격리를 부분적으로 열어야 일을 한다. 커널·파일시스템·네트워크 셋은 각각 다른 "
      "격리를 열고, 넷째는 격리가 아니라 스케줄 자리를 지킨다.",
      "네 영역 사이에 순서가 없다 — 필요한 것만 골라 읽는다")

AREAS = [("§1  커널", "privileged 로 전부 열거나", "capabilities 로 골라 연다", 0, 0),
         ("§2  파일시스템", "hostPath 로", "노드의 경로를 마운트한다", 1, 0),
         ("§3  네트워크", "hostNetwork 로", "노드의 네트워크를 그대로 쓴다", 0, 1),
         ("§4  우선순위", "격리를 여는 게 아니라", "스케줄 자리를 지킨다", 1, 1)]
BW, BH = 500, 140
X0, Y0 = 90, 176
for t, l1, l2, ci, ri in AREAS:
    x = X0 + ci * (BW + 40)
    y = Y0 + ri * (BH + 32)
    c = ACC if ri == 1 and ci == 1 else INFO
    d.box(x, y, BW, BH, PAPER2, c, 1.2, 8)
    d.t(x + 28, y + 40, t, 14, c, KR, "start", 600)
    d.t(x + 28, y + 74, l1, 11, MUTED, KR, "start")
    d.t(x + 28, y + 98, l2, 11, MUTED, KR, "start")

d.t(590, 508, "privileged 는 커널 권한 검사를 통째로 우회하고, hostNetwork 는 파드가 자기 IP 없이 노드 IP 를 쓰게 만든다",
     11, SOFT, KR)

d.t(24, 552, "앞의 셋은 격리를 여는 일이라 열수록 노출면이 넓어진다. 넷째만 성격이 달라 "
             "'무엇을 열까'가 아니라 '어디까지 밀려나지 않을까'를 정한다.", 11, MUTED, KR, "start")
d.legend(576, [("격리를 여는 셋", INFO), ("성격이 다른 넷째", ACC)])
d.save("17-02.chapter-overview.svg")
print("ok")
