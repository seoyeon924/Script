# 강의 제작 규칙 문서

## 파일 목록

| 파일 | 내용 |
|------|------|
| `ppt_design_rules.md` | 슬라이드 디자인 규칙 (폰트·색상·레이아웃·금지 표현) |
| `script_style_guide.md` | 강의 스크립트 말투 스타일 가이드 (구어체 규칙) |

## 다른 컴퓨터에서 작업 시작하는 방법

```bash
# 1. 레포 클론
git clone https://github.com/seoyeon924/Script.git

# 2. Claude Code 메모리에 규칙 파일 등록
mkdir -p ~/.claude/projects/-Users-sy/memory
cp _docs/ppt_design_rules.md ~/.claude/projects/-Users-sy/memory/
cp _docs/script_style_guide.md ~/.claude/projects/-Users-sy/memory/
```

> `~/.claude/projects/-Users-sy/` 경로는 홈 디렉토리가 `/Users/sy`인 경우 기준.
> 다른 경로면 Claude Code `/memory` 명령으로 현재 메모리 위치 확인 후 복사.
