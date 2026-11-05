# 06-02 §1 — 태그는 다른 이미지를 가리키도록 옮겨질 수 있고, 다이제스트는 내용의 해시라 옮겨지지 않는다.
# 본문 근거: 이 노트 ### 1 「이미지가 바뀌지 않았음을 확인하기」.
# 검증 근거: kind v1.35.0 에서 alpine 인덱스 다이제스트의 마지막 글자를 바꾼 파드가
#            failed to resolve reference … not found → ErrImagePull → ImagePullBackOff 로 끝나는 것을 확인.
# 공식 근거: kubernetes.io/docs/concepts/containers/images 「Image names」.
# 타입 스펙: type-swimlane — 태그 레인과 다이제스트 레인.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "CKS STUDY GUIDE · 06-02 §1",
      "태그와 다이제스트가 이미지를 가리키는 방식",
      "위 레인은 태그가 레지스트리에서 다른 이미지로 옮겨질 수 있어 같은 이름이 날마다 다른 내용을 내려받게 하는 흐름이고, "
      "아래 레인은 다이제스트가 파드의 image 필드에서 컨테이너 런타임을 거쳐 레지스트리에 해시 그대로 전달되고 일치하는 이미지가 없으면 ImagePullBackOff 로 끝나는 흐름이다.",
      "태그는 옮겨지는 이름표이고, 다이제스트는 내용에서 계산한 해시라 옮겨지지 않습니다")

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
        if i < len(items) - 1:
            d.path(f"M {x + BW + 2} {by + BH / 2} L {x + PITCH - 2} {by + BH / 2}", MUTED, 1.4, m="ar")


lane(A_Y, "태그로 가리킬 때")
lane_steps(A_Y, [
    ("image 필드", "alpine:3.20", INFO),
    ("레지스트리 태그", "이름표 하나", INFO),
    ("월요일 이미지", "내용 A", SOFT),
    ("화요일 이미지", "같은 태그, 내용 B", WARN),
])
lane(S_Y, "다이제스트로 가리킬 때")
lane_steps(S_Y, [
    ("image 필드", "alpine@sha256:d9e8…", INFO),
    ("컨테이너 런타임", "해시로 이미지 요청", ACC),
    ("레지스트리", "해시가 같은 이미지만", INFO),
    ("실행 또는 실패", "Running / ImagePullBackOff", SOFT),
])

d.legend(392, [("요청과 준비", INFO), ("이름표가 옮겨진 결과", WARN), ("해시를 묻는 자리", ACC), ("결과", SOFT)])
d.save("06-02.tag-vs-digest.svg")
