# 타입 스펙: type-sequence — ECN 기반 종단간 혼잡 신호 교환과 송신자 창 축소 시퀀스.
# 사실 출처: ch16.txt 2976~3032행 — 송신자 ECT(0) 송출, 라우터 CE 마킹, 수신자 ECE 반복, 송신자 cwnd 반감 및 CWR 통보, ECE 해제.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        # 중간 라우터 레일 점선이 가로지르는 텍스트를 관통하지 않도록 배경 마스킹
        if abs(x1 - x2) > 300:
            lw = len(str(label)) * 8 + 20
            s.o.append(f'<rect x="{mx - lw/2:.1f}" y="{y - 20}" width="{lw}" height="18" fill="{PAPER}"/>')
            if sub:
                sw = len(str(sub)) * 7 + 16
                s.o.append(f'<rect x="{mx - sw/2:.1f}" y="{y + 6}" width="{sw}" height="16" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

W, H = 920, 720
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-05 §3",
          "ECN 무손실 혼잡 신호 교환과 송신 창 축소 순서",
          "송신자가 ECT(0)를 켜서 보내면 병목 라우터는 패킷을 버리지 않고 IP 헤더를 CE(11)로 바꿔 보냅니다. 수신자는 ECE 플래그로 혼잡을 송신자에게 반복 전달하고, 송신자는 cwnd를 절반으로 줄인 뒤 CWR 플래그로 통보하여 ECE 에코를 멈춥니다.",
          "패킷 손실 없이 라우터 마킹과 TCP 플래그 피드백으로 감속합니다")

S, R, C = "송신자", "중간 라우터", "수신자"
d.lanes([(S, "TCP 송신 호스트"), (R, "AQM 지원 병목 라우터"), (C, "TCP 수신 호스트")], y0=100, lane_w=200)
d.rails(650)
xs, xr, xc = d.LX[S], d.LX[R], d.LX[C]

# 1. 핸드셰이크 ECN 협상
d.msg(S, C, "SYN [ECE=1, CWR=1]", 170, INFO, "info", sub="ECN 사용 제안")
d.msg(C, S, "SYN+ACK [ECE=1, CWR=0]", 220, OK, "ok", dash="4 3", sub="ECN 협상 동의")

# 2. 데이터 전송 및 라우터 CE 마킹
d.msg(S, R, "데이터 패킷 · IP ECT(0)", 280, MUTED, "ar", sub="혼잡 미발생 상태")
d.path(f"M {xr + 10} 280 L {xc - 12} 280", MUTED, 1.4, m="ar")

# 라우터 큐 축적 및 CE 마킹 (화살표가 칩 상자 바깥에서 시작·끝나도록 배치)
d.path(f"M {xs + 10} 340 L {xr - 66} 340", WARN, 1.5, m="warn")
d.t((xs + xr) / 2, 331, "후속 데이터 · IP ECT(0)", 12, WARN, KR, "middle", 600)
d.t((xs + xr) / 2, 355, "대기열 임계치 초과", 11, MUTED, KR, "middle")

d.chip(xr, 340, "CE 마킹 (11)", WARN, 11)

d.path(f"M {xr + 66} 340 L {xc - 12} 340", BAD, 1.5, m="bad")
d.t((xr + xc) / 2, 331, "패킷 보존 통과 · IP CE", 12, BAD, KR, "middle", 600)

# 3. 수신자 ECE 에코 반복 전송 (매 ACK 마다 반복되는 동작을 복수 ACK 로 가시화)
d.msg(C, S, "ACK 1 · TCP ECE=1 (에코)", 405, ACC, "acc", dash="4 3", sub="혼잡 신호 1차 전달 · 송신자가 여기서 한 번 반응")
# 4. 송신자 혼잡 반응 (첫 ECE 에 한 번만 반응) 및 이후 ECE 반복
d.state(S, "cwnd 반감 · ssthresh 갱신", 450, ACC)
d.msg(C, S, "ACK 2 · TCP ECE=1 (반복)", 500, ACC, "acc", dash="4 3", sub="같은 RTT 안이라 다시 줄이지 않음")
d.msg(S, C, "새 데이터 · IP ECT(0) · TCP CWR=1", 565, OK, "ok", sub="창 축소 통보로 피드백 해제 요청")

# 5. 수신자 ECE 해제
d.msg(C, S, "후속 ACK · TCP ECE=0", 615, MUTED, "ar", dash="4 3", sub="정상 전송 상태 복귀")

d.legend(H - 48, [
    ("ECN 협상", OK),
    ("임계 초과", WARN),
    ("CE 마킹", BAD),
    ("ECE 에코", ACC),
    ("일반 제어", INFO),
])

d.save("16-05.ecn-signaling.svg")
