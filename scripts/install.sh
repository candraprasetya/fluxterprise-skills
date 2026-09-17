#!/usr/bin/env bash
# fluxterprise-skills installer
# Usage: ./install.sh /path/to/your/project
# Or:    ./install.sh .  (from your project directory)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$(dirname "$SCRIPT_DIR")/skills"

if [ $# -eq 0 ]; then
  echo "Usage: $0 <project-directory>"
  echo "  Installs fluxterprise skills into the target project."
  echo ""
  echo "Example:"
  echo "  $0 /path/to/my-flutter-app"
  echo "  $0 ."
  exit 1
fi

PROJECT_DIR="$(cd "$1" && pwd)"

if [ ! -d "$PROJECT_DIR" ]; then
  echo "Error: '$1' is not a valid directory."
  exit 1
fi

# Detect entry file
ENTRY_FILE=""
if [ -f "$PROJECT_DIR/CLAUDE.md" ]; then
  ENTRY_FILE="$PROJECT_DIR/CLAUDE.md"
elif [ -f "$PROJECT_DIR/AGENTS.md" ]; then
  ENTRY_FILE="$PROJECT_DIR/AGENTS.md"
elif [ -f "$PROJECT_DIR/GEMINI.md" ]; then
  ENTRY_FILE="$PROJECT_DIR/GEMINI.md"
fi

echo "fluxterprise-skills installer"
echo "============================="
echo ""
echo "Project:   $PROJECT_DIR"
echo "Skills:    $SKILLS_DIR"

# Copy skills directory
TARGET_SKILLS="$PROJECT_DIR/skills"

if [ -d "$TARGET_SKILLS" ]; then
  echo ""
  echo "Existing skills/ directory found. Merging..."
  cp -rv "$SKILLS_DIR"/* "$TARGET_SKILLS"/
else
  echo ""
  echo "Creating skills/ directory..."
  cp -r "$SKILLS_DIR" "$TARGET_SKILLS"
fi

echo ""
echo "Skills installed to: $TARGET_SKILLS"

# Detect which skills are available
AVAILABLE_SKILLS=""
for skill_dir in "$TARGET_SKILLS"/fluxterprise*/; do
  if [ -f "$skill_dir/SKILL.md" ]; then
    skill_name="$(basename "$skill_dir")"
    AVAILABLE_SKILLS="$AVAILABLE_SKILLS
- \`skills/$skill_name/SKILL.md\`"
  fi
done

# Pointer block
POINTER_BLOCK="<!-- fluxterprise:start -->
## fluxterprise
For UI, copy, people, mobile layout, code comments, or Flutter work, read \`skills/fluxterprise/SKILL.md\` (core) and then the skill for the task:$AVAILABLE_SKILLS
Before starting, ask the user when fluxterprise applies: during the work, or after it is done.
<!-- fluxterprise:end -->"

if [ -z "$ENTRY_FILE" ]; then
  echo ""
  echo "No entry file found (CLAUDE.md, AGENTS.md, or GEMINI.md)."
  echo "Creating CLAUDE.md with the pointer block..."
  ENTRY_FILE="$PROJECT_DIR/CLAUDE.md"
  echo "$POINTER_BLOCK" > "$ENTRY_FILE"
  echo "Created: $ENTRY_FILE"
else
  echo ""
  echo "Entry file: $ENTRY_FILE"

  # Check if fluxterprise block already exists
  if grep -q "<!-- fluxterprise:start -->" "$ENTRY_FILE" 2>/dev/null; then
    echo "Existing fluxterprise block found. Replacing..."
    # Use temp file for macOS compatibility
    TEMP_FILE=$(mktemp)
    awk '
      /<!-- fluxterprise:start -->/ { print "'"$POINTER_BLOCK"'"; skip=1; next }
      /<!-- fluxterprise:end -->/ { skip=0; next }
      !skip { print }
    ' "$ENTRY_FILE" > "$TEMP_FILE"
    mv "$TEMP_FILE" "$ENTRY_FILE"
  else
    echo "Appending pointer block to $ENTRY_FILE..."
    echo "" >> "$ENTRY_FILE"
    echo "$POINTER_BLOCK" >> "$ENTRY_FILE"
  fi
  echo "Updated: $ENTRY_FILE"
fi

echo ""
echo "Done! Skills are installed."
echo ""
echo "Next steps:"
echo "  1. Review the pointer block in your entry file"
echo "  2. Start a new session (pointer block takes effect next session)"
echo "  3. When the agent asks about fluxterprise, choose:"
echo "     - DURING: rules apply while working"
echo "     - AFTER: audit existing code"
echo ""
echo "For Flutter projects, also load:"
echo "  skills/fluxterprise-flutter/SKILL.md       - architecture, Dart shorthand, memory"
echo "  skills/fluxterprise-flutter-motion/SKILL.md - 60fps animations, micro-interactions"
echo ""
echo "For testing, also load:"
echo "  skills/fluxterprise-testing/SKILL.md        - unit, widget, integration, a11y testing"
