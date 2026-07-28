#!/bin/sh
# Install the owned pre-push hook for the current repository only.
# Usage: sh scripts/install-hooks.sh

set -eu

ROOT=$(git rev-parse --show-toplevel) || {
    echo "Not inside a Git work tree; hook was not installed." >&2
    exit 1
}
COMMON_DIR=$(git rev-parse --path-format=absolute --git-common-dir)
HOOKS=$(git rev-parse --path-format=absolute --git-path hooks)
SOURCE="$ROOT/scripts/pre-push"
TARGET="$HOOKS/pre-push"

case "$HOOKS" in
    "$COMMON_DIR"/hooks) ;;
    *)
        echo "Refusing unsafe hook destination." >&2
        exit 1
        ;;
esac

if [ ! -f "$SOURCE" ]; then
    echo "Owned pre-push hook is missing." >&2
    exit 1
fi

if [ -e "$TARGET" ] || [ -L "$TARGET" ]; then
    echo "Existing pre-push hook preserved at $TARGET; refusing to overwrite it." >&2
    exit 1
fi

mkdir -p "$HOOKS"
cp "$SOURCE" "$TARGET"
chmod 755 "$TARGET"
echo "Installed owned pre-push hook: $TARGET"