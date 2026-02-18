from agentscope.tool import ToolResponse


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def text_response(text: str) -> ToolResponse:
    return ToolResponse(content=[{"type": "text", "text": text}])


def extract_text(resp: ToolResponse) -> str:
    parts: list[str] = []
    for block in resp.content:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(str(block.get("text", "")))
    return " ".join(parts).strip()
