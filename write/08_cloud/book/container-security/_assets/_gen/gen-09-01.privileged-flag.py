# 타입 스펙: type-nested — UID 0 · root 고리 안에 --privileged 의 capability 전부, 그 안에 Docker 기본 열네 개가 들어 있어 root 는 그대로이고 capability 집합만 커짐을 보인다. focal 은 --privileged 가 더하는 cap_sys_admin.
# 사실 출처: 노트 L161~L169(root UID 는 같고 capability 가 갈림 · cap_sys_admin 이 namespace 조작·마운트를 열고 /dev 장치를 마운트해 호스트로 탈출) · L165(capsh 비교표) · L171(cap_sys_admin 은 기본 집합에 없음) · L365(Docker 기본 열네 개 이름)
# Layout conventions: 고리 셋 L1 x=24 · L2 x=56 · L3 x=88(들여쓰기 32), 고리 라벨은 고리 안쪽 좌상단, 바깥 고리일수록 흐린 선, 오른쪽은 L2 안쪽 칩 격자(열 폭 132 · 간격 18). 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 556


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "NESTED · 09-01 §3",
      "--privileged 가 바꾸는 것은 사용자 ID 가 아니라 capability 집합입니다",
      "UID 0 root 는 플래그 없이도 같다. 플래그 없이 주어지는 Docker 기본 capability 열네 개가 --privileged 에서는 전부로 커지고, "
      "더해진 것 가운데 cap_sys_admin 이 /dev 장치를 마운트해 호스트로 탈출하는 길을 연다.",
      lead="root 는 플래그 없이도 UID 0 이고, 플래그는 cap_sys_admin 을 비롯한 나머지 capability 를 더합니다.")

# 고리 셋
d.box(24, 100, 936, 368, PAPER2, "rgba(191,192,192,0.30)", 1.0, 8)
d.t(48, 128, "UID 0 · root — 플래그 없이도 --privileged 에서도 같음", 12, MUTED, KR, "start", 600)

d.o.append(f'<rect x="56" y="148" width="872" height="288" rx="8" fill="{MUTED}0F" stroke="{MUTED}" stroke-width="1.1"/>')
d.t(80, 176, "--privileged · capability 전부", 12, INK, MONO, "start", 600)

d.o.append(f'<rect x="88" y="196" width="352" height="216" rx="8" fill="{INFO}14" stroke="{INFO}" stroke-width="1.2"/>')
d.t(112, 224, "플래그 없이 · Docker 기본 열네 개", 12, INFO, KR, "start", 600)

# L3: 기본 열네 개 (L165 일곱 + L365 나머지 일곱, 소문자 cap_ 표기)
LEFT = ["cap_chown", "cap_dac_override", "cap_fowner", "cap_setuid",
        "cap_net_bind_service", "cap_net_raw", "cap_sys_chroot"]
RIGHT = ["cap_audit_write", "cap_fsetid", "cap_kill", "cap_mknod",
         "cap_setfcap", "cap_setgid", "cap_setpcap"]
for k, (a, b) in enumerate(zip(LEFT, RIGHT)):
    y = 252 + k * 24
    fit(a, 12, 156)
    fit(b, 12, 156)
    d.t(112, y, a, 12, INK, MONO, "start")
    d.t(280, y, b, 12, INK, MONO, "start")

# L2 오른쪽: --privileged 가 더하는 것
RX, RW = 472, 432
d.o.append(f'<rect x="{RX}" y="196" width="{RW}" height="64" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.6"/>')
d.t(RX + 16, 224, "cap_sys_admin", 14, ACC, MONO, "start", 600)
d.t(RX + 16, 246, "/dev 장치를 마운트 → 호스트 탈출", 12, MUTED, KR, "start")
d.t(RX + RW - 16, 224, "namespace 조작 · 마운트", 12, MUTED, KR, "end")

ADDED = ["cap_sys_module", "cap_sys_rawio", "cap_sys_ptrace",
         "cap_sys_boot", "cap_sys_time", "cap_mac_admin",
         "cap_audit_read", "그 밖의 전부"]
for k, name in enumerate(ADDED):
    x = RX + (k % 3) * 150
    y = 292 + (k // 3) * 44
    fit(name, 12, 132 - 16)
    if k == len(ADDED) - 1:
        d.o.append(f'<rect x="{x}" y="{y}" width="132" height="32" rx="6" fill="none" stroke="{BAD}" stroke-width="1.0" stroke-dasharray="5 4"/>')
        d.t(x + 66, y + 20, name, 12, MUTED, KR, "middle")
    else:
        d.tone(x, y, 132, 32, BAD, 6, "14", 1.1)
        d.t(x + 66, y + 20, name, 12, INK, MONO, "middle")

d.legend(H - 56, [("UID 0 · root", MUTED), ("플래그 없이", INFO), ("--privileged 가 더함", BAD), ("cap_sys_admin", ACC)])
d.save(str(ASSETS / "09-01.privileged-flag.svg"))
print("ok 09-01 privileged-flag")
