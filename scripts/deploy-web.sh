#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd "$(dirname "$0")/.." && pwd)"
"$project_dir/scripts/build-web.sh"
cd "$project_dir"
# Uses the existing local Vercel link. On a fresh clone, run vercel link first.
vercel deploy "$@"
