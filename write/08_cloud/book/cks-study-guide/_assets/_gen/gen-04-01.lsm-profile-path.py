# 04-01 §4 — AppArmor 와 seccomp 는 프로파일을 노드에 먼저 두고, 파드가 이름이나 상대 경로로 가리킨다.
# 본문 근거: 이 노트 ### 4 「프로파일은 노드에 먼저 두고 파드는 이름으로 가리킵니다」.
# 검증 근거: kind v1.35.0 워커 노드(arm64)에서 seccompProfile Localhost(profiles/mkdir-violation.json)가 mkdir 을
#            Operation not permitted 로 막는 것을 확인. AppArmor 는 apparmor_parser -Q -T 파싱과 appArmorProfile 필드의
#            서버 dry-run 수용을 확인했고, 이 커널에서는 AppArmor 가 꺼져 있어 강제 적용은 돌리지 않았다.
# 공식 근거: kubernetes.io 「Restrict a Container's Access to Resources with AppArmor」·「Restrict a Container's Syscalls with seccomp」.
# 타입 스펙: type-swimlane — AppArmor 와 seccomp 두 레인이 같은 네 단계를 밟는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "CKS STUDY GUIDE · 04-01 §4",
      "프로파일이 파드에 닿는 길",
      "AppArmor 와 seccomp 두 레인에서 프로파일 파일을 만들고, 노드에 두거나 적재하고, 파드 매니페스트가 가리키고, "
      "컨테이너 시작 때 커널이 적용하는 네 단계를 같은 열에 맞춰 그린 도식이다.",
      "두 도구 모두 프로파일을 노드에 먼저 두고 파드는 이름이나 상대 경로로 가리키기만 합니다")

BW, BH, PITCH, X0 = 190, 76, 212, 24
LANE_X, LANE_W, LANE_H = 12, 856, 132
A_Y, S_Y = 96, 244


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def lane_steps(y, items):
    by = y + 40
    for i, (title, sub, c) in enumerate(items):
        x = X0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
        d.t(x + BW / 2, by + 32, title, 13, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 56, sub, 11, MUTED, MONO)
        if i < 3:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "AppArmor")
lane_steps(A_Y, [
    ("프로파일 파일 작성", "network-deny", INFO),
    ("노드에 적재", "apparmor_parser", INFO),
    ("파드가 이름으로 참조", "appArmorProfile", SOFT),
    ("컨테이너 시작 때 적용", "deny network,", ACC),
])
lane(S_Y, "seccomp")
lane_steps(S_Y, [
    ("프로파일 JSON 작성", "mkdir-violation.json", INFO),
    ("kubelet 루트 아래 배치", "/var/lib/kubelet/seccomp", INFO),
    ("파드가 상대 경로로 참조", "seccompProfile", SOFT),
    ("시스템 콜 호출 때 차단", "SCMP_ACT_ERRNO", ACC),
])

d.legend(392, [("노드에서 준비", INFO), ("파드 매니페스트", SOFT), ("커널이 막는 자리", ACC)])
d.save("04-01.lsm-profile-path.svg")
