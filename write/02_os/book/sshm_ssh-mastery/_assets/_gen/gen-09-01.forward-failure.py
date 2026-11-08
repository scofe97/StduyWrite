# 타입 스펙: type-flowchart
# 사실 출처: 2026-11-07 실측 — 서버 AllowTcpForwarding local 에 -R 2224:127.0.0.1:18099 요청(경고 뒤 연결 유지, ExitOnForwardFailure=yes 면 종료 코드 255),
#            OpenSSH V_10_6_P1 ssh_config.5 ExitOnForwardFailure.
# 논지: 서버가 remote 포워딩을 거절하는 갈림길과, 그 뒤 ssh 가 연결을 끊을지 남길지의 갈림길.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, RULE, INK, MUTED, SOFT, ACC, OK, WARN, BAD, KR, MONO

W, H = 984, 648
CX = 300

d = D(W, H, "FLOWCHART · 09-01 FORWARD FAILURE",
      "서버가 -R 을 거절하면 ssh 는 경고를 내고 연결을 남긴다",
      "ssh -N -R 요청이 서버에 닿으면 서버가 remote 포워딩을 허락하는지에 따라 갈립니다. 허락하면 수신 포트가 열립니다. "
      "거절하면 ssh 는 Warning 을 내고, ExitOnForwardFailure 가 yes 이면 Error 와 종료 코드 255 로 끝나며 no 이면 포워딩 없는 연결이 남습니다.",
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
d.arrow([(CX, 268), (CX, 308)], SOFT, "soft", 1.4)
d.t(CX - 8, 292, "아니오", 12, MUTED, KR, "end", 600)

# 경고
d.box(84, 312, 432, 60, PAPER2, RULE, 0.9)
d.t(CX, 336, "Warning: remote port forwarding failed for listen port 2224", 11, INK, MONO, "middle", 600)
d.t(CX, 358, "AllowTcpForwarding local 서버에서 측정 · 연결은 그대로", 11, MUTED, KR, "middle")
d.arrow([(CX, 372), (CX, 404)], SOFT, "soft", 1.4)

# 갈림길 2: ExitOnForwardFailure — 본문이 짚는 한 곳
diamond(CX, 452, 148, 44, "ExitOnForwardFailure", "= yes ?", True, True)
d.arrow([(452, 452), (516, 452)], BAD, "bad", 1.6)
d.t(484, 444, "예", 12, BAD, KR, "middle", 600)
oval(520, 420, 432, 64, BAD, "Error: remote port forwarding failed for listen port 2224", "종료 코드 255 · 연결 종료", True)
d.arrow([(CX, 496), (CX, 528)], SOFT, "soft", 1.4)
d.t(CX - 8, 516, "아니오", 12, MUTED, KR, "end", 600)
oval(140, 530, 320, 56, WARN, "포워딩 없는 연결이 남음", "-N 이면 셸도 없는 빈 연결")

d.legend(600, [("포워딩 성공", OK), ("연결이 남음", WARN), ("ssh 가 종료", BAD), ("본문이 짚는 갈림길", ACC)])
svg_path = pathlib.Path(__file__).resolve().parent.parent / "09-01.forward-failure.svg"
d.save(str(svg_path))
print("ok 09-01 forward-failure")
