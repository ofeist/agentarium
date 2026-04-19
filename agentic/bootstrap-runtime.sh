#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$REPO_ROOT"

FILES=(
  "agentic/state.example.yaml:agentic/state.yaml"
  "agentic/tasks.example.yaml:agentic/tasks.yaml"
  "agentic/agent-config.example.yaml:agentic/agent-config.yaml"
)

existing=()
for mapping in "${FILES[@]}"; do
  src="${mapping%%:*}"
  dst="${mapping##*:}"
  if [ -e "$dst" ]; then
    existing+=("$dst")
  fi
done

if [ "${#existing[@]}" -gt 0 ]; then
  echo "Refusing to overwrite existing runtime files:" >&2
  printf ' - %s\n' "${existing[@]}" >&2
  exit 1
fi

for mapping in "${FILES[@]}"; do
  src="${mapping%%:*}"
  dst="${mapping##*:}"
  cp "$src" "$dst"
  echo "initialized $dst from $src"
done
