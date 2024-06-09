
DB_USER="dev_user"
DB_PASSWORD="dev_password"
DB_NAME="unmatched_dev"
DB_NAME_TEST="unmatched_test"

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
  psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
  psql -U postgres -d $DB_NAME -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;"
  echo "Database '$DB_NAME' created."
else
  echo "Database '$DB_NAME' already exists."
fi

# Create test database
if ! psql -U postgres -lqt | cut -d \| -f 1 | grep -qw $DB_NAME_TEST; then
  psql -U postgres -c "CREATE DATABASE $DB_NAME_TEST;"
  psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME_TEST TO $DB_USER;"
  psql -U postgres -d $DB_NAME_TEST -c "GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;"
  echo "Test database '$DB_NAME_TEST' created."
else
  echo "Test database '$DB_NAME_TEST' already exists."
fi

echo "Setup complete. Please restart your terminal."