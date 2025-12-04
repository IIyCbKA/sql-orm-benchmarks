#!/usr/bin/env bash
set -euo pipefail

DC=""
if command -v docker-compose >/dev/null 2>&1; then
  DC="docker-compose"
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  DC="docker compose"
else
  echo "ERROR: neither 'docker-compose' nor 'docker compose' found in PATH." >&2
  exit 1
fi

declare -A MAP=(
  ["pony"]="./benchmarks/pony_bench"
  ["sqlalchemy"]="./benchmarks/sqlalchemy_bench"
)

NAME="${1:-}"
MODE="${2:-sync}"
if [ -z "$NAME" ]; then
  echo "Usage: $0 <solution-name> [sync|async]"
  echo "Available: ${!MAP[@]}"
  exit 1
fi

CONTEXT="${MAP[$NAME]:-}"
if [ -z "$CONTEXT" ]; then
  echo "ERROR: unknown solution name: '$NAME'. Available: ${!MAP[@]}" >&2
  exit 2
fi

case "$MODE" in
  sync|async) ;;
  *)
    echo "ERROR: unknown mode: '$MODE'. Use 'sync' or 'async'." >&2
    exit 3
    ;;
esac

export RUNNER_BUILD_CONTEXT="$CONTEXT"
export RUNNER_NAME="$NAME"
export RUNNER_COMMAND="$MODE"

echo "Using compose command: $DC"
echo "Starting '$NAME' (mode: $MODE) with context '$CONTEXT' ..."

$DC -f docker-compose.yaml up -d --build

echo
echo "Done. To follow logs: $DC -f docker-compose.yaml logs -f"
echo "To stop and remove containers+volumes: ./stop.sh $NAME"
