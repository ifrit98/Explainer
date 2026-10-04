"""Stage 3 web toolkit: shared CSS and JS, inlined into each page so pages stay single-file.

A page opts in with two empty tags:

    <style id="explainer-toolkit-css"></style>
    <script id="explainer-toolkit-js"></script>

`explainer sync <slug>` fills them with the current toolkit (and the model block).
"""

from __future__ import annotations

import re

from explainer_kit.paths import WEB

BLOCKS = {
    "css": (re.compile(r'(<style id="explainer-toolkit-css">)(.*?)(</style>)', re.S), "explainer.css"),
    "js": (re.compile(r'(<script id="explainer-toolkit-js">)(.*?)(</script>)', re.S), "explainer.js"),
}


def toolkit_source(kind: str) -> str:
    return (WEB / BLOCKS[kind][1]).read_text()


def inline_toolkit(page: str) -> str:
    for kind, (pattern, _) in BLOCKS.items():
        if pattern.search(page):
            body = "\n" + toolkit_source(kind).strip() + "\n"
            page = pattern.sub(lambda m: m.group(1) + body + m.group(3), page)
    return page


def toolkit_current(page: str) -> bool:
    return inline_toolkit(page) == page
