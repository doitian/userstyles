#!/usr/bin/env python3

import os
import json
import glob
from datetime import datetime


def yield_files():
    for css_file in glob.glob("*.css"):
        name = css_file[:-4]
        modified = datetime.fromtimestamp(os.path.getmtime(css_file)).isoformat()
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
                "modifiedTime": modified,
                "readability": False,
            },
        )


def main():
    config = dict(yield_files())
    output = json.dumps(config, indent=2)
    print(output)


if __name__ == "__main__":
    main()
