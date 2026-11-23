# 타입 스펙: type-sequence
"""01-02 SSH Agent 가 뜨는 순서 — 도식 생성기.

실행: cd ~/runners-high/write/07_devops/docs/jenkins/_assets && python3 -B _gen/gen-01-02.agent-launch.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (  # noqa: E402
    Seq, PAPER, PAPER2, INK, MUTED, RULE, ACC, OK, INFO, KR, MONO,
)


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


def _text_w(txt, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(txt)) + 16


class SeqKR(Seq):
    def lanes_grid(s, names, y0=104, lane_w=176, x0=36, stride=224):
        s.LX = {}
        for i, (nm, sub) in enumerate(names):
            cx = x0 + lane_w // 2 + i * stride
            s.LX[nm] = cx
            s.box(cx - lane_w // 2, y0, lane_w, 44, PAPER2, RULE, 1.0, 6)
            s.t(cx, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(cx, y0 + 36, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, num=None, num_at_start=False):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 8 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) // 2
        lw = int(_text_w(label, 13))
        s.o.append(f'<rect x="{mx - lw // 2}" y="{y - 24}" width="{lw}" height="18" rx="3" fill="{PAPER}"/>')
        s.t(mx, y - 10, label, 13, c, _kr(label), "middle", 600)
        if num is not None:
            # 번호는 Controller 줄기 왼쪽 한 세로줄에 두되, 그 줄기에서 시작하지 않는 화살표는 자기 시작 줄기 왼쪽에 둔다
            bx = (x1 if num_at_start else s.LX["Controller"]) - 18
            s.o.append(f'<circle cx="{bx}" cy="{y - 15}" r="9" fill="{PAPER}" stroke="{c}" stroke-width="1.2"/>')
            s.t(bx, y - 11, str(num), 12, c, MONO, "middle", 600)
        if sub:
            sw = int(_text_w(sub, 12))
            s.o.append(f'<rect x="{mx - sw // 2}" y="{y + 6}" width="{sw}" height="16" rx="3" fill="{PAPER}"/>')
            s.t(mx, y + 19, sub, 12, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = int(_text_w(txt, 12)) + 8
        s.o.append(f'<rect x="{x - w // 2}" y="{y - 12}" width="{w}" height="24" rx="4" '
                   f'fill="{PAPER}" stroke="{c}" stroke-width="1.1"/>')
        s.o.append(f'<rect x="{x - w // 2}" y="{y - 12}" width="{w}" height="24" rx="4" '
                   f'fill="{c}22"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W = 920
S = 60
Y_START = 180
# 9 msgs + 1 final state
Y_FINAL_STATE = Y_START + S * 9 - 16
RAIL_BOT = Y_FINAL_STATE + 24
LEG_Y = RAIL_BOT + 20
H = LEG_Y + 48

d = SeqKR(
    W,
    H,
    "JENKINS · SSH AGENT LAUNCH",
    "SSH Agent 가 뜨는 순서",
    "사람이 JDK·빌드 도구·sshd 를 미리 설치하고 노드를 저장하면 Controller 의 config.xml 만 바뀌며, Launch agent 를 누르면 Controller 가 다섯 단계로 SSH 접속부터 채널 연결까지 수행하는 순서",
    "번호는 본문 「Launch agent 실행 순서」 의 단계이고, 노드 저장은 Controller 에서 끝납니다",
)

d.lanes_grid([
    ("사람", "사전 준비 · 웹 화면"),
    ("Controller", "SSHLauncher"),
    ("Agent 기계 sshd", "포트 22 · Remote root"),
    ("Agent JVM", "remoting.jar"),
])
d.rails(RAIL_BOT)

y = Y_START
d.msg("사람", "Agent 기계 sshd", "사전 설치", y, MUTED, sub="JDK · 빌드 도구 · sshd")
y += S
d.msg("사람", "Controller", "노드 등록 · 저장", y, MUTED, sub="config.xml")
d.state("Agent 기계 sshd", "Agent 쪽 변화 없음", y, MUTED)
y += S
d.msg("사람", "Controller", "Launch agent", y, MUTED)
y += S
d.msg("Controller", "Agent 기계 sshd", "SSH 접속 · 인증", y, INFO, "info", sub="자격 증명 · 호스트 키", num=1)
y += S
d.msg("Controller", "Agent 기계 sshd", "java 경로 확인", y, INFO, "info", sub="JavaPath 또는 PATH", num=2)
y += S
d.msg("Controller", "Agent 기계 sshd", "remoting.jar 해시 비교", y, INFO, "info", sub="다를 때만 SFTP 복사", num=3)
y += S
d.msg("Controller", "Agent 기계 sshd", "java ‹JVM Options› -jar", y, ACC, "acc", sub="JVM Options 적용 지점", num=4)
y += S
d.msg("Agent 기계 sshd", "Agent JVM", "remoting.jar 기동", y, INFO, "info", sub="시작 시 옵션 1회 읽기", num=4, num_at_start=True)
y += S
d.msg("Agent JVM", "Controller", "표준 입출력 채널 연결", y, OK, "ok", dash="5 4", sub="stdin / stdout 스트림", num=5)
y += 44
d.state("Agent JVM", "online", y, OK)

d.legend(LEG_Y, [
    ("사람 작업", MUTED),
    ("Controller SSH", INFO),
    ("JVM Options", ACC),
    ("채널 연결", OK),
])

out_path = pathlib.Path(__file__).resolve().parent.parent / "01-02.agent-launch.svg"
d.save(str(out_path))
print("saved", out_path)
