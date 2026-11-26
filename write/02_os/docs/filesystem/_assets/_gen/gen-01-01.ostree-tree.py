# 01-01 §5 OSTree 불변 OS 루트 계층과 /var 심볼릭 링크 방향.
# 타입 스펙: type-tree — 부팅 배포본 루트(/) 직속 디렉터리·심볼릭 링크와 /var·/sysroot 실제 대상 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 980, 544
d = D(W, H, "OSTREE · IMMUTABLE DEPLOYMENT TREE",
      "OSTree 부팅 루트 계층과 /var 심볼릭 링크 방향",
      "OSTree 부팅 배포본 루트(/ostree/deploy/$stateroot/deploy/$checksum) 아래 읽기 전용 /usr, 3-way merge /etc, 그리고 /var 와 /sysroot 로 향하는 최상위 심볼릭 링크 계층.",
      "최상위 쓰기 경로(/opt·/srv·/home 등)와 /usr/local 은 심볼릭 링크로 보존 영역(/var)과 물리 루트(/sysroot)를 가리킵니다")

RCX = 490
L1Y, L1H = 200, 72
L2Y, L2H = 348, 96

# Level 1 (모두 / 직속):
# /usr:      20..228  (w=208, cx=124)  [FOCAL ACC]
# /etc:      244..444 (w=200, cx=344)  [WARN]
# 쓰기 링크: 460..768 (w=308, cx=614)  [PAPER2, dashed symlink → /var]
# /tmp:      784..960 (w=176, cx=872)  [PAPER2, dashed symlink → /sysroot]
L1 = [
    (20,  208, 124, "/usr",                   "RO 바인드 · UsrMove",         "focal"),
    (244, 200, 344, "/etc",                   "구/신 /usr/etc + 활성 병합",   "warn"),
    (460, 308, 614, "/opt·/srv·/home·/root·/mnt", "최상위 쓰기 심볼릭 링크",   "link"),
    (784, 176, 872, "/tmp",                   "임시 공간 심볼릭 링크",        "link"),
]

# 1. 커넥터 먼저 (z-order)
# Root → Level 1
d.path(f"M {RCX} 156 L {RCX} 176", MUTED, 1.3)
d.path(f"M 124 176 L 872 176", MUTED, 1.3)
for _, _, cx, _, _, _ in L1:
    d.arrow([(cx, 176), (cx, L1Y - 2)], MUTED, "ar", 1.3)

# /usr → /usr/etc & /usr/local (직각 트리)
d.arrow([(124, L1Y + L1H), (124, L2Y - 2)], MUTED, 1.3 if False else "ar", 1.3)

# /usr/etc → /etc (3-way merge 기본값 입력, 점선 L-elbow)
d.arrow([(228, L2Y + 28), (344, L2Y + 28), (344, L1Y + L1H + 2)], WARN, "warn", 1.3, dash="4 3")
d.t(356, 314, "3-way 입력", 13, WARN, KR, "start", 500)

# /usr/local → /var (점선 심볼릭 링크)
d.arrow([(228, L2Y + 68), (458, L2Y + 68)], OK, "ok", 1.3, dash="4 3")
d.t(344, L2Y + 58, "/usr/local → /var/usrlocal", 11, OK, MONO, "middle", 500)

# 최상위 쓰기 링크 → /var (점선 심볼릭 링크 화살표)
d.arrow([(614, L1Y + L1H), (614, L2Y - 2)], OK, "ok", 1.6, dash="4 3")
d.t(630, 314, "심볼릭 링크 대상", 13, OK, KR, "start", 500)

# /tmp → /sysroot (점선 심볼릭 링크 화살표)
d.arrow([(872, L1Y + L1H), (872, L2Y - 2)], INFO, "info", 1.6, dash="4 3")
d.t(856, 314, "링크 대상", 13, INFO, KR, "end", 500)

# 2. Level 0 루트
d.box(276, 104, 428, 52, PAPER2, RULE, 1.0, 6)
d.t(RCX, 126, "/  (부팅 배포본 체크아웃)", 14, INK, KR, "middle", 600)
d.t(RCX, 146, "/ostree/deploy/$stateroot/deploy/$checksum", 11, MUTED, MONO)

# 3. Level 1 노드
for x, w, cx, path, sub, kind in L1:
    if kind == "focal":
        d.o.append(f'<rect x="{x}" y="{L1Y}" width="{w}" height="{L1H}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc, psize = ACC, 15
    elif kind == "warn":
        d.tone(x, L1Y, w, L1H, WARN, r=6, op="12", sw=1.1)
        tc, psize = WARN, 15
    else:
        d.box(x, L1Y, w, L1H, PAPER2, RULE, 1.0, 6)
        tc, psize = INK, 12 if len(path) > 10 else 15
    d.t(cx, L1Y + 28, path, psize, tc, MONO, "middle", 600)
    d.t(cx, L1Y + 54, sub, 13, MUTED, KR)

# 4. Level 2 노드
# /usr 하위 (/usr/etc + /usr/local)
d.box(20, L2Y, 208, L2H, PAPER2, RULE, 0.9, 6)
d.t(124, L2Y + 28, "/usr/etc", 13, INK, MONO, "middle", 600)
d.t(124, L2Y + 48, "배포본 기본 설정 원본", 13, MUTED, KR)
d.line(36, L2Y + 58, 212, L2Y + 58, RULE, 0.8)
d.t(124, L2Y + 78, "/usr/local  (심볼릭 링크)", 12, OK, KR)

# /var 보존 대상 (stateroot 공유)
d.tone(460, L2Y, 308, L2H, OK, r=6, op="12", sw=1.2)
d.t(614, L2Y + 24, "/var  (stateroot 공유 · 유지)", 14, OK, KR, "middle", 600)
d.t(614, L2Y + 48, "/var/opt · srv · roothome · usrlocal · mnt", 11, INK, MONO)
d.t(614, L2Y + 72, "/var/home (기본 ../sysroot/home 링크)", 12, MUTED, KR)

# /sysroot 물리 루트 대상
d.tone(784, L2Y, 176, L2H, INFO, r=6, op="12", sw=1.2)
d.t(872, L2Y + 26, "/sysroot  (물리 /)", 14, INFO, KR, "middle", 600)
d.t(872, L2Y + 52, "/sysroot/tmp", 12, INK, MONO)
d.t(872, L2Y + 76, "/ostree → /sysroot/ostree", 11, MUTED, MONO)

d.legend(492, [("읽기 전용 /usr", ACC), ("3-way merge 설정", WARN), ("업그레이드 보존 (/var)", OK), ("물리 루트 (/sysroot)", INFO)])
d.save("01-01.ostree-tree.svg")
