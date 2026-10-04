#!/usr/bin/env python3

import os
import json
import glob
import subprocess
from datetime import datetime, timezone


def modified_time(css_file):
    # File mtimes are reset on checkout, so prefer the last commit time.
    try:
        committed = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", css_file],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        committed = ""
    if committed:
        modified = datetime.fromisoformat(committed)
    else:
        modified = datetime.fromtimestamp(os.path.getmtime(css_file), timezone.utc)
    # Stylebot timestamps use the format yyyy-MM-dd'T'HH:mm:ss.SSSxxx
    return modified.isoformat(timespec="milliseconds")


def yield_files():
    for css_file in sorted(glob.glob("*.css")):
        name = css_file[:-4]
        with open(css_file, "r") as file:
            css_content = file.read()
        css_content = css_content.replace(" !important;", ";")
        css_content = "\n".join(
            line
            for line in css_content.split("\n")
            if not line.startswith("@import") or "fonts" not in line
        )
        yield (
            name,
            {
                "css": css_content,
                "enabled": True,
                "modifiedTime": modified_time(css_file),
                "readability": False,
            },
        )


def main():
    config = dict(yield_files())
    output = json.dumps(config, indent=2)
    print(output)


if __name__ == "__main__":
    main()
