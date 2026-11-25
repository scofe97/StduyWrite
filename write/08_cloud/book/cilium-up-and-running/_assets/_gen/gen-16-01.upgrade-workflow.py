# 타입 스펙: type-flowchart — Cilium 마이너 업그레이드 순서와 사전 점검(preflight), 값 파일 적용 및 롤백 분기 흐름도.
# 값 근거: 16-01 본문 §2, 원문 ch16.txt 줄 170-222, docs.cilium.io/en/v1.20/operations/upgrade/ (Gateway API v1.6.1+, cilium-preflight, --reuse-values 금지, upgradeCompatibility, helm rollback)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 744
CX = 268
BW, BH = 288, 54
DW, DH = 216, 64
RX = 540
RW = 344

def fam(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

d = D(W, H, "FLOWCHART · 16-01 §2",
      "연속 마이너 확인에서 preflight·값 파일 적용까지 업그레이드 순서",
      "16-01 §2 순서도. 현재 버전의 최신 패치로 먼저 올린 뒤 연속 마이너 여부와 Upgrade Notes 를 확인한다. "
      "cilium-preflight 로 새 이미지를 노드마다 미리 받아 READY 수를 맞춘 다음 삭제하고, --reuse-values 없이 값 파일과 upgradeCompatibility 로 helm upgrade 를 실행한다. "
      "롤아웃이 틀어지면 helm rollback 으로 최신 패치 상태로 되돌린다.",
      lead="타원은 시작·끝, 마름모는 점검 분기, 아래로 정상 경로가 이어집니다.")

def oval(cx, y, w, h, title, sub, c=MUTED):
    d.tone(cx - w / 2, y, w, h, c, r=24, op="14", sw=1.2)
    d.t(cx, y + 21, title, 13, c if c != MUTED else INK, fam(title), "middle", 600)
    d.t(cx, y + 39, sub, 11 if fam(sub) == MONO else 12, MUTED, fam(sub), "middle")

def step(cx, y, w, h, title, sub, c=MUTED, focal=False):
    if focal:
        d.tone(cx - w / 2, y, w, h, c, r=6, op="18", sw=1.4)
    elif c != MUTED:
        d.tone(cx - w / 2, y, w, h, c, r=6, op="12", sw=1.0)
    else:
        d.box(cx - w / 2, y, w, h, PAPER2, RULE, 1.0, r=6)
    d.t(cx, y + 22, title, 13, c if focal else INK, fam(title), "middle", 600)
    d.t(cx, y + 41, sub, 11 if fam(sub) == MONO else 12, MUTED, fam(sub), "middle")

def diamond(cx, cy, w, h, label):
    hw, hh = w / 2, h / 2
    pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{SOFT}" stroke-width="1.2"/>')
    d.t(cx, cy + 4, label, 13, INK, fam(label), "middle", 600)

Y0 = 92;  H0 = 48
Y1 = 156; H1 = 52
CY2 = 256
Y3 = 308; H3 = 52
CY4 = 408
Y5 = 460; H5 = 54
CY6 = 562
Y7 = 616; H7 = 48
LEG_Y = 684

# 세로 연결선 (먼저 그려 도형 뒤에 깐다)
d.arrow([(CX, Y0 + H0), (CX, Y1 - 2)], MUTED, "ar", 1.3)
d.arrow([(CX, Y1 + H1), (CX, CY2 - 34)], OK, "ok", 1.3)
d.arrow([(CX, CY2 + 32), (CX, Y3 - 2)], OK, "ok", 1.3)
d.t(CX + 10, CY2 + 45, "예", 12, OK, KR, "start", 600)
d.arrow([(CX, Y3 + H3), (CX, CY4 - 34)], OK, "ok", 1.3)
d.arrow([(CX, CY4 + 32), (CX, Y5 - 2)], ACC, "acc", 1.4)
d.t(CX + 10, CY4 + 45, "예", 12, ACC, KR, "start", 600)
d.arrow([(CX, Y5 + H5), (CX, CY6 - 34)], ACC, "acc", 1.4)
d.arrow([(CX, CY6 + 32), (CX, Y7 - 2)], OK, "ok", 1.3)
d.t(CX + 10, CY6 + 45, "예", 12, OK, KR, "start", 600)

# 오른쪽 분기 화살표
d.arrow([(CX + DW / 2, CY2), (RX - 3, CY2)], BAD, "bad", 1.4)
d.t((CX + DW / 2 + RX) / 2, CY2 - 8, "아니오", 12, BAD, KR, "middle", 600)

d.arrow([(CX + DW / 2, CY4), (RX - 3, CY4)], WARN, "warn", 1.4)
d.t((CX + DW / 2 + RX) / 2, CY4 - 8, "아니오", 12, WARN, KR, "middle", 600)

d.line(CX + BW / 2 + 2, Y5 + H5 / 2, RX - 2, Y5 + H5 / 2, BAD, 1.2, "4 3")

d.arrow([(CX + DW / 2, CY6), (RX - 3, CY6)], WARN, "warn", 1.4)
d.t((CX + DW / 2 + RX) / 2, CY6 - 8, "아니오", 12, WARN, KR, "middle", 600)

# 메인 스파인 노드
oval(CX, Y0, BW, H0, "업그레이드 시작", "현재 X.Y.Z · Upgrade Notes 확인", MUTED)
step(CX, Y1, BW, H1, "최신 패치로 먼저 올리기", "X.Y.최신 Z · 롤백 대비", OK)
diamond(CX, CY2, DW, 64, "연속 마이너인가")
step(CX, Y3, BW, H3, "cilium-preflight 설치", "agent=false · preflight.enabled=true")
diamond(CX, CY4, DW, 64, "READY 수 일치")
step(CX, Y5, BW, H5, "preflight 삭제 · helm upgrade", "-f values · upgradeCompatibility", ACC, focal=True)
diamond(CX, CY6, DW, 64, "검증 정상 동작")
oval(CX, Y7, BW, H7, "업그레이드 완료", "모든 구성 요소 버전 일치", OK)

# 오른쪽 분기·주의 노드
step(RX + RW / 2, CY2 - 26, RW, 52, "마이너 건너뛰기 금지", "1.1 → 1.3 불가 · 단계 분할", BAD)
step(RX + RW / 2, CY4 - 26, RW, 52, "이미지 풀 완료 대기", "DaemonSet·Deployment READY 까지 대기", WARN)
step(RX + RW / 2, Y5, RW, H5, "--reuse-values 사용 금지", "새 릴리스 값 누락 · helm get values 점검", BAD)
step(RX + RW / 2, CY6 - 26, RW, 52, "helm rollback 실행", "직전 리비전으로 복귀", WARN)

d.legend(LEG_Y, [("정상 경로", OK), ("금지 · 중단", BAD), ("대기 · 롤백", WARN), ("핵심 적용 단계", ACC)])
d.save("16-01.upgrade-workflow.svg")
