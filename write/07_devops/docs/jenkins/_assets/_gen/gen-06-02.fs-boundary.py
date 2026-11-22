# 사실 출처: 06-02.빌드 격리와 공격 표면.md 57~71행
# 타입 스펙: type-layers
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 504

d = D(
    W, H,
    "JENKINS · FILESYSTEM ISOLATION LAYERS",
    "파일시스템 방어 계층과 워킹 디렉토리 경계",
    "셸 옵션의 한계부터 비-root 실행, 루트 읽기 전용화, 그리고 임시 Pod 에 이르는 파일시스템 격리 4계층",
    lead="앞 방어의 구멍(셸 옵션·비-root)을 뒤 방어(루트 읽기 전용·임시 Pod)가 메워 파괴 명령을 워킹 디렉토리에 가둡니다."
)

# 좌측 진행 화살표 (방어 단계 진행: 상단 셸 옵션 → 하단 임시 Pod 격리)
d.t(44, 116, "방어 단계 ↓", 11, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(44, 128), (44, 396)], SOFT, "soft", 1.2)
d.t(44, 412, "격리 완성", 11, SOFT, fam=KR, anchor="middle")

LX, LW = 88, 848

# ── L1: 셸 옵션 ────────────────────────────────────────────────────────
y_l1 = 96
h_l1 = 64
d.box(LX, y_l1, LW, h_l1, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
# 태그
d.box(LX + 12, y_l1 + 18, 32, 28, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(LX + 28, y_l1 + 36, "L1", 11, SOFT, fam=MONO, anchor="middle", weight=600)
# 계층명 및 설명
d.t(LX + 56, y_l1 + 27, "셸 옵션 (set -e · set -u)", 14, INK, fam=KR, anchor="start", weight=600)
d.t(LX + 56, y_l1 + 47, "sh 스텝에 선언하는 옵션", 11, MUTED, fam=KR, anchor="start")
d.chip(LX + 400, y_l1 + 24, "정상 성공 종료로 통과", BAD, size=11)
d.t(LX + LW - 18, y_l1 + 38, "cd / · rm -rf / 차단 불가 (악의적 명령과 정상 명령 구분 불가)", 11, MUTED, fam=KR, anchor="end")

# ── L2: 비-root 실행 ───────────────────────────────────────────────────
y_l2 = 176
h_l2 = 64
d.box(LX, y_l2, LW, h_l2, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
# 태그
d.box(LX + 12, y_l2 + 18, 32, 28, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(LX + 28, y_l2 + 36, "L2", 11, SOFT, fam=MONO, anchor="middle", weight=600)
# 계층명 및 설명
d.t(LX + 56, y_l2 + 27, "비-root 실행 (전용 계정)", 14, INK, fam=KR, anchor="start", weight=600)
d.t(LX + 56, y_l2 + 47, "Jenkins 프로세스 root 권한 박탈", 11, MUTED, fam=KR, anchor="start")
d.chip(LX + 400, y_l2 + 24, "시스템 파일 접근 거부", OK, size=11)
d.t(LX + LW - 18, y_l2 + 38, "/etc/shadow 시스템 보호 vs 쓰기 허용 영역 파괴 잔류", 11, MUTED, fam=KR, anchor="end")

# ── L3: 워킹 디렉토리 경계 (Focal Layer) ───────────────────────────────
y_l3 = 256
h_l3 = 88
d.tone(LX, y_l3, LW, h_l3, ACC, r=6, op="12", sw=1.4)
# 태그
d.box(LX + 12, y_l3 + 18, 32, 28, fill=PAPER, stroke=ACC, sw=0.8, r=4)
d.t(LX + 28, y_l3 + 36, "L3", 11, ACC, fam=MONO, anchor="middle", weight=600)
# 계층명 및 설명
d.t(LX + 56, y_l3 + 27, "워킹 디렉토리 경계 (루트 읽기 전용화)", 14, INK, fam=KR, anchor="start", weight=600)
d.t(LX + 56, y_l3 + 46, "루트 파일시스템 전체 읽기 전용화 · JENKINS_HOME 과 워크스페이스만 허용", 11, MUTED, fam=KR, anchor="start")
d.chip(LX + 440, y_l3 + 24, "rm -rf / 파일 삭제 차단", ACC, size=11)
d.t(LX + LW - 18, y_l3 + 26, "허용 경로 외 삭제 거부", 11, MUTED, fam=KR, anchor="end")

# L3 하단 배포 환경별 구현
d.t(LX + 56, y_l3 + 68, "배포 환경별 선언:", 11, ACC, fam=KR, anchor="start", weight=600)
d.chip(LX + 240, y_l3 + 66, "systemd: ProtectSystem=strict", INFO, size=10)
d.chip(LX + 476, y_l3 + 66, "Docker: --read-only", INFO, size=10)
d.chip(LX + 700, y_l3 + 66, "K8s: readOnlyRootFilesystem", INFO, size=10)

# ── L4: 남는 위험과 임시 Pod ───────────────────────────────────────────
y_l4 = 360
h_l4 = 64
d.box(LX, y_l4, LW, h_l4, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
# 태그
d.box(LX + 12, y_l4 + 18, 32, 28, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(LX + 28, y_l4 + 36, "L4", 11, SOFT, fam=MONO, anchor="middle", weight=600)
# 계층명 및 설명
d.t(LX + 56, y_l4 + 27, "빌드 격리 (임시 Pod)", 14, INK, fam=KR, anchor="start", weight=600)
d.t(LX + 56, y_l4 + 47, "동일 에이전트 내 빌드 간 데이터 접근 방어", 11, MUTED, fam=KR, anchor="start")
d.chip(LX + 400, y_l4 + 24, "빌드 간 데이터 격리", OK, size=11)
d.t(LX + LW - 18, y_l4 + 38, "빌드마다 새 에이전트(임시 Pod) 생성으로 데이터 접촉 차단", 11, MUTED, fam=KR, anchor="end")

# ── 범례 ────────────────────────────────────────────────────────────────
LEG_Y = 448
d.legend(LEG_Y, [
    ("워킹 디렉토리 경계", ACC),
    ("방어 성공", OK),
    ("방어 구멍", BAD),
    ("배포 환경별 선언", INFO),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "06-02.fs-boundary.svg")
d.save(out_path)
print(f"saved: {out_path}")
