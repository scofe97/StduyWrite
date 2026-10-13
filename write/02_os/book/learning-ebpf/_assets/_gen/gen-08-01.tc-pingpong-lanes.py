# 타입 스펙: type-swimlane — 레인 셋(veth · docker0 · TC ingress · 스택), 단계 여덟. 레인을 가로지르는 인계 셋: 요청 도착 → ping 판정, 복제본 → 응답 송신, 원본 → TC_ACT_SHOT, 비 ping → TC_ACT_OK. 코랄은 bpf_clone_redirect 한 단계.
# 사실 출처: 예제 저장소 lizrice/learning-ebpf chapter8 (HEAD 91ded4a) network.bpf.c 50~64행(tc_drop_ping: type 8 이면 TC_ACT_SHOT, 아니면 TC_ACT_OK)·71~100행(tc_pingpong: is_icmp_ping_request,
#   swap_mac_addresses, swap_ip_addresses, update_icmp_type(skb, 8, 0), bpf_clone_redirect(skb, skb->ifindex, 0), TC_ACT_SHOT), network.h 57~88행(헬퍼),
#   chapter8/README.md 55~67·92행(pingbox 의 요청은 veth 를 지나 docker0 로 들어옴)(pingbox 172.17.0.2 와 docker0 172.17.0.1, docker exec -it pingbox ping 172.17.0.1), linux v7.2 include/uapi/linux/bpf.h 2213~2237행(bpf_clone_redirect: flags 에 BPF_F_INGRESS 가 없으면 egress 경로),
#   include/uapi/linux/pkt_cls.h 63~71행.
# Layout conventions: 레인 높이 96(y=108 시작), 단계 상자 136×56, 열 x=136·312·488·664·840(간격 40). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 556
d = D(W, H, "LEARNING EBPF · 08-01 §5", "tc_pingpong 은 요청을 응답으로 고쳐 되돌리고 원본은 버린다",
      "pingbox 172.17.0.2 의 ICMP type 8 요청이 docker0 172.17.0.1 의 TC ingress 에 도착하면 tc_pingpong 이 MAC 과 IP 를 맞바꾸고 type 을 0 으로 바꾼 뒤 bpf_clone_redirect 로 복제본을 같은 인터페이스로 내보내고 원본은 TC_ACT_SHOT 으로 버린다. ping 이 아닌 패킷은 TC_ACT_OK 로 스택에 간다.",
      "복제본이 응답이 되고 원본은 스택에 닿지 않습니다")

LANES = [("veth · docker0", 108), ("TC ingress", 204), ("스택", 300)]
for nm, y in LANES:
    d.box(24, y, 952, 96, PAPER2 if nm != "TC ingress" else PAPER, RULE, 0.9, 0)
    d.t(36, y + 20, nm, 11, SOFT, MONO, "start", 600)

CX = [136, 312, 488, 664, 840]
SW, SH = 136, 56
LY = {"NIC": 128, "TC": 224, "ST": 332}

def step(col, lane, t1, t2, c, mono1=True, focal=False):
    x, y = CX[col], LY[lane]
    if focal:
        d.tone(x, y, SW, SH, ACC, 6, "1F", 1.4)
    else:
        d.tone(x, y, SW, SH, c, 6, "12", 1.2)
    d.t(x + SW / 2, y + 24, t1, 11 if len(t1) > 14 else 12, c, MONO if mono1 else KR, "middle", 600)
    d.t(x + SW / 2, y + 44, t2, 11, MUTED, MONO if any(ch in t2 for ch in ">_(") and not any("가" <= ch <= "힣" for ch in t2) else KR)

step(0, "NIC", "요청 도착", "type 8 · .2 → .1", INFO, False)
step(0, "TC", "ping 요청?", "type == 8", MUTED, False)
step(0, "ST", "TC_ACT_OK · 0", "ping 이 아닌 패킷", OK)
step(1, "TC", "주소 맞바꿈", "MAC · IP", INFO, False)
step(2, "TC", "type 8 → 0", "체크섬 갱신", INFO, True)
step(3, "TC", "bpf_clone_redirect", "skb->ifindex, 0", ACC, True, focal=True)
step(3, "ST", "TC_ACT_SHOT · 2", "스택에 닿지 않음", BAD)
step(4, "NIC", "응답 송신", "type 0 · .1 → .2", OK, False)

def mid(col): return CX[col] + SW // 2
# 요청 → 판정
d.arrow([(mid(0), LY["NIC"] + SH + 2), (mid(0), LY["TC"] - 6)], MUTED, "ar", 1.5)
# 판정 → 맞바꿈 (예)
d.arrow([(CX[0] + SW + 2, LY["TC"] + SH // 2), (CX[1] - 6, LY["TC"] + SH // 2)], INFO, "info", 1.5)
d.chip(CX[0] + SW + 20, LY["TC"] + SH // 2 - 14, "예", MUTED, 11)
# 판정 → OK (아니오)
d.arrow([(mid(0), LY["TC"] + SH + 2), (mid(0), LY["ST"] - 6)], OK, "ok", 1.5)
d.chip(mid(0), LY["TC"] + SH + 32, "아니오", MUTED, 11)
# 맞바꿈 → type → clone
d.arrow([(CX[1] + SW + 2, LY["TC"] + SH // 2), (CX[2] - 6, LY["TC"] + SH // 2)], INFO, "info", 1.5)
d.arrow([(CX[2] + SW + 2, LY["TC"] + SH // 2), (CX[3] - 6, LY["TC"] + SH // 2)], INFO, "info", 1.5)
# clone → 응답 (복제본)
d.path(f"M {mid(3)} {LY['TC'] - 2} L {mid(3)} {LY['NIC'] + SH // 2} L {CX[4] - 6} {LY['NIC'] + SH // 2}", ACC, 1.6, m="acc")
d.chip(mid(3) + 52, LY["NIC"] + SH // 2 - 14, "복제본", ACC, 11)
# clone → SHOT (원본)
d.arrow([(mid(3), LY["TC"] + SH + 2), (mid(3), LY["ST"] - 6)], BAD, "bad", 1.5)
d.chip(mid(3), LY["TC"] + SH + 32, "원본", MUTED, 11)

# 비교 줄
d.t(36, 432, "비교", 11, SOFT, MONO, "start", 600)
d.t(136, 432, "tc_drop_ping", 12, INK, MONO, "start", 600)
d.chip(404, 428, "type 8 → TC_ACT_SHOT", BAD, 11)
d.chip(612, 428, "그 밖 → TC_ACT_OK", OK, 11)

d.legend(H - 56, [("판정", MUTED), ("고쳐 쓰기", INFO), ("복제·리다이렉트", ACC), ("버림", BAD), ("스택으로", OK)])
d.save("08-01.tc-pingpong-lanes.svg")
