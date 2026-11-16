# 05-02 §5 — /etc/fstab 의 한 줄이 systemd-fstab-generator 를 거쳐 /run/systemd/generator/ 아래의
#           .mount 유닛 파일이 되고, local-fs.target 과 맺는 의존(Requires= 냐 Wants= 냐)이 nofail 하나로
#           갈려 부팅이 멈추거나(emergency.target) 계속되는 실제 구조.
# 타입 스펙: type-architecture — 파일 → 유닛 → 타깃의 구성요소와 의존 간선. accent 는 nofail 필드.
# 근거: 본문 §5 의 fstab 예시 줄(UUID=be9ae4e4-…, /mnt/lv, ext4, defaults,nofail, 0, 2), 「부팅 실패와
#       emergency 셸 복구」의 세 단계(generator 가 /run/systemd/generator/ 에 .mount 생성, local-fs.target 이
#       required + 순서, OnFailure=emergency.target)와 systemd.mount(5) 의 nofail 설명(wanted, 순서 없음).
# 예시: 유닛 이름 mnt-lv.mount 와 유닛 파일의 Where=·Type=·Options= 줄은 fstab 줄에서 옮겨 적은 것으로
#       본문 출력에는 없다. 도식 아래 한 줄에 밝힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 896
d = D(W, H, "LEARNING MODERN LINUX · 05-02 §5",
      "fstab 한 줄이 마운트 유닛이 되고, nofail 이 의존을 바꾼다",
      "부팅 초기에 systemd-fstab-generator 가 /etc/fstab 의 줄마다 /run/systemd/generator/ 아래에 .mount "
      "유닛을 만든다. nofail 이 없으면 local-fs.target 이 그 유닛을 Requires= 와 Before= 로 묶어, 마운트가 "
      "실패하면 타깃도 실패하고 OnFailure=emergency.target 으로 빠진다. nofail 이 있으면 Wants= 로만 "
      "이어지고 순서도 없어 부팅이 계속된다.",
      "같은 실패라도 의존이 Requires= 냐 Wants= 냐에 따라 부팅이 멈추거나 계속된다")

# ── 1. /etc/fstab ─────────────────────────────────────────────
FX, FY, FW, FH = 24, 104, 872, 112
d.box(FX, FY, FW, FH, PAPER2, INFO, 1.2, 8)
d.t(FX + 16, FY + 24, "/etc/fstab", 13, INFO, MONO, "start", 600)
d.t(FX + 112, FY + 24, "필드 여섯 개 · 공백으로 구분", 12, MUTED, KR, "start")
fields = [("UUID=be9ae4e4-…", "식별자", 172), ("/mnt/lv", "마운트 지점", 104),
          ("ext4", "종류", 64), ("defaults,nofail", "옵션", 172), ("0", "dump", 48), ("2", "fsck", 48)]
CY, CH = FY + 40, 36
x = FX + 24
centers = {}
for txt, lab, w in fields:
    d.box(x, CY, w, CH, PAPER, RULE, 0.9, 4)
    if txt == "defaults,nofail":
        d.o.append(f'<rect x="{x + 88}" y="{CY + 5}" width="{w - 96}" height="{CH - 10}" rx="3" '
                   f'fill="{ACC}24" stroke="{ACC}" stroke-width="1.4"/>')
        d.t(x + 86, CY + 23, "defaults,", 13, MUTED, MONO, "end")
        d.t(x + 88 + (w - 96) / 2, CY + 23, "nofail", 13, ACC, MONO, "middle", 600)
    else:
        d.t(x + w / 2, CY + 23, txt, 13, INK, MONO)
    d.t(x + w / 2, CY + CH + 20, lab, 12, SOFT, KR if any('가' <= ch <= '힣' for ch in lab) else MONO)
    centers[lab] = x + w / 2
    x += w + 12

# ── 2. generator → .mount 유닛 파일 ───────────────────────────
UX, UY, UW, UH = 24, FY + FH + 64, 420, 112
GX = UX + 60
d.arrow([(GX, FY + FH + 2), (GX, UY - 3)], INFO, "info", 1.4)
d.t(GX + 12, FY + FH + 28, "systemd-fstab-generator", 12, INFO, MONO, "start", 600)
d.t(GX + 12, FY + FH + 46, "부팅 초기 · 줄마다 하나", 12, MUTED, KR, "start")
d.box(UX, UY, UW, UH, PAPER2, INFO, 1.2, 8)
d.t(UX + 16, UY + 24, "/run/systemd/generator/mnt-lv.mount", 13, INFO, MONO, "start", 600)
for i, ln in enumerate(("[Mount]", "Where=/mnt/lv · Type=ext4", "Options=defaults,nofail")):
    d.t(UX + 16, UY + 52 + i * 20, ln, 12, INK if i else MUTED, MONO, "start")
d.t(UX + UW + 24, UY + 52, "유닛 파일 · 런타임에 생성", 12, MUTED, KR, "start")
d.t(UX + UW + 24, UY + 72, "재부팅마다 fstab 에서 다시 만듦", 12, SOFT, KR, "start")

# ── 3. local-fs.target 과의 의존 — 두 갈래 ─────────────────────
PY = UY + UH + 56
PW = 428
# 같은 유닛 파일에서 두 갈래로(nofail 을 뺀 경우와 둔 경우)
PCL, PCR = 24 + PW / 2, 24 + PW + 16 + PW / 2
d.arrow([(PCL, UY + UH + 2), (PCL, PY - 3)], MUTED, "ar", 1.2)
d.arrow([(PCL, PY - 28), (PCR, PY - 28), (PCR, PY - 3)], MUTED, "ar", 1.2)
NW, NH = 216, 48


def node(cx, y, name, sub, c, kind="box"):
    if kind == "tone":
        d.tone(cx - NW / 2, y, NW, NH, c, 6)
    else:
        d.box(cx - NW / 2, y, NW, NH, PAPER2, c, 1.2, 6)
    fam = KR if any('가' <= ch <= '힣' for ch in name) else MONO
    d.t(cx, y + 21, name, 13, c if kind == "tone" else INK, fam, "middle", 600)
    d.t(cx, y + 39, sub, 12, MUTED, KR)


for k, (title, c) in enumerate((("nofail 없음 · 기본", BAD), ("nofail 있음", OK))):
    px = 24 + k * (PW + 16)
    pc = px + PW / 2
    d.box(px, PY, PW, 360, PAPER, c, 1.0, 8)
    d.t(px + 16, PY + 24, title, 14, c, KR, "start", 600)
    my, ty, ry = PY + 48, PY + 48 + NH + 80, PY + 48 + NH + 80 + NH + 64
    if k == 0:
        d.arrow([(pc - 40, ty - 2), (pc - 40, my + NH + 3)], MUTED, "ar", 1.4)
        d.t(pc - 52, my + NH + 34, "Requires=", 12, INK, MONO, "end")
        d.t(pc - 52, my + NH + 52, "Before=", 12, INK, MONO, "end")
        d.arrow([(pc + 40, my + NH + 2), (pc + 40, ty - 3)], BAD, "bad", 1.6)
        d.t(pc + 52, my + NH + 44, "실패가 번짐", 12, BAD, KR, "start", 600)
        d.arrow([(pc, ty + NH + 2), (pc, ry - 3)], BAD, "bad", 1.6)
        d.t(pc + 12, ty + NH + 36, "OnFailure=", 12, BAD, MONO, "start")
        node(pc, my, "mnt-lv.mount", "장치 없음 · 오타 → 실패", BAD)
        node(pc, ty, "local-fs.target", "필수 마운트 실패 → 실패", BAD)
        node(pc, ry, "emergency.target", "emergency 셸 · 부팅 멈춤", BAD, "tone")
    else:
        d.arrow([(pc - 40, ty - 2), (pc - 40, my + NH + 3)], OK, "ok", 1.4, "4 3")
        d.t(pc - 52, my + NH + 34, "Wants=", 12, INK, MONO, "end")
        d.t(pc - 52, my + NH + 52, "순서 없음", 12, MUTED, KR, "end")
        d.t(pc + 12, my + NH + 44, "실패가 안 번짐", 12, OK, KR, "start", 600)
        d.arrow([(pc, ty + NH + 2), (pc, ry - 3)], OK, "ok", 1.6)
        d.t(pc + 12, ty + NH + 36, "기다리지 않음", 12, OK, KR, "start")
        node(pc, my, "mnt-lv.mount", "장치 없음 · 오타 → 실패", MUTED)
        node(pc, ty, "local-fs.target", "원하기만 함 → 성공", OK)
        node(pc, ry, "부팅 계속", "마운트 성공·실패와 무관", OK, "tone")

d.t(24, PY + 360 + 28, "유닛 이름 mnt-lv.mount 와 유닛 파일의 Where=·Type=·Options= 줄은 fstab 줄에서 옮겨 적은 예",
    11, SOFT, KR, "start")
LEG = PY + 360 + 48
d.legend(LEG, [("파일 · 유닛", INFO), ("nofail", ACC), ("부팅 멈춤", BAD), ("부팅 계속", OK)])
assert LEG + 40 <= H, (LEG, H)
d.save("05-02.boot-mount.svg")
print("ok 05-02.boot-mount")
