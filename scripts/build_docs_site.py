# File: scripts/build_docs_site.py
# Format: UTF-8
# =============================
# File Description: Build the multilingual Docs tree into a dependency-free static HTML site.
# TAG: docs, github-pages, static-site
# =============================
from __future__ import annotations

import argparse
import html
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit


LANGUAGES = ("EN", "JP", "ZH")
LANGUAGE_LABELS = {
    "EN": "English",
    "JP": "日本語",
    "ZH": "中文",
}
HTML_LANG = {
    "EN": "en",
    "JP": "ja",
    "ZH": "zh",
}
SITE_TITLE = "N.I.L.O. Docs"
EXCLUDED_PAGE_PATHS = {
    "Developer/packaging.md",
}
EXCLUDED_PAGE_PREFIXES = (
    "Developer/Reference/Skills/test_copies/",
)
NAV_LABELS = {
    "EN": {
        "home": "English documentation",
        "User": "User documentation",
        "Developer": "Developer documentation",
        "Other": "Other documentation",
        "user_overview": "Overview",
        "user_setup": "Setup and connection",
        "user_support": "Maintenance and troubleshooting",
        "user_cli": "CLI reference",
        "user_skills": "Skills template library",
        "developer_overview": "Overview",
        "developer_api": "API",
        "developer_mcp_tools": "MCP tools",
        "developer_testing": "Testing",
        "other_changelog": "Changelog",
        "uncategorized": "Uncategorized",
    },
    "JP": {
        "home": "日本語ドキュメント",
        "User": "ユーザードキュメント",
        "Developer": "開発者ドキュメント",
        "Other": "その他のドキュメント",
        "user_overview": "概要",
        "user_setup": "セットアップと接続",
        "user_support": "保守とトラブルシューティング",
        "user_cli": "CLI リファレンス",
        "user_skills": "Skills テンプレートライブラリ",
        "developer_overview": "概要",
        "developer_api": "API",
        "developer_mcp_tools": "MCP ツール",
        "developer_testing": "テスト",
        "other_changelog": "変更履歴",
        "uncategorized": "未分類",
    },
    "ZH": {
        "home": "中文文档",
        "User": "用户文档",
        "Developer": "开发者文档",
        "Other": "其他文档",
        "user_overview": "概览",
        "user_setup": "安装与连接",
        "user_support": "维护与故障排查",
        "user_cli": "CLI 参考",
        "user_skills": "Skills 模板库",
        "developer_overview": "概览",
        "developer_api": "API",
        "developer_mcp_tools": "MCP 工具",
        "developer_testing": "测试",
        "other_changelog": "变更日志",
        "uncategorized": "未分类",
    },
}
NAV_GROUPS = (
    (
        "User",
        (
            ("user_overview", False, ("User/README.md",), ()),
            (
                "user_setup",
                False,
                (
                    "User/Guide.md",
                    "User/Installation.md",
                    "User/Configuration.md",
                    "User/MCP_Clients.md",
                ),
                (),
            ),
            (
                "user_support",
                False,
                (
                    "User/Troubleshooting.md",
                    "User/Uninstallation.md",
                ),
                (),
            ),
            (
                "user_cli",
                True,
                ("User/Cli.md",),
                ("User/Cli/",),
            ),
            (
                "user_skills",
                True,
                (
                    "Developer/Reference/Skills/README.md",
                    "Developer/Reference/Skills/codex/SKILL.md",
                    "Developer/Reference/Skills/claude/SKILL.md",
                    "Developer/Reference/Skills/third_party/SKILL.md",
                    "Developer/Reference/Skills/references/quick.md",
                    "Developer/Reference/Skills/references/normal.md",
                    "Developer/Reference/Skills/references/full.md",
                ),
                (),
            ),
        ),
    ),
    (
        "Developer",
        (
            (
                "developer_overview",
                False,
                (
                    "Developer/README.md",
                    "Developer/architecture/overview.md",
                ),
                (),
            ),
            (
                "developer_api",
                True,
                (
                    "Developer/API.md",
                    "Developer/api/core.md",
                    "Developer/api/cli.md",
                ),
                (),
            ),
            (
                "developer_mcp_tools",
                True,
                ("Developer/mcp_tools/README.md",),
                ("Developer/mcp_tools/",),
            ),
            (
                "developer_testing",
                True,
                ("Developer/testing/strategy.md",),
                ("Developer/testing/",),
            ),
        ),
    ),
    (
        "Other",
        (
            (
                "other_changelog",
                False,
                ("Developer/Reference/Skills/CHANGELOG.md",),
                (),
            ),
        ),
    ),
)
LOCALIZED_TITLES = {
    "JP": {
        "README.md": "日本語ドキュメント",
        "User/README.md": "ユーザードキュメント",
        "User/Guide.md": "利用ガイド",
        "User/Installation.md": "インストール",
        "User/Configuration.md": "設定",
        "User/MCP_Clients.md": "MCP クライアント",
        "User/Cli.md": "CLI ドキュメント",
        "User/Troubleshooting.md": "トラブルシューティング",
        "User/Uninstallation.md": "アンインストール",
        "Developer/README.md": "開発者ドキュメント",
        "Developer/API.md": "開発者 API 索引",
        "Developer/architecture/overview.md": "アーキテクチャ概要",
        "Developer/mcp_tools/README.md": "MCP ツール",
        "Developer/testing/strategy.md": "テスト戦略",
    },
    "ZH": {
        "README.md": "中文文档",
        "User/README.md": "用户文档",
        "User/Guide.md": "使用指南",
        "User/Installation.md": "安装",
        "User/Configuration.md": "配置",
        "User/MCP_Clients.md": "MCP 客户端",
        "User/Cli.md": "CLI 文档",
        "User/Troubleshooting.md": "故障排查",
        "User/Uninstallation.md": "卸载",
        "User/Cli/Overview.md": "CLI 概览",
        "User/Cli/Project_Config.md": "项目配置 CLI",
        "User/Cli/Page.md": "页面 CLI",
        "User/Cli/Block.md": "内容块 CLI",
        "User/Cli/Database_DataSource.md": "数据库与数据源 CLI",
        "User/Cli/Auth_And_User.md": "认证与用户 CLI",
        "User/Cli/Comments.md": "评论 CLI",
        "User/Cli/Views.md": "视图 CLI",
        "User/Cli/File_Uploads.md": "文件上传 CLI",
        "User/Cli/Search_And_Custom_Emoji.md": "搜索与自定义表情 CLI",
        "User/Cli/Raw_API.md": "Raw API CLI",
        "User/Cli/MCP_Server.md": "MCP Server CLI",
        "Developer/README.md": "开发者文档",
        "Developer/API.md": "开发者接口索引",
        "Developer/architecture/overview.md": "架构概览",
        "Developer/api/core.md": "Core API",
        "Developer/api/cli.md": "CLI API",
        "Developer/mcp_tools/README.md": "MCP 工具",
        "Developer/mcp_tools/auth.md": "认证工具",
        "Developer/mcp_tools/blocks.md": "内容块工具",
        "Developer/mcp_tools/comments.md": "评论工具",
        "Developer/mcp_tools/config.md": "配置工具",
        "Developer/mcp_tools/custom_emojis.md": "自定义表情工具",
        "Developer/mcp_tools/data_sources.md": "数据源工具",
        "Developer/mcp_tools/databases.md": "数据库工具",
        "Developer/mcp_tools/file_uploads.md": "文件上传工具",
        "Developer/mcp_tools/pages.md": "页面工具",
        "Developer/mcp_tools/raw_api.md": "Raw API 工具",
        "Developer/mcp_tools/search.md": "搜索工具",
        "Developer/mcp_tools/users.md": "用户工具",
        "Developer/mcp_tools/views.md": "视图工具",
        "Developer/testing/strategy.md": "测试策略",
        "Developer/testing/cli.md": "CLI 测试",
        "Developer/testing/core.md": "Core 测试",
        "Developer/testing/live.md": "Live 测试",
        "Developer/testing/mcp.md": "MCP 测试",
        "Developer/testing/scenarios.md": "场景测试",
        "Developer/Reference/Skills/README.md": "Skills 模板库",
        "Developer/Reference/Skills/CHANGELOG.md": "变更日志",
        "Developer/Reference/Skills/claude/SKILL.md": "Claude Skill 模板",
        "Developer/Reference/Skills/codex/SKILL.md": "Codex Skill 模板",
        "Developer/Reference/Skills/references/full.md": "完整 Skill 参考",
        "Developer/Reference/Skills/references/normal.md": "标准 Skill 参考",
        "Developer/Reference/Skills/references/quick.md": "快速 Skill 参考",
        "Developer/Reference/Skills/third_party/SKILL.md": "第三方 Skill 模板",
    },
}


@dataclass(frozen=True)
class Page:
    source_path: Path
    output_path: Path
    lang: str
    lang_rel: Path
    title: str


# --------------------------------
# Function Description: Parse command-line arguments for the docs site builder.
# Inputs/Outputs: Accepts argv-like input; returns argparse.Namespace with source and output paths.
# Usage: args = parse_args(["--source", "Docs", "--output", "build/docs-site"])
# --------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the Docs tree into a GitHub Pages static site.")
    parser.add_argument("--source", default="Docs", type=Path, help="Docs source directory.")
    parser.add_argument("--output", default=Path("build/docs-site"), type=Path, help="Output site directory.")
    return parser.parse_args()


# --------------------------------
# Function Description: Convert a Markdown source path to its generated HTML output path.
# Inputs/Outputs: Takes Docs root, output root, and source path; returns output HTML path.
# Usage: output_path_for(source_root, output_root, source_path)
# --------------------------------
def output_path_for(source_root: Path, output_root: Path, source_path: Path) -> Path:
    rel = source_path.relative_to(source_root)
    if source_path.name == "README.md":
        return output_root / rel.parent / "index.html"
    return output_root / rel.with_suffix(".html")


# --------------------------------
# Function Description: Read the first Markdown heading from a document.
# Inputs/Outputs: Takes Markdown text and fallback path; returns a display title.
# Usage: title = read_title(markdown_text, source_path)
# --------------------------------
def read_title(markdown_text: str, source_path: Path) -> str:
    for line in markdown_text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    if source_path.name == "README.md":
        return source_path.parent.name or SITE_TITLE
    return source_path.stem.replace("_", " ")


# --------------------------------
# Function Description: Return a localized display title for generated navigation and page headings.
# Inputs/Outputs: Takes language, language-relative path, and fallback title; returns a display title.
# Usage: title = localized_title("ZH", Path("User/Guide.md"), "Guide")
# --------------------------------
def localized_title(lang: str, lang_rel: Path, fallback: str) -> str:
    key = lang_rel.as_posix()
    return LOCALIZED_TITLES.get(lang, {}).get(key, fallback)


# --------------------------------
# Function Description: Return whether a language-relative source page is excluded from the public site.
# Inputs/Outputs: Takes a Docs/<LANG>-relative path; returns True when it should not be rendered.
# Usage: if is_excluded_page(Path("Developer/packaging.md")): continue
# --------------------------------
def is_excluded_page(lang_rel: Path) -> bool:
    key = lang_rel.as_posix()
    return key in EXCLUDED_PAGE_PATHS or any(key.startswith(prefix) for prefix in EXCLUDED_PAGE_PREFIXES)


# --------------------------------
# Function Description: Discover Markdown pages from Docs/<LANG> trees.
# Inputs/Outputs: Takes source and output roots; returns generated Page metadata.
# Usage: pages = discover_pages(Path("Docs"), Path("build/docs-site"))
# --------------------------------
def discover_pages(source_root: Path, output_root: Path) -> list[Page]:
    pages: list[Page] = []
    for lang in LANGUAGES:
        lang_root = source_root / lang
        if not lang_root.is_dir():
            continue
        for source_path in sorted(lang_root.rglob("*.md")):
            markdown_text = source_path.read_text(encoding="utf-8")
            lang_rel = source_path.relative_to(lang_root)
            if is_excluded_page(lang_rel):
                continue
            fallback_title = read_title(markdown_text, source_path)
            pages.append(
                Page(
                    source_path=source_path,
                    output_path=output_path_for(source_root, output_root, source_path),
                    lang=lang,
                    lang_rel=lang_rel,
                    title=localized_title(lang, lang_rel, fallback_title),
                )
            )
    return pages


# --------------------------------
# Function Description: Create stable, readable IDs for generated heading anchors.
# Inputs/Outputs: Takes heading text and existing counter map; returns a unique anchor ID.
# Usage: anchor_id = heading_id("Installation", seen)
# --------------------------------
def heading_id(text: str, seen: dict[str, int]) -> str:
    normalized = re.sub(r"[^\w\u3040-\u30ff\u3400-\u9fff-]+", "-", text.lower(), flags=re.UNICODE)
    normalized = normalized.strip("-") or "section"
    count = seen.get(normalized, 0)
    seen[normalized] = count + 1
    if count:
        return f"{normalized}-{count}"
    return normalized


# --------------------------------
# Function Description: Check whether a Markdown table separator row is present.
# Inputs/Outputs: Takes one stripped line; returns True for rows such as | --- | --- |.
# Usage: if is_table_separator(lines[index + 1].strip()): ...
# --------------------------------
def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


# --------------------------------
# Function Description: Split a simple Markdown table row into cells.
# Inputs/Outputs: Takes one Markdown table row; returns stripped cell strings.
# Usage: cells = split_table_row("| Command | Purpose |")
# --------------------------------
def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


# --------------------------------
# Function Description: Return True for URLs that should not be rewritten as local docs links.
# Inputs/Outputs: Takes a URL string; returns whether it has an external scheme or local anchor form.
# Usage: if is_external_or_anchor(url): return url
# --------------------------------
def is_external_or_anchor(url: str) -> bool:
    parsed = urlsplit(url)
    return bool(parsed.scheme or parsed.netloc) or url.startswith("#") or url.startswith("mailto:")


# --------------------------------
# Function Description: Rewrite Markdown links to generated HTML page links when they point to .md files.
# Inputs/Outputs: Takes a raw URL and current page context; returns an HTML-safe URL string.
# Usage: href = rewrite_url("Configuration.md", page, source_root, output_root)
# --------------------------------
def rewrite_url(url: str, page: Page, source_root: Path, output_root: Path) -> str:
    if is_external_or_anchor(url):
        return html.escape(url, quote=True)

    target, sep, anchor = url.partition("#")
    if not target.lower().endswith(".md"):
        return html.escape(url, quote=True)

    target_source = (page.source_path.parent / target).resolve()
    try:
        target_source.relative_to(source_root.resolve())
    except ValueError:
        return html.escape(url, quote=True)

    target_output = output_path_for(source_root.resolve(), output_root.resolve(), target_source)
    rel_url = os.path.relpath(target_output, page.output_path.parent.resolve()).replace(os.sep, "/")
    if sep:
        rel_url = f"{rel_url}#{anchor}"
    return html.escape(rel_url, quote=True)


# --------------------------------
# Function Description: Render inline Markdown spans used by the repository docs.
# Inputs/Outputs: Takes raw text and page context; returns HTML with links, code spans, and emphasis.
# Usage: html_text = render_inline("See [Config](Configuration.md)", page, source_root, output_root)
# --------------------------------
def render_inline(text: str, page: Page, source_root: Path, output_root: Path) -> str:
    tokens: list[str] = []

    def stash(value: str) -> str:
        tokens.append(value)
        return f"\x00TOKEN{len(tokens) - 1}\x00"

    def image_replacement(match: re.Match[str]) -> str:
        alt = html.escape(match.group(1), quote=True)
        src = rewrite_url(match.group(2), page, source_root, output_root)
        return stash(f'<img src="{src}" alt="{alt}">')

    def link_replacement(match: re.Match[str]) -> str:
        label = render_inline(match.group(1), page, source_root, output_root)
        href = rewrite_url(match.group(2), page, source_root, output_root)
        return stash(f'<a href="{href}">{label}</a>')

    def code_replacement(match: re.Match[str]) -> str:
        code = html.escape(match.group(1))
        return stash(f"<code>{code}</code>")

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image_replacement, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_replacement, text)
    text = re.sub(r"`([^`]+)`", code_replacement, text)
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    for index, value in enumerate(tokens):
        escaped = escaped.replace(f"\x00TOKEN{index}\x00", value)
    return escaped


# --------------------------------
# Function Description: Render a collected Markdown table to HTML.
# Inputs/Outputs: Takes table rows and page context; returns table HTML.
# Usage: html_table = render_table(rows, page, source_root, output_root)
# --------------------------------
def render_table(rows: list[str], page: Page, source_root: Path, output_root: Path) -> str:
    header = split_table_row(rows[0])
    body_rows = rows[2:]
    rendered = ["<div class=\"table-wrap\"><table>", "<thead><tr>"]
    rendered.extend(
        f"<th>{render_inline(cell, page, source_root, output_root)}</th>"
        for cell in header
    )
    rendered.append("</tr></thead>")
    if body_rows:
        rendered.append("<tbody>")
        for row in body_rows:
            rendered.append("<tr>")
            rendered.extend(
                f"<td>{render_inline(cell, page, source_root, output_root)}</td>"
                for cell in split_table_row(row)
            )
            rendered.append("</tr>")
        rendered.append("</tbody>")
    rendered.append("</table></div>")
    return "\n".join(rendered)


# --------------------------------
# Function Description: Render repository Markdown into HTML fragments without external dependencies.
# Inputs/Outputs: Takes Markdown text and page context; returns body HTML.
# Usage: body_html = render_markdown(markdown_text, page, source_root, output_root)
# --------------------------------
def render_markdown(markdown_text: str, page: Page, source_root: Path, output_root: Path) -> str:
    lines = markdown_text.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    heading_counts: dict[str, int] = {}
    list_type: str | None = None
    in_code = False
    code_lang = ""
    code_lines: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(f"<p>{render_inline(' '.join(paragraph), page, source_root, output_root)}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal list_type
        if list_type:
            output.append(f"</{list_type}>")
            list_type = None

    while index < len(lines):
        line = lines[index]

        if in_code:
            if line.startswith("```"):
                code = html.escape("\n".join(code_lines))
                lang_class = f" language-{html.escape(code_lang, quote=True)}" if code_lang else ""
                output.append(f'<pre><code class="{lang_class}">{code}</code></pre>')
                in_code = False
                code_lang = ""
                code_lines = []
            else:
                code_lines.append(line)
            index += 1
            continue

        if line.startswith("```"):
            flush_paragraph()
            close_list()
            in_code = True
            code_lang = line[3:].strip()
            index += 1
            continue

        if not line.strip():
            flush_paragraph()
            close_list()
            index += 1
            continue

        if index + 1 < len(lines) and line.lstrip().startswith("|") and is_table_separator(lines[index + 1].strip()):
            flush_paragraph()
            close_list()
            table_rows = [line, lines[index + 1]]
            index += 2
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                table_rows.append(lines[index])
                index += 1
            output.append(render_table(table_rows, page, source_root, output_root))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            flush_paragraph()
            close_list()
            level = len(heading.group(1))
            title = page.title if level == 1 else heading.group(2).strip()
            anchor = heading_id(title, heading_counts)
            output.append(
                f'<h{level} id="{html.escape(anchor, quote=True)}">'
                f"{render_inline(title, page, source_root, output_root)}</h{level}>"
            )
            index += 1
            continue

        quote = re.match(r"^>\s?(.*)$", line)
        if quote:
            flush_paragraph()
            close_list()
            output.append(f"<blockquote>{render_inline(quote.group(1), page, source_root, output_root)}</blockquote>")
            index += 1
            continue

        list_item = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.+)$", line)
        if list_item:
            flush_paragraph()
            kind = "ol" if list_item.group(2).endswith(".") else "ul"
            if list_type != kind:
                close_list()
                list_type = kind
                output.append(f"<{kind}>")
            indent = min(len(list_item.group(1)) // 2, 6)
            item = render_inline(list_item.group(3), page, source_root, output_root)
            output.append(f'<li class="indent-{indent}">{item}</li>')
            index += 1
            continue

        paragraph.append(line.strip())
        index += 1

    flush_paragraph()
    close_list()
    if in_code:
        code = html.escape("\n".join(code_lines))
        output.append(f"<pre><code>{code}</code></pre>")
    return "\n".join(output)


# --------------------------------
# Function Description: Build a relative URL from one generated page to another generated path.
# Inputs/Outputs: Takes current output file and target output path; returns a POSIX relative URL.
# Usage: href = relative_url(current_page.output_path, target_page.output_path)
# --------------------------------
def relative_url(from_output: Path, to_output: Path) -> str:
    return os.path.relpath(to_output, from_output.parent).replace(os.sep, "/")


# --------------------------------
# Function Description: Render the language switcher for the current page.
# Inputs/Outputs: Takes page and page maps; returns HTML links to same-path translations when present.
# Usage: switcher_html = render_language_switcher(page, pages_by_lang_rel, output_root)
# --------------------------------
def render_language_switcher(page: Page, pages_by_lang_rel: dict[tuple[str, Path], Page], output_root: Path) -> str:
    links = []
    for lang in LANGUAGES:
        target_page = pages_by_lang_rel.get((lang, page.lang_rel))
        if target_page is None:
            target_path = output_root / lang / "index.html"
        else:
            target_path = target_page.output_path
        active = " active" if lang == page.lang else ""
        href = html.escape(relative_url(page.output_path, target_path), quote=True)
        links.append(f'<a class="lang-link{active}" href="{href}">{LANGUAGE_LABELS[lang]}</a>')
    return "\n".join(links)


# --------------------------------
# Function Description: Return a localized navigation label with English fallback.
# Inputs/Outputs: Takes language and label key; returns display text.
# Usage: label = nav_label("ZH", "developer_testing")
# --------------------------------
def nav_label(lang: str, key: str) -> str:
    return NAV_LABELS.get(lang, NAV_LABELS["EN"]).get(key, NAV_LABELS["EN"].get(key, key))


# --------------------------------
# Function Description: Return pages that belong to a configured navigation group.
# Inputs/Outputs: Takes pages, exact paths, prefixes, and seen keys; returns ordered Page entries.
# Usage: targets = pages_for_nav_group(pages_by_key, lang_pages, paths, prefixes, seen)
# --------------------------------
def pages_for_nav_group(
    pages_by_key: dict[str, Page],
    lang_pages: list[Page],
    paths: tuple[str, ...],
    prefixes: tuple[str, ...],
    seen: set[str],
) -> list[Page]:
    targets: list[Page] = []
    for path in paths:
        target = pages_by_key.get(path)
        if target is None or path in seen:
            continue
        targets.append(target)
        seen.add(path)

    prefix_targets = [
        target for target in lang_pages
        if target.lang_rel.as_posix() not in seen
        and any(target.lang_rel.as_posix().startswith(prefix) for prefix in prefixes)
    ]
    for target in sorted(prefix_targets, key=page_sort_key):
        targets.append(target)
        seen.add(target.lang_rel.as_posix())
    return targets


# --------------------------------
# Function Description: Compute sidebar indentation relative to a configured group prefix.
# Inputs/Outputs: Takes a page and prefixes; returns a bounded depth class value.
# Usage: depth = nav_depth(page, ("Developer/Reference/Skills/",))
# --------------------------------
def nav_depth(target: Page, prefixes: tuple[str, ...]) -> int:
    if not prefixes:
        return 0
    target_key = target.lang_rel.as_posix()
    matching_prefixes = [prefix for prefix in prefixes if target_key.startswith(prefix)]
    if not matching_prefixes:
        return 0
    base_depth = min(len(Path(prefix.rstrip("/")).parts) for prefix in matching_prefixes)
    return min(max(len(target.lang_rel.parts) - base_depth - 1, 0), 4)


# --------------------------------
# Function Description: Render one sidebar link with active state and indentation.
# Inputs/Outputs: Takes current page, target page, and depth; returns link HTML.
# Usage: html_link = render_nav_link(page, target, 1)
# --------------------------------
def render_nav_link(page: Page, target: Page, depth: int) -> str:
    active = " active" if target.source_path == page.source_path else ""
    href = html.escape(relative_url(page.output_path, target.output_path), quote=True)
    label = html.escape(target.title)
    return f'<a class="nav-link depth-{depth}{active}" href="{href}">{label}</a>'


# --------------------------------
# Function Description: Render a configured sidebar group as a flat or collapsible navigation block.
# Inputs/Outputs: Takes current page, target pages, group label, prefixes, and collapse flag; returns HTML.
# Usage: block = render_nav_group(page, targets, "CLI reference", ("User/Cli/",), True)
# --------------------------------
def render_nav_group(
    page: Page,
    targets: list[Page],
    label: str,
    prefixes: tuple[str, ...],
    collapsible: bool,
) -> str:
    links = "\n".join(
        render_nav_link(page, target, nav_depth(target, prefixes))
        for target in targets
    )
    if collapsible:
        open_attr = " open" if any(target.source_path == page.source_path for target in targets) else ""
        return (
            f'<details class="nav-collapsible"{open_attr}>'
            f'<summary class="nav-subsection-title">{label}</summary>'
            f'<div class="nav-collapsible-body">{links}</div>'
            "</details>"
        )
    if len(targets) == 1 and targets[0].title == label:
        return links
    return f'<div class="nav-subsection-title">{label}</div>\n{links}'


# --------------------------------
# Function Description: Render a grouped sidebar for one language.
# Inputs/Outputs: Takes current page and language pages; returns navigation HTML grouped by content purpose.
# Usage: nav_html = render_sidebar(page, pages_by_lang["EN"])
# --------------------------------
def render_sidebar(page: Page, lang_pages: list[Page]) -> str:
    root_page = next((target for target in lang_pages if target.lang_rel == Path("README.md")), None)
    sections: list[str] = []
    seen: set[str] = set()
    pages_by_key = {target.lang_rel.as_posix(): target for target in lang_pages}

    if root_page is not None:
        active = " active" if root_page.source_path == page.source_path else ""
        href = html.escape(relative_url(page.output_path, root_page.output_path), quote=True)
        label = html.escape(nav_label(page.lang, "home"))
        sections.append(f'<a class="nav-home{active}" href="{href}">{label}</a>')
        seen.add(root_page.lang_rel.as_posix())

    for section_key, groups in NAV_GROUPS:
        rendered_groups: list[str] = []
        for group_key, collapsible, paths, prefixes in groups:
            targets = pages_for_nav_group(pages_by_key, lang_pages, paths, prefixes, seen)
            if not targets:
                continue
            group_label = html.escape(nav_label(page.lang, group_key))
            rendered_groups.append(render_nav_group(page, targets, group_label, prefixes, collapsible))
        if rendered_groups:
            sections.append(f'<div class="nav-section-title">{html.escape(nav_label(page.lang, section_key))}</div>')
            sections.extend(rendered_groups)

    uncategorized = [
        target for target in lang_pages
        if target.lang_rel.as_posix() not in seen
    ]
    if uncategorized:
        sections.append(f'<div class="nav-section-title">{html.escape(nav_label(page.lang, "Other"))}</div>')
        sections.append(f'<div class="nav-subsection-title">{html.escape(nav_label(page.lang, "uncategorized"))}</div>')
        sections.extend(render_nav_link(page, target, 0) for target in sorted(uncategorized, key=page_sort_key))
    return "\n".join(sections)


# --------------------------------
# Function Description: Sort README pages before sibling content while preserving directory shape.
# Inputs/Outputs: Takes a Page; returns a sortable key.
# Usage: sorted(pages, key=page_sort_key)
# --------------------------------
def page_sort_key(page: Page) -> tuple[tuple[str, ...], int, str]:
    parent = page.lang_rel.parent.parts
    readme_rank = 0 if page.lang_rel.name == "README.md" else 1
    return parent, readme_rank, page.lang_rel.name.lower()


# --------------------------------
# Function Description: Wrap one rendered Markdown document in the static site layout.
# Inputs/Outputs: Takes page metadata and rendered fragments; returns full HTML document.
# Usage: html_doc = render_page(page, body, nav, lang_switcher)
# --------------------------------
def render_page(page: Page, body: str, nav: str, language_switcher: str) -> str:
    site_root = page.output_path.parents[len(page.lang_rel.parts)]
    css_href = html.escape(relative_url(page.output_path, site_root / "assets/site.css"))
    home_href = html.escape(relative_url(page.output_path, site_root / "index.html"), quote=True)
    return f"""<!doctype html>
<html lang="{html.escape(HTML_LANG.get(page.lang, page.lang.lower()), quote=True)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(page.title)} - {SITE_TITLE}</title>
  <link rel="stylesheet" href="{css_href}">
</head>
<body>
  <header class="topbar">
    <a class="brand" href="{home_href}">{SITE_TITLE}</a>
    <nav class="language-switch" aria-label="Language switcher">
      {language_switcher}
    </nav>
  </header>
  <div class="layout">
    <aside class="sidebar" aria-label="Documentation navigation">
      {nav}
    </aside>
    <main class="content">
      {body}
    </main>
  </div>
</body>
</html>
"""


# --------------------------------
# Function Description: Render the root language selection page.
# Inputs/Outputs: Takes output root; returns root index HTML.
# Usage: root_html = render_root_index(output_root)
# --------------------------------
def render_root_index() -> str:
    links = "\n".join(
        f'<a class="language-card" href="{lang}/index.html">{LANGUAGE_LABELS[lang]}<span>Docs/{lang}</span></a>'
        for lang in LANGUAGES
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{SITE_TITLE}</title>
  <link rel="stylesheet" href="assets/site.css">
</head>
<body class="home">
  <main class="home-content">
    <p class="eyebrow">N.I.L.O.</p>
    <h1>{SITE_TITLE}</h1>
    <p class="summary">Choose a language to browse the repository documentation.</p>
    <nav class="language-grid" aria-label="Documentation languages">
      {links}
    </nav>
  </main>
</body>
</html>
"""


# --------------------------------
# Function Description: Return CSS for the generated static documentation site.
# Inputs/Outputs: No inputs; returns stylesheet content.
# Usage: css = site_css()
# --------------------------------
def site_css() -> str:
    return """
:root {
  color-scheme: light;
  --bg: #f7f7f4;
  --panel: #ffffff;
  --text: #1d2528;
  --muted: #667174;
  --line: #d9dfdc;
  --accent: #0f766e;
  --accent-strong: #115e59;
  --code-bg: #eef2ef;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.65;
}

a {
  color: var(--accent-strong);
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
}

.topbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  min-height: 56px;
  padding: 10px 24px;
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.94);
  backdrop-filter: blur(10px);
}

.brand {
  color: var(--text);
  font-weight: 700;
  text-decoration: none;
}

.language-switch {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.lang-link {
  min-height: 34px;
  padding: 5px 10px;
  border: 1px solid var(--line);
  border-radius: 6px;
  color: var(--text);
  text-decoration: none;
  font-size: 14px;
}

.lang-link.active {
  border-color: var(--accent);
  background: #e0f2ee;
  color: var(--accent-strong);
}

.layout {
  display: grid;
  grid-template-columns: minmax(220px, 300px) minmax(0, 1fr);
  max-width: 1320px;
  margin: 0 auto;
}

.sidebar {
  position: sticky;
  top: 57px;
  align-self: start;
  height: calc(100vh - 57px);
  overflow: auto;
  padding: 22px 16px;
  border-right: 1px solid var(--line);
}

.nav-link {
  display: block;
  padding: 6px 8px;
  border-radius: 6px;
  color: var(--text);
  text-decoration: none;
  font-size: 14px;
  line-height: 1.35;
}

.nav-home {
  display: block;
  margin: 2px 0 16px;
  padding: 7px 8px;
  border-radius: 6px;
  color: var(--text);
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
}

.nav-section-title {
  margin: 20px 0 8px;
  padding: 0 8px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: none;
}

.nav-subsection-title {
  margin: 10px 0 2px;
  padding: 0 8px;
  color: var(--accent-strong);
  font-size: 12px;
  font-weight: 700;
}

.nav-collapsible {
  margin: 4px 0;
}

.nav-collapsible > summary.nav-subsection-title {
  display: flex;
  align-items: center;
  gap: 6px;
  border-radius: 6px;
  cursor: pointer;
  list-style: none;
  padding: 5px 8px;
}

.nav-collapsible > summary.nav-subsection-title::-webkit-details-marker {
  display: none;
}

.nav-collapsible > summary.nav-subsection-title::before {
  content: "+";
  width: 10px;
  color: var(--muted);
  font-weight: 700;
}

.nav-collapsible[open] > summary.nav-subsection-title::before {
  content: "-";
}

.nav-collapsible > summary.nav-subsection-title:hover {
  background: #e7eee9;
}

.nav-collapsible-body {
  margin: 2px 0 8px;
}

.nav-link:hover,
.nav-link.active,
.nav-home:hover,
.nav-home.active {
  background: #e7eee9;
  color: var(--accent-strong);
}

.depth-1 { padding-left: 18px; }
.depth-2 { padding-left: 30px; }
.depth-3 { padding-left: 42px; }
.depth-4,
.depth-5,
.depth-6 { padding-left: 54px; }

.content {
  min-width: 0;
  max-width: 920px;
  padding: 36px 42px 72px;
}

.content h1,
.content h2,
.content h3,
.content h4 {
  line-height: 1.25;
}

.content h1 {
  margin-top: 0;
  font-size: 34px;
}

.content h2 {
  margin-top: 36px;
  border-top: 1px solid var(--line);
  padding-top: 24px;
}

code {
  border-radius: 5px;
  background: var(--code-bg);
  padding: 1px 5px;
  font-size: 0.94em;
}

pre {
  overflow: auto;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: #172024;
  padding: 16px;
}

pre code {
  background: transparent;
  color: #eef7f3;
  padding: 0;
}

.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 18px 0;
  background: var(--panel);
}

th,
td {
  border: 1px solid var(--line);
  padding: 8px 10px;
  text-align: left;
  vertical-align: top;
}

blockquote {
  margin: 18px 0;
  border-left: 4px solid var(--accent);
  padding-left: 14px;
  color: var(--muted);
}

.indent-1 { margin-left: 18px; }
.indent-2 { margin-left: 36px; }
.indent-3,
.indent-4,
.indent-5,
.indent-6 { margin-left: 54px; }

.home {
  min-height: 100vh;
  display: grid;
  place-items: center;
}

.home-content {
  width: min(760px, calc(100vw - 32px));
  padding: 48px 0;
}

.eyebrow {
  margin: 0 0 8px;
  color: var(--accent-strong);
  font-weight: 700;
}

.home h1 {
  margin: 0;
  font-size: 42px;
  line-height: 1.15;
}

.summary {
  margin: 14px 0 28px;
  color: var(--muted);
}

.language-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.language-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-height: 96px;
  justify-content: center;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--panel);
  padding: 18px;
  color: var(--text);
  text-decoration: none;
  font-weight: 700;
}

.language-card span {
  color: var(--muted);
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 820px) {
  .topbar {
    position: static;
    align-items: flex-start;
    flex-direction: column;
  }

  .layout {
    display: block;
  }

  .sidebar {
    position: static;
    height: auto;
    max-height: 320px;
    border-right: 0;
    border-bottom: 1px solid var(--line);
  }

  .content {
    padding: 28px 20px 56px;
  }

  .language-grid {
    grid-template-columns: 1fr;
  }
}
""".strip() + "\n"


# --------------------------------
# Function Description: Copy non-Markdown files from Docs/<LANG> into the generated site.
# Inputs/Outputs: Takes source and output roots; writes static assets next to generated HTML.
# Usage: copy_static_assets(Path("Docs"), Path("build/docs-site"))
# --------------------------------
def copy_static_assets(source_root: Path, output_root: Path) -> None:
    for lang in LANGUAGES:
        lang_root = source_root / lang
        if not lang_root.is_dir():
            continue
        for source_path in lang_root.rglob("*"):
            if source_path.is_dir() or source_path.suffix.lower() == ".md":
                continue
            target_path = output_root / source_path.relative_to(source_root)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


# --------------------------------
# Function Description: Build the full static site from discovered Docs pages.
# Inputs/Outputs: Takes source and output roots; writes HTML, CSS, and static copied assets.
# Usage: build_site(Path("Docs"), Path("build/docs-site"))
# --------------------------------
def build_site(source_root: Path, output_root: Path) -> None:
    source_root = source_root.resolve()
    output_root = output_root.resolve()
    if not source_root.is_dir():
        raise SystemExit(f"Docs source directory does not exist: {source_root}")

    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)

    pages = discover_pages(source_root, output_root)
    pages_by_lang: dict[str, list[Page]] = {lang: [] for lang in LANGUAGES}
    pages_by_lang_rel: dict[tuple[str, Path], Page] = {}
    for page in pages:
        pages_by_lang[page.lang].append(page)
        pages_by_lang_rel[(page.lang, page.lang_rel)] = page

    (output_root / "assets").mkdir(parents=True, exist_ok=True)
    (output_root / "assets/site.css").write_text(site_css(), encoding="utf-8")
    (output_root / ".nojekyll").write_text("", encoding="utf-8")
    (output_root / "index.html").write_text(render_root_index(), encoding="utf-8")

    for page in pages:
        markdown_text = page.source_path.read_text(encoding="utf-8")
        body = render_markdown(markdown_text, page, source_root, output_root)
        nav = render_sidebar(page, pages_by_lang[page.lang])
        switcher = render_language_switcher(page, pages_by_lang_rel, output_root)
        page.output_path.parent.mkdir(parents=True, exist_ok=True)
        page.output_path.write_text(render_page(page, body, nav, switcher), encoding="utf-8")

    copy_static_assets(source_root, output_root)
    print(f"Built {len(pages)} documentation pages into {output_root}")


# --------------------------------
# Function Description: Entry point for command-line execution.
# Inputs/Outputs: Reads CLI arguments; writes the static documentation site.
# Usage: python scripts/build_docs_site.py --source Docs --output build/docs-site
# --------------------------------
def main() -> None:
    args = parse_args()
    build_site(args.source, args.output)


if __name__ == "__main__":
    main()
