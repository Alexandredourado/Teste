#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/Hub_Painel/HUB"
FRONTEND_DIR="$ROOT_DIR/Frontend Design for Hansu"
API_PORT="${API_PORT:-8000}"
WEB_PORT="${WEB_PORT:-5173}"
API_BASE_URL="${VITE_API_BASE_URL:-http://localhost:${API_PORT}/api}"
INSTALL_DEPS=1

usage() {
  cat <<'EOF'
Hansu Hub launcher (backend + frontend)

Usage:
  ./start_hub.sh [--no-install]

Options:
  --no-install   Skip dependency install steps (pip/npm).
  -h, --help     Show this help.

Environment variables:
  API_PORT             Backend port (default: 8000)
  WEB_PORT             Frontend port (default: 5173)
  VITE_API_BASE_URL    Frontend API base URL (default: http://localhost:$API_PORT/api)
EOF
}

for arg in "$@"; do
  case "$arg" in
    --no-install)
      INSTALL_DEPS=0
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg"
      usage
      exit 1
      ;;
  esac
done

if [[ ! -d "$BACKEND_DIR" || ! -d "$FRONTEND_DIR" ]]; then
  echo "❌ Could not find expected project directories."
  echo "Expected:"
  echo "  - $BACKEND_DIR"
  echo "  - $FRONTEND_DIR"
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "❌ npm not found in PATH."
  exit 1
fi

if [[ "$INSTALL_DEPS" -eq 0 ]] && ! command -v uvicorn >/dev/null 2>&1; then
  echo "❌ uvicorn not found in PATH. Install dependencies first or run without --no-install."
  exit 1
fi

if [[ "$INSTALL_DEPS" -eq 1 ]]; then
  echo "📦 Installing backend dependencies..."
  python3 -m pip install -r "$BACKEND_DIR/requirements.txt"

  echo "📦 Installing frontend dependencies..."
  (cd "$FRONTEND_DIR" && npm install)
else
  echo "⏭️  Skipping dependency installation (--no-install)."
fi

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
  echo
  echo "🧹 Stopping services..."
  if [[ -n "$FRONTEND_PID" ]] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
    kill "$FRONTEND_PID" 2>/dev/null || true
  fi
  if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

echo "🚀 Starting backend on port $API_PORT..."
(
  cd "$BACKEND_DIR"
  uvicorn backend.api:app --host 0.0.0.0 --port "$API_PORT" --reload
) &
BACKEND_PID=$!

sleep 2
if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
  echo "❌ Backend failed to start."
  wait "$BACKEND_PID" || true
  exit 1
fi

echo "🚀 Starting frontend on port $WEB_PORT..."
(
  cd "$FRONTEND_DIR"
  VITE_API_BASE_URL="$API_BASE_URL" npm run dev -- --host 0.0.0.0 --port "$WEB_PORT"
) &
FRONTEND_PID=$!

sleep 2
if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
  echo "❌ Frontend failed to start."
  wait "$FRONTEND_PID" || true
  exit 1
fi

echo ""
echo "✅ Services started"
echo "   Backend:  http://localhost:${API_PORT}/api/health"
echo "   Frontend: http://localhost:${WEB_PORT}"
echo ""
echo "Press Ctrl+C to stop both services."

wait "$BACKEND_PID" "$FRONTEND_PID"
