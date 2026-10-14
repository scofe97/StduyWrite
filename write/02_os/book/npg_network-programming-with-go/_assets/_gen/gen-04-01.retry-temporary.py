# 타입 스펙: type-flowchart
# 사실 출처: NPG Ch.4 Listing 4-13 (p.17-18) · Go net.Error
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 560
d = D(W, H, "RETRY TEMPORARY ERRORS",
      "일시적 오류 판별과 재시도 흐름",
      "net.Error 의 Timeout 감지 시 10초 대기 후 최대 7회 재시도 및 영구 오류 즉시 반환",
      "네트워크 지연과 영구 단절을 분기하는 오류 복구 제어 흐름")

# --- 1. Start (Oval) ---
d.box(340, 86, 200, 36, fill=PAPER2, stroke=INFO, sw=1.2, r=18)
d.t(440, 108, "시작: i = 7 (최대 7회)", 11, INFO, KR, "middle", 600)

d.arrow([(440, 122), (440, 150)], MUTED, "ar", 1.4)

# --- 2. Action: conn.Write (Rect) ---
d.box(330, 150, 220, 38, fill=PAPER2, stroke=RULE, sw=1.1, r=6)
d.t(440, 167, 'conn.Write("hello world")', 11, INK, MONO, "middle", 600)
d.t(440, 181, "소켓 쓰기 호출", 11, MUTED, KR, "middle")

d.arrow([(440, 188), (440, 216)], MUTED, "ar", 1.4)

# --- 3. Decision 1: err != nil ? (Diamond) ---
d.o.append(f'<polygon points="440,216 530,242 440,268 350,242" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.2"/>')
d.t(440, 246, "err != nil ?", 11, INK, MONO, "middle", 600)

# Branch 1-No: 정상 전송 (Right -> Break)
d.arrow([(530, 242), (616, 242)], OK, "ok", 1.4)
d.t(573, 232, "nil (성공)", 11, OK, KR, "middle")

d.box(616, 224, 190, 36, fill=PAPER2, stroke=OK, sw=1.3, r=18)
d.t(711, 246, "전송 성공 (break)", 11, OK, KR, "middle", 600)

# Branch 1-Yes: 오류 발생 (Down -> Decision 2)
d.arrow([(440, 268), (440, 296)], WARN, "warn", 1.4)
d.t(474, 282, "오류 발생", 11, WARN, KR, "middle")

# --- 4. Decision 2: net.Error && Timeout() ? (Diamond, Focal!) ---
d.o.append(f'<polygon points="440,296 536,324 440,352 344,324" fill="{PAPER2}" stroke="{ACC}" stroke-width="1.4"/>')
d.t(440, 317, "net.Error 타입 단언", 11, ACC, KR, "middle", 600)
d.t(440, 332, "&& Timeout() ?", 10, ACC, MONO, "middle", 600)

# Branch 2-No: 영구 오류 (Right -> return err)
d.arrow([(536, 324), (616, 324)], BAD, "bad", 1.4)
d.t(576, 314, "영구 오류", 11, BAD, KR, "middle")

d.box(616, 306, 190, 36, fill=PAPER2, stroke=BAD, sw=1.3, r=18)
d.t(711, 328, "return err (즉시 반환)", 11, BAD, KR, "middle", 600)

# Branch 2-Yes: 일시적 타임아웃 (Down -> time.Sleep)
d.arrow([(440, 352), (440, 380)], WARN, "warn", 1.4)
d.t(474, 366, "타임아웃", 11, WARN, KR, "middle")

# --- 5. Action: time.Sleep(10s) (Rect) ---
d.box(330, 380, 220, 38, fill=PAPER2, stroke=WARN, sw=1.2, r=6)
d.t(440, 397, "time.Sleep(10 * time.Second)", 10, WARN, MONO, "middle", 600)
d.t(440, 411, "10초 대기 후 재시도", 11, MUTED, KR, "middle")

d.arrow([(440, 418), (440, 444)], MUTED, "ar", 1.4)

# --- 6. Decision 3: i > 0 (재시도 잔여)? (Diamond) ---
d.o.append(f'<polygon points="440,444 516,468 440,492 364,468" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.2"/>')
d.t(440, 472, "i > 0 ?", 11, INK, MONO, "middle", 600)

# Branch 3-No: 재시도 소진 (Right -> 한도 초과 오류)
d.arrow([(516, 468), (616, 468)], BAD, "bad", 1.4)
d.t(566, 458, "i == 0 (소진)", 11, BAD, KR, "middle")

d.box(616, 450, 190, 36, fill=PAPER2, stroke=BAD, sw=1.3, r=18)
d.t(711, 472, "한도 초과 오류 (포기)", 11, BAD, KR, "middle", 600)

# Branch 3-Yes: 재시도 루프 (Left -> Up -> conn.Write)
# Route: Left from (364, 468) to (170, 468), Up to (170, 169), Right to (330, 169)
d.arrow([(364, 468), (170, 468), (170, 169), (330, 169)], WARN, "warn", 1.4)
d.t(240, 458, "재시도 가능 (i > 0)", 11, WARN, KR, "middle")
d.t(162, 308, "i-- 차감 후 재시도", 11, MUTED, KR, "end")

# Legend (bottom margin >= 16px: 560 - (512 + 24) = 24px)
d.legend(512, [
    ("타임아웃 감지 (focal)", ACC),
    ("대기 및 재시도", WARN),
    ("영구 오류 / 포기", BAD),
    ("전송 성공", OK),
    ("초기화 상태", INFO),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-01.retry-temporary.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
