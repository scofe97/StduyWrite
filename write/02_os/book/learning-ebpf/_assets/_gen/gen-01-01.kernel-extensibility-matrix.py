# 타입 스펙: type-dp-security-matrix — 업스트림 커널 패치·커널 모듈·eBPF 세 가지 커널 확장 방식의 특성 및 제약 비교 행렬
# 사실 출처: 원문 ebpf1.txt 272-363(패치 채택률 33%·배포판 수년 지연·모듈 커널 패닉 위험·eBPF 검증기 안전 보장)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W = 920
LP, LBL_W, GAP, COL_W = 20, 196, 16, 212
HDR_Y, HDR_H, ROW_Y0, STRIDE, ROW_H = 100, 44, 156, 56, 48

cols = ["업스트림 커널 패치", "커널 모듈 (LKM)", "eBPF 프로그램"]
rows = [
    ("반영까지 걸리는 시간", "수년 (배포판 지연)", "즉시 (독립 바이너리)", "즉시 (동적 적재)"),
    ("커널 재부팅 필요", "필수 (새 커널 부팅)", "불필요 (동적 삽입)", "불필요 (실행 중 적재)"),
    ("시스템 충돌 안전성", "검증됨 (하드닝 거침)", "위험 (머신 전체 정지)", "안전 보장 (검증기 검사)"),
    ("배포 및 실행 방식", "배포판 커널 패키지", "모듈 적재", "bpf() 시스템 콜"),
]

LEG_Y = ROW_Y0 + len(rows) * STRIDE + 8
H = LEG_Y + 54

d = D(W, H, "LEARNING EBPF · 01-01 §3", "커널 확장 방식 세 가지의 특성 비교",
      "업스트림 기여·커널 모듈·eBPF 프로그램의 배포 주기와 안전 보장 모델을 대조합니다",
      "행 = 평가 축 · 열 = 확장 방식 · 안전성과 속도의 트레이드오프 해소")

def cx(j): return LP + LBL_W + GAP + j * (COL_W + GAP)

# 헤더 행
d.box(LP, HDR_Y, LBL_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LP + LBL_W / 2, HDR_Y + 27, "평가 기준", 13, INK, KR, "middle", 600)
for j, c in enumerate(cols):
    col_tone = ACC if j == 2 else PAPER2
    sw = 1.3 if j == 2 else 0.9
    if j == 2:
        d.tone(cx(j), HDR_Y, COL_W, HDR_H, ACC, r=6, op="14", sw=sw)
        d.t(cx(j) + COL_W / 2, HDR_Y + 27, c, 13, ACC, KR, "middle", 600)
    else:
        d.box(cx(j), HDR_Y, COL_W, HDR_H, PAPER2, RULE, sw, 6)
        d.t(cx(j) + COL_W / 2, HDR_Y + 27, c, 13, INK, KR, "middle", 600)

# 데이터 행
for i, (lab, a, b, c) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, LBL_W, ROW_H, PAPER2, RULE, 0.9, 4)
    d.t(LP + 16, y + 29, lab, 12, INK, KR, "start", 600)

    # Col 0: 업스트림
    d.tone(cx(0), y, COL_W, ROW_H, INFO, r=4, op="08", sw=0.9)
    d.t(cx(0) + COL_W / 2, y + 29, a, 12, INFO, KR, "middle")

    # Col 1: 커널 모듈
    c1_col = BAD if "위험" in b else WARN
    d.tone(cx(1), y, COL_W, ROW_H, c1_col, r=4, op="08", sw=0.9)
    d.t(cx(1) + COL_W / 2, y + 29, b, 12, c1_col, KR, "middle")

    # Col 2: eBPF (Focal Column)
    if i == 2:  # 안전 보장 (핵심 셀)
        d.tone(cx(2), y, COL_W, ROW_H, ACC, r=4, op="18", sw=1.4)
        d.t(cx(2) + COL_W / 2, y + 29, c, 12, ACC, KR, "middle", 600)
    else:
        d.tone(cx(2), y, COL_W, ROW_H, OK, r=4, op="12", sw=1.1)
        d.t(cx(2) + COL_W / 2, y + 29, c, 12, OK, KR, "middle", 600)

d.legend(LEG_Y, [
    ("업스트림", INFO),
    ("커널 모듈", WARN),
    ("정지 위험", BAD),
    ("eBPF 안전", OK),
    ("핵심 이점", ACC),
])
d.save("01-01.kernel-extensibility-matrix.svg")
