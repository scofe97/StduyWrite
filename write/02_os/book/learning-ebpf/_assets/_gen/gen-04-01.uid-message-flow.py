# 타입 스펙: type-data-flow — 사례(레인) 셋 × 단계 넷. execve 를 낸 UID 가 config 조회를 거쳐 출력 줄이 된다. focal 은 항목이 없어 기본 메시지로 떨어지는 UID 1.
# 사실 출처: 원서 Ch.4 4쪽(실행 및 출력 결과: 37926 501 bash Hi user 501!, 37929 0 sudo Hey root!, 37933 1 sudo Hello World), 예제 저장소 chapter4/hello-buffer-config.py, 본문 §1(108행 — sudo ls 한 번이 execve 두 번, bash 가 sudo 를 띄울 때 UID 501, sudo 가 ls 를 띄울 때 0). sudo 레인은 둘째 execve 만 그린다.
# Layout formulas(type-data-flow §2) 변형: 레인 3 · lane_h 88 · node_h 64 · 단계 폭은 내용에 맞춰 단계별 값. 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 500
d = D(W, H, "LEARNING EBPF · 04-01 §1",
      "execve 를 낸 UID 가 메시지를 고른다",
      "UID 501 과 0 은 config 에 항목이 있어 그 메시지를 쓰고, 항목이 없는 UID 1 은 기본 메시지 Hello World 를 쓴다. sudo 두 레인은 sudo 가 ls 를 띄운 둘째 execve 이고, bash 가 sudo 를 띄운 첫 줄(37927·37931, UID 501)은 첫 레인과 같아 뺐다.",
      "호출 UID 에 따른 메시지 조회와 출력 분기")

TOP, LH, NH = 140, 88, 64
LANES = [("ls", None), ("sudo ls", "sudo 가 띄운 ls"), ("sudo -u daemon ls", "sudo 가 띄운 ls")]
COLX = [200, 408, 616, 788]
COLW = [176, 176, 140, 148]
HEAD = ["01 execve", "02 config 조회", "03 메시지", "04 출력 줄"]

for i, (x, w) in enumerate(zip(COLX, COLW)):
    d.box(x + w/2 - 56, 100, 112, 20, PAPER2, RULE, 0.9, 10)
    d.t(x + w/2, 114, HEAD[i], 13, MUTED, KR, "middle", 600)
for k, (nm, sub) in enumerate(LANES):
    y = TOP + k * LH
    if k % 2 == 0:
        d.o.append(f'<rect x="12" y="{y}" width="{W-24}" height="{LH}" fill="#F5F5F3" fill-opacity="0.025"/>')
    d.t(24, y + LH/2 + (4 if sub is None else -6), nm, 13, INK, MONO, "start", 600)
    if sub:
        d.t(24, y + LH/2 + 16, sub, 13, MUTED, KR, "start")

# (pid, uid, comm, lookup 키, 항목 있음?, 메시지, 출력 둘째 줄 앞)
CASES = [(37926, 501, "bash", 501, True, "Hi user 501!"),
         (37929, 0, "sudo", 0, True, "Hey root!"),
         (37933, 1, "sudo", 1, False, "Hello World")]
for k, (pid, uid, comm, key, hit, msg) in enumerate(CASES):
    y = TOP + k * LH + (LH - NH) // 2
    cy = y + NH // 2
    # 단계 1 — execve
    d.tone(COLX[0], y, COLW[0], NH, INFO, 6, "12", 1.2)
    d.t(COLX[0] + COLW[0]/2, y + 28, f"uid {uid}", 13, INFO, MONO, "middle", 600)
    d.t(COLX[0] + COLW[0]/2, y + 48, f"pid {pid} · {comm}", 13, MUTED, MONO)
    # 단계 2 — config 조회
    c2 = OK if hit else WARN
    d.tone(COLX[1], y, COLW[1], NH, c2, 6, "12", 1.2)
    d.t(COLX[1] + COLW[1]/2, y + 28, f"lookup({key})", 13, c2, MONO, "middle", 600)
    d.t(COLX[1] + COLW[1]/2, y + 48, "항목 있음" if hit else "항목 없음", 13, MUTED, KR)
    # 단계 3 — 메시지
    c3 = OK if hit else ACC
    d.tone(COLX[2], y, COLW[2], NH, c3, 6, "12" if hit else "1F", 1.4 if not hit else 1.2)
    d.t(COLX[2] + COLW[2]/2, y + 28, msg, 13, c3, MONO, "middle", 600)
    d.t(COLX[2] + COLW[2]/2, y + 48, "config 의 값" if hit else "기본 메시지", 13, MUTED, KR)
    # 단계 4 — 출력 줄
    d.box(COLX[3], y, COLW[3], NH, PAPER2, RULE, 0.9, 6)
    d.t(COLX[3] + COLW[3]/2, y + 28, f"{pid} {uid} {comm}", 13, INK, MONO, "middle", 600)
    d.t(COLX[3] + COLW[3]/2, y + 48, msg, 13, MUTED, MONO)
    d.arrow([(COLX[0] + COLW[0] + 2, cy), (COLX[1] - 6, cy)], INFO, "info", 1.5)
    d.arrow([(COLX[1] + COLW[1] + 2, cy), (COLX[2] - 6, cy)], c2, "ok" if hit else "warn", 1.5)
    d.arrow([(COLX[2] + COLW[2] + 2, cy), (COLX[3] - 6, cy)], c3, "ok" if hit else "acc", 1.5)

d.legend(H - 56, [("execve 호출", INFO), ("조회 성공·값", OK), ("항목 없음", WARN), ("기본 메시지", ACC)])
d.save("04-01.uid-message-flow.svg")
