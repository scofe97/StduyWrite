# 05-02 §5 — fstab 설정이 부팅 마운트 유닛으로 변환되는 경로와 nofail 분기.
# 타입 스펙: type-flowchart — fstab 한 줄이 systemd-fstab-generator 에 의해 .mount 유닛이 되고,
#           마운트 실패 시 nofail 유무에 따라 emergency.target 과 부팅 계속으로 갈리는 분기 논리.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 620
d = D(W, H, "LEARNING MODERN LINUX · 05-02 §5",
      "fstab 설정이 부팅 마운트로 변환되는 경로와 nofail 분기",
      "systemd-fstab-generator 는 fstab 각 줄을 동적 .mount 유닛으로 변환합니다. "
      "마운트 실패 시 nofail 옵션이 없으면 필수 의존성 실패로 emergency 셸에 떨어집니다.",
      "근거: systemd.mount(5) · systemd-fstab-generator(8) · systemd.special(7)")

# 상단: fstab 한 줄과 generator
BX, BY, BW, BH = 40, 120, 800, 64
d.box(BX, BY, BW, BH, PAPER2, INFO, 1.2, 8)
d.t(BX + 20, BY + 24, "1. /etc/fstab 설정 파싱", 13.5, INFO, KR, "start", 600)
d.t(BX + 20, BY + 46, "UUID=be9ae4e4... /mnt/lv ext4 defaults 0 2 (또는 defaults,nofail)", 11.5, INK, MONO, "start")
d.t(BX + BW - 20, BY + 34, "systemd-fstab-generator(8)", 11, SOFT, MONO, "end")

# 화살표
d.arrow([(W / 2, BY + BH), (W / 2, BY + BH + 28)], MUTED, "ar", 1.4)
d.t(W / 2 + 10, BY + BH + 18, "부팅 초기 실행", 11, MUTED, KR, "start")

# 중간 1: 런타임 .mount 유닛 생성
UX, UY, UW, UH = 140, 214, 600, 64
d.box(UX, UY, UW, UH, PAPER2, OK, 1.2, 8)
d.t(UX + 20, UY + 24, "2. 동적 마운트 유닛 생성 (/run/systemd/generator/mnt-lv.mount)", 13.5, OK, KR, "start", 600)
d.t(UX + 20, UY + 46, "local-fs.target 에 등록: 기본은 Requires= + Before=, nofail 이면 Wants= 만", 11.5, INK, MONO, "start")

# 화살표: 마운트 시도 (장치 없음/오류 가정)
d.arrow([(W / 2, UY + UH), (W / 2, UY + UH + 28)], MUTED, "ar", 1.4)
d.t(W / 2 + 10, UY + UH + 18, "마운트 수행 (장치 누락 또는 오타 발생 시)", 11, MUTED, KR, "start")

# 중간 2: 판단 다이아몬드/박스 (nofail 여부)
DX, DY, DW, DH = 240, 308, 400, 56
d.box(DX, DY, DW, DH, PAPER2, WARN, 1.2, 8)
d.t(DX + DW / 2, DY + 26, "마운트 옵션에 nofail 이 지정되었는가?", 13.5, WARN, KR, "middle", 600)
d.t(DX + DW / 2, DY + 44, "systemd.mount(5) nofail 옵션 평가", 11, SOFT, MONO, "middle")

# 좌측 분기: nofail 있음 -> Wants= 완화, 부팅 계속
L_X, L_Y, L_W, L_H = 40, 400, 380, 120
d.box(L_X, L_Y, L_W, L_H, PAPER2, OK, 1.2, 8)
d.t(L_X + 20, L_Y + 26, "YES (nofail 있음) — Wants= 로 완화", 13.5, OK, KR, "start", 600)
d.t(L_X + 20, L_Y + 50, "local-fs.target 이 이 마운트를 기다리지 않음", 11, INK, KR, "start")
d.t(L_X + 20, L_Y + 74, "마운트가 실패해도 부팅은 계속 -> default.target", 11, OK, KR, "start")
d.t(L_X + 20, L_Y + 98, "서비스 정상 시작 (필수 아닌 데이터 볼륨 권장)", 11, MUTED, KR, "start")

# 우측 분기: nofail 없음 -> Requires= 기본, emergency.target 진입
R_X, R_Y, R_W, R_H = 460, 400, 380, 120
d.box(R_X, R_Y, R_W, R_H, PAPER2, BAD, 1.2, 8)
d.t(R_X + 20, R_Y + 26, "NO (기본값) — Requires= 필수 의존", 13.5, BAD, KR, "start", 600)
d.t(R_X + 20, R_Y + 50, "마운트 실패 -> local-fs.target 실패", 11, INK, KR, "start")
d.t(R_X + 20, R_Y + 74, "OnFailure=emergency.target -> 응급 셸", 11, BAD, KR, "start")
d.t(R_X + 20, R_Y + 98, "조치: 루트가 ro 면 remount,rw 후 fstab 수정", 11, WARN, MONO, "start")

# 분기 화살표
d.path(f"M {DX + 60} {DY + DH} L {DX + 60} {L_Y - 18} L {L_X + L_W / 2} {L_Y - 18} L {L_X + L_W / 2} {L_Y - 2}", OK, 1.4, m="ok")
d.path(f"M {DX + DW - 60} {DY + DH} L {DX + DW - 60} {R_Y - 18} L {R_X + R_W / 2} {R_Y - 18} L {R_X + R_W / 2} {R_Y - 2}", BAD, 1.4, m="bad")

d.legend(552, [("정상 부팅 진행 경로", OK), ("설정 및 평가 계층", INFO), ("부팅 실패 및 복구 경로", BAD)])
d.save("05-02.boot-mount.svg")
print("ok 05-02.boot-mount")
