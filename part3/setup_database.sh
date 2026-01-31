#!/bin/bash

# HBnB Database Setup Script
# This script automates the database creation and initialization

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
DB_TYPE="mysql"
DB_NAME="hbnb_db"
DB_USER="root"
DB_PASS=""

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Function to show usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    -t, --type      Database type (mysql|sqlite|postgres) [default: mysql]
    -n, --name      Database name [default: hbnb_db]
    -u, --user      Database user [default: root]
    -p, --password  Database password
    -h, --help      Show this help message

Examples:
    # MySQL with password prompt
    $0 -t mysql -n hbnb_db -u root

    # SQLite
    $0 -t sqlite -n hbnb.db

    # PostgreSQL
    $0 -t postgres -n hbnb_db -u postgres -p mypassword

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            DB_TYPE="$2"
            shift 2
            ;;
        -n|--name)
            DB_NAME="$2"
            shift 2
            ;;
        -u|--user)
            DB_USER="$2"
            shift 2
            ;;
        -p|--password)
            DB_PASS="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Function to setup MySQL/MariaDB
setup_mysql() {
    print_info "Setting up MySQL/MariaDB database..."

    # Prepare password option
    PASS_OPT=""
    if [ -n "$DB_PASS" ]; then
        PASS_OPT="-p${DB_PASS}"
    else
        PASS_OPT="-p"
    fi

    # Create database
    print_info "Creating database ${DB_NAME}..."
    mysql -u ${DB_USER} ${PASS_OPT} -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME};" || {
        print_error "Failed to create database"
        exit 1
    }
    print_success "Database created"

    # Create schema
    print_info "Creating tables..."
    mysql -u ${DB_USER} ${PASS_OPT} ${DB_NAME} < schema.sql || {
        print_error "Failed to create schema"
        exit 1
    }
    print_success "Tables created"

    # Insert seed data
    print_info "Inserting initial data..."
    mysql -u ${DB_USER} ${PASS_OPT} ${DB_NAME} < seed_data.sql || {
        print_error "Failed to insert seed data"
        exit 1
    }
    print_success "Initial data inserted"

    print_success "MySQL database setup complete!"
}

# Function to setup SQLite
setup_sqlite() {
    print_info "Setting up SQLite database..."

    # Remove existing database if exists
    if [ -f "${DB_NAME}" ]; then
        print_info "Removing existing database..."
        rm "${DB_NAME}"
    fi

    # Create database and schema
    print_info "Creating database and tables..."
    sqlite3 ${DB_NAME} < schema.sql || {
        print_error "Failed to create schema"
        exit 1
    }
    print_success "Tables created"

    # Insert seed data
    print_info "Inserting initial data..."
    sqlite3 ${DB_NAME} < seed_data.sql || {
        print_error "Failed to insert seed data"
        exit 1
    }
    print_success "Initial data inserted"

    print_success "SQLite database setup complete!"
    print_info "Database file: ${DB_NAME}"
}

# Function to setup PostgreSQL
setup_postgres() {
    print_info "Setting up PostgreSQL database..."

    # Prepare password option
    if [ -n "$DB_PASS" ]; then
        export PGPASSWORD="${DB_PASS}"
    fi

    # Create database
    print_info "Creating database ${DB_NAME}..."
    psql -U ${DB_USER} -c "CREATE DATABASE ${DB_NAME};" 2>/dev/null || {
        print_info "Database might already exist, continuing..."
    }
    print_success "Database ready"

    # Create schema
    print_info "Creating tables..."
    psql -U ${DB_USER} -d ${DB_NAME} -f schema.sql || {
        print_error "Failed to create schema"
        exit 1
    }
    print_success "Tables created"

    # Insert seed data
    print_info "Inserting initial data..."
    psql -U ${DB_USER} -d ${DB_NAME} -f seed_data.sql || {
        print_error "Failed to insert seed data"
        exit 1
    }
    print_success "Initial data inserted"

    unset PGPASSWORD
    print_success "PostgreSQL database setup complete!"
}

# Main execution
echo ""
echo "═══════════════════════════════════"
echo "  HBnB Database Setup"
echo "═══════════════════════════════════"
echo ""

case $DB_TYPE in
    mysql|mariadb)
        setup_mysql
        ;;
    sqlite)
        setup_sqlite
        ;;
    postgres|postgresql)
        setup_postgres
        ;;
    *)
        print_error "Unknown database type: $DB_TYPE"
        echo "Supported types: mysql, sqlite, postgres"
        exit 1
        ;;
esac

echo ""
echo "═══════════════════════════════════"
print_success "Setup Complete!"
echo "═══════════════════════════════════"
echo ""
echo "Initial Data:"
echo "  • Admin User: admin@hbnb.io (password: admin1234)"
echo "  • Amenities: WiFi, Swimming Pool, Air Conditioning"
echo ""
echo "To test the database, run:"
echo "  ${DB_TYPE} -u ${DB_USER} ${DB_NAME} < test_queries.sql"
echo ""
