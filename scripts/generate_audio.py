#!/usr/bin/env python3
"""
스크립트 .md → 나레이션 추출 → ElevenLabs TTS → MP3
사용: python3 generate_audio.py <script.md> [output.mp3]
"""

import sys
import re
import os
import json
import urllib.request
import urllib.error

# ── 설정 ────────────────────────────────────────────────────
ENV_FILE = os.path.join(os.path.dirname(__file__), "../.elevenlabs.env")

def load_env(path):
    env = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

cfg = load_env(ENV_FILE)
API_KEY  = cfg.get("ELEVENLABS_API_KEY", os.environ.get("ELEVENLABS_API_KEY", ""))
VOICE_ID = cfg.get("ELEVENLABS_VOICE_ID", "PKCQixu576r2HwnYdK7U")
MODEL    = cfg.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")

# ── 스킵할 섹션 이름 ─────────────────────────────────────────
SKIP_SECTIONS = re.compile(
    r"^(📌\s*클립\s*정보|🗒️\s*서연\s*메모|직접\s*해보기|준비물|참고\s*링크)",
    re.IGNORECASE
)

# ── 텍스트 정제 ──────────────────────────────────────────────
def clean_script(text):
    # 1) frontmatter 제거
    text = re.sub(r"^---[\s\S]+?---\n", "", text.strip())

    # 2) 섹션 분리 후 불필요 섹션 제거
    parts = re.split(r"\n(#{1,3} .+)\n", text)
    result_parts = []
    skip = False

    i = 0
    while i < len(parts):
        chunk = parts[i]

        # 헤더 청크인지 확인
        header_match = re.match(r"#{1,3} (.+)", chunk.strip())
        if header_match:
            title = header_match.group(1).strip()
            # 타이틀에서 이모지/번호 제거한 핵심 부분 추출
            title_clean = re.sub(r"[^\w\s가-힣]", " ", title).strip()
            if SKIP_SECTIONS.search(title):
                skip = True
            else:
                skip = False
        else:
            # 본문 청크
            if not skip:
                result_parts.append(chunk)

        i += 1

    body = "\n".join(result_parts)

    # 3) 코드 블록 제거
    body = re.sub(r"```[\s\S]+?```", "", body)

    # 4) 참고 링크 블록 제거 (> 로 시작하는 인용 전체)
    body = re.sub(r"(>.*\n?)+", "", body)

    # 5) [화면: ...] 지시문 제거
    body = re.sub(r"\[화면:.*?\]", "", body)
    body = re.sub(r"\*\*\[화면:.*?\]\*\*", "", body)

    # 6) 마크다운 문법 제거
    body = re.sub(r"\*\*(.+?)\*\*", r"\1", body)  # 볼드
    body = re.sub(r"\*(.+?)\*", r"\1", body)       # 이탤릭
    body = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", body) # 링크
    body = re.sub(r"^#{1,6}\s+", "", body, flags=re.MULTILINE)  # 남은 헤더
    body = re.sub(r"^[-•*]\s+", "", body, flags=re.MULTILINE)   # 불릿

    # 7) 빈 줄 정리
    body = re.sub(r"\n{3,}", "\n\n", body)

    # 8) 표(|) 제거
    body = re.sub(r"^\|.*\|.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^[-|: ]+$", "", body, flags=re.MULTILINE)

    # 9) 아스키 다이어그램 / 화살표 정리
    body = re.sub(r"[↓→←↑├└│─┐┘]", "", body)
    body = re.sub(r"```", "", body)

    # 10) 고아 볼드 기호 / 코드 명령어 줄 제거
    body = re.sub(r"^\*+$", "", body, flags=re.MULTILINE)  # 고아 **
    body = re.sub(r"^`+$", "", body, flags=re.MULTILINE)   # 고아 ```

    # 11) 셸 명령어처럼 보이는 줄 제거 (mkdir, printf, claude, python 등)
    body = re.sub(
        r"^(mkdir|cd |printf|claude|python|pip|npm|curl|echo|cat |ls |git |data\.csv|\.\/|~\/).*$",
        "", body, flags=re.MULTILINE | re.IGNORECASE
    )

    # 12) 최종 공백 정리
    lines = [l.strip() for l in body.split("\n")]
    lines = [l for l in lines if l]
    return "\n".join(lines)

# ── TTS API 호출 (10000자 청크 분할) ────────────────────────
CHUNK_SIZE = 4500  # ElevenLabs 권장 최대

def call_tts(text_chunk, idx):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    payload = json.dumps({
        "text": text_chunk,
        "model_id": MODEL,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.2,
            "use_speaker_boost": True
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
    )
    print(f"  [청크 {idx+1}] {len(text_chunk)}자 → 요청 중...")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        print(f"  [ERROR] HTTP {e.code}: {e.read().decode()}")
        sys.exit(1)

def generate_audio(text, output_path):
    # 문장 단위로 분할 후 청크화
    sentences = re.split(r"(?<=[다요까죠]\.) +|\n\n+", text)
    chunks, cur = [], ""
    for s in sentences:
        if len(cur) + len(s) < CHUNK_SIZE:
            cur += s + " "
        else:
            if cur.strip():
                chunks.append(cur.strip())
            cur = s + " "
    if cur.strip():
        chunks.append(cur.strip())

    print(f"[TTS] 총 {len(text)}자 → {len(chunks)}개 청크")
    parts = []
    for i, chunk in enumerate(chunks):
        parts.append(call_tts(chunk, i))

    # MP3 청크 합치기 (ffmpeg concat)
    if len(parts) == 1:
        with open(output_path, "wb") as f:
            f.write(parts[0])
    else:
        tmp_dir = output_path + "_parts"
        os.makedirs(tmp_dir, exist_ok=True)
        list_path = os.path.join(tmp_dir, "list.txt")
        with open(list_path, "w") as lf:
            for i, data in enumerate(parts):
                p = os.path.join(tmp_dir, f"part{i:02d}.mp3")
                with open(p, "wb") as f:
                    f.write(data)
                lf.write(f"file '{p}'\n")
        os.system(f"ffmpeg -y -f concat -safe 0 -i '{list_path}' -c copy '{output_path}' 2>/dev/null")
        import shutil; shutil.rmtree(tmp_dir)

    size = os.path.getsize(output_path)
    print(f"[완료] {output_path} ({size//1024}KB)")

# ── 메인 ─────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 generate_audio.py <script.md> [output.mp3]")
        sys.exit(1)

    md_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else md_path.replace(".md", ".mp3")

    with open(md_path, encoding="utf-8") as f:
        raw = f.read()

    narration = clean_script(raw)
    print("── 추출된 나레이션 (앞 800자) ──────────────────")
    print(narration[:800])
    print(f"\n... 총 {len(narration)}자")
    print("────────────────────────────────────────────────")

    generate_audio(narration, out_path)
