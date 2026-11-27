# 01-01 §2 — CKS 시험 응시자가 PSI 원격 데스크톱에서 지정 호스트로 접속해 과제를 푸는 경로.
# 본문 근거: 이 노트 §2 「시험 방식과 쿠버네티스 버전」.
# 공식 근거: Linux Foundation Important Instructions: CKS (PSI Secure Browser, Remote Desktop, base, ssh <nodename>, sudo -i, v1.37).
# 타입 스펙: type-flowchart — 응시자 브라우저에서 과제 클러스터까지의 접속 흐름과 과제 완료 후 base 복귀 경로를 그린다.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, MUTED, INK, PAPER2, RULE, INFO, WARN, KR, MONO

W, H = 920, 344
d = D(W, H, "CKS STUDY GUIDE · 01-01 §2",
      "CKS 시험 환경 접속과 과제 수행 경로",
      "응시자가 PSI Secure Browser와 Linux 원격 데스크톱을 거쳐 base 노드 터미널에서 ssh <nodename> 으로 지정 호스트에 접속하고, 과제 뒤 base 로 돌아오는 흐름도다.",
      "base 노드에는 도구가 없으므로 반드시 지정 호스트로 ssh 접속해 풀고, 다음 과제 전에 base 로 돌아옵니다")

Y = 120
BH = 64
CY = Y + BH / 2

# 1. 시작 (Oval rx=20)
d.o.append(f'<rect x="16" y="{Y}" width="176" height="{BH}" rx="20" fill="{INFO}14" stroke="{INFO}" stroke-width="1.2"/>')
d.t(104, CY - 4, "PSI Secure Browser", 12, INK, MONO, "middle", 600)
d.t(104, CY + 16, "Linux 원격 데스크톱", 12, MUTED, KR)

# 2. base 터미널
d.box(232, Y, 172, BH, PAPER2, RULE, 1.0, 6)
d.t(318, CY - 4, "시험 터미널 (base)", 13, INK, KR, "middle", 600)
d.t(318, CY + 16, "사전 도구 미설치", 12, MUTED, KR)

# 3. 지정 호스트 (focal 1곳)
d.tone(536, Y, 184, BH, ACC, 6, "18", 1.4)
d.t(628, CY - 4, "지정 호스트", 14, ACC, KR, "middle", 600)
d.t(628, CY + 16, "sudo -i · k · yq", 12, INK, MONO)

# 4. 과제 클러스터 (종료/대상)
d.o.append(f'<rect x="760" y="{Y}" width="144" height="{BH}" rx="20" fill="{INFO}14" stroke="{INFO}" stroke-width="1.2"/>')
d.t(832, CY - 4, "과제 클러스터", 13, INK, KR, "middle", 600)
d.t(832, CY + 16, "Kubernetes v1.37", 12, MUTED, MONO)

# 정방향 화살표
d.path(f"M 192 {CY} L 230 {CY}", MUTED, 1.4, m="ar")
d.path(f"M 404 {CY} L 534 {CY}", ACC, 1.5, m="acc")
d.t(470, CY - 12, "ssh <nodename>", 12, ACC, MONO, "middle", 600)
d.path(f"M 720 {CY} L 758 {CY}", MUTED, 1.4, m="ar")

# 복귀 경로 (과제 완료 후 base 노드로 복귀, 중첩 ssh 금지)
RY = 232
d.path(f"M 628 {Y + BH} L 628 {RY} L 318 {RY} L 318 {Y + BH + 2}", WARN, 1.4, m="warn", dash="5 4")
d.t(473, RY + 20, "과제 완료 후 base 복귀 · 중첩 ssh 불가", 12, WARN, KR, "middle", 600)

d.legend(300, [("접속·대상 환경", INFO), ("과제 수행 지점", ACC), ("과제 간 복귀", WARN)])
d.save("01-01.exam-access.svg")
