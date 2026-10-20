# 타입 스펙: type-sequence
# 사실 출처: NPG Ch.13 Listing 13-2, 13-3, go doc io.MultiWriter
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, MONO, KR

W, H = 940, 770
s = Seq(W, H, "SEQUENCE · MULTIWRITER ERROR BEHAVIOR",
        "쓰기 오류 발생 시 io.MultiWriter 와 sustainedMultiWriter 의 동작 비교",
        "io.MultiWriter 는 첫 writer 에서 오류가 나면 즉시 중단되어 뒤쪽 출력을 건너뜁니다. "
        "반면 sustainedMultiWriter 는 오류가 나도 모든 writer 에 끝까지 쓰고 에러를 누적 반환합니다.",
        lead="한쪽 출력(디스크 풀 등) 장애가 다른 출력(터미널 표준 출력)의 로그 유실로 번지는 현상을 막습니다.")

s.lanes([("호출자", "Logger"),
         ("다중 출력기", "MultiWriter"),
         ("파일 Writer", "1순위 대상"),
         ("os.Stdout", "2순위 대상")], y0=104, lane_w=170)

# 구분 1: io.MultiWriter (Fail-Stop)
s.t(36, 170, "[A] io.MultiWriter — 첫 쓰기 오류 시 즉시 중단 (Fail-Stop)", 12, BAD, KR, "start", 600)

s.msg("호출자", "다중 출력기", "Write(p)", 198, INFO, "info", sub="로그 바이트 쓰기 요청")
s.msg("다중 출력기", "파일 Writer", "Write(p)", 244, WARN, "warn", sub="첫째 writer 에 쓰기")
s.msg("파일 Writer", "다중 출력기", "err != nil (ENOSPC)", 290, BAD, "bad", dash="4 4", sub="디스크 공간 부족 오류")

# 중단 표시
x_mw = s.LX["다중 출력기"]
x_fw = s.LX["파일 Writer"]
x_out = s.LX["os.Stdout"]
x_gap = (x_fw + x_out) / 2
s.line(x_mw + 20, 330, x_out - 20, 330, BAD, 1.2, "3 3")
s.t(x_gap, 320, "호출 중단 (건너뜀)", 11, BAD, KR, "middle", 600)
s.t(x_gap, 350, "표준 출력 로그 유실", 11, SOFT, KR, "middle")

s.msg("다중 출력기", "호출자", "return (n, err)", 380, BAD, "bad", dash="4 4", sub="즉시 에러 반환 및 중단")

# 구분선
s.line(24, 412, W - 24, 412, RULE, 1.0)

# 구분 2: sustainedMultiWriter (Sustained)
s.t(36, 436, "[B] sustainedMultiWriter — 오류 발생 시에도 모든 대상에 지속 쓰기", 12, OK, KR, "start", 600)

s.msg("호출자", "다중 출력기", "Write(p)", 464, INFO, "info", sub="로그 바이트 쓰기 요청")
s.msg("다중 출력기", "파일 Writer", "Write(p)", 510, WARN, "warn", sub="첫째 writer 쓰기 시도")
s.msg("파일 Writer", "다중 출력기", "wErr (ENOSPC)", 556, BAD, "bad", dash="4 4", sub="오류 발생")

s.msg("다중 출력기", "os.Stdout", "Write(p)", 602, OK, "ok", sub="중단 없이 다음 writer 진행")
s.msg("os.Stdout", "다중 출력기", "return (n, nil)", 648, OK, "ok", dash="4 4", sub="정상 출력 성공")

s.msg("다중 출력기", "호출자", "return (n, multierr)", 692, ACC, "acc", dash="4 4", sub="가장 적게 쓴 writer 의 바이트 수 · 누적 오류")

s.rails(706)
s.legend(726, [("호출 흐름", INFO), ("정상 쓰기", OK), ("에러 발생", BAD), ("누적 반환", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-01.multiwriter-error-handling.svg"
s.save(str(svg_path))
print("ok 13-01 multiwriter-error-handling")
