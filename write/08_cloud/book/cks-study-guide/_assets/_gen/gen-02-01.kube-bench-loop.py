# 02-01 §2 — kube-bench 결과의 WARN·FAIL 은 정적 파드 매니페스트를 고친 뒤 Job 을 다시 돌려 PASS 로 확인한다.
# 본문 근거: 이 노트 §2 「지적은 컨트롤 플레인 매니페스트에서 고치고 Job 을 다시 돌려 확인합니다」.
# 책 쪽: "The configuration files of the control plane components can be found in the directory /etc/kubernetes/manifests" /
#        "The Pod running the API server in the kube-system namespace will be restarted automatically" /
#        "You will need to delete the existing Job object before you can verify the changed result".
# 타입 스펙: type-flowchart — WARN·FAIL 항목이 남았는가라는 판단 하나로 갈리고, 예 쪽은 처음으로 되돌아간다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 836
d = D(W, H, "CKS STUDY GUIDE · 02-01 §2",
      "kube-bench 점검과 수정의 한 바퀴",
      "kube-bench Job 을 실행해 로그의 PASS·WARN·FAIL 을 읽고, 남은 WARN·FAIL 의 조치를 컨트롤 플레인 정적 파드 매니페스트에 "
      "반영한 뒤 Job 을 지우고 다시 돌려 결과를 확인하는 순환 절차를 그린 흐름도다.",
      "고친 항목이 PASS 로 바뀌었는지 같은 바퀴로 확인합니다")

CX = 440
BW, BH = 400, 64


def step(y, title, sub, mono_sub=False, c=INK):
    d.box(CX - BW / 2, y, BW, BH, PAPER2, RULE, 1.0)
    d.t(CX, y + 26, title, 15, c, KR, "middle", 600)
    d.t(CX, y + 48, sub, 12, MUTED, MONO if mono_sub else KR)


def oval(cx, y, w, h, txt, c):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, y + h / 2 + 5, txt, 15, c, KR, "middle", 600)


oval(CX, 100, 320, 48, "kube-bench Job 실행", INFO)
d.path(f"M {CX} 148 L {CX} 178", MUTED, 1.4, m="ar")
step(180, "Pod kube-bench 의 로그", "[PASS] · [WARN] · [FAIL] 목록과 Remediations")
d.path(f"M {CX} 244 L {CX} 274", MUTED, 1.4, m="ar")

DW, DH = 320, 96
DY = 276
d.o.append(f'<path d="M {CX} {DY} L {CX + DW / 2} {DY + DH / 2} L {CX} {DY + DH} L {CX - DW / 2} {DY + DH / 2} Z" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX, DY + 44, "고칠 WARN·FAIL 항목이", 14, ACC, KR, "middle", 600)
d.t(CX, DY + 64, "남았는가", 14, ACC, KR, "middle", 600)

# 아니요 → 종료
d.path(f"M {CX + DW / 2} {DY + DH / 2} L 674 {DY + DH / 2}", MUTED, 1.4, m="ar")
d.t(CX + DW / 2 + 12, DY + DH / 2 - 8, "없음", 13, MUTED, KR, "start")
oval(756, DY + 24, 160, 48, "점검 종료", OK)
# 예 → 아래
d.path(f"M {CX} {DY + DH} L {CX} 408", MUTED, 1.4, m="ar")
d.t(CX + 12, DY + DH + 24, "있음", 13, MUTED, KR, "start")

step(410, "Remediations 의 조치 확인", "항목 번호와 같은 번호의 조치 문구")
d.path(f"M {CX} 474 L {CX} 502", MUTED, 1.4, m="ar")
step(504, "정적 파드 매니페스트 수정", "/etc/kubernetes/manifests/kube-apiserver.yaml", True, ACC)
d.path(f"M {CX} 568 L {CX} 596", MUTED, 1.4, m="ar")
step(598, "kubelet 의 Pod 재생성", "kube-system 의 kube-apiserver Pod 재시작")
d.path(f"M {CX} 662 L {CX} 690", MUTED, 1.4, m="ar")
step(692, "Job 삭제 후 다시 실행", "kubectl delete job kube-bench", True)

# U자 복귀 경로
d.path(f"M {CX - BW / 2} 724 L 96 724 L 96 212 L {CX - BW / 2 - 2} 212", WARN, 1.4, m="warn")
d.chip(96, 468, "다시 점검", WARN, 12)

d.legend(788, [("점검 실행", INFO), ("판단 지점", ACC), ("종료", OK), ("다시 점검 경로", WARN)])
d.save("02-01.kube-bench-loop.svg")
