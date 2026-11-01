#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd "$(dirname "$0")/.." && pwd)"
sdk_dir="${RENPY_SDK:-$HOME/Applications/renpy-8.5.3-sdk}"
if [[ ! -x "$sdk_dir/renpy.sh" || ! -d "$sdk_dir/web" ]]; then
  echo "Install Ren'Py 8.5.3 with web support; set RENPY_SDK to its directory." >&2
  exit 1
fi
sdk_dir="$(cd "$sdk_dir" && pwd)"
cd "$sdk_dir"
"$sdk_dir/renpy.sh" launcher web_build "$project_dir" --destination "$project_dir/dist/SeasCompany-1.0-web"
test -s "$project_dir/dist/SeasCompany-1.0-web/index.html"
