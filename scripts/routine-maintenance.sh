#!/bin/bash

# Routine Maintenance Script for BASH Consultants
# This script prepares prompt workflows for VS Code Chat extension
# Usage: ./routine-maintenance.sh [command] [file/folder] [options]

set -e

# Configuration
PROMPTS_DIR=".github/prompts"
WORKSPACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print usage
usage() {
    echo "Usage: $0 [command] [target] [options]"
    echo ""
    echo "Commands:"
    echo "  refactor [file]          - Prepare refactoring prompt for a file"
    echo "  test [file]              - Prepare test generation prompt for a file"
    echo "  docs [file/folder]       - Prepare documentation prompt for a file or folder"
    echo "  debug [file]             - Prepare debugging prompt for a file"
    echo "  full-maintenance [file]  - Run complete maintenance workflow (refactor -> test -> docs)"
    echo "  analyze [file/folder]    - Prepare requirements analysis for a file or folder"
    echo "  design [file]            - Prepare system design prompt for a file"
    echo "  implement [spec]         - Prepare code implementation prompt for a spec"
    echo "  review [file/folder]     - Prepare article review and expansion prompt"
    echo "  workflow [type] [target] - Run predefined workflow"
    echo ""
    echo "Options:"
    echo "  --copy                   - Copy output to clipboard (macOS only)"
    echo "  --chat                   - Format output for direct chat paste"
    echo "  --verbose                - Show detailed output"
    echo ""
    echo "Examples:"
    echo "  $0 refactor src/main.js"
    echo "  $0 full-maintenance src/component.js --copy"
    echo "  $0 workflow feature pages/_posts/new-feature.md"
}

# Function to check if file exists
check_file() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo -e "${RED}Error: File '$file' not found${NC}" >&2
        exit 1
    fi
}

# Function to check if folder exists
check_folder() {
    local folder="$1"
    if [[ ! -d "$folder" ]]; then
        echo -e "${RED}Error: Folder '$folder' not found${NC}" >&2
        exit 1
    fi
}

# Function to read file content safely
read_file_content() {
    local file="$1"
    local max_lines=100

    if [[ ! -f "$file" ]]; then
        echo "[File not found: $file]"
        return
    fi

    # Get file size
    local size=$(wc -c < "$file")
    if [[ $size -gt 100000 ]]; then
        echo "[Large file ($size bytes). Showing first $max_lines lines:]"
        head -n $max_lines "$file"
        echo "... [truncated - $((size/1024))KB total]"
    else
        cat "$file"
    fi
}

# Function to load prompt template
load_prompt() {
    local prompt_name="$1"
    local prompt_file="$WORKSPACE_ROOT/$PROMPTS_DIR/${prompt_name}.prompt.md"

    if [[ ! -f "$prompt_file" ]]; then
        echo -e "${RED}Error: Prompt file '$prompt_file' not found${NC}" >&2
        exit 1
    fi

    # Extract content after the frontmatter
    awk '
    BEGIN { in_frontmatter = 0; found_separator = 0 }
    /^---$/ {
        if (in_frontmatter == 0) {
            in_frontmatter = 1
        } else if (in_frontmatter == 1) {
            in_frontmatter = 2
            next
        }
    }
    in_frontmatter == 2 { print }
    ' "$prompt_file"
}

# Function to format output for chat
format_for_chat() {
    local prompt_content="$1"
    local context="$2"

    echo "---"
    echo "Copy and paste the following into your VS Code Chat extension:"
    echo "---"
    echo ""
    echo "$prompt_content"
    echo ""
    echo "Context/Input:"
    echo "$context"
    echo ""
    echo "---"
}

# Function to copy to clipboard (macOS)
copy_to_clipboard() {
    local content="$1"
    if command -v pbcopy &> /dev/null; then
        echo "$content" | pbcopy
        echo -e "${GREEN}✓ Output copied to clipboard${NC}"
    else
        echo -e "${YELLOW}Note: pbcopy not available. Install it or manually copy the output.${NC}"
    fi
}

# Command: refactor
cmd_refactor() {
    local file="$1"
    check_file "$file"

    echo -e "${BLUE}Preparing refactoring prompt for: $file${NC}"

    local prompt_content=$(load_prompt "code-refactoring")
    local file_content=$(read_file_content "$file")

    local context="File to refactor: $file

\`\`\`
$file_content
\`\`\`"

    if [[ "$CHAT_MODE" == "true" ]]; then
        format_for_chat "$prompt_content" "$context"
    else
        echo "$prompt_content"
        echo ""
        echo "Context/Input:"
        echo "$context"
    fi
}

# Command: test
cmd_test() {
    local file="$1"
    check_file "$file"

    echo -e "${BLUE}Preparing test generation prompt for: $file${NC}"

    local prompt_content=$(load_prompt "test-generation")
    local file_content=$(read_file_content "$file")

    local context="Code to test: $file

\`\`\`
$file_content
\`\`\`"

    if [[ "$CHAT_MODE" == "true" ]]; then
        format_for_chat "$prompt_content" "$context"
    else
        echo "$prompt_content"
        echo ""
        echo "Context/Input:"
        echo "$context"
    fi
}

# Command: docs
cmd_docs() {
    local target="$1"

    if [[ -f "$target" ]]; then
        check_file "$target"
        echo -e "${BLUE}Preparing documentation prompt for file: $target${NC}"
        local content_type="file"
        local content=$(read_file_content "$target")
    elif [[ -d "$target" ]]; then
        check_folder "$target"
        echo -e "${BLUE}Preparing documentation prompt for folder: $target${NC}"
        local content_type="folder"
        local content="[Folder contents would be listed here - $target]"
    else
        echo -e "${RED}Error: Target '$target' is neither a file nor folder${NC}" >&2
        exit 1
    fi

    local prompt_content=$(load_prompt "documentation")

    local context="Content to document: $target ($content_type)

\`\`\`
$content
\`\`\`"

    if [[ "$CHAT_MODE" == "true" ]]; then
        format_for_chat "$prompt_content" "$context"
    else
        echo "$prompt_content"
        echo ""
        echo "Context/Input:"
        echo "$context"
    fi
}

# Command: debug
cmd_debug() {
    local file="$1"
    check_file "$file"

    echo -e "${BLUE}Preparing debugging prompt for: $file${NC}"

    local prompt_content=$(load_prompt "debugging")
    local file_content=$(read_file_content "$file")

    local context="Code to debug: $file

\`\`\`
$file_content
\`\`\`

Error/Symptoms: [Please describe the error or unexpected behavior here]"

    if [[ "$CHAT_MODE" == "true" ]]; then
        format_for_chat "$prompt_content" "$context"
    else
        echo "$prompt_content"
        echo ""
        echo "Context/Input:"
        echo "$context"
    fi
}

# Command: analyze
cmd_analyze() {
    local target="$1"

    if [[ -f "$target" ]]; then
        check_file "$target"
        echo -e "${BLUE}Preparing requirements analysis for file: $target${NC}"
        local content=$(read_file_content "$target")
    elif [[ -d "$target" ]]; then
        check_folder "$target"
        echo -e "${BLUE}Preparing requirements analysis for folder: $target${NC}"
        local content="[Folder contents: $target]"
    else
        echo -e "${RED}Error: Target '$target' is neither a file nor folder${NC}" >&2
        exit 1
    fi

    local prompt_content=$(load_prompt "requirements-analysis")

    local context="Content to analyze: $target

$content"

    if [[ "$CHAT_MODE" == "true" ]]; then
        format_for_chat "$prompt_content" "$context"
    else
        echo "$prompt_content"
        echo ""
        echo "Context/Input:"
        echo "$context"
    fi
}

# Command: design
cmd_design() {
    local file="$1"
    check_file "$file"

    echo -e "${BLUE}Preparing system design prompt for: $file${NC}"

    local prompt_content=$(load_prompt "system-design")
    local file_content=$(read_file_content "$file")

    local context="Requirements/Specification: $file

\`\`\`
$file_content
\`\`\`"

    if [[ "$CHAT_MODE" == "true" ]]; then
        format_for_chat "$prompt_content" "$context"
    else
        echo "$prompt_content"
        echo ""
        echo "Context/Input:"
        echo "$context"
    fi
}

# Command: implement
cmd_implement() {
    local spec="$1"
    check_file "$spec"

    echo -e "${BLUE}Preparing code implementation prompt for spec: $spec${NC}"

    local prompt_content=$(load_prompt "code-implementation")
    local spec_content=$(read_file_content "$spec")

    local context="Specification to implement: $spec

\`\`\`
$spec_content
\`\`\`

Target language/framework: [Specify here, e.g., Python, React, etc.]"

    if [[ "$CHAT_MODE" == "true" ]]; then
        format_for_chat "$prompt_content" "$context"
    else
        echo "$prompt_content"
        echo ""
        echo "Context/Input:"
        echo "$context"
    fi
}

# Command: review
cmd_review() {
    local target="$1"
    local content=""
    local context_note=""

    if [[ -f "$target" ]]; then
        check_file "$target"
        echo -e "${BLUE}Preparing article review for file: $target${NC}"
        content=$(read_file_content "$target")
    elif [[ -d "$target" ]]; then
        check_folder "$target"
        echo -e "${BLUE}Preparing article review for folder: $target${NC}"
        
        # Find the most recent markdown file
        local recent_file=$(find "$target" -name "*.md" -type f -print0 | xargs -0 ls -t | head -n 1)
        
        if [[ -n "$recent_file" ]]; then
            echo -e "${YELLOW}Selected most recent file: $recent_file${NC}"
            content=$(read_file_content "$recent_file")
            context_note="[Note: Automatically selected most recent file from $target]"
        else
            echo -e "${RED}No markdown files found in $target${NC}" >&2
            exit 1
        fi
    else
        echo -e "${RED}Error: Target '$target' is neither a file nor folder${NC}" >&2
        exit 1
    fi

    local prompt_content=$(load_prompt "article-review")

    local context="Article to review: $target
$context_note

\`\`\`
$content
\`\`\`"

    if [[ "$CHAT_MODE" == "true" ]]; then
        format_for_chat "$prompt_content" "$context"
    else
        echo "$prompt_content"
        echo ""
        echo "Context/Input:"
        echo "$context"
    fi
}

# Command: full-maintenance
cmd_full_maintenance() {
    local file="$1"
    check_file "$file"

    echo -e "${BLUE}Running full maintenance workflow for: $file${NC}"
    echo -e "${YELLOW}This will generate prompts for refactoring, testing, and documentation.${NC}"
    echo ""

    # Refactor step
    echo "=== STEP 1: Code Refactoring ==="
    CHAT_MODE="$CHAT_MODE" cmd_refactor "$file"
    echo ""

    # Test step
    echo "=== STEP 2: Test Generation ==="
    CHAT_MODE="$CHAT_MODE" cmd_test "$file"
    echo ""

    # Docs step
    echo "=== STEP 3: Documentation ==="
    CHAT_MODE="$CHAT_MODE" cmd_docs "$file"
    echo ""

    echo -e "${GREEN}Full maintenance workflow prepared. Run each step in your VS Code Chat extension.${NC}"
}

# Command: workflow
cmd_workflow() {
    local workflow_type="$1"
    local target="$2"

    case "$workflow_type" in
        "feature")
            echo -e "${BLUE}Running feature development workflow for: $target${NC}"
            # Analyze -> Design -> Implement -> Test -> Docs
            cmd_analyze "$target"
            echo ""
            cmd_design "$target"
            echo ""
            cmd_implement "$target"
            echo ""
            cmd_test "$target"
            echo ""
            cmd_docs "$target"
            ;;
        "maintenance")
            cmd_full_maintenance "$target"
            ;;
        "debug")
            cmd_debug "$target"
            ;;
        "content-review")
            cmd_review "$target"
            ;;
        *)
            echo -e "${RED}Error: Unknown workflow type '$workflow_type'${NC}" >&2
            echo "Available workflows: feature, maintenance, debug, content-review"
            exit 1
            ;;
    esac
}

# Main script logic
main() {
    if [[ $# -lt 1 ]]; then
        usage
        exit 1
    fi

    local command="$1"
    shift

    # Parse options
    COPY_MODE=false
    CHAT_MODE=false
    VERBOSE=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            --copy)
                COPY_MODE=true
                shift
                ;;
            --chat)
                CHAT_MODE=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            *)
                break
                ;;
        esac
    done

    # Execute command
    case "$command" in
        refactor)
            [[ $# -lt 1 ]] && { echo -e "${RED}Error: refactor requires a file argument${NC}"; exit 1; }
            output=$(cmd_refactor "$1")
            ;;
        test)
            [[ $# -lt 1 ]] && { echo -e "${RED}Error: test requires a file argument${NC}"; exit 1; }
            output=$(cmd_test "$1")
            ;;
        docs)
            [[ $# -lt 1 ]] && { echo -e "${RED}Error: docs requires a file/folder argument${NC}"; exit 1; }
            output=$(cmd_docs "$1")
            ;;
        debug)
            [[ $# -lt 1 ]] && { echo -e "${RED}Error: debug requires a file argument${NC}"; exit 1; }
            output=$(cmd_debug "$1")
            ;;
        analyze)
            [[ $# -lt 1 ]] && { echo -e "${RED}Error: analyze requires a file/folder argument${NC}"; exit 1; }
            output=$(cmd_analyze "$1")
            ;;
        design)
            [[ $# -lt 1 ]] && { echo -e "${RED}Error: design requires a file argument${NC}"; exit 1; }
            output=$(cmd_design "$1")
            ;;
        implement)
            [[ $# -lt 1 ]] && { echo -e "${RED}Error: implement requires a spec file argument${NC}"; exit 1; }
            output=$(cmd_implement "$1")
            ;;
        review)
            [[ $# -lt 1 ]] && { echo -e "${RED}Error: review requires a file/folder argument${NC}"; exit 1; }
            output=$(cmd_review "$1")
            ;;
        full-maintenance)
            [[ $# -lt 1 ]] && { echo -e "${RED}Error: full-maintenance requires a file argument${NC}"; exit 1; }
            cmd_full_maintenance "$1"
            exit 0
            ;;
        workflow)
            [[ $# -lt 2 ]] && { echo -e "${RED}Error: workflow requires type and target arguments${NC}"; exit 1; }
            cmd_workflow "$1" "$2"
            exit 0
            ;;
        *)
            echo -e "${RED}Error: Unknown command '$command'${NC}" >&2
            usage
            exit 1
            ;;
    esac

    # Handle output
    if [[ "$COPY_MODE" == "true" ]]; then
        copy_to_clipboard "$output"
    else
        echo "$output"
    fi

    if [[ "$VERBOSE" == "true" ]]; then
        echo ""
        echo -e "${BLUE}Prompt preparation complete. Copy the output above into your VS Code Chat extension.${NC}"
    fi
}

# Run main function
main "$@"