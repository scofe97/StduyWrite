# 02-02 §4 — 바이너리와 .sha256 파일을 받아 해시를 대조하면, 일치할 때만 OK 와 종료 코드 0 이 나온다.
# 근거 문장: "Comparing the binary file with the checksum file results in a failure, as the versions do not match:
#            kube-apiserver: FAILED / shasum: WARNING: 1 computed checksum did NOT match"
#           (kubernetes.io 「Install and Set Up kubectl on Linux」의 검증 절차와 같은 echo + --check 형식)
# 타입 스펙: type-flowchart — 같은 입력에서 두 갈래로 나뉘는 판정 절차가 논지다. 도형이 종류를 나른다(타원=시작·끝,
#           사각=단계, 마름모=판정). 코랄은 정상 경로에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, BAD, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    """한글이 섞인 라벨은 한글 스택으로 — mono 에 넣으면 자간이 벌어진다(스타일 계약 §타이포그래피)."""
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


W, H = 880, 640
d = D(W, H, "CKS STUDY GUIDE · 02-02 §4",
      "해시가 같을 때만 OK 와 종료 코드 0 이 나온다",
      "dl.k8s.io 에서 kube-apiserver 와 kube-apiserver.sha256 을 받아 shasum -a 256 --check 로 대조한다. "
      "해시가 같으면 OK 와 종료 코드 0, 다르면 FAILED 와 0 이 아닌 종료 코드가 나온다.",
      "바이너리와 같은 버전의 .sha256 파일이어야 일치합니다")

CX = 300


def shape_box(y, h, title, sub, oval=False, tone=None, w=440):
    x = CX - w / 2
    if tone:
        d.tone(x, y, w, h, tone, r=h / 2 if oval else 6)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, r=h / 2 if oval else 6)
    d.t(CX, y + h / 2 - 3, title, 13, INK, _kr(title), "middle", 600)
    d.t(CX, y + h / 2 + 15, sub, 11, MUTED, _kr(sub))


# 연결선 먼저
d.arrow([(CX, 152), (CX, 178)], MUTED, "ar", 1.4)
d.arrow([(CX, 238), (CX, 264)], MUTED, "ar", 1.4)
d.arrow([(CX, 324), (CX, 350)], MUTED, "ar", 1.4)
d.arrow([(430, 410), (600, 410)], ACC, "acc", 1.6)
d.t(515, 400, "일치", 12, ACC, KR, "middle", 600)
d.arrow([(CX, 470), (CX, 500)], BAD, "bad", 1.6)
d.t(CX + 12, 490, "불일치", 12, BAD, KR, "start", 600)

# 노드
shape_box(100, 52, "dl.k8s.io 에서 내려받기", "kube-apiserver · kube-apiserver.sha256", oval=True)
shape_box(180, 58, "기대 해시 줄 만들기", 'echo "$(cat kube-apiserver.sha256)  kube-apiserver"')
shape_box(266, 58, "파일 해시를 계산해 대조", "shasum -a 256 --check · Linux 는 sha256sum --check")

# 판정: 마름모
dx, dy, hw, hh = CX, 410, 130, 60
d.o.append(f'<polygon points="{dx},{dy - hh} {dx + hw},{dy} {dx},{dy + hh} {dx - hw},{dy}" '
           f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
d.t(dx, dy + 5, "두 해시가 같은가?", 13, INK, KR, "middle", 600)

# 끝: 타원 2개
d.tone(600, 384, 240, 52, ACC, r=26)
d.t(720, 407, "kube-apiserver: OK", 13, INK, MONO, "middle", 600)
d.t(720, 425, "종료 코드 0", 11, MUTED, KR)
d.tone(CX - 150, 504, 300, 52, BAD, r=26)
d.t(CX, 527, "kube-apiserver: FAILED", 13, INK, MONO, "middle", 600)
d.t(CX, 545, "0 이 아닌 종료 코드", 11, MUTED, KR)

d.legend(588, [("정상 경로", ACC), ("검증 실패", BAD)])
d.save("02-02.checksum-verify.svg")
