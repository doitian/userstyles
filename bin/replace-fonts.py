#!/usr/bin/env python3

import os

fonts_css = open("bin/fonts.css", "r").read()


def get_fonts(pattern):
    lines = fonts_css.splitlines(keepends=True)
    start_index = None
    for i, line in enumerate(lines):
        if pattern in line:
            start_index = i
            break
    if start_index is None:
        return ""
    end_index = None
    for i in range(start_index, len(lines)):
        if lines[i].strip().endswith(";"):
            end_index = i
            break
    if end_index is None:
        return ""
    return "".join(lines[start_index : end_index + 1])


def remove_fonts(css_file):
    with open(css_file, "r") as file:
        lines = file.readlines()
        result = []
        skip_lines = False
        for line in lines:
            if line.lstrip().startswith("--") and "font:" in line:
                skip_lines = True
            elif skip_lines and line.strip().endswith(";"):
                skip_lines = False
            elif not skip_lines:
                result.append(line)
        return "".join(result)


def insert_fonts(template, used_fonts):
    lines = template.split("\n")
    root_index = None
    for i, line in enumerate(lines):
        if line.strip() == "@media all {":
            root_index = i
            break
    if root_index is None:
        return template

    result = []
    result.extend(
        line
        for line in lines[:root_index]
        if not (line.startswith("@import") and "fonts" in line)
    )
    if "--iy-atki-font" in template:
        result.insert(
            0,
            '@import url("https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&display=swap");',
        )
    result.append("  :root {")
    result.append(used_fonts)
    result.extend(lines[root_index + 1 :])

    return "\n".join(result)


def has_used(template, pattern):
    return pattern in template


def get_used_fonts(template):
    used_fonts = []
    if has_used(template, "--iy-sans-font"):
        used_fonts.append(SANS_FONT)
    if has_used(template, "--iy-serif-font"):
        used_fonts.append(SERIF_FONT)
    if has_used(template, "--iy-mono-font"):
        used_fonts.append(MONO_FONT)
    if has_used(template, "--iy-ui-font"):
        used_fonts.append(UI_FONT)
    if has_used(template, "--iy-grey-font"):
        used_fonts.append(GREY_FONT)
    if has_used(template, "--iy-atki-font"):
        used_fonts.append(ATKI_FONT)
    if has_used(template, "--iy-code-font"):
        used_fonts.append(CODE_FONT)
    return "\n".join(used_fonts)


SANS_FONT = get_fonts("--iy-sans-font")
SERIF_FONT = get_fonts("--iy-serif-font")
MONO_FONT = get_fonts("--iy-mono-font")
CODE_FONT = get_fonts("--iy-code-font")
UI_FONT = get_fonts("--iy-ui-font")
GREY_FONT = get_fonts("--iy-grey-font")
ATKI_FONT = get_fonts("--iy-atki-font")

css_files = [file for file in os.listdir() if file.endswith(".css")]
css_files.extend(
    [os.path.join("apps", file) for file in os.listdir("apps") if file.endswith(".css")]
)

for css_file in css_files:
    template = remove_fonts(css_file)
    print(template)
    break
    used_fonts = get_used_fonts(template)
    backup_file = css_file + ".bak"
    os.rename(css_file, backup_file)
    if used_fonts:
        with open(css_file, "w", newline="\n") as file:
            file.write(insert_fonts(template, used_fonts))
    else:
        with open(css_file, "w", newline="\n") as file:
            file.write(template)
    os.remove(backup_file)
