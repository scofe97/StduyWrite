# 타입 스펙: type-sequence
# 06-02 TFTP 정지-대기(Stop-and-Wait) 재전송 흐름
# 사실 출처: NPG Ch.6 p.8-9 (Fig 6-3, Downloading a file by using TFTP), p.19-22
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 840, 580
d = Seq(W, H, "NPG CH.6 — STOP AND WAIT ARQ",
        "TFTP 전송과 정지-대기 재전송",
        "Figure 6-3 블록별 ACK 확인과 타임아웃 재전송 흐름",
        "블록마다 ACK 를 확인하고 타임아웃 시 재전송")

# 레인 2개
d.lanes([("클라이언트", "Client"), ("TFTP 서버", "Server")], y0=95, lane_w=180)
d.rails(515)

x_client, x_server = d.LX["클라이언트"], d.LX["TFTP 서버"]
mx_mid = (x_client + x_server) / 2

def msg_seq(a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
    x1, x2 = d.LX[a], d.LX[b]
    d.path(f"M {x1} {y} L {x2} {y}", c, 1.5, m=mk, dash=dash)
    mx = (x1 + x2) / 2
    if sub:
        w_lbl = len(label) * 7.2
        w_sub = sum(11.0 if '가' <= ch <= '힣' else 7.0 for ch in sub)
        gap = 14
        total_w = w_lbl + gap + w_sub
        sx = mx - total_w / 2
        d.t(sx, y - 8, label, 11, c, MONO, "start", 600)
        d.t(sx + w_lbl + gap, y - 8, sub, 11, MUTED, KR, "start")
    else:
        d.t(mx, y - 8, label, 11, c, MONO, "middle", 600)

def selfmsg_seq(a, label, y, c=MUTED, mk="warn", sub=None):
    x = d.LX[a]
    d.path(f"M {x} {y - 10} L {x + 48} {y - 10} L {x + 48} {y + 10} L {x} {y + 10}", c, 1.4, m=mk)
    d.t(x + 58, y - 4, label, 11, c, MONO, "start", 600)
    if sub:
        d.t(x + 58, y + 13, sub, 11, MUTED, KR, "start")

# 1. RRQ
msg_seq("클라이언트", "TFTP 서버", "RRQ", 150, c=INFO, mk="info", sub="test.svg (octet)")

# 2. DATA 1
msg_seq("TFTP 서버", "클라이언트", "DATA 1", 190, c=OK, mk="ok", sub="512B 페이로드")

# 3. ACK 1
msg_seq("클라이언트", "TFTP 서버", "ACK 1", 230, c=WARN, mk="warn", sub="Block 1 확인")

# 4. DATA 2 (유실 또는 무응답)
# 중간까지 가다 끊긴 화살표 (생명선에서 출발)
d.path(f"M {x_server} 270 L {mx_mid + 30} 270", BAD, 1.5, dash="4 4")
w_lbl_d2 = len("DATA 2") * 7.2
w_sub_d2 = sum(11.0 if '가' <= ch <= '힣' else 7.0 for ch in "응답 없음 (손실)")
sx_d2 = mx_mid - (w_lbl_d2 + 14 + w_sub_d2) / 2
d.t(sx_d2, 255, "DATA 2", 11, BAD, MONO, "start", 600)
d.t(sx_d2 + w_lbl_d2 + 14, 255, "응답 없음 (손실)", 11, BAD, KR, "start")
# X 표식
mx = mx_mid + 30
d.line(mx - 6, 264, mx + 6, 276, BAD, 2.0)
d.line(mx - 6, 276, mx + 6, 264, BAD, 2.0)

# 5. 서버 타임아웃
selfmsg_seq("TFTP 서버", "Timeout", 315, c=WARN, sub="6초 만료")

# 6. DATA 2 재전송
msg_seq("TFTP 서버", "클라이언트", "DATA 2", 360, c=OK, mk="ok", sub="512B 재전송")

# 7. ACK 2
msg_seq("클라이언트", "TFTP 서버", "ACK 2", 400, c=WARN, mk="warn", sub="Block 2 확인")

# 생략 줄 (...)
d.line(mx_mid, 422, mx_mid, 436, RULE, 1.2, dash="3 3")

# 8. 최종 데이터 블록 (< 512B)
msg_seq("TFTP 서버", "클라이언트", "DATA 148", 455, c=OK, mk="ok", sub="< 512B 최종 블록")

# 9. 최종 ACK
msg_seq("클라이언트", "TFTP 서버", "ACK 148", 495, c=WARN, mk="warn", sub="전송 완료")

# Legend
d.legend(H - 42, [("요청", INFO), ("데이터 블록", OK), ("확인응답", WARN), ("손실 및 타임아웃", BAD)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "06-02.stop-and-wait.svg"))
d.save(out)
print(f"saved: {out}")
