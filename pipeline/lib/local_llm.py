"""Local LLM fallback client (OpenAI-compatible endpoint).

한국망↔Anthropic 이 끝까지 막혀 ``topic_modeling.generate_connections_from_candidates``
가 max_rounds 를 다 돌고도 *연결을 못 만든 papers* 가 남을 때, **로컬에서 도는
모델로 그 잔여분을 마저 연결**하는 opt-in fallback 의 클라이언트.

클라우드 키·외부 네트워크 없이 동작하며, 환경에 로컬 모델이 떠 있고 사용자가
``--local-fallback`` 을 켰을 때만 실행된다. OpenAI 호환 엔드포인트(/v1/chat/completions
+ /v1/models) 만 가정하므로 러너에 독립적이다:

  - Ollama:    base_url=http://localhost:11434/v1   model=qwen2.5:7b-instruct
  - LM Studio: base_url=http://localhost:1234/v1    model=<loaded model id>
  - llama.cpp: base_url=http://localhost:8080/v1    model=<any>
  - vLLM:      base_url=http://localhost:8000/v1    model=<served name>

설정은 config.json 의 ``local_model`` 블록 또는 환경변수
(LOCAL_MODEL_BASE_URL / LOCAL_MODEL_NAME / LOCAL_MODEL_API_KEY) 로 준다
(config_loader.get_local_model_config 참조).
"""
import json
import re
import urllib.request

# 가장 바깥 JSON object 추출용 (로컬 모델은 서론/코드펜스/trailing comma 를 자주 붙인다)
_JSON_OBJ = re.compile(r"\{.*\}", re.DOTALL)


def probe(base_url, timeout=5.0):
    """엔드포인트가 살아 있는지 GET {base_url}/models 로 빠르게 확인. 실패해도 예외 없이 False."""
    url = base_url.rstrip("/") + "/models"
    try:
        req = urllib.request.Request(
            url, headers={"Authorization": "Bearer local"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return 200 <= getattr(r, "status", 200) < 300
    except Exception:
        return False


def get_client(cfg):
    """OpenAI SDK 를 로컬 base_url 로 향하게 한 클라이언트. SDK 미설치/실패 시 None."""
    try:
        from openai import OpenAI
    except Exception:
        return None
    try:
        return OpenAI(
            base_url=cfg["base_url"],
            api_key=cfg.get("api_key") or "local",
            timeout=float(cfg.get("timeout", 300.0)),
            max_retries=1,
        )
    except Exception:
        return None


def chat_json(client, model, prompt, max_tokens=8000, temperature=0.2):
    """단일 chat completion → 첫 JSON object 를 dict 로 견고하게 파싱.

    로컬 모델은 ```json 펜스·서론 문장·trailing comma 를 흘리곤 한다. 방어:
      1) ```...``` 코드펜스 벗기기  2) 바깥 {...} 추출  3) trailing comma 제거
    파싱 실패는 호출자가 잡도록 그대로 예외를 올린다(해당 배치만 건너뜀).
    """
    resp = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[{"role": "user", "content": prompt}],
    )
    text = (resp.choices[0].message.content or "").strip()
    if text.startswith("```"):
        parts = text.split("```")
        if len(parts) >= 2:
            text = parts[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
    m = _JSON_OBJ.search(text)
    if m:
        text = m.group(0)
    text = re.sub(r",\s*([}\]])", r"\1", text)  # trailing comma 정리
    return json.loads(text)
