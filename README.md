# PSE_demo1 — Claude Code 마켓플레이스

아스펜 공정모사 연구 비서 플러그인(`PSE_demo1`)을 배포하는 Claude Code 마켓플레이스입니다.

## 설치 (사용자)

```
/plugin marketplace add yongha11446-cpu/PSE_demo1_marketplace
/plugin install PSE_demo1@PSE_demo1
```

설치 후 `/주제분석` `/분석시작` `/가상시뮬레이션` `/업데이트` 커맨드와
`논문탐색가`·`정독분석가`·`노벨티설계가` 에이전트, `가상시뮬-atj표준` 스킬이 활성화됩니다.

자세한 내용은 [plugins/PSE_demo1/README.md](plugins/PSE_demo1/README.md) 참고.

## 요구사항

- Windows (훅이 PowerShell 기반)
- Python + `openpyxl` (`pip install openpyxl`)

## 구조

```
PSE_demo1_marketplace/
├─ .claude-plugin/
│  └─ marketplace.json        ← 이 repo가 마켓플레이스임을 선언
└─ plugins/
   └─ PSE_demo1/              ← 실제 플러그인
      ├─ .claude-plugin/plugin.json
      ├─ commands/  skills/  agents/  hooks/  scripts/  templates/
      └─ README.md
```

## 배포 (개발자)

1. 이 폴더를 GitHub 저장소로 push (예: `PSE_demo1_marketplace`).
2. 작성자(`marketplace.json`의 `owner.name`, `plugin.json`의 `author.name`)는
   `yongha11446-cpu` 로 채워져 있다. (다른 사람이 포크하면 본인 ID로 바꾸면 됨)
3. 사용자는 위 "설치" 명령으로 바로 받는다.
