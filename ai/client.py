import json
import urllib.error
import urllib.request


OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "qwen3:8b"


class OllamaError(RuntimeError):
    pass


def chat_with_ollama(
    messages: list[dict[str, str]],
    model: str = DEFAULT_MODEL,
    timeout: int = 180,
) -> str:
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": False,
        "keep_alive": "10m",
        "options": {
            "temperature": 0.55,
        },
    }

    request = urllib.request.Request(
        OLLAMA_CHAT_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))

    except urllib.error.URLError as error:
        raise OllamaError(
            "I couldn't reach Ollama. Make sure Ollama is running."
        ) from error

    except TimeoutError as error:
        raise OllamaError(
            "Ollama took too long to answer. Try again."
        ) from error

    except json.JSONDecodeError as error:
        raise OllamaError(
            "Ollama returned something I couldn't read."
        ) from error

    content = result.get("message", {}).get("content", "").strip()

    if not content:
        raise OllamaError("Ollama answered, but the response was empty.")

    return content