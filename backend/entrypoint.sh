#!/bin/sh

HASH_FILE="/app/src/data/data_file_hash"
CURRENT_HASH=$(sha256sum /app/src/data/deck-fighter.xls | awk '{ print $1 }')

if [ -f "$HASH_FILE" ]; then
    STORED_HASH=$(cat "$HASH_FILE")
else
    STORED_HASH=""
fi

if [ "$CURRENT_HASH" != "$STORED_HASH" ]; then
    echo "Data file has changed. Running the populate_db script."
    python /app/src/scripts/populate_db.py
    echo "$CURRENT_HASH" > "$HASH_FILE"
else
    echo "Data file has not changed. Skipping the populate_db script."
fi

exec "$@"
