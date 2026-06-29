#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PreToolUse 훅: 자동승인(Automode) 상태여도 아래 작업은 항상 사용자에게 확인을 요청한다.
  - 제거: rm, del, rmdir, Remove-Item
  - 푸시: git push
  - 설치: pip/pip3/python -m pip install, npm install/i/ci, yarn add, pnpm add, conda install
  - 스킬: Skill 도구 사용

stdin 으로 들어온 도구 호출 정보를 보고, 해당하면
permissionDecision="ask" 를 돌려줘서 강제로 허락 창을 띄운다.
해당 없으면 아무것도 출력하지 않아 평소 권한 흐름을 그대로 따른다.
"""
import json
import re
import sys


def ask(reason: str) -> None:
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(0)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # 입력을 못 읽으면 막지 않고 통과

    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}

    # 1) 스킬 사용은 무조건 확인
    if tool == "Skill":
        name = tool_input.get("skill", "")
        ask(f"스킬 '{name}' 실행 — 자동승인이어도 확인이 필요합니다.")

    # 2) Bash 명령은 내용을 검사
    if tool == "Bash":
        cmd = tool_input.get("command", "") or ""

        rules = [
            (r"(?:^|[\s;&|(])(?:rm|del|rmdir)(?:\s|$)", "파일/폴더 제거"),
            (r"Remove-Item", "파일/폴더 제거(Remove-Item)"),
            (r"git\s+push", "원격 저장소 푸시"),
            (r"(?:pip3?|python\s+-m\s+pip)\s+install", "패키지 설치(pip)"),
            (r"npm\s+(?:install|i|ci)\b", "패키지 설치(npm)"),
            (r"yarn\s+add\b", "패키지 설치(yarn)"),
            (r"pnpm\s+add\b", "패키지 설치(pnpm)"),
            (r"conda\s+install\b", "패키지 설치(conda)"),
        ]

        for pattern, label in rules:
            if re.search(pattern, cmd, re.IGNORECASE):
                ask(f"{label} 명령 — 자동승인이어도 확인이 필요합니다: {cmd}")

    # 해당 없음 → 통과
    sys.exit(0)


if __name__ == "__main__":
    main()
