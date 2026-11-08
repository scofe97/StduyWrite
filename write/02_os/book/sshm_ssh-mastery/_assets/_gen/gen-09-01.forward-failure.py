# 타입 스펙: type-flowchart
# 사실 출처: 2026-11-07 실측 — 서버 AllowTcpForwarding local 에 -R 2224:127.0.0.1:18099 요청(no 면 Warning 만 내고 연결 유지, yes 면 Error 만 내고 종료 코드 255),
#            OpenSSH V_10_6_P1 ssh_config.5 ExitOnForwardFailure.
# 논지: 서버가 remote 포워딩을 거절하는 갈림길과, 거절 직후 ExitOnForwardFailure 가 연결을 끊을지 남길지 정하는 갈림길. ssh.c 1972~1988 (V_10_6_P1) 에서 Error(fatal)와 Warning(logit)은 서로 배타.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, RULE, INK, MUTED, SOFT, ACC, OK, WARN, BAD, KR, MONO

W, H = 984, 546
CX = 300

d = D(W, H, "FLOWCHART · 09-01 FORWARD FAILURE",
      "서버가 -R 을 거절하면 ExitOnForwardFailure 가 ssh 의 행동을 정한다",
      "ssh -N -R 요청이 서버에 닿으면 서버의 허락 여부에 따라 갈립니다. 허락하면 수신 포트가 열립니다. "
      "거절되면 ExitOnForwardFailure 값에 따라 갈립니다. yes 이면 Error 와 종료 코드 255 로 즉시 끝나고, no(기본값)이면 Warning 을 내고 포워딩 없는 연결이 남습니다.",
      lead="갈림길은 둘입니다. 서버의 허락 여부, 그리고 ssh 의 ExitOnForwardFailure 입니다.")


def oval(x, y, w, h, c, l1, l2=None, mono1=False):
    if c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{c}14" stroke="{c}" stroke-width="1.1"/>')
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9"/>')
    if l2:
        d.t(x + w / 2, y + h / 2 - 3, l1, 11 if mono1 else 12, INK, MONO if mono1 else KR, "middle", 600)
        d.t(x + w / 2, y + h / 2 + 16, l2, 11, MUTED, KR, "middle")
    else:
        d.t(x + w / 2, y + h / 2 + 4, l1, 11 if mono1 else 12, c or INK, MONO if mono1 else KR, "middle", 600)


def diamond(cx, cy, hw, hh, l1, l2, focal=False, mono1=False):
    pts = f"{cx},{cy-hh} {cx+hw},{cy} {cx},{cy+hh} {cx-hw},{cy}"
    if focal:
        d.o.append(f'<polygon points="{pts}" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
    d.t(cx, cy - 2, l1, 11 if mono1 else 12, INK, MONO if mono1 else KR, "middle", 600)
    d.t(cx, cy + 16, l2, 11, MUTED, MONO if l2[0] in "=A" else KR, "middle")


# 시작
oval(160, 104, 280, 40, None, "ssh -N -R 2224:127.0.0.1:18099", None, True)
d.arrow([(CX, 144), (CX, 176)], SOFT, "soft", 1.4)

# 갈림길 1: 서버가 허락하나
diamond(CX, 224, 148, 44, "서버가 -R 을 허락하나?", "AllowTcpForwarding")
d.arrow([(452, 224), (556, 224)], OK, "ok", 1.6)
d.t(504, 216, "예", 12, OK, KR, "middle", 600)
oval(560, 204, 320, 40, OK, "서버에 수신 포트가 열림")
d.arrow([(CX, 268), (CX, 296)], SOFT, "soft", 1.4)
d.t(CX - 8, 288, "아니오", 12, MUTED, KR, "end", 600)

# 갈림길 2: ExitOnForwardFailure — 거절 직후 ssh 가 판단하며 Error 와 Warning 은 서로 배타다
diamond(CX, 340, 148, 44, "ExitOnForwardFailure", "= yes ?", True, True)
d.arrow([(452, 340), (516, 340)], BAD, "bad", 1.6)
d.t(484, 332, "예", 12, BAD, KR, "middle", 600)
oval(520, 308, 432, 64, BAD, "Error: remote port forwarding failed for listen port 2224", "종료 코드 255 · 연결 종료", True)
d.arrow([(CX, 384), (CX, 420)], SOFT, "soft", 1.4)
d.t(CX - 8, 408, "아니오", 12, MUTED, KR, "end", 600)
oval(84, 420, 432, 64, WARN, "Warning: remote port forwarding failed for listen port 2224", "포워딩 없는 연결이 남음 · -N 이면 셸도 없는 빈 연결", True)

d.legend(498, [("포워딩 성공", OK), ("연결이 남음", WARN), ("ssh 가 종료", BAD), ("본문이 짚는 갈림길", ACC)])
svg_path = pathlib.Path(__file__).resolve().parent.parent / "09-01.forward-failure.svg"
d.save(str(svg_path))
print("ok 09-01 forward-failure")
