#!/usr/bin/env python3
"""Self-check for the Loon -> Stash converter (run: python3 scripts/test_convert_loon_to_stash.py)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "convert_loon_to_stash", Path(__file__).with_name("convert-loon-to-stash.py")
)
converter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(converter)
converter.fetch = lambda url: "# fetched\n.data = {}\n"

SOURCE = r"""
#!name=Test plugin

[Argument]
alpha=switch, true, false, tag=Alpha, desc=alpha switch
beta=select, "off", "on", tag=Beta, desc=beta level

[Rule]
DOMAIN, ad.example, REJECT

[Rewrite]
^https?:\/\/legacy\.example\/ad reject
request if ${url} ~= /^https?:\/\/a\.example\/x\?/i then reject_dict(200)
request if ${url} ~= /^https?:\/\/b\.example\/y/i then reject(404)
request if ${url} ~= /^https?:\/\/(www\.)?c\.example/i then redirect(307, "https://d.example")
request if ${url} ~= /(^https?:\/\/e\.example\/go\?u=)(http.*)/i as urlMatch then redirect(307, "${urlMatch.2}")
response if ${url} ~= /^https?:\/\/f\.example\/json\?/i then response.json.delete(["data.a", "data.b"])
response if ${url} ~= /^https?:\/\/g\.example\/json\?/i then response.json.jq("del(.data)")
response if ${url} ~= /^https?:\/\/h\.example\/json\?/i then response.json.jq_file("https://raw.example/rule.jq")
response if ${url} ~= /^https?:\/\/i\.example\/cfg\?/i then response.json.replace(["data.a", "data.b"], [1, 2])
response if ${url} ~= /^https?:\/\/i\.example\/items\?/i then response.json.replace("Data.Items", "[]")
response if ${url} ~= /^https?:\/\/j\.example\/api\?/i then response.body.mock("text", "hello", 200)
response if ${url} ~= /^https?:\/\/k\.example\/api\?/i then response.body.mock("text", "AAAAAAA=", 200, true)
response if ${url} ~= /^https?:\/\/l\.example\/api$/i then response.header.add("grpc-status", "0")

[Script]
request if ${url} ~= /^https?:\/\/m\.example\/api\?/i then script("https://kelee.one/Resource/JavaScript/demo.js", {${alpha}, ${beta}}) with enable=${alpha}, tag="demo tag", timeout=10, requires_body=true, binary_body_mode=true

[MITM]
hostname=m.example
"""

output = converter.render("Test plugin", SOURCE, "test_plugin", "json")


def quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def expect(value: str) -> None:
    assert quoted(value) in output, f"missing entry: {value!r}\n---\n{output}"


for entry in (
    "^https?:\\/\\/legacy\\.example\\/ad - reject",
    "(?i)^https?:\\/\\/a\\.example\\/x\\? - reject-dict",
    "(?i)^https?:\\/\\/b\\.example\\/y - reject",
    "(?i)^https?:\\/\\/(www\\.)?c\\.example https://d.example 307",
    "(?i)(^https?:\\/\\/e\\.example\\/go\\?u=)(http.*) $2 307",
    "(?i)^https?:\\/\\/l\\.example\\/api$ response-add grpc-status 0",
):
    expect(entry)

for entry in (
    "(?i)^https?:\\/\\/f\\.example\\/json\\? response-json-del data.a data.b",
    "(?i)^https?:\\/\\/g\\.example\\/json\\? response-jq del(.data)",
    "(?i)^https?:\\/\\/h\\.example\\/json\\? response-jq .data = {}",
    "(?i)^https?:\\/\\/i\\.example\\/items\\? response-json-replace Data.Items []",
    "(?i)^https?:\\/\\/i\\.example\\/cfg\\? response-json-replace data.a 1 data.b 2",
):
    expect(entry)

for entry in ("text: \"hello\"", "base64: \"AAAAAAA=\"", "status-code: 200"):
    assert entry in output, f"missing mock field: {entry!r}\n---\n{output}"

assert 'type: "request"' in output, "request script lost its type"
assert 'require-body: true' in output and 'binary-mode: true' in output
assert 'timeout: 10' in output
assert 'argument: "{\\"alpha\\":true,\\"beta\\":\\"off\\"}"' in output, output
assert 'url: "https://git.repcz.link/kelee.one/Resource/JavaScript/demo.js"' in output

print("converter self-check passed")