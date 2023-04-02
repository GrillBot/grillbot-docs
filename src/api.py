from typing import List


def _multi_line(data: List[str]) -> str:
    return "<br>".join(data)


def _bold(value: str) -> str:
    return f"<b>{value}</b>"


status_codes = {
    200: "OK",
    204: "No content",
    400: "Bad request",
    404: "Not Found",
    406: "Not acceptable",
    409: "Conflict",
    500: "Internal server error",
}


def format_codes(values: List[int]) -> List[str]:
    return list(map(lambda x: f"{x} {status_codes[x]}", values))


def build_api_description(
    endpoint: str, status_codes: List[int], content_types: List[str], description: str
) -> List[str]:
    return [
        _bold(endpoint),
        _multi_line(format_codes(status_codes)),
        _multi_line(content_types),
        description,
    ]
