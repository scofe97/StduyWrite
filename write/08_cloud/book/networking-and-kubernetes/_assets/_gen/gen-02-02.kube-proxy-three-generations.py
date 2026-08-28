# 02-02.kube-proxy-three-generations — 세 세대를 다섯 축으로 나란히 놓는다
# 본문 요구: "세 세대가 무엇을 바꿨는지는 결국 '어떻게 찾는가'로 요약됩니다.
#            왼쪽이 세대와 그 세대가 쓰는 자료구조이고, 오른쪽이 목적지를 찾는 방법과 그 비용입니다.
#            각 세대를 눈으로 확인하는 명령도 함께 적었습니다."
#            "리스트는 규칙이 늘수록 대조 횟수가 함께 늘지만 해시는 규칙 수와 무관합니다."
# 타입 스펙: type-dp-security-matrix.md 의 행 대조 — 행이 세대, 열이 다섯 축.
#           평가 대상이 role×component 가 아니라 세대×축이라 열 폭만 이 내용에 맞춰 잡는다.
#           비용 열을 행 색으로 칠해 O(n) 과 O(1) 의 대비가 한 열에서 읽히게 한다.
# 이력: 2026-08-28 신설. 이 SVG 는 생성기 없이 손으로 만들어져 있어 타입 선택 단계를 건너뛴
#       자산이었다(러너 "생성기가 없는 SVG 는 만들지 않는다"). 값은 기존 SVG 에서 그대로 옮겼다.
# 좌표: stride 없이 열마다 내용 폭이 달라 열 폭을 개별로 두되 전부 4의 배수, gap 12 고정.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 1236, 532
X0, GAP, HDR_Y, ROW_H = 24, 12, 108, 84
COLS = [(176, "세대"), (168, "자료구조"), (196, "목적지를 찾는 법"),
        (180, "비용"), (232, "확인 명령"), (176, "할 수 있게 된 일")]
COST_COL = 3                                       # 본문의 논점이 서는 열

d = D(W, H, "COMPARISON MATRIX · 02-02 KUBE-PROXY",
      "서비스 조회의 세 세대 — 바뀐 것은 찾는 방법이다",
      "kube-proxy 세 세대(iptables·IPVS·eBPF)를 자료구조·조회 방법·비용·확인 명령·"
      "새로 가능해진 일 다섯 축으로 비교한 행렬. 리스트 순회에서 해시 조회로 바뀌며 비용이 규칙 수와 무관해진다.",
      lead="리스트는 규칙이 늘수록 대조가 늘지만, 해시는 규칙 수와 무관합니다 — 16만 규칙 5시간이 여기서 나옵니다.")

ROWS = [
    (BAD, [("iptables", "kube-proxy 1세대"), ("규칙 리스트", None),
           ("첫 줄부터 순차 대조", None), ("규칙 수에 비례", "O(n)"),
           ("iptables -t nat -S", None), ("랜덤 분배만", None)]),
    (INFO, [("IPVS", "커널 L4 LB"), ("해시 테이블", None),
            ("해시 조회", None), ("규칙 수와 무관", "O(1)"),
            ("ipvsadm -Ln", None), ("밸런싱 모드 선택", None)]),
    (OK, [("eBPF", "Cilium 등"), ("BPF 맵", "해시"),
          ("맵 조회 · 커널 내 처리", None), ("규칙 수와 무관", "O(1)"),
          ("cilium-dbg bpf lb list", None), ("L7 정책 · 관측", None)]),
]

XS, x = [], X0
for w, name in COLS:
    XS.append((x, w))
    d.t(x + w // 2, HDR_Y, name, 11, SOFT, KR, "middle", 600)
    x += w + GAP

for r, (rc, cells) in enumerate(ROWS):
    y = HDR_Y + 24 + r * (ROW_H + GAP)
    for i, ((cx0, cw), (main, sub)) in enumerate(zip(XS, cells)):
        hit = (i == COST_COL)
        if hit:
            d.tone(cx0, y, cw, ROW_H, rc, 6, "12", 1.4)
        else:
            d.box(cx0, y, cw, ROW_H, PAPER2, RULE, 1.1, 6)
        mono = all(ord(ch) < 128 for ch in main)
        my = y + (ROW_H // 2 + 5 if sub is None else 34)
        d.t(cx0 + 20, my, ddx.fit(main, 13, cw - 40, main), 13,
            rc if (hit or i == 0) else INK, MONO if mono else KR, "start", 600)
        if sub:
            d.t(cx0 + 20, y + 58, ddx.fit(sub, 11, cw - 40, sub), 11, MUTED,
                MONO if all(ord(ch) < 128 for ch in sub) else KR, "start")

d.t(X0, 448, "리스트는 규칙이 늘수록 대조 횟수가 함께 늘고, 해시는 규칙 수와 무관하다. "
             "세대가 바꾼 것은 결국 목적지를 찾는 방법 하나다.", 12, MUTED, KR, "start")
d.legend(468, [("규칙 수에 비례 · 이 편의 병목", BAD),
               ("해시 조회로 상수시간", INFO),
               ("커널 안에서 처리 · L7 까지", OK)])
d.save("02-02.kube-proxy-three-generations.svg")
print("ok kube-proxy-three-generations")
