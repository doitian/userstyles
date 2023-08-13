##!/usr/bin/env bash

set -e
set -u
[ -n "${DEBUG:-}" ] && set -x || true

get_fonts() {
  sed -e "/$1/bx" -e 'd' -e ':x' -e '/;$/q' -e 'N' -e 'bx' bin/fonts.css
}

remove_fonts() {
  sed -e '/--.*font:/bx' -e 'b' -e ':x' -e '/;$/d' -e 'N' -e 'bx' "$1"
}

insert_fonts() {
  echo "$1" | sed '/^  :root {$/,$d'
  echo '  :root {'
  echo "$2"
  echo "$1" | sed '1,/^  :root {$/d'
}

has_used() {
  echo "$1" | grep -q -- "$2"
}

get_used_fonts() {
  if has_used "$1" '--iy-sans-font'; then
    echo "$SANS_FONT"
  fi
  if has_used "$1" '--iy-serif-font'; then
    echo "$SERIF_FONT"
  fi
  if has_used "$1" '--iy-mono-font'; then
    echo "$MONO_FONT"
  fi
  if has_used "$1" '--iy-deco-font'; then
    echo "$DECO_FONT"
  fi
  if has_used "$1" '--iy-read-font'; then
    echo "$READ_FONT"
  fi
}

SANS_FONT="$(get_fonts '--iy-sans-font')"
SERIF_FONT="$(get_fonts '--iy-serif-font')"
MONO_FONT="$(get_fonts '--iy-mono-font')"
DECO_FONT="$(get_fonts '--iy-deco-font')"
READ_FONT="$(get_fonts '--iy-read-font')"

for css in *.css; do
  TEMPLATE="$(remove_fonts "$css")"
  USED_FONTS="$(get_used_fonts "$TEMPLATE")"
  mv "$css" "$css.bak"
  if [ -n "$USED_FONTS" ]; then
    insert_fonts "$TEMPLATE" "$USED_FONTS" >"$css"
  else
    echo "$TEMPLATE" >"$css"
  fi
  rm -f "$css.bak"
done
