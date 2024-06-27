#!/bin/bash
set -e

# Set environment variables
export DATABASE_URL="postgresql+psycopg2://dev_user:dev_password@localhost:5432/unmatched_dev"

# Change to the directory where the script is located
cd "$(dirname "$0")"

# Run the database population script
python populate_db.py
