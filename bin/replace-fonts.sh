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
  if has_used "$1" '--iy-ui-font'; then
    echo "$UI_FONT"
  fi
  if has_used "$1" '--iy-grey-font'; then
    echo "$GREY_FONT"
  fi
  if has_used "$1" '--iy-atki-font'; then
    echo "$ATKI_FONT"
  fi
  if has_used "$1" '--iy-code-font'; then
    echo "$CODE_FONT"
  fi
}

SANS_FONT="$(get_fonts '--iy-sans-font')"
SERIF_FONT="$(get_fonts '--iy-serif-font')"
MONO_FONT="$(get_fonts '--iy-mono-font')"
CODE_FONT="$(get_fonts '--iy-code-font')"
UI_FONT="$(get_fonts '--iy-ui-font')"
GREY_FONT="$(get_fonts '--iy-grey-font')"
ATKI_FONT="$(get_fonts '--iy-atki-font')"

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
