#!/usr/bin/env bash
# Vercel's Linux build environment starts with source, without a Ren'Py SDK.
set -euo pipefail
project_dir="$(cd "$(dirname "$0")/.." && pwd)"
renpy_version="8.5.3"
build_tools_dir="$(mktemp -d)"
trap 'rm -rf "$build_tools_dir"' EXIT
base_url="https://www.renpy.org/dl/$renpy_version"
curl --fail --location --retry 3 --silent --show-error \
  "$base_url/renpy-$renpy_version-sdk.tar.bz2" -o "$build_tools_dir/sdk.tar.bz2"
curl --fail --location --retry 3 --silent --show-error \
  "$base_url/renpy-$renpy_version-web.zip" -o "$build_tools_dir/web.zip"
tar -xjf "$build_tools_dir/sdk.tar.bz2" -C "$build_tools_dir"
export RENPY_SDK="$build_tools_dir/renpy-$renpy_version-sdk"
unzip -q "$build_tools_dir/web.zip" -d "$RENPY_SDK"
export SDL_VIDEODRIVER=dummy
export SDL_AUDIODRIVER=dummy
bash "$project_dir/scripts/build-web.sh"
# Engine debug symbols are not needed by players.
rm -f "$project_dir/dist/SeasCompany-1.0-web/index.html.symbols"
