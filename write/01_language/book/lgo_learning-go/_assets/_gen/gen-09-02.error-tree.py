# 09-02.error-tree — fileChecker 가 만든 오류 트리와 errors.Is 가 그 안을 내려가며 비교하는 모습
# 본문 요구(09-02 §3 「errors.Is 는 트리에서 특정 인스턴스를 찾습니다」): fmt.Errorf("in fileChecker: %w") 가 os.Open 의
#           *fs.PathError 를 감싸고, 그것이 다시 syscall.Errno(ENOENT)를 감싼다. errors.Is(err, os.ErrNotExist) 는 위에서부터
#           == 로 비교하다가 ENOENT 의 Is 메서드가 true 를 돌려 멈춘다. errors.As(&pe) 는 둘째 층에서 타입이 맞는다.
# 타입 스펙: type-tree — 세로 사슬(root → 자식 → 손자), 노드 폭 360, 층 간격 112. 오른쪽 열에 층마다 Is·As 판정 칩.
#           focal 은 Is 메서드가 true 를 돌리는 맨 아래 층 판정 하나.
# 사실 출처: Learning Go 2판 9장 「Wrapping Errors」·「Is and As」, go1.25.1 실행(2026-09-27) — Unwrap 타입 *fs.PathError,
#           그 아래 syscall.Errno, errors.Is(err, os.ErrNotExist) true, errors.As(err, &pe) true · open not_here.txt.
#           트리 구조의 세부는 원문 밖 확인이다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 540
NX, NW, NH = 36, 360, 76
YS = [132, 244, 356]
JX, JW = 488, 216
AX, AW = 724, 224

nodes = [("*fmt.wrapError", "in fileChecker: open not_here.txt: …", "fmt.Errorf 의 %w"),
         ("*fs.PathError", "open not_here.txt: no such file…", "os.Open 이 돌려준 오류"),
         ("syscall.Errno", "ENOENT · no such file or directory", "운영체제 오류 번호")]
is_res = [("== ErrNotExist? 아님", BAD), ("== ErrNotExist? 아님", BAD), ("Is 메서드 → true", ACC)]
as_res = [("*fs.PathError? 아님", BAD), ("타입 맞음 → pe 에 대입", OK), ("", None)]

d = D(W, H, "TREE · 09-02 §3",
      "fileChecker 가 만든 오류 트리",
      "fileChecker 가 돌려준 오류는 세 층이다. 맨 위는 %w 로 감싼 오류, 그 아래는 os.Open 의 *fs.PathError, 맨 아래는 syscall.Errno(ENOENT)다. "
      "errors.Is(err, os.ErrNotExist) 는 위에서부터 == 로 비교하다 맨 아래 ENOENT 의 Is 메서드가 ErrNotExist 와 맞다고 답해 true 가 된다. "
      "errors.As(err, &pe) 는 둘째 층에서 *fs.PathError 타입이 맞아 그 오류를 pe 에 대입한다.",
      lead="왼쪽은 Unwrap 으로 이어진 오류 사슬, 가운데와 오른쪽은 각 층에서 Is·As 가 내린 판정입니다.")

d.t(JX + JW // 2, 116, "errors.Is(err, os.ErrNotExist)", 12, MUTED, MONO, "middle", 600)
d.t(AX + AW // 2, 116, "errors.As(err, &pe)", 12, MUTED, MONO, "middle", 600)
for i, (typ, msg, sub) in enumerate(nodes):
    y = YS[i]
    d.box(NX, y, NW, NH)
    d.t(NX + 20, y + 26, typ, 14, INK, MONO, "start", 600)
    d.t(NX + 20, y + 46, msg, 12, MUTED, MONO, "start")
    d.t(NX + 20, y + 64, sub, 11, MUTED, KR, "start")
    if i < 2:
        d.arrow([(NX + 60, y + NH), (NX + 60, YS[i + 1] - 2)], SOFT, "soft", 1.2)
        d.t(NX + 72, y + NH + 22, "Unwrap", 11, MUTED, MONO, "start")
    txt, c = is_res[i]
    d.tone(JX, y + 18, JW, 40, c, 4, "22" if c == ACC else "14", 1.4 if c == ACC else 1.0)
    d.t(JX + JW // 2, y + 43, txt, 12, c, KR, "middle", 600)
    txt, c = as_res[i]
    if c:
        d.tone(AX, y + 18, AW, 40, c, 4, "14", 1.0)
        d.t(AX + AW // 2, y + 43, txt, 12, c, KR, "middle", 600)
    else:
        d.t(AX + AW // 2, y + 43, "이미 멈춤", 12, SOFT, KR, "middle")

d.legend(484, [("일치하지 않음", BAD), ("타입이 맞음", OK), ("Is 메서드가 맞다고 답함", ACC)])
d.save("09-02.error-tree.svg")
print("ok 09-02 error-tree")
