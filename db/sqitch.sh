#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    set -o allexport
    source .env
    set +o allexport
else
    echo "Warning: .env file not found. Ensure database URLs are set in the environment."
fi

# Check if the first argument is a stage
if [[ "$1" =~ ^(dev|beta|gamma|prod)$ ]]; then
    STAGE="$1"
    shift  # Remove stage argument from the list
else
    STAGE="dev"  # Default to dev if no stage is specified
fi

# Define stage-based database URLs
case "$STAGE" in
    dev)
        DATABASE_URL=${DATABASE_URL_DEV}
        ;;
    beta)
        DATABASE_URL=${DATABASE_URL_BETA}
        ;;
    gamma)
        DATABASE_URL=${DATABASE_URL_GAMMA}
        ;;
    prod)
        DATABASE_URL=${DATABASE_URL_PROD}
        ;;
    *)
        echo "Error: Unknown STAGE '$STAGE'. Allowed values: dev, beta, gamma, prod."
        exit 1
        ;;
esac


if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL is not set for stage '$STAGE'. Please set it in the .env file or environment."
    exit 1
fi

# Check for revert command and ensure --to is specified
if [[ "$@" == *"revert"* ]]; then
    if [[ "$@" != *"--to"* ]]; then
        echo "Error: The 'revert' command requires the '--to' option to specify the target migration."
        exit 1
    fi
fi

# Ensure all migration SQL files in deploy/ and revert/ directories have BEGIN as first and COMMIT as last statement
MIGRATION_DIRS=("deploy" "revert")
MISSING_STATEMENTS=0

for DIR in "${MIGRATION_DIRS[@]}"; do
    if [ -d "$DIR" ]; then
        for FILE in $(find "$DIR" -name '*.sql'); do
            # Get first non-empty, non-comment line
            FIRST_STATEMENT=$(grep -E '^\s*[^--]' "$FILE" | head -n 1 | tr -d '[:space:]')
            # Get last non-empty, non-comment line
            LAST_STATEMENT=$(grep -E '^\s*[^--]' "$FILE" | tail -n 1 | tr -d '[:space:]')

            if [[ "$FIRST_STATEMENT" != "BEGIN;" ]]; then
                echo "Error: BEGIN; is not the first statement in $FILE"
                echo "First statement: $FIRST_STATEMENT"
                MISSING_STATEMENTS=1
            fi
            if [[ "$LAST_STATEMENT" != "COMMIT;" ]]; then
                echo "Error: COMMIT; is not the last statement in $FILE"
                MISSING_STATEMENTS=1
            fi
        done
    else
        echo "Warning: Directory '$DIR' does not exist."
    fi
done

if [ "$MISSING_STATEMENTS" -eq 1 ]; then
    echo "Error: One or more SQL migration files are missing BEGIN; as the first statement or COMMIT; as the last statement."
    exit 1
fi

# Run the Sqitch command with the DATABASE_URL as the target
sqitch "$@" --target "$DATABASE_URL"

# Clean up database connections
psql "$DATABASE_URL" -c "DISCARD ALL;"
