
DB_USER="devuser"
DB_PASSWORD="devpassword"
DB_NAME="devunmatched"

echo "Creating PostgreSQL user and database..."

# Check for PostgreSQL
if ! command -v psql > /dev/null; then
  echo "psql command not found. Please install PostgreSQL and try again."
  exit 1
fi

# Create user
if ! psql -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
  psql -U postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
  echo "User '$DB_USER' created."
else
  echo "User '$DB_USER' already exists."
fi

# Create database
if ! psql -U postgres -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
  psql -U postgres -c "CREATE DATABASE $DB_NAME;"
  echo "Database '$DB_NAME' created."
else
  echo "Database '$DB_NAME' already exists."
fi

# Grant privileges
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
echo "Granted all privileges on database '$DB_NAME' to user '$DB_USER'."

echo "Setup complete. Please restart your terminal."