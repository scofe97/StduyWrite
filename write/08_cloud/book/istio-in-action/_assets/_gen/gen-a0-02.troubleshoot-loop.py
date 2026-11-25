# a0-02 §7 만들고 고치고 다시 띄우는 고리.
# 값 근거(본문 §7 · 부록 E 마지막):
#   - 초기 생성은 istioctl 이 낫다.
#   - 워크로드가 메시에 안 붙을 때는 파일을 직접 고치고 프록시를 재시작하는 고리가 반복이 빠르다.
#   - 어긋난 값 찾기: 액세스 로그 UH 플래그 -> 엔드포인트 목록 -> WorkloadEntry status.conditions(13장 진단 순서).
#   - 연결이 되면 고리를 빠져나간다(메시 합류).
# 타입 스펙: type-loop — 처음 한 번(생성)은 고리 밖에 두고, 연결 확인 -> 실패 시 찾기·고치기·재시작 고리, 성공 시 탈출.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 920, 488
d = D(W, H, "ISTIO IN ACTION · A0-02 §7",
      "처음 한 번은 도구가 짓고 장애 추적은 손이 돈다",
      "설정을 처음 맞출 때는 istioctl 자동화가 낫지만, VM 이 메시에 붙지 않는 원인을 쫓을 때는 "
      "생성된 파일을 직접 고치고 프록시를 다시 띄우는 고리가 빠르다.",
      lead="목적이 다릅니다 — 처음부터 맞추기와 이미 만들어진 값 하나 바꿔 보기.")

BW, BH = 228, 72
def box(x, y, name, sub, focal=False, c=None):
    if focal:
        d.tone(x, y, BW, BH, ACC, 8, "14", 1.4)
    elif c:
        d.tone(x, y, BW, BH, c, 8, "12", 1.2)
    else:
        d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(x + BW / 2, y + 28, name, 13, ACC if focal else (c or INK), KR, "middle", 600)
    fam = KR if any("가" <= ch <= "힣" for ch in sub) else MONO
    d.t(x + BW / 2, y + 52, sub, 13, MUTED, fam, "middle")


EXIT_Y, TOP, BOT, LX, RX = 108, 212, 328, 304, 632
# 고리 밖 — 처음 한 번
box(24, 244, "istioctl 이 파일 생성", "처음 한 번", c=INFO)
d.path(f"M 252 280 L 276 280 L 276 {TOP + BH / 2} L {LX - 2} {TOP + BH / 2}", INFO, 1.4, m="info")

# 성공하면 고리를 나간다
box(LX, EXIT_Y, "메시에 합류한다", "여기서 끝", c=OK)
d.arrow([(LX + BW / 2, TOP), (LX + BW / 2, EXIT_Y + BH + 2)], OK, "ok", 1.5)
d.t(LX + BW / 2 + 12, 196, "연결됨", 13, OK, KR, "start", 600)

# 고리 안 — 실패하면 도는 넷
box(LX, TOP, "프록시를 띄워 연결을 확인한다", "처음에도 여기서 시작", focal=True)
box(RX, TOP, "어긋난 값을 찾는다", "로그 · 엔드포인트 · 상태", focal=True)
box(RX, BOT, "파일을 직접 고친다", "값 하나만 수정", focal=True)
box(LX, BOT, "프록시를 다시 띄운다", "변경 반영", focal=True)

d.arrow([(LX + BW, TOP + BH / 2), (RX - 2, TOP + BH / 2)], ACC, "acc", 1.5)
d.t((LX + BW + RX) / 2, TOP + BH / 2 - 10, "연결 안 됨", 13, ACC, KR, "middle", 600)
d.arrow([(RX + BW / 2, TOP + BH), (RX + BW / 2, BOT - 2)], ACC, "acc", 1.5)
d.arrow([(RX, BOT + BH / 2), (LX + BW + 2, BOT + BH / 2)], ACC, "acc", 1.5)
d.arrow([(LX + BW / 2, BOT), (LX + BW / 2, TOP + BH + 2)], ACC, "acc", 1.5)

d.legend(432, [("연결이 안 될 때 도는 반복", ACC), ("처음 생성 (명령 전체 실행)", INFO), ("반복에서 나가는 자리", OK)])
d.save("a0-02.troubleshoot-loop.svg")
print("ok troubleshoot-loop")
