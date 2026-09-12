#!/usr/bin/env python3
"""Convert the tracked Loon LPX plugins into Stash override files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "rules" / "stash" / "loon-sources.json"
OUTPUT_DIR = ROOT / "rules" / "stash"
USER_AGENT = "clash-rules-stash-converter/1.0"


def runtime_url(url: str) -> str:
    if url.startswith("https://kelee.one/"):
        return "https://git.repcz.link/" + url.removeprefix("https://")
    return url


def fetch(url: str) -> str:
    candidates = [url]
    if url.startswith("https://kelee.one/"):
        candidates.append("https://git.repcz.link/" + url.removeprefix("https://"))
    errors: list[str] = []
    for candidate in candidates:
        try:
            request = Request(candidate, headers={"User-Agent": USER_AGENT})
            with urlopen(request, timeout=45) as response:
                data = response.read()
            if not data:
                raise RuntimeError("empty response")
            return data.decode("utf-8")
        except Exception as exc:  # pragma: no cover - network-dependent branch
            errors.append(f"{candidate}: {exc}")
    raise RuntimeError("; ".join(errors))


def sections(text: str) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    current: str | None = None
    for raw in text.splitlines():
        match = re.match(r"^\s*\[([^\]]+)\]\s*$", raw)
        if match:
            section_name: str = match.group(1).lower()
            current = section_name
            result.setdefault(section_name, [])
        elif current is not None:
            result[current].append(raw.rstrip())
    return result


def nonempty(lines: list[str]) -> list[str]:
    return [line.strip() for line in lines if line.strip() and not line.lstrip().startswith(("#", ";"))]


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def split_csv(value: str) -> list[str]:
    result: list[str] = []
    start = 0
    quote: str | None = None
    escaped = False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quote:
            escaped = True
            continue
        if char in "'\"":
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
        elif char == "," and quote is None:
            result.append(value[start:index].strip())
            start = index + 1
    result.append(value[start:].strip())
    return result


def parse_argument_value(value: str):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        if value[0] == '"':
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value[1:-1]
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_arguments(lines: list[str]) -> dict[str, object]:
    result: dict[str, object] = {}
    for line in nonempty(lines):
        if "=" not in line:
            continue
        key, definition = line.split("=", 1)
        parts = split_csv(definition)
        if len(parts) < 2:
            continue
        result[key.strip()] = parse_argument_value(parts[1])
    return result


def parse_attributes(value: str, allowed_keys: set[str] | None = None) -> dict[str, str]:
    if allowed_keys:
        keys = "|".join(re.escape(key) for key in sorted(allowed_keys, key=len, reverse=True))
        pattern = rf"(?<!\S)({keys})="
    else:
        pattern = r"([A-Za-z][A-Za-z0-9-]*)="
    matches = list(re.finditer(pattern, value))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(value)
        item = value[match.end() : end].strip().rstrip(",").strip()
        result[match.group(1)] = item
    return result


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def normalize_rule(line: str) -> str:
    line = re.sub(r",\s+", ",", line.strip())
    line = re.sub(r"\(\s+", "(", line)
    line = re.sub(r"\s+\)", ")", line)
    return line


def url_regex_rule_to_rewrite(rule: str) -> str | None:
    if rule.startswith("URL-REGEX,"):
        fields = split_csv(rule)
        if len(fields) >= 3 and fields[0] == "URL-REGEX":
            return f"{unquote(fields[1])} - reject"
    if "URL-REGEX," in rule:
        match = re.search(r"URL-REGEX,\s*(\"(?:\\\\.|[^\"])*\"|[^,)]+)", rule)
        if match:
            return f"{unquote(match.group(1))} - reject"
    return None


def clean_jq(value: str) -> str:
    lines = []
    for line in value.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            lines.append(stripped)
    return " ".join(lines)


def parse_rewrites(lines: list[str]) -> dict[str, list]:
    url_rewrite: list[str] = []
    body_rewrite: list[str] = []
    header_rewrite: list[str] = []
    mocks: list[dict[str, object]] = []

    for line in nonempty(lines):
        parts = line.split(None, 2)
        if len(parts) < 2:
            raise ValueError(f"invalid Rewrite line: {line}")
        match, action = parts[0], parts[1]
        rest = parts[2] if len(parts) == 3 else ""

        if action in {"reject", "reject-dict", "reject-img"}:
            url_rewrite.append(f"{match} - reject")
        elif action == "307":
            if not rest:
                raise ValueError(f"missing redirect target: {line}")
            url_rewrite.append(f"{match} {rest} 307")
        elif action == "response-header-add":
            header_rewrite.append(f"{match} response-add {rest}")
        elif action == "response-body-json-jq":
            jq_path = re.fullmatch(r'jq-path="([^"]+)"', rest.strip())
            if jq_path:
                expression = clean_jq(fetch(jq_path.group(1)))
            else:
                expression = unquote(rest)
            body_rewrite.append(f"{match} response-jq {expression}")
        elif action in {
            "response-body-json-del",
            "response-body-json-replace",
            "response-body-json-add",
        }:
            body_action = "response-" + action.removeprefix("response-body-")
            body_rewrite.append(f"{match} {body_action} {rest}".rstrip())
        elif action == "mock-response-body":
            attributes = parse_attributes(
                rest, {"data-type", "status-code", "data", "mock-data-is-base64"}
            )
            data = unquote(attributes.get("data", ""))
            mock: dict[str, object] = {"match": match}
            if "status-code" in attributes:
                mock["status-code"] = int(attributes["status-code"])
            if attributes.get("mock-data-is-base64", "").lower() == "true":
                mock["base64"] = data
            else:
                mock["text"] = data
            mocks.append(mock)
        else:
            raise ValueError(f"unsupported Rewrite action {action!r}: {line}")

    return {
        "url-rewrite": dedupe(url_rewrite),
        "body-rewrite": dedupe(body_rewrite),
        "header-rewrite": dedupe(header_rewrite),
        "mock": mocks,
    }


def parse_mitm(lines: list[str]) -> list[str]:
    result: list[str] = []
    for line in nonempty(lines):
        match = re.match(r"^hostname\s*=\s*(.*)$", line, re.I)
        if match:
            result.extend(item.strip() for item in match.group(1).split(",") if item.strip())
    return dedupe(result)


def script_argument(
    attributes: dict[str, str], defaults: dict[str, object], style: str
) -> str | None:
    keys = re.findall(r"\{([^{}]+)\}", attributes.get("argument", ""))
    keys += re.findall(r"\{([^{}]+)\}", attributes.get("enable", ""))
    keys = list(dict.fromkeys(keys))
    if not keys:
        return None
    values = {key: defaults.get(key, "") for key in keys}
    if style == "pairs":
        return "&".join(f"{key}={str(value).lower() if isinstance(value, bool) else value}" for key, value in values.items())
    return json.dumps(values, ensure_ascii=False, separators=(",", ":"))


def parse_scripts(
    lines: list[str], defaults: dict[str, object], slug: str, argument_style: str
) -> tuple[list[dict[str, object]], dict[str, dict[str, object]]]:
    scripts: list[dict[str, object]] = []
    providers: dict[str, dict[str, object]] = {}
    index = 0
    for line in nonempty(lines):
        match = re.match(r"^(http-request|http-response)\s+(\S+)\s+(.*)$", line)
        if not match:
            raise ValueError(f"invalid Script line: {line}")
        kind, url_match, attribute_text = match.groups()
        attributes = parse_attributes(
            attribute_text,
            {
                "script-path",
                "requires-body",
                "binary-body-mode",
                "timeout",
                "argument",
                "enable",
                "tag",
            },
        )
        script_url = attributes.pop("script-path", "")
        if not script_url:
            raise ValueError(f"missing script-path: {line}")
        index += 1
        provider_name = f"loon_{slug}_{index:02d}"
        item: dict[str, object] = {
            "match": url_match,
            "name": provider_name,
            "type": "request" if kind == "http-request" else "response",
        }
        if attributes.get("requires-body", "").lower() == "true":
            item["require-body"] = True
        if attributes.get("binary-body-mode", "").lower() == "true":
            item["binary-mode"] = True
        if "timeout" in attributes:
            item["timeout"] = int(attributes["timeout"])
        argument = script_argument(attributes, defaults, argument_style)
        if argument is not None:
            item["argument"] = argument
        scripts.append(item)
        providers[provider_name] = {"url": runtime_url(script_url), "interval": 86400}
    return scripts, providers


def yaml_scalar(value: object) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def emit_mapping_item(lines: list[str], indent: str, key: str, value: object) -> None:
    lines.append(f"{indent}{key}: {yaml_scalar(value)}")


def render(
    display_name: str,
    source_text: str,
    slug: str,
    argument_style: str,
) -> str:
    parsed = sections(source_text)
    defaults = parse_arguments(parsed.get("argument", []))
    rules: list[str] = []
    rule_rewrites: list[str] = []
    for line in nonempty(parsed.get("rule", [])):
        normalized = normalize_rule(line)
        converted = url_regex_rule_to_rewrite(normalized)
        if converted:
            rule_rewrites.append(converted)
        else:
            rules.append(normalized)
    rules = dedupe(rules)
    rewrites = parse_rewrites(parsed.get("rewrite", []))
    rewrites["url-rewrite"] = dedupe(rule_rewrites + rewrites["url-rewrite"])
    scripts, providers = parse_scripts(parsed.get("script", []), defaults, slug, argument_style)
    mitm = parse_mitm(parsed.get("mitm", []) + parsed.get("mITM", []))

    lines = [f"name: {yaml_scalar(display_name)}"]
    if rules:
        lines.append("rules:")
        lines.extend(f"  - {yaml_scalar(rule)}" for rule in rules)

    http: dict[str, list] = {}
    if mitm:
        http["mitm"] = mitm
    if rewrites["url-rewrite"]:
        http["url-rewrite"] = rewrites["url-rewrite"]
    if rewrites["header-rewrite"]:
        http["header-rewrite"] = rewrites["header-rewrite"]
    if rewrites["body-rewrite"]:
        http["body-rewrite"] = rewrites["body-rewrite"]
    if rewrites["mock"]:
        http["mock"] = rewrites["mock"]
    if scripts:
        http["script"] = scripts

    if http:
        lines.append("http:")
        if "mitm" in http:
            lines.append("  mitm:")
            lines.extend(f"    - {yaml_scalar(item)}" for item in http["mitm"])
        for key in ("url-rewrite", "header-rewrite", "body-rewrite"):
            if key in http:
                lines.append(f"  {key}:")
                lines.extend(f"    - {yaml_scalar(item)}" for item in http[key])
        if "mock" in http:
            lines.append("  mock:")
            for item in http["mock"]:
                lines.append(f"    - match: {yaml_scalar(item['match'])}")
                for key in ("text", "base64", "status-code"):
                    if key in item:
                        emit_mapping_item(lines, "      ", key, item[key])
        if "script" in http:
            lines.append("  script:")
            for item in http["script"]:
                lines.append(f"    - match: {yaml_scalar(item['match'])}")
                for key in ("name", "type", "require-body", "binary-mode", "timeout", "argument"):
                    if key in item:
                        emit_mapping_item(lines, "      ", key, item[key])

    if providers:
        lines.append("script-providers:")
        for name, provider in providers.items():
            lines.append(f"  {yaml_scalar(name)}:")
            emit_mapping_item(lines, "    ", "url", provider["url"])
            emit_mapping_item(lines, "    ", "interval", provider["interval"])

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for item in manifest:
        source_url = item["source"]
        output = OUTPUT_DIR / item["output"]
        slug = re.sub(r"[^A-Za-z0-9]+", "_", Path(item["output"]).stem).strip("_").lower()
        text = fetch(source_url)
        output.write_text(
            render(
                item["name"],
                text,
                slug,
                item.get("argument_style", "json"),
            ),
            encoding="utf-8",
        )
        print(f"{item['source']} -> {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"conversion failed: {exc}", file=sys.stderr)
        raise
