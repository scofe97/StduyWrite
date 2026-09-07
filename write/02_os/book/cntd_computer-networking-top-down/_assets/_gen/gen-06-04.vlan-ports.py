# 타입 스펙: type-dp-security-matrix — 어느 조합이 되고 안 되는가를 격자로 본다.
#   축약: 역할×대상 권한 격자가 아니라 포트×VLAN 배정 격자다. "이 포트는 이 도메인" 이라는 결정을 칸으로 읽는 구조는 같다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.4.4 Figure 6.25 · Figure 6.26 —
#   16 포트 스위치, 2~8 이 EE VLAN, 9~15 가 CS VLAN, 1 과 16 은 미배정
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 508
d = D(W, H, "SECTION 6.4.4 · PORT-BASED VLANS",
      "포트를 갈라 브로드캐스트 도메인을 나눕니다",
      "물리 스위치 하나의 포트를 그룹으로 나누면 그룹마다 별개의 브로드캐스트 도메인이 된다. 사람이 부서를 옮기면 배선이 아니라 설정을 바꾼다.",
      "포트 배정은 원문 Figure 6.25 그대로입니다")

PX, PY, PW, PH = 40, 140, 56, 56
d.t(40, 122, "물리 스위치 하나 · 포트 16 개", 11, SOFT, KR, "start", 600)
for i in range(16):
    p = i + 1
    x = PX + i * PW
    if 2 <= p <= 8:
        c, tag = INFO, "EE"
    elif 9 <= p <= 15:
        c, tag = OK, "CS"
    else:
        c, tag = MUTED, "미배정"
    d.tone(x, PY, PW - 4, PH, c, 4, "14", 1.2)
    d.t(x + (PW - 4) / 2, PY + 24, str(p), 12, c, MONO, "middle", 600)
    d.t(x + (PW - 4) / 2, PY + 42, tag, 10, c, KR)

d.line(PX + PW, 212, PX + 8 * PW - 4, 212, INFO, 1.4)
d.t(PX + 4.5 * PW, 230, "EE VLAN — 포트 2 ~ 8", 11, INFO, KR)
d.line(PX + 8 * PW, 212, PX + 15 * PW - 4, 212, OK, 1.4)
d.t(PX + 11.5 * PW, 230, "CS VLAN — 포트 9 ~ 15", 11, OK, KR)

d.t(40, 268, "이 배치가 푸는 세 가지", 12, INK, KR, "start", 600)
for i, (head, body) in enumerate([
    ("트래픽 격리", "브로드캐스트가 자기 그룹 밖으로 안 나갑니다"),
    ("스위치 낭비", "그룹마다 스위치를 두지 않고 하나로 끝냅니다"),
    ("사람 관리", "부서를 옮기면 배선 대신 설정을 바꿉니다"),
]):
    y = 294 + i * 26
    d.t(40, y, "·", 11, ACC, KR, "start", 600)
    d.t(54, y, head, 11, INK, KR, "start", 600)
    d.t(160, y, body, 11, MUTED, KR, "start")

d.box(560, 268, 400, 128, PAPER2, f"{ACC}44", 1.2, 7)
d.t(576, 292, "스위치 둘을 잇는 법 — VLAN 트렁킹", 11, ACC, KR, "start", 600)
d.line(576, 302, 944, 302, RULE, 0.8)
d.t(576, 324, "VLAN 마다 포트를 하나씩 이으면 N 개 VLAN 에", 11, MUTED, KR, "start")
d.t(576, 342, "포트가 N 개씩 듭니다. 대신 트렁크 포트 하나를", 11, MUTED, KR, "start")
d.t(576, 360, "모든 VLAN 에 속하게 두고 802.1Q 태그 4 바이트로", 11, MUTED, KR, "start")
d.t(576, 378, "어느 VLAN 의 프레임인지 표시합니다.", 11, MUTED, KR, "start")

d.line(24, 416, W - 48, 416, RULE, 0.8)
d.t(24, 438, "802.1Q 태그는 고정값 81-00 인 TPID 2 바이트와 태그 제어 정보 2 바이트로 이뤄지고, "
             "그 안에 12 비트 VLAN 식별자와 3 비트 우선순위 필드가 들어갑니다.", 11, MUTED, KR, "start")
d.t(24, 456, "태그는 보내는 쪽 스위치가 붙이고 받는 쪽 스위치가 읽어 떼어 냅니다.", 11, MUTED, KR, "start")

d.legend(468, [("EE VLAN", INFO), ("CS VLAN", OK), ("미배정 포트", MUTED), ("VLAN 이 푸는 것", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-04.vlan-ports.svg"
d.save(out)
print("→", out)
