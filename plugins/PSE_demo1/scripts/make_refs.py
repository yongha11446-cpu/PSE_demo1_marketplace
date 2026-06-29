# -*- coding: utf-8 -*-
# /주제분석 표준 refs 빌더 — 논문 목록 JSON을 받아
#   ① refs/00_문헌목록.md (번호↔논문, 학습⭐, 상태표)
#   ② 각 논문의 NN_약칭_[업로드필요].txt 자리표시(링크+넣는 법)
# 를 생성한다. 이미 NN_*.pdf 가 있으면 ✅ 보유로 처리하고 자리표시는 안 만든다.
#
# 사용법: python make_refs.py <papers.json> <refs_dir>
# papers.json:
# { "topic":"...", "papers":[
#     {"rank":1,"short":"NREL2011_Humbird","name":"NREL 2011 ...","journal":"NREL 보고서",
#      "access":"OA","url":"https://...","study":true,"mustread":true}, ... ] }
#   study   = ⭐ 먼저 읽을 학습 논문(2편)
#   mustread= 📖 종합점수 상위 필독 논문(사용자가 직접 출력해 읽을 배경지식용)
import sys, json, os, glob

def main():
    if len(sys.argv) < 3:
        print("사용법: python make_refs.py <papers.json> <refs_dir>"); sys.exit(1)
    papers_json, refs_dir = sys.argv[1], sys.argv[2]
    with open(papers_json, encoding="utf-8") as f:
        data = json.load(f)
    papers = sorted(data.get("papers", []), key=lambda p: p.get("rank", 0))
    topic = data.get("topic", "")

    rows, made = [], 0
    for p in papers:
        n = int(p.get("rank", 0))
        short = p.get("short", f"paper{n}")
        name = p.get("name", "")
        jour = p.get("journal", "")
        acc = p.get("access", "")
        url = p.get("url", "")
        study = bool(p.get("study", False))
        mustread = bool(p.get("mustread", False))
        # 이미 PDF가 있는지 (NN_*.pdf)
        has_pdf = bool(glob.glob(os.path.join(refs_dir, f"{n:02d}_*.pdf")))
        status = "✅ 있음" if has_pdf else "⬜ 업로드 필요"
        star = "⭐" if study else ""
        book = "📖" if mustread else ""
        rows.append((n, star, book, name, jour, acc, status))
        # 자리표시 생성(PDF 없을 때만)
        if not has_pdf:
            fn = os.path.join(refs_dir, f"{n:02d}_{short}_[업로드필요].txt")
            star_line = "  ⭐ 먼저 읽을 학습 논문\n" if study else ""
            book_line = "  📖 필독(직접 출력해 읽을 배경지식용)\n" if mustread else ""
            txt = (f"[{n:02d}] {name}\n{star_line}{book_line}저널: {jour}  |  접근성: {acc}\n링크: {url}\n\n"
                   f"→ PDF를 받아 이 폴더에 '{n:02d}_{short}.pdf' 로 넣고, 이 자리표시 파일은 지우세요.")
            with open(fn, "w", encoding="utf-8") as g:
                g.write(txt)
            made += 1

    # 학습 논문(⭐) / 필독(📖) 목록
    studies = [r for r in rows if r[1]]
    musts = [r for r in rows if r[2]]

    # 00_문헌목록.md 작성
    lines = []
    lines.append("# refs 문헌 목록 — (번호 ↔ 논문)\n")
    lines.append(f"> 주제: {topic}\n")
    lines.append("> PDF는 `번호_약칭.pdf`로 저장. ✅=있음 / ⬜=업로드 필요(같은 번호 `[업로드필요].txt`에 링크·넣는 법).")
    lines.append("> ⭐ = 처음 공부할 때 먼저 읽을 학습 논문.  📖 = 직접 출력해 읽을 배경지식용 필독 논문.\n")
    lines.append("| 번호 | 학습 | 필독 | 논문 | 저널 | 접근성 | 상태 |")
    lines.append("|---|---|---|---|---|---|---|")
    for n, star, book, name, jour, acc, status in rows:
        lines.append(f"| {n:02d} | {star} | {book} | {name} | {jour} | {acc} | {status} |")
    if studies:
        lines.append("\n## ⭐ 먼저 읽을 학습 논문")
        for n, star, book, name, jour, acc, status in studies:
            lines.append(f"- **{n:02d}** {name} ({status})")
    if musts:
        lines.append("\n## 📖 필독 — 직접 출력해 읽으며 배경지식 잡기 (자동 분석과 별개)")
        for n, star, book, name, jour, acc, status in musts:
            lines.append(f"- **{n:02d}** {name} ({status})")
    with open(os.path.join(refs_dir, "00_문헌목록.md"), "w", encoding="utf-8") as g:
        g.write("\n".join(lines) + "\n")

    print(f"refs 생성: 문헌 {len(papers)}편, 자리표시 {made}개, 학습 {len(studies)}편, 필독 {len(musts)}편 → {refs_dir}")

if __name__ == "__main__":
    main()
