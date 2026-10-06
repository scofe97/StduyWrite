# 타입 스펙: type-flowchart
# 07-02 피어 자격 증명 기반 프로세스 인증 흐름
# 사실 출처: NPG Ch.7 Listing 7-13, 7-16 (p.19-24)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 840, 540
d = D(W, H, "NPG CH.7 — PEER CREDENTIALS AUTH",
      "피어 자격 증명 기반 프로세스 인증 흐름",
      "Listing 7-13 및 7-16의 접속 수락부터 자격 증명 조회, 그룹 대조, 응대 및 차단 분기")

# 1. 시작 노드 (s.AcceptUnix)
d.box(340, 96, 160, 44, fill=PAPER2, stroke=INFO, sw=1.2, r=22)
d.t(420, 114, "s.AcceptUnix()", 11, INFO, MONO, "middle", 600)
d.t(420, 129, "conn *net.UnixConn", 11, MUTED, MONO, "middle")

# 화살표 1: 시작 -> GetsockoptUcred (길이 36px)
d.arrow([(420, 140), (420, 176)], MUTED, "ar", 1.4)

# 2. 피어 자격 증명 조회 (unix.GetsockoptUcred)
d.box(290, 176, 260, 48, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(420, 195, "unix.GetsockoptUcred", 11, INK, MONO, "middle", 600)
d.t(420, 211, "SO_PEERCRED → ucred.Uid", 11, MUTED, MONO, "middle")

# 화살표 2: GetsockoptUcred -> LookupId & GroupIds (길이 36px)
d.arrow([(420, 224), (420, 260)], MUTED, "ar", 1.4)

# 3. 사용자 ID 및 그룹 조회 (user.LookupId & GroupIds)
d.box(290, 260, 260, 48, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(420, 279, "user.LookupId & GroupIds", 11, INK, MONO, "middle", 600)
d.t(420, 295, "UID 조회 → 보조 그룹 gids 반환", 11, MUTED, KR, "middle")

# 화살표 3: GroupIds -> Decision Diamond (길이 36px)
d.arrow([(420, 308), (420, 344)], MUTED, "ar", 1.4)

# 4. 판정 다이아몬드 (groups[gid] 존재 여부)
cx, cy, dw, dh = 420, 374, 110, 30
pts = f"{cx},{cy-dh} {cx+dw},{cy} {cx},{cy+dh} {cx-dw},{cy}"
d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{ACC}" stroke-width="1.2"/>')
d.t(cx, cy + 4, "groups[gid] 존재?", 11, ACC, KR, "middle", 600)

# 분기 1 (거부): 왼쪽으로 수평 이동 (길이 110px)
d.arrow([(cx - dw, cy), (200, cy)], BAD, "bad", 1.4)
d.t(255, cy - 16, "불일치 (false)", 11, BAD, KR, "middle", 600)

# 거부 처리 상자
d.box(50, cy - 24, 150, 48, fill=PAPER2, stroke=BAD, sw=1.2, r=6)
d.t(125, cy - 6, "Access denied\\n", 11, BAD, MONO, "middle", 600)
d.t(125, cy + 12, "conn.Write 전송", 11, MUTED, KR, "middle")

# 거부 후 연결 닫기 (길이 36px)
d.arrow([(125, cy + 24), (125, 434)], BAD, "bad", 1.4)
d.box(65, 434, 120, 36, fill=PAPER2, stroke=BAD, sw=1.2, r=18)
d.t(125, 456, "conn.Close()", 11, BAD, MONO, "middle", 600)

# 분기 2 (허용): 오른쪽으로 수평 이동 (길이 110px)
d.arrow([(cx + dw, cy), (640, cy)], OK, "ok", 1.4)
d.t(585, cy - 16, "일치 (true)", 11, OK, KR, "middle", 600)

# 허용 처리 상자
d.box(640, cy - 24, 150, 48, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(715, cy - 6, "Welcome\\n", 11, OK, MONO, "middle", 600)
d.t(715, cy + 12, "conn.Write 전송", 11, MUTED, KR, "middle")

# 허용 후 연결 처리 고루틴 (길이 36px)
d.arrow([(715, cy + 24), (715, 434)], OK, "ok", 1.4)
d.box(635, 434, 160, 36, fill=PAPER2, stroke=OK, sw=1.2, r=18)
d.t(715, 456, "연결 처리 (고루틴)", 11, OK, KR, "middle", 600)

# 범례 (y=490, 높이 540)
d.legend(490, [("접속 수락", INFO), ("자격 대조", ACC), ("접속 허용", OK), ("접속 거부", BAD)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "07-02.peer-cred-auth.svg"))
d.save(out)
print(f"saved: {out}")
