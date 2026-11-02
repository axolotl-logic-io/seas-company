#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd "$(dirname "$0")/.." && pwd)"
cd "$project_dir"
# Vercel builds from source. On a fresh clone, run vercel link first.
vercel deploy "$@"
