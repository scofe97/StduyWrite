# 07-01 §2 — 루트 파일 시스템이 읽기 전용이면 공격자의 쓰기는 거부되고, 앱이 쓰는 경로만 emptyDir 로 열리며, 설정은 이미지 밖의 볼륨으로 들어온다.
# 본문 근거: 이 노트 ### 2 「컨테이너를 불변으로 두기」.
# 검증 근거: kind v1.35.0 에서 readOnlyRootFilesystem 만 켠 nginx:1.27 파드는 mkdir() "/var/cache/nginx/client_temp" failed (30: Read-only file system) 로 시작하지 못하고,
#            /var/run 과 /var/cache/nginx 에 emptyDir 를 붙인 파드는 Running 이 되며, hash 파드의 루트는 ro 이고 /var/x 쓰기는 거부되고 /var/config/hash.txt 는 쌓임.
# 공식 근거: kubernetes.io security-context 의 readOnlyRootFilesystem, volumes 의 emptyDir 수명.
# 타입 스펙: type-swimlane — 쓰기 시도마다 한 레인.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 500
d = D(W, H, "CKS STUDY GUIDE · 07-01 §2",
      "읽기 전용 루트 파일 시스템에서 쓰기가 거부되거나 허용되는 경로",
      "첫째 레인은 공격자의 쓰기가 읽기 전용 루트 파일 시스템에서 Read-only file system 으로 거부되는 흐름이고, "
      "둘째 레인은 앱이 쓰는 /var/cache/nginx 에 emptyDir 를 붙여 그 경로만 허용하는 흐름이며, "
      "셋째 레인은 설정을 ConfigMap 이나 Secret 볼륨으로 이미지 밖에서 넣어 이미지를 바꾸지 않는 흐름이다.",
      "루트는 읽기 전용으로 잠그고, 쓸 자리와 설정은 볼륨으로 따로 엽니다")

BW, BH, PITCH, X0 = 238, 60, 280, 28
LANE_X, LANE_W, LANE_H = 12, 856, 108
Y0, GAP = 96, 12


def lane(y, name):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{SOFT}0A" stroke="{SOFT}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def lane_steps(y, items):
    by = y + 32
    for i, (title, sub, c) in enumerate(items):
        x = X0 + i * PITCH
        d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
        d.t(x + BW / 2, by + 26, title, 13, INK, KR, "middle", 600)
        d.t(x + BW / 2, by + 46, sub, 11, MUTED, MONO)
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


rows = [
    ("공격자가 쓸 때", [
        ("공격자의 쓰기", "touch /x", BAD),
        ("읽기 전용 루트", "readOnlyRootFilesystem: true", ACC),
        ("쓰기 거부", "Read-only file system", SOFT),
    ]),
    ("앱이 쓸 때", [
        ("nginx 의 쓰기", "/var/cache/nginx", INFO),
        ("emptyDir 마운트", "이 경로만 쓰기 허용", ACC),
        ("쓰기 허용", "파드가 지워지면 함께 삭제", OK),
    ]),
    ("설정을 넣을 때", [
        ("설정 변경", "ConfigMap · Secret", INFO),
        ("볼륨 마운트", "이미지 밖의 원본", ACC),
        ("파드에 반영", "이미지는 그대로", OK),
    ]),
]
for n, (name, items) in enumerate(rows):
    y = Y0 + n * (LANE_H + GAP)
    lane(y, name)
    lane_steps(y, items)

d.legend(H - 40, [("요청한 쪽", INFO), ("공격자의 시도", BAD), ("읽기 전용과 볼륨이 갈라 주는 자리", ACC), ("결과", SOFT), ("허용된 결과", OK)])
d.save("07-01.immutable-write-paths.svg")
