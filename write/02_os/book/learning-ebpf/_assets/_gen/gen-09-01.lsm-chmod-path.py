# 타입 스펙: type-flowchart — fchmodat 한 번이 chmod_common 을 거쳐 security_path_chmod 에서 LSM 목록으로 들어가고 반환값이 -EPERM 이면 거부, 0 이면 notify_change 로 가는 분기.
# 사실 출처: 커널 v7.2 arch/x86/entry/syscalls/syscall_64.tbl 줄 102·103·280·379(chmod 90 · fchmod 91 · fchmodat 268 · fchmodat2 452),
#   fs/open.c 651~657행 vfs_fchmod(fchmod 91), 618~636행 chmod_common(632행 security_path_chmod, 이어 notify_change)·698~707행(fchmodat · chmod → do_fchmodat),
#   security/security.c 1577~1582행 security_path_chmod · 479~496행 call_int_hook(0 이 아닌 첫 값에서 멈춤),
#   security/apparmor/lsm.c 1688행 · security/tomoyo/tomoyo.c 576행 LSM_HOOK_INIT(path_chmod …), security/bpf/hooks.c 11~14행 + kernel/bpf/bpf_lsm.c 24~25행(bpf_lsm_<훅> 빈 함수),
#   kernel/bpf/bpf_lsm.c 453~473행 bpf_lsm_get_retval_range([-MAX_ERRNO, 0]).
# Layout conventions: 윗줄 상자 w=208 x=24·260·496·732(stride 236) y=140, 아랫줄 상자 y=300, 마름모 중심 x=600 반폭 92·반높이 44. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 660
d = D(W, H, "LEARNING EBPF · 09-01 §4",
      "chmod 한 번이 훅을 거쳐 EPERM 이나 notify_change 로 간다",
      "chmod · fchmodat · fchmodat2 는 do_fchmodat 으로, fchmod 는 vfs_fchmod 로 들어가 모두 chmod_common 에서 만난다. 거기서 security_path_chmod 가 LSM 을 차례로 부르고 bpf 프로그램이 -EPERM 을 돌려주면 모드는 바뀌지 않는다.",
      "syscall 네 개가 훅 하나에서 만납니다")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def box(x, y, w, title, sub, c, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="64" rx="6" fill="{c}1F" stroke="{c}" stroke-width="1.4"/>')
    else:
        d.tone(x, y, w, 64, c, 6, "12", 1.2)
    d.t(x + w / 2, y + 28, title, 13, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 50, sub, 13, MUTED, kr(sub))


# 윗줄 — 호출 경로
XS = (24, 260, 496, 732)
box(XS[0], 140, 208, "fchmodat", '268 · "/etc/passwd"', INFO)
box(XS[1], 140, 208, "do_fchmodat", "chmod 90 · fchmodat2 452", MUTED)
box(XS[2], 140, 208, "chmod_common", "inode 잠근 뒤 호출", MUTED)
box(XS[3], 140, 208, "security_path_chmod", "path · mode 0777", ACC, True)
for i in range(3):
    d.arrow([(XS[i] + 210, 172), (XS[i + 1] - 4, 172)], MUTED, "ar", 1.5)

# 윗줄 끝 → 아랫줄 처음 (ㄷ자)
d.arrow([(836, 206), (836, 324), (128, 324), (128, 356)], ACC, "acc", 1.6)
# fchmod 는 vfs_fchmod 를 거쳐 chmod_common 으로 들어오는 둘째 입력
box(XS[1], 224, 208, "vfs_fchmod", "fchmod 91", INFO)
d.arrow([(470, 256), (600, 256), (600, 208)], INFO, "info", 1.5)

# 아랫줄 — LSM 목록과 프로그램, 반환값 분기
box(24, 360, 208, "LSM 목록", "0 아닌 첫 값에서 정지", MUTED)
box(260, 360, 208, "lsm/path_chmod", "path · mode 판정", INFO)
d.arrow([(234, 392), (256, 392)], MUTED, "ar", 1.5)
d.arrow([(470, 392), (502, 392)], INFO, "info", 1.5)

CX, CY = 600, 392
d.o.append(f'<polygon points="{CX-92},{CY} {CX},{CY-44} {CX+92},{CY} {CX},{CY+44}" fill="{PAPER2}" stroke="{ACC}" stroke-width="1.2"/>')
d.t(CX, CY + 5, "반환값", 13, INK, KR, "middle", 600)

# -EPERM → 거부
d.arrow([(696, 392), (762, 392)], BAD, "bad", 1.6)
d.chip(729, 374, "-EPERM", BAD, 13)
box(768, 360, 168, "EPERM", "syscall 오류 반환", BAD)
# 0 → 진행
d.arrow([(600, 438), (600, 496)], OK, "ok", 1.6)
d.chip(628, 468, "0", OK, 13)
box(496, 500, 208, "notify_change", "mode 변경 진행", OK)

d.legend(H - 56, [("syscall 입구", INFO), ("훅 호출", ACC), ("거부", BAD), ("허용", OK)])
d.save("09-01.lsm-chmod-path.svg")
