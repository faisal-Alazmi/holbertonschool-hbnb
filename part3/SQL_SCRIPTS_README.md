# HBnB SQL Scripts Documentation

This directory contains SQL scripts for creating and managing the HBnB database schema.

## Files Overview

### 1. `schema.sql`
Creates the complete database schema including:
- **users** table - Stores user information
- **places** table - Stores place listings
- **reviews** table - Stores reviews for places
- **amenities** table - Stores available amenities
- **place_amenity** table - Junction table for many-to-many relationship

### 2. `seed_data.sql`
Inserts initial data:
- Administrator user (email: admin@hbnb.io, password: admin1234)
- Three amenities: WiFi, Swimming Pool, Air Conditioning

### 3. `test_queries.sql`
Contains comprehensive test queries to verify:
- CRUD operations (Create, Read, Update, Delete)
- Relationship queries with JOINs
- Constraint validations
- Cascade operations

### 4. `generate_password_hash.py`
Python script to generate bcrypt password hashes

## Usage

### MySQL/MariaDB

```bash
# 1. Create database
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS hbnb_db;"

# 2. Create schema
mysql -u root -p hbnb_db < schema.sql

# 3. Insert initial data
mysql -u root -p hbnb_db < seed_data.sql

# 4. Run tests (optional)
mysql -u root -p hbnb_db < test_queries.sql
```

### SQLite

```bash
# 1. Create database and schema
sqlite3 hbnb.db < schema.sql

# 2. Insert initial data
sqlite3 hbnb.db < seed_data.sql

# 3. Run tests (optional)
sqlite3 hbnb.db < test_queries.sql
```

### PostgreSQL

```bash
# 1. Create database
psql -U postgres -c "CREATE DATABASE hbnb_db;"

# 2. Create schema
psql -U postgres -d hbnb_db -f schema.sql

# 3. Insert initial data
psql -U postgres -d hbnb_db -f seed_data.sql

# 4. Run tests (optional)
psql -U postgres -d hbnb_db -f test_queries.sql
```

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐
│     users       │       │     places      │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │◄──────┤ owner_id (FK)   │
│ first_name      │       │ id (PK)         │
│ last_name       │       │ title           │
│ email (UNIQUE)  │       │ description     │
│ password        │       │ price           │
│ is_admin        │       │ latitude        │
│ created_at      │       │ longitude       │
│ updated_at      │       │ created_at      │
└────────┬────────┘       │ updated_at      │
         │                └────────┬────────┘
         │                         │
         │                         │
         │   ┌──────────────────┐  │
         │   │     reviews      │  │
         │   ├──────────────────┤  │
         └───┤ user_id (FK)     │  │
             │ place_id (FK)    │◄─┘
             │ id (PK)          │
             │ text             │
             │ rating (1-5)     │
             │ created_at       │
             │ updated_at       │
             └──────────────────┘


┌─────────────────┐       ┌──────────────────┐       ┌─────────────────┐
│   amenities     │       │  place_amenity   │       │     places      │
├─────────────────┤       ├──────────────────┤       ├─────────────────┤
│ id (PK)         │◄──────┤ amenity_id (FK)  │       │ id (PK)         │
│ name (UNIQUE)   │       │ place_id (FK)    │──────►│ ...             │
│ created_at      │       └──────────────────┘       └─────────────────┘
│ updated_at      │         (Composite PK)
└─────────────────┘
```

## Relationships

### One-to-Many Relationships

1. **User → Places**
   - One user can own many places
   - Foreign Key: `places.owner_id` → `users.id`
   - Cascade: DELETE user deletes their places

2. **Place → Reviews**
   - One place can have many reviews
   - Foreign Key: `reviews.place_id` → `places.id`
   - Cascade: DELETE place deletes its reviews

3. **User → Reviews**
   - One user can write many reviews
   - Foreign Key: `reviews.user_id` → `users.id`
   - Cascade: DELETE user deletes their reviews

### Many-to-Many Relationship

1. **Places ↔ Amenities**
   - One place can have many amenities
   - One amenity can belong to many places
   - Junction table: `place_amenity`
   - Composite Primary Key: (`place_id`, `amenity_id`)
   - Cascade: DELETE place/amenity removes associations

## Constraints

### Primary Keys
- All tables use CHAR(36) for UUID-based primary keys

### Foreign Keys
- All foreign keys have CASCADE DELETE for referential integrity

### Unique Constraints
- `users.email` - Each email must be unique
- `amenities.name` - Each amenity name must be unique
- `reviews(user_id, place_id)` - One review per user per place

### Check Constraints
- `places.price > 0` - Price must be positive
- `places.latitude` between -90 and 90
- `places.longitude` between -180 and 180
- `reviews.rating` between 1 and 5

## Initial Data

### Administrator User
- **ID**: `36c9050e-ddd3-4c3b-9731-9f487208bbc1`
- **Email**: admin@hbnb.io
- **Password**: admin1234 (hashed with bcrypt)
- **Role**: Administrator (is_admin = TRUE)

### Amenities
1. **WiFi** - UUID: `557d60c7-88ee-411b-9384-4f8d0742f398`
2. **Swimming Pool** - UUID: `53b0e16f-1bd0-4572-b3f9-f3957537ed5f`
3. **Air Conditioning** - UUID: `f842930b-630a-4741-8bda-8e346e49bb7a`

## Testing

The `test_queries.sql` file includes 19 comprehensive tests:

1. **SELECT Tests** - Verify data retrieval
2. **INSERT Tests** - Test data creation
3. **JOIN Tests** - Verify relationships
4. **UPDATE Tests** - Test data modification
5. **DELETE Tests** - Test data removal and cascades
6. **Constraint Tests** - Verify integrity rules

Run the test file to ensure schema is working correctly:

```bash
mysql -u root -p hbnb_db < test_queries.sql
```

## Password Hashing

To generate a bcrypt hash for passwords:

```bash
python3 generate_password_hash.py
```

Or manually:

```python
import bcrypt
password = "your_password"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

## Notes

- All timestamps use `CURRENT_TIMESTAMP` for automatic tracking
- UUIDs are in CHAR(36) format (e.g., `36c9050e-ddd3-4c3b-9731-9f487208bbc1`)
- Indexes are created on foreign keys for query optimization
- Schema supports both MySQL and SQLite (with minor syntax adjustments)

## Troubleshooting

### Issue: "Table already exists"
```bash
# Drop and recreate
mysql -u root -p -e "DROP DATABASE IF EXISTS hbnb_db; CREATE DATABASE hbnb_db;"
mysql -u root -p hbnb_db < schema.sql
```

### Issue: "Duplicate entry for email"
The admin user might already exist. Check before inserting:
```sql
SELECT * FROM users WHERE email = 'admin@hbnb.io';
```

### Issue: "Foreign key constraint fails"
Ensure parent records exist before inserting child records:
1. Insert users first
2. Then insert places
3. Then insert reviews and amenities associations
