# 02-01 §4 「커널에서 거르면 오히려 비싸지 않나」·「BPF 는 커널 안의 작은 가상머신입니다」 — 프레임이 NIC 에서
# 사용자 공간까지 가는 커널 경로 위에서 BPF 가 서는 자리를 세 장으로 그린다. 앞 소절은 "커널에서 거르지 않을 때" 한 장,
# 뒤 소절은 "검증 없는 필터" 와 "검증을 통과한 BPF" 한 쌍이다. BPF 로 거르는 흐름은 뒤 소절의 마지막 장이 보인다.
# 세 장이 같은 좌표를 써서 나란히 놓고 비교할 수 있다.
# 구조 근거: [^bpf93] "the driver first calls BPF. BPF feeds the packet to each participating process' filter. ...
#           For each filter that accepts the packet, BPF copies the requested amount of data to the buffer associated
#           with that filter. The device driver then regains control. ... normal protocol processing proceeds."
#           [^bpf4] 디스크립터마다 자기 사본 · [^xnu-validate] 검증 없는 프로그램이 시스템을 무너뜨림.
# 세 장 모두 레인은 실행 주체(하드웨어 · 커널 · 사용자 공간)이고 레인 사이를 건너가는 것은 프레임과 그 사본이다.
# 레인 구분선 하나(커널 · 사용자 공간)가 논문이 말하는 보호 경계다. 호출 순서는 칩 1 · 2 와 복귀 화살표로 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 600
LABEL_W = 140
LANES = [("하드웨어", "NIC", 96, 176), ("커널", "KRN", 176, 440), ("사용자 공간", "USR", 440, 536)]
NW, NH = 192, 56
LX, CX, RX = 340, 500, 660                         # 왼쪽(캡처) · 가운데 · 오른쪽(프로토콜) 열 중심
Y_NIC, Y_DRV, Y_MID, Y_LOW, Y_USR = 108, 188, 284, 372, 468
TONE = {"ok": OK, "warn": WARN, "bad": BAD}
MARK = {"ok": "ok", "warn": "warn", "bad": "bad", "acc": "acc", "plain": "ar", "soft": "soft"}
COLOR = {"ok": OK, "warn": WARN, "bad": BAD, "acc": ACC, "plain": MUTED, "soft": SOFT}


def draw(out, title, desc, lead, s, legend):
    d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-01 §4", title, desc, lead)

    # 레인
    for name, key, top, bot in LANES:
        d.line(0, top, W - 12, top, RULE, 0.8)
        d.t(16, (top + bot) / 2 - 4, name, 12, SOFT, KR, "start", 600)
        d.t(16, (top + bot) / 2 + 14, key, 9, SOFT, MONO, "start")
    d.line(0, LANES[-1][3], W - 12, LANES[-1][3], RULE, 0.8)
    d.line(LABEL_W, LANES[0][2], LABEL_W, LANES[-1][3], RULE, 0.8)
    d.t(W - 12, 456, "보호 경계", 11, SOFT, KR, "end", 600)

    def arrow(pts, style, sw=1.4):
        dash = "3,3" if style == "soft" else None
        d.arrow(pts, COLOR[style], MARK[style], 1.0 if style == "soft" else sw, dash=dash)

    def node(cx, y, state, title, sub, sub_mono=False):
        x = cx - NW / 2
        if state == "focal":
            d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        elif state == "none":
            d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{PAPER}" '
                       f'stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="4,3"/>')
        elif state == "plain":
            d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 6)
        else:
            d.tone(x, y, NW, NH, TONE[state], 6)
        col = {"focal": ACC, "none": SOFT, "plain": INK}.get(state, TONE.get(state))
        d.t(cx, y + 24, title, 13, col, KR, "middle", 600)
        d.t(cx, y + 44, sub, 12, MUTED, MONO if sub_mono else KR)

    # 연결선 먼저
    arrow([(CX, Y_NIC + NH), (CX, Y_DRV - 4)], "plain")
    arrow([(CX - NW / 2, Y_DRV + 20), (LX - 24, Y_DRV + 20), (LX - 24, Y_MID - 4)], s["a_call"])       # 1 BPF 먼저
    arrow([(LX + 24, Y_MID), (LX + 24, Y_DRV + 40), (CX - NW / 2 - 4, Y_DRV + 40)], s["a_return"])  # 복귀
    arrow([(CX + NW / 2, Y_DRV + 28), (RX, Y_DRV + 28), (RX, Y_MID - 4)], s["a_proto"])            # 2 그다음
    arrow([(LX, Y_MID + NH), (LX, Y_LOW - 4)], s["a_keep"], s.get("w_keep", 1.4))
    arrow([(LX, Y_LOW + NH), (LX, Y_USR - 4)], s["a_copy"], s.get("w_copy", 1.4))
    arrow([(RX, Y_MID + NH), (RX, Y_LOW - 4)], s["a_right"])
    arrow([(RX, Y_LOW + NH), (RX, Y_USR - 4)], s["a_right"])

    d.chip(LX - 44, Y_DRV + 68, "1", MUTED)
    d.t(LX - 60, Y_DRV + 72, "먼저", 12, MUTED, KR, "end", 600)
    d.chip(RX + 24, Y_DRV + 68, "2", MUTED)
    d.t(RX + 40, Y_DRV + 72, "그다음", 12, MUTED, KR, "start", 600)
    rc, rl = s["return_label"]
    d.t(LX + 36, Y_DRV + 72, rl, 12, COLOR[rc], KR, "start", 600)
    if s.get("return_cross"):                      # ✕ — 돌아오지 못한 복귀
        mx, my = LX + 24, Y_DRV + 56
        d.line(mx - 5, my - 5, mx + 5, my + 5, BAD, 1.8); d.line(mx - 5, my + 5, mx + 5, my - 5, BAD, 1.8)
    for (lc, lt), ly in ((s["keep_label"], Y_LOW - 12), (s["copy_label"], Y_USR - 12)):
        if lt:
            d.t(LX + 12, ly, lt, 12, COLOR[lc], KR, "start", 600)

    if s.get("drop_filter"):                       # 커널에서 버림
        arrow([(LX - NW / 2, Y_MID + 28), (LX - NW / 2 - 44, Y_MID + 28)], "bad", 1.2)
        d.t(LX - NW / 2 - 52, Y_MID + 33, s["drop_filter"], 12, BAD, KR, "end", 600)
    if s.get("drop_user"):                         # 사용자 공간에서 버림
        arrow([(LX - NW / 2, Y_USR + 28), (LX - NW / 2 - 44, Y_USR + 28)], "bad", 1.2)
        d.t(LX - NW / 2 - 52, Y_USR + 33, s["drop_user"], 12, BAD, KR, "end", 600)
    if s.get("loop"):                              # 끝나지 않는 실행 — 뒤로 가는 점프
        x0 = LX - NW / 2
        d.arrow([(x0 + 16, Y_MID + NH), (x0 + 16, Y_MID + NH + 16), (x0 - 20, Y_MID + NH + 16),
                 (x0 - 20, Y_MID + 16), (x0 - 4, Y_MID + 16)], BAD, "bad", 1.4)
        d.t(x0 - 28, Y_MID + 44, "무한 루프", 12, BAD, KR, "end", 600)

    # 노드
    node(CX, Y_NIC, "plain", "NIC", "en0", sub_mono=True)
    node(CX, Y_DRV, *s["driver"])
    node(LX, Y_MID, *s["filter"])
    node(LX, Y_LOW, *s["buffer"])
    node(LX, Y_USR, *s["dump"])
    node(RX, Y_MID, s["right"][0], "프로토콜 스택", s["right"][1])
    node(RX, Y_LOW, s["right"][0], "소켓 버퍼", s["right"][2])
    node(RX, Y_USR, s["right"][0], "앱", s["right"][3])

    d.legend(552, legend)
    d.save(out)


PLAIN_RIGHT = ("plain", "IP · TCP", "앱에 넘길 몫", "curl · 브라우저")

# ── 소절 「커널에서 거르면 오히려 비싸지 않나」 ─────────────────────────────
# 타입 스펙: type-data-flow — 문제 흐름. 커널에 필터가 없어 모든 프레임의 사본이 경계를 넘고, 거르기는 사용자 공간에서
#           한다. focal 은 경계를 넘는 굵은 복사 화살표 하나.
draw("02-01.bpf-cost-no-filter.svg",
     "커널에서 거르지 않으면",
     "드라이버가 넘긴 프레임을 커널이 조건 없이 모두 캡처 버퍼에 담고, 그 사본이 전부 커널과 사용자 공간의 보호 경계를 넘어 dumpcap 으로 복사된다. 거르기는 사용자 공간에서 뒤늦게 일어나 대부분의 사본은 옮긴 뒤에 버려진다.",
     "모든 프레임이 보호 경계를 넘어 복사되고, 버리는 일은 사용자 공간에 가서야 합니다",
     dict(driver=("plain", "드라이버", "link-level driver", True),
          filter=("none", "필터 없음", "조건 없이 통과"),
          buffer=("warn", "캡처 버퍼", "모든 프레임 사본"),
          dump=("warn", "dumpcap", "여기서 거름"),
          right=PLAIN_RIGHT,
          a_call="plain", a_return="plain", a_proto="plain", a_right="plain",
          a_keep="warn", w_keep=2.4, a_copy="acc", w_copy=4.0,
          return_label=("plain", "복귀"), keep_label=("warn", "전부"), copy_label=("acc", "모든 프레임 복사"),
          drop_user="대부분 버림"),
     [("경계를 넘는 복사", ACC), ("불필요한 사본", WARN), ("버림", BAD)])

# ── 소절 「BPF 는 커널 안의 작은 가상머신입니다」 ──────────────────────────
# 타입 스펙: type-data-flow — 문제 흐름. 검증 없이 붙은 필터가 뒤로 점프해 끝나지 않으면 드라이버가 제어를 돌려받지
#           못해, 캡처 쪽도 프로토콜 쪽도 프레임이 넘어가지 않는다. focal 은 멈춘 드라이버 하나.
draw("02-01.bpf-vm-unverified.svg",
     "검증 없는 필터를 커널에서 돌리면",
     "드라이버는 BPF 를 먼저 부르고 필터가 끝나야 제어를 돌려받는다. 검증 없이 붙은 필터 코드가 뒤로 점프해 같은 명령을 반복하면 복귀가 일어나지 않아, 캡처 버퍼로도 프로토콜 스택으로도 프레임이 넘어가지 않는다.",
     "필터가 끝나지 않으면 드라이버가 제어를 돌려받지 못해 양쪽 길이 모두 멈춥니다",
     dict(driver=("focal", "드라이버", "제어를 못 돌려받음"),
          filter=("bad", "필터 코드", "뒤로 점프 · 반복"),
          buffer=("none", "캡처 버퍼", "닿지 않음"),
          dump=("none", "dumpcap", "닿지 않음"),
          right=("none", "닿지 않음", "닿지 않음", "닿지 않음"),
          a_call="plain", a_return="soft", a_proto="soft", a_right="soft",
          a_keep="soft", a_copy="soft",
          return_label=("bad", "복귀 못 함"), return_cross=True,
          keep_label=("soft", ""), copy_label=("soft", ""),
          loop=True),
     [("멈춘 드라이버", ACC), ("끝나지 않는 필터", BAD), ("닿지 않음", SOFT)])

# 타입 스펙: type-data-flow — BPF 흐름. 붙일 때 검증을 통과한 필터는 앞으로만 가다 ret 에서 끝나, 드라이버가 제어를
#           돌려받고 프로토콜 처리로 넘어간다. focal 은 검증을 통과한 BPF 필터 하나.
draw("02-01.bpf-vm-verified.svg",
     "검증을 통과한 BPF 필터라면",
     "붙일 때 검증을 통과한 필터는 모든 분기가 앞으로만 가고 ret 명령에서 끝난다. 필터가 끝나면 드라이버가 제어를 돌려받아 프레임을 프로토콜 스택으로 넘기고, 받아들인 사본은 캡처 버퍼를 거쳐 dumpcap 으로 간다.",
     "필터가 반드시 ret 에서 끝나므로 드라이버가 복귀해 프로토콜 처리로 넘어갑니다",
     dict(driver=("plain", "드라이버", "link-level driver", True),
          filter=("focal", "BPF 필터", "검증 통과 · ret 로 끝"),
          buffer=("ok", "캡처 버퍼", "받은 프레임 사본"),
          dump=("ok", "dumpcap", "libpcap", True),
          right=("ok", "IP · TCP", "앱에 넘길 몫", "curl · 브라우저"),
          a_call="plain", a_return="ok", a_proto="ok", a_right="ok",
          a_keep="ok", a_copy="ok",
          return_label=("ok", "복귀"), keep_label=("ok", "받아들인 것만"), copy_label=("ok", "받은 것만 복사"),
          drop_filter="버림"),
     [("검증을 통과한 필터", ACC), ("정상 진행", OK), ("버림", BAD)])
