# 타입 스펙: type-process
# 01-03.chapter-overview — 두 문제에서 세 축, 6종 빌더 비교와 실행 환경별 선택 흐름
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 960, 410

d = D(W, H, "CONTAINER · 01-03 OVERVIEW",
      "이미지 빌더 선정과 아키텍처 흐름",
      "두 문제와 세 축 기준에서 6종 빌더 비교와 실행 환경별 선택 흐름",
      lead="문제 정의에서 분류 축, 도구 비교를 거쳐 환경별 선택에 이르는 4단계 흐름")

steps = ("1 문제", "2 세 축", "3 비교", "4 선택과 한계")
col_w = 210
gap = 24
start_x = 24
y_top = 114
h_box = 88
y_mid = 222
h_mid = 88

# 4개 단계 박스
# 1단계: 문제 (01-01, 01-02)
x0 = start_x
d.t(x0 + col_w // 2, y_top - 12, "1단계: 문제 정의", 14, MUTED, KR, "middle", 600)
d.tone(x0, y_top, col_w, h_box, WARN, 6, "12", 1.2)
d.t(x0 + col_w // 2, y_top + 28, "데몬 권한 상승", 13, WARN, KR, "middle", 600)
d.t(x0 + col_w // 2, y_top + 50, "소켓 공유 시 호스트 장악", 12, INK, KR, "middle")
d.t(x0 + col_w // 2, y_top + 70, "01-01 컨테이너 안 빌드", 11, SOFT, KR, "middle")

d.tone(x0, y_mid, col_w, h_mid, WARN, 6, "12", 1.2)
d.t(x0 + col_w // 2, y_mid + 28, "rootless 환경 제약", 13, WARN, KR, "middle", 600)
d.t(x0 + col_w // 2, y_mid + 50, "새 네임스페이스와 권한", 12, INK, KR, "middle")
d.t(x0 + col_w // 2, y_mid + 70, "01-02 rootless 조건", 11, SOFT, KR, "middle")

# 화살표 1 -> 2 (상단)
d.arrow([(x0 + col_w + 2, y_top + h_box // 2), (x0 + col_w + gap - 2, y_top + h_box // 2)], MUTED, "ar", 1.3)
# 화살표 1 -> 2 (하단)
d.arrow([(x0 + col_w + 2, y_mid + h_mid // 2), (x0 + col_w + gap - 2, y_mid + h_mid // 2)], MUTED, "ar", 1.3)

# 2단계: 세 축
x1 = x0 + col_w + gap
d.t(x1 + col_w // 2, y_top - 12, "2단계: 세 가지 축", 14, MUTED, KR, "middle", 600)
d.tone(x1, y_top, col_w, h_box, INFO, 6, "12", 1.2)
d.t(x1 + col_w // 2, y_top + 28, "데몬 유무 · rootless", 13, INFO, KR, "middle", 600)
d.t(x1 + col_w // 2, y_top + 50, "백그라운드 데몬 의존성", 12, INK, KR, "middle")
d.t(x1 + col_w // 2, y_top + 70, "비특권 사용자 실행 여부", 11, SOFT, KR, "middle")

d.tone(x1, y_mid, col_w, h_mid, INFO, 6, "12", 1.2)
d.t(x1 + col_w // 2, y_mid + 28, "Dockerfile 필요 여부", 13, INFO, KR, "middle", 600)
d.t(x1 + col_w // 2, y_mid + 50, "명세 파일 필요성", 12, INK, KR, "middle")
d.t(x1 + col_w // 2, y_mid + 70, "소스 감지 및 언어 플러그인", 11, SOFT, KR, "middle")

# 화살표 2 -> 3 (상단)
d.arrow([(x1 + col_w + 2, y_top + h_box // 2), (x1 + col_w + gap - 2, y_top + h_box // 2)], MUTED, "ar", 1.3)
# 화살표 2 -> 3 (하단)
d.arrow([(x1 + col_w + 2, y_mid + h_mid // 2), (x1 + col_w + gap - 2, y_mid + h_mid // 2)], MUTED, "ar", 1.3)

# 3단계: 도구 지형 (6종 도구)
x2 = x1 + col_w + gap
d.t(x2 + col_w // 2, y_top - 12, "3단계: 도구 지형", 14, MUTED, KR, "middle", 600)
d.tone(x2, y_top, col_w, h_box, ACC, 6, "12", 1.2)
d.t(x2 + col_w // 2, y_top + 28, "범용 빌더 4종", 13, ACC, KR, "middle", 600)
d.t(x2 + col_w // 2, y_top + 50, "Docker · BuildKit", 12, INK, KR, "middle")
d.t(x2 + col_w // 2, y_top + 70, "Buildah · Kaniko(보관)", 11, SOFT, KR, "middle")

d.tone(x2, y_mid, col_w, h_mid, ACC, 6, "12", 1.2)
d.t(x2 + col_w // 2, y_mid + 28, "특화·다언어 빌더", 13, ACC, KR, "middle", 600)
d.t(x2 + col_w // 2, y_mid + 50, "Jib (JVM 최적화)", 12, INK, KR, "middle")
d.t(x2 + col_w // 2, y_mid + 70, "Buildpacks (소스 감지)", 11, SOFT, KR, "middle")

# 화살표 3 -> 4 (상단)
d.arrow([(x2 + col_w + 2, y_top + h_box // 2), (x2 + col_w + gap - 2, y_top + h_box // 2)], MUTED, "ar", 1.3)
# 화살표 3 -> 4 (하단)
d.arrow([(x2 + col_w + 2, y_mid + h_mid // 2), (x2 + col_w + gap - 2, y_mid + h_mid // 2)], MUTED, "ar", 1.3)

# 4단계: 선택과 한계
x3 = x2 + col_w + gap
d.t(x3 + col_w // 2, y_top - 12, "4단계: 선택과 분업", 14, MUTED, KR, "middle", 600)
d.tone(x3, y_top, col_w, h_box, OK, 6, "12", 1.2)
d.t(x3 + col_w // 2, y_top + 28, "환경별 도구 선택", 13, OK, KR, "middle", 600)
d.t(x3 + col_w // 2, y_top + 50, "VM · 일반 Pod · 엄격 Pod", 12, INK, KR, "middle")
d.t(x3 + col_w // 2, y_top + 70, "언어 및 Dockerfile 유무", 11, SOFT, KR, "middle")

d.tone(x3, y_mid, col_w, h_mid, OK, 6, "12", 1.2)
d.t(x3 + col_w // 2, y_mid + 28, "오케스트레이터 분업", 13, OK, KR, "middle", 600)
d.t(x3 + col_w // 2, y_mid + 50, "빌더: 이미지 생성 전담", 12, INK, KR, "middle")
d.t(x3 + col_w // 2, y_mid + 70, "오케스트레이터: 파이프라인 조율", 11, SOFT, KR, "middle")

# 범례
LEG_Y = 346
d.legend(LEG_Y, [
    ("문제 배경", WARN),
    ("분류 축", INFO),
    ("도구 지형 (focal)", ACC),
    ("선택 및 분업", OK),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "01-03.chapter-overview.svg")
d.save(out_path)
print("ok gen-01-03.chapter-overview")
