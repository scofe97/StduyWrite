# 2026-09-10 E · 원인 분석 "왜 스스로 풀리지 않는가" — 기다림이 원으로 닫히는 자리만 세운다.
# 앞 장 pinning-deadlock 은 "갈림길"이 논지였고, 이 장은 사고 쪽 갈래 안에서 원이 닫히는 구조다.
# 등장인물은 Netflix 원문(2024-07-30)의 스레드 덤프·힙 덤프를 따른다.
#   A~D  — synchronized 안에서 ReentrantLock 을 기다리며 pinned 된 가상 스레드 4개
#   락   — exclusiveOwnerThread 가 null. 방금 풀렸고 다음 차례가 아직 못 가져간 상태
#   E    — 락을 푼 스레드가 신호를 보낸 대기열 첫 차례. pinned 가 아니라 캐리어가 필요한 가상 스레드(#119516)
#   (락 대기자는 원문상 6개 — A~D, E, 플랫폼 스레드 #107. #107 은 신호를 못 받은 대기자라 원을 닫지 않아 뺐다)
#   캐리어 — 4 vCPU 라 4개, 전부 A~D 가 쥐고 있다
#   새 요청 — 스택 없는 가상 스레드. 수가 CLOSE_WAIT 소켓 수와 거의 같았다
# 2026-09-13 이전 판은 원을 "I/O 완료 콜백"으로 닫았는데 원문과 달라 다시 그렸다.
# 타입 스펙: type-dependency — 트리로 못 그리는 두 가지가 다 있다.
#           (a) fan-in — E 와 새 요청이 캐리어 풀 하나로 몰린다 (2 in, 가장 큰 fan-in).
#           (b) cycle — 캐리어가 A~D 를 기다리는 점선 하나가 랭크를 거슬러 원을 닫는다.
#           loop 는 station 5~8 과 상태를 쌓는 hub 가 없어 기각, flowchart 는 경로가 끝나지 않아 기각.
# 좌표: 스펙 — 랭크 행 간격 120, rx=6, 순환선은 노드 더미 바깥으로. 노드는 스펙 160x56 대신
#       224x64 를 쓴다(한글 14px 를 1em 예산으로 담으려고). 모든 값 4의 배수.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 648
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-10 E",
      "기다림이 원으로 닫히는 자리",
      "가상 스레드 A~D 가 synchronized 안에서 ReentrantLock 을 기다리며 캐리어 4개를 전부 붙든다. "
      "락을 푼 스레드가 다음 차례 E 에게 신호를 보내지만 E 는 캐리어에 올라타야 락을 가져갈 수 있다. "
      "캐리어는 A~D 가 쥐고 있고 A~D 는 락을 기다리므로 원이 닫힌다.",
      lead="화살표는 '기다린다'로 읽습니다. 거슬러 올라가는 점선 하나가 원을 닫습니다.")

def kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

NW, NH = 224, 64
R = [112, 232, 352, 472]           # 랭크 stride 120
MX = 248                            # 주 기둥 왼쪽 끝 (중심 360)
SX = 584                            # 새 요청 노드 왼쪽 끝 (중심 696)

def node(x, y, name, sub, badge):
    d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, y + 27, name, 14, INK, kr(name), "start", 600)
    d.t(x + 16, y + 49, sub, 12, MUTED, kr(sub), "start")
    bw = len(badge) * 7 + 12
    d.box(x + NW - bw - 8, y + 8, bw, 18, PAPER, RULE, 0.8, 2)
    d.t(x + NW - bw / 2 - 8, y + 21, badge, 11, SOFT, MONO, "middle")

node(MX, R[0], "가상 스레드 A~D", "synchronized 안 · lock() 대기", "1 in")
node(MX, R[1], "ReentrantLock", "주인 null · 방금 풀림", "1 in")
node(MX, R[2], "가상 스레드 E", "synchronized 밖 · 신호 받음", "1 in")
node(SX, R[2], "새 요청 가상 스레드", "스택 없음 · 수 ≈ CLOSE_WAIT", "0 in")
node(MX, R[3], "캐리어 스레드 ×4", "4 vCPU · parallelism 4", "2 in")

CXM = MX + NW // 2                  # 360
CXS = SX + NW // 2                  # 696

# ── 순방향: 랭크를 아래로 건넌다 ──
def down(y_from, label):
    d.arrow([(CXM, y_from + NH), (CXM, y_from + 120)], MUTED, "ar", 1.3)
    d.t(CXM + 12, y_from + NH + 32, label, 13, MUTED, KR, "start")

down(R[0], "락을 얻어야 블록을 나감")
down(R[1], "E 가 가져가야 넘어감")
down(R[2], "올라타야 락을 가져감")

# 새 요청 → 캐리어: 오른쪽에서 꺾어 캐리어 노드 오른쪽 변으로 들어간다
d.arrow([(CXS, R[2] + NH), (CXS, R[3] + 32), (MX + NW, R[3] + 32)], MUTED, "ar", 1.3)
d.t(CXS + 12, R[2] + NH + 32, "올라타야 첫 줄을 실행", 13, MUTED, KR, "start")

# ── 역방향 하나: 캐리어는 A~D 가 놓아야 풀린다. accent 2개 예산은 이 선과 CYCLE 칩에만 ──
BX = 160
d.path(f"M {MX} {R[3] + 32} L {BX} {R[3] + 32} L {BX} {R[0] + 32} L {MX - 4} {R[0] + 32}",
       ACC, 1.6, m="acc", dash="5 4")
d.box(BX - 28, R[0] + 72, 56, 18, PAPER, ACC, 0.9, 2)
d.t(BX, R[0] + 85, "CYCLE", 11, ACC, MONO, "middle")
d.t(BX - 12, R[2] + 20, "캐리어 4개를", 13, MUTED, KR, "end")
d.t(BX - 12, R[2] + 40, "A~D 가 쥐고 있음", 13, MUTED, KR, "end")

d.line(12, 564, W - 48, 564, RULE, 0.8)
d.t(W // 2, 596, "락은 비었는데, 가져갈 E 가 올라탈 자리를 락을 기다리는 A~D 가 쥐고 있습니다",
    13, MUTED, KR, "middle")
d.t(W // 2, 620, "락 하나와 자리 4개짜리 세마포어의 교착 — 끊는 방법은 재시작뿐입니다.",
    12, SOFT, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-10.deadlock-cycle.svg"))
print("ok")
