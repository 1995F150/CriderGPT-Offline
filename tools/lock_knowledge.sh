#!/usr/bin/env bash
# Advisory: make knowledge.json immutable on Linux
set -e
KNOW="$(pwd)/knowledge/knowledge.json"
if [ ! -f "$KNOW" ]; then
  echo "knowledge.json not found at $KNOW"
  exit 1
fi
sudo chattr +i "$KNOW"
echo "Marked $KNOW immutable (chattr +i)."
