# 타입 스펙: type-process
# 사실 출처: NPG Ch.13 Listing 13-18, gopkg.in/natefinch/lumberjack.v2 Logger
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 980, 480
d = D(W, H, "PROCESS · LUMBERJACK LOG ROTATION",
      "파일 크기 초과부터 백업 압축과 만료 정리까지의 회전 흐름",
      "활성 로그 파일이 MaxSize 에 도달하면 타임스탬프 이름으로 변경해 백업하고, gzip 압축 후 오래된 파일을 정리합니다.",
      lead="로거는 일반 io.Writer 처럼 쓰며 회전과 파일 관리는 Lumberjack 내부에서 투명하게 일어납니다.")

stages = [
    ("1. 활성 파일 기록", "debug.log",
     ["zapcore.AddSync 연결", "MaxSize 100MB 미만", "io.Writer 투명 기록", "일반 로그 추가 쓰기"], INFO),
    ("2. 임계치 도달 회전", "debug.log 닫기",
     ["100MB 초과 쓰기 감지", "현재 파일 디스크립터 닫기", "타임스탬프 이름 변경", "debug-2026-10-20…log"], WARN),
    ("3. 백그라운드 압축", "gzip 압축",
     ["Compress: true 설정", "비동기 .gz 압축 수행", "debug-…log.gz 생성", "디스크 점유량 축소"], OK),
    ("4. 새 활성 파일", "새 debug.log",
     ["동일 파일명 신규 오픈", "크기 0에서 로깅 지속", "핸들 재오픈 시그널 불필요", "무중단 쓰기 이어짐"], INFO),
    ("5. 오래된 백업 정리", "보관 주기 관리",
     ["MaxBackups 5개 초과 삭제", "MaxAge 7일 경과 삭제", "디렉터리 자동 정리", "디스크 고갈 방지"], ACC),
]

BW, BH = 168, 240
Y0 = 130

for idx, (title, sub, items, c) in enumerate(stages):
    x = 26 + idx * 190
    d.tone(x, Y0, BW, BH, c, 6, "14", 1.2)
    d.t(x + BW / 2, Y0 + 28, title, 13, c, KR, "middle", 600)
    d.t(x + BW / 2, Y0 + 48, sub, 11, INK, MONO if any(ch in sub for ch in ".-_") else KR, "middle")
    d.line(x + 10, Y0 + 60, x + BW - 10, Y0 + 60, RULE, 0.8)

    y_item = Y0 + 86
    for it in items:
        d.t(x + BW / 2, y_item, it, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in it) else MONO, "middle")
        y_item += 34

    if idx < 4:
        x_arr_start = x + BW + 2
        x_arr_end = x + BW + 20
        d.arrow([(x_arr_start, Y0 + BH / 2), (x_arr_end, Y0 + BH / 2)], c=SOFT, m="soft", sw=1.3)

d.legend(410, [("활성 기록 및 재생성", INFO), ("회전 트리거", WARN), ("압축 보관", OK), ("만료 정리", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-02.lumberjack-rotation.svg"
d.save(str(svg_path))
print("ok 13-02 lumberjack-rotation")
