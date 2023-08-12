#!/usr/bin/env bash

set -e
set -u
[ -n "${DEBUG:-}" ] && set -x || true

yield_files() {
  local css name
  for css in *.css; do
    name="${css%.css}"
    modified="$(date -r "$css" +%s | jq -rR 'strptime("%s")|todateiso8601')"
    jq --arg name "$name" --arg modified "$modified" -Rs '{($name):{
      "css": .,
      "enabled": true,
      "modifiedTime": $modified,
      "readability": false
    }}' <"$css"
  done
}

main() {
  yield_files | jq -s add
}

main "$@"
