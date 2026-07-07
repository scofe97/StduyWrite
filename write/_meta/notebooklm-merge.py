#!/usr/bin/env python3
"""
notebooklm-merge.py — write/ 카테고리 하나를 NotebookLM 소스 1개로 병합한다.

목적: write/ 아래 수백 개 .md 를 NotebookLM 노트북당 소스 한도(무료 50) 안에
      넣기 위해, 카테고리 하나를 단일 .txt 로 합친다. 각 노트 앞에
      `## [상대경로]` 헤더를 붙여, NotebookLM 인용이 어느 원본 노트에서
      왔는지 추적할 수 있게 한다.

안전장치 (3중):
  - 화이트리스트 방식. 대상 카테고리를 인자로 명시해야만 처리한다.
  - `_` 로 시작하는 디렉토리(_company/_archive/_review/_meta)는 거부한다.
    특히 _company 는 사내 전용이라 Google 유출을 원천 차단한다.
  - 카테고리 안의 `_` 접두 파일(_AUDIT_*, _INDEX 등 메타·감사 문서)도 스킵한다.
  - 전송용 사본에 한해 사내 경로(okestro/tps-gitlab2 등)가 든 문장/블록을
    통째로 삭제한다. 원본 .md 는 절대 건드리지 않는다.
    (dev-standards '전송 전 redaction' 원칙 — 여기선 마스킹이 아니라 제거)

사용:
  python3 notebooklm-merge.py 04_messaging
  python3 notebooklm-merge.py 04_messaging --out /custom/path.txt

출력: write/_notebooklm/<카테고리>.txt (기본)
"""
import argparse
import re
import sys
from pathlib import Path

# 이 스크립트는 write/_meta/ 안에 있다 → write/ 는 부모의 부모
WRITE_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT_DIR = WRITE_ROOT / "_notebooklm"

FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
TITLE_RE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)

# 사내 자료 탐지 패턴 (전송용 사본에만 적용, 원본 불변).
# okestro 조직 경로·repo·Java 패키지·도메인을 포괄.
INTERNAL_RE = re.compile(
    r"okestro/[\w.-]+|tps-gitlab2|(?:org\.)?okestro\.[\w.]+"
)

# 문장 경계: 한국어 종결('다.','요.','까?','음.' 등)·마침표/물음표/느낌표 뒤.
# 사내경로가 든 문장을 통째로 지운다(토큰만 지우면 문장이 깨지므로).
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|(?<=[다요음])\.\s*")


def strip_internal_sentences(text: str) -> tuple[str, int]:
    """사내경로가 든 '줄'을 문장 단위로 정리한다. 원본은 불변, 사본에만.

    라인 단위로 순회하며, 사내경로가 든 라인은 그 라인 안에서
    사내경로를 포함하는 문장만 제거한다. 문장 분해가 애매한 라인
    (표·코드·헤더)은 라인 통째로 드롭한다. 마크다운 구조 파괴를
    피하기 위해 코드블록(``` )은 건드리지 않되, 그 안에 사내경로가
    있으면 코드블록 통째로 드롭한다.
    """
    removed = 0
    out_lines = []
    in_code = False
    code_buf = []
    code_has_internal = False

    def flush_code():
        nonlocal removed, code_has_internal
        if code_has_internal:
            removed_local = sum(1 for _ in code_buf)
            # 코드블록 통째 드롭
            return removed_local
        out_lines.extend(code_buf)
        return 0

    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                code_buf = [line]
                code_has_internal = False
            else:
                code_buf.append(line)
                if code_has_internal:
                    removed += len(code_buf)  # 통째 드롭
                else:
                    out_lines.extend(code_buf)
                in_code = False
                code_buf = []
            continue
        if in_code:
            code_buf.append(line)
            if INTERNAL_RE.search(line):
                code_has_internal = True
            continue

        if not INTERNAL_RE.search(line):
            out_lines.append(line)
            continue

        # 사내경로가 든 일반 라인 → 문장 단위로 쪼개 해당 문장만 제거
        sentences = SENTENCE_SPLIT_RE.split(line)
        if len(sentences) <= 1:
            # 문장 분해 불가(표·헤더·짧은 라인) → 라인 통째 드롭
            removed += 1
            continue
        kept = [s for s in sentences if not INTERNAL_RE.search(s)]
        removed += len(sentences) - len(kept)
        if kept:
            out_lines.append(" ".join(kept))
        # 남는 문장이 없으면 라인 자체가 사라짐

    return "\n".join(out_lines), removed


def strip_frontmatter(text: str) -> tuple[str, str | None]:
    """YAML 프론트매터를 제거하고, 있으면 title 값을 반환한다."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return text, None
    block = m.group(0)
    title_m = TITLE_RE.search(block)
    title = title_m.group(1).strip().strip('"').strip("'") if title_m else None
    return text[m.end():], title


def merge_category(category: str, out_path: Path) -> dict:
    cat_dir = WRITE_ROOT / category

    # --- 안전장치 ---
    if category.startswith("_"):
        sys.exit(f"[거부] '{category}' 는 예약 디렉토리(_)입니다. "
                 f"_company 등 사내·아카이브는 병합 대상이 아닙니다.")
    if not cat_dir.is_dir():
        sys.exit(f"[오류] 카테고리 디렉토리 없음: {cat_dir}")

    # `_` 접두 파일(_AUDIT_*, _INDEX 등 메타·감사 문서)은 학습 콘텐츠가
    # 아니고 사내 경계 정보를 담기 쉬워 제외한다.
    md_files = sorted(
        p for p in cat_dir.rglob("*.md") if not p.name.startswith("_")
    )
    skipped = sorted(
        p for p in cat_dir.rglob("*.md") if p.name.startswith("_")
    )
    if not md_files:
        sys.exit(f"[오류] {category} 안에 병합 대상 .md 파일이 없습니다.")

    parts = []
    total_words = 0
    total_redactions = 0
    for md in md_files:
        rel = md.relative_to(WRITE_ROOT)
        raw = md.read_text(encoding="utf-8")
        body, title = strip_frontmatter(raw)
        body, n_red = strip_internal_sentences(body)
        total_redactions += n_red
        header = f"## [{rel}]"
        if title:
            header += f" — {title}"
        parts.append(f"{header}\n\n{body.strip()}\n")
        total_words += len(body.split())

    merged = "\n\n".join(parts)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(merged, encoding="utf-8")

    return {
        "files": len(md_files),
        "skipped": [str(p.relative_to(WRITE_ROOT)) for p in skipped],
        "words": total_words,
        "redactions": total_redactions,
        "out": out_path,
    }


def main():
    ap = argparse.ArgumentParser(description="write/ 카테고리를 NotebookLM 소스로 병합")
    ap.add_argument("category", help="병합할 카테고리 (예: 04_messaging)")
    ap.add_argument("--out", type=Path, default=None, help="출력 경로 (기본: _notebooklm/<카테고리>.txt)")
    args = ap.parse_args()

    out_path = args.out or (DEFAULT_OUT_DIR / f"{args.category}.txt")
    result = merge_category(args.category, out_path)

    print(f"✓ 병합 완료: {result['out']}")
    print(f"  병합 .md: {result['files']}개")
    if result["skipped"]:
        print(f"  스킵(_ 접두 메타파일): {len(result['skipped'])}개 → {', '.join(result['skipped'])}")
    print(f"  본문 단어: 약 {result['words']:,} (프론트매터 제외)")
    print(f"  사내경로 문장/블록 삭제: {result['redactions']}건")

    WORD_LIMIT = 500_000
    if result["words"] > WORD_LIMIT:
        print(f"  ⚠️ 경고: 단어 수가 NotebookLM 소스 한도({WORD_LIMIT:,})를 초과. "
              f"하위폴더로 2분할 권장.")
    else:
        print(f"  단어 한도({WORD_LIMIT:,}) 여유 있음.")


if __name__ == "__main__":
    main()
