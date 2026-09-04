# a0-02 §7 만들고 고치고 다시 띄우는 고리.
# 본문(부록 E 마지막): "It's preferable to always use istioctl to generate the configuration;
#       but when troubleshooting why a workload is not connecting to the mesh, you will iterate
#       faster by making changes directly to the files and restarting the service proxy to pick
#       up the changes."
# 타입 스펙: type-loop — 같은 자리로 되돌아오는 반복이 논점이다. 고리를 닫고 각 단계에 드는 비용을
#           옆에 적어 왜 손이 빠른지 보이게 한다.
#           축약: 처음 한 번(생성)은 고리 밖에 두고, 고리 안에는 반복되는 셋만 넣는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 940, 536
d = D(W, H, "ISTIO IN ACTION · A0-02 §7",
      "처음 한 번은 도구가 짓고 그다음은 손이 돈다",
      "설정을 처음 만들 때는 istioctl 이 낫다. 워크로드가 왜 안 붙는지 쫓을 때는 파일을 직접 고치고 "
      "프록시를 다시 띄우는 고리가 빠르다. 색이 붙은 고리가 저자가 예외로 둔 자리다.",
      "목적이 달라서 권고가 갈립니다 — 처음 맞추기와 값 하나 바꿔 보기")

BW, BH = 220, 68
def box(x, y, name, sub, focal=False, c=None):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="8" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(x + BW / 2, y + 28, name, 12, ACC if focal else (c or INK), KR, "middle", 600)
    d.t(x + BW / 2, y + 48, sub, 11, MUTED, KR, "middle")

# 고리 밖 — 처음 한 번
box(28, 216, "istioctl 이 짓는다", "처음 한 번", c=INFO)
# 고리의 첫 칸(파일을 고친다, y 152~220)으로 들어가게 한다. y=250 은 두 행 사이 빈칸이었다.
d.path("M 248 250 L 272 250 L 272 186 L 296 186", INFO, 1.4, m="info")

# 고리 안 — 셋
TOP, BOT, LX, RX = 152, 320, 300, 620
box(LX, TOP, "파일을 고친다", "값 하나만 바꾼다", focal=True)
box(RX, TOP, "프록시를 다시 띄운다", "변경을 물린다", focal=True)
box(RX, BOT, "붙는지 본다", "status.conditions", focal=True)
box(LX, BOT, "어긋난 값을 찾는다", "13 장의 진단 순서", focal=True)

d.arrow([(LX + BW, TOP + BH / 2), (RX - 2, TOP + BH / 2)], ACC, "acc", 1.5)
d.arrow([(RX + BW / 2, TOP + BH), (RX + BW / 2, BOT - 2)], ACC, "acc", 1.5)
d.arrow([(RX, BOT + BH / 2), (LX + BW + 2, BOT + BH / 2)], ACC, "acc", 1.5)
d.arrow([(LX + BW / 2, BOT), (LX + BW / 2, TOP + BH + 2)], ACC, "acc", 1.5)

d.t(28, 428, "앞에서 자동화를 권한 이유는 처음부터 맞추기가 어려워서다", 11, SOFT, KR, "start")
d.t(28, 452, "여기서 손을 권하는 이유는 이미 만들어진 것에서 한 값만 바꿔 보는 데 명령 전체를 다시 도는 것이 느려서다", 11, MUTED, KR, "start")
d.legend(476, [("문제를 쫓을 때 도는 고리", ACC), ("처음 한 번", INFO)])
d.save("a0-02.troubleshoot-loop.svg")
