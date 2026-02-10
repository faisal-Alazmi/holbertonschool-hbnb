# Part 3: Enhanced Backend with Authentication and Database Integration

Welcome to Part 3 of the HBnB Project, where you will extend the backend of the application by introducing user authentication, authorization, and database integration using SQLAlchemy and SQLite for development. Later, you'll configure MySQL for production environments. In this part, you will secure the backend, introduce persistent storage, and prepare the application for a scalable, real-world deployment.

## Objectives of the Project

- **Authentication and Authorization**: Implement JWT-based user authentication using Flask-JWT-Extended and role-based access control with the `is_admin` attribute for specific endpoints.
- **Database Integration**: Replace in-memory storage with SQLite for development using SQLAlchemy as the ORM and prepare for MySQL or other production grade RDBMS.
- **CRUD Operations with Database Persistence**: Refactor all CRUD operations to interact with a persistent database.
- **Database Design and Visualization**: Design the database schema using mermaid.js and ensure all relationships between entities are correctly mapped.
- **Data Consistency and Validation**: Ensure that data validation and constraints are properly enforced in the models.

## Learning Objectives

By the end of this part, you will:

- Implement JWT authentication to secure your API and manage user sessions.
- Enforce role-based access control to restrict access based on user roles (regular users vs. administrators).
- Replace in-memory repositories with a SQLite-based persistence layer using SQLAlchemy for development and configure MySQL for production.
- Design and visualize a relational database schema using mermaid.js to handle relationships between users, places, reviews, and amenities.
- Ensure the backend is secure, scalable, and provides reliable data storage for production environments.

## Project Context

In the previous parts of the project, you worked with in-memory storage, which is ideal for prototyping but insufficient for production environments. In Part 3, you'll transition to SQLite, a lightweight relational database, for development, while preparing the system for MySQL in production. This will give you hands-on experience with real-world database systems, allowing your application to scale effectively.

Additionally, you'll introduce JWT-based authentication to secure the API, ensuring that only authenticated users can interact with certain endpoints. You will also implement role-based access control to enforce restrictions based on the user's privileges (regular users vs. administrators).

## Project Resources

Here are some resources that will guide you through this part of the project:

- **JWT Authentication**: [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- **SQLAlchemy ORM**: [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- **SQLite**: [SQLite Documentation](https://www.sqlite.org/docs.html)
- **Flask Documentation**: [Flask Official Documentation](https://flask.palletsprojects.com/)
- **Mermaid.js for ER Diagrams**: [Mermaid.js Documentation](https://mermaid.js.org/)

## Structure of the Project

In this part of the project, the tasks are organized in a way that builds progressively towards a complete, secure, and database-backed backend system:

1. **Modify the User Model to Include Password**: You will start by modifying the User model to store passwords securely using bcrypt and update the user registration logic.

2. **Implement JWT Authentication**: Secure the API using JWT tokens, ensuring only authenticated users can access protected endpoints.

3. **Implement Authorization for Specific Endpoints**: You will implement role-based access control to restrict certain actions (e.g., admin-only actions).

4. **SQLite Database Integration**: Transition from in-memory data storage to SQLite as the persistent database during development.

5. **Map Entities Using SQLAlchemy**: Map existing entities (User, Place, Review, Amenity) to the database using SQLAlchemy and ensure relationships are well-defined.

6. **Prepare for MySQL in Production**: Towards the end of this phase, you'll configure the application to use MySQL in production and SQLite for development.

7. **Database Design and Visualization**: Use mermaid.js to create entity-relationship diagrams for your database schema.

Each task is carefully designed to build on previous work and ensure the system transitions smoothly from development to production readiness.

By the end of Part 3, you will have a backend that not only stores data in a persistent and secure database but also ensures that only authorized users can access and modify specific data. You will have implemented industry-standard authentication and database management practices that are crucial for real-world web applications.

---

## Project Structure

```
part3/
├── app/
│   ├── __init__.py              # Flask app initialization with SQLAlchemy
│   ├── config.py                # Configuration for different environments
│   ├── models/                  # SQLAlchemy models
│   │   ├── base.py             # BaseModel with common attributes
│   │   ├── user.py             # User model with password hashing
│   │   ├── place.py            # Place model with relationships
│   │   ├── review.py           # Review model
│   │   └── amenity.py          # Amenity model
│   ├── persistence/            # Repository pattern implementation
│   │   └── repository.py       # SQLAlchemy repositories
│   ├── services/               # Business logic layer
│   │   └── facade.py           # Facade pattern for services
│   └── api/
│       └── v1/                 # API endpoints
│           ├── auth.py         # Authentication endpoints
│           ├── users.py        # User CRUD endpoints
│           ├── places.py       # Place CRUD endpoints
│           ├── reviews.py      # Review CRUD endpoints
│           └── amenities.py    # Amenity CRUD endpoints
├── sql/                        # SQL scripts and utilities
│   ├── schema.sql              # Database schema definition
│   ├── seed_data.sql           # Initial data (admin user, amenities)
│   ├── test_queries.sql        # Test queries for CRUD operations
│   ├── setup_database.sh       # Automated database setup script
│   └── SQL_SCRIPTS_README.md   # SQL documentation
├── diagrams/                   # Database diagrams
│   ├── er_diagram_simple.md    # Quick reference ER diagram
│   ├── sqlalchemy_relationships.md  # ORM relationships documentation
│   └── README.md               # Diagrams documentation
├── DATABASE_DIAGRAM.md         # Comprehensive ER diagram
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
└── README.md                   # This file
```

---

## Setup and Installation

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/faisal-Alazmi/holbertonschool-hbnb.git
   cd holbertonschool-hbnb/part3
   ```

2. **Install dependencies**

   On Windows:
   ```bash
   py -3.12 -m pip install -r requirements.txt
   ```

   On macOS/Linux:
   ```bash
   pip install -r requirements.txt
   # or
   python3 -m pip install -r requirements.txt
   ```

3. **Set up the database** (Optional - for SQL database)
   ```bash
   cd sql
   ./setup_database.sh -t sqlite -n ../development.db
   cd ..
   ```

4. **Run the application**

   On Windows:
   ```bash
   py -3.12 run.py
   ```

   On macOS/Linux:
   ```bash
   python3 run.py
   ```

5. **Access the application**
   - Server: `http://127.0.0.1:5000`
   - API Documentation (Swagger): `http://127.0.0.1:5000/api/v1/`
   - Health Check: `http://127.0.0.1:5000/api/v1/health`

---

## Default Administrator Account

A default admin user is automatically created when the application starts with no existing users:

- **Email**: `admin@example.com`
- **Password**: `admin123`

Use these credentials to:
1. Login via `POST /api/v1/auth/login`
2. Receive a JWT token
3. Access protected endpoints with `Authorization: Bearer <token>`

---

## API Overview

### Authentication
- `POST /api/v1/auth/login` — Returns JWT token for authenticated users

### Users
- `POST /api/v1/users/` — Create user (Admin only)
- `GET /api/v1/users/` — List all users (Admin only)
- `GET /api/v1/users/<id>` — Get user by ID (Self or Admin)
- `PUT /api/v1/users/<id>` — Update user (Self or Admin)

### Amenities
- `POST /api/v1/amenities/` — Create amenity (Admin only)
- `GET /api/v1/amenities/` — List all amenities (Public)
- `GET /api/v1/amenities/<id>` — Get amenity by ID (Public)
- `PUT /api/v1/amenities/<id>` — Update amenity (Admin only)
- `DELETE /api/v1/amenities/<id>` — Delete amenity (Admin only)

### Places
- `POST /api/v1/places/` — Create place (Authenticated users)
- `GET /api/v1/places/` — List all places (Public)
- `GET /api/v1/places/<id>` — Get place by ID (Public)
- `PUT /api/v1/places/<id>` — Update place (Owner or Admin)
- `DELETE /api/v1/places/<id>` — Delete place (Owner or Admin)

### Reviews
- `POST /api/v1/reviews/` — Create review (Authenticated users)
- `GET /api/v1/reviews/` — List all reviews (Public)
- `GET /api/v1/reviews/<id>` — Get review by ID (Public)
- `PUT /api/v1/reviews/<id>` — Update review (Author or Admin)
- `DELETE /api/v1/reviews/<id>` — Delete review (Author or Admin)

---

## Database Schema

### Entities

1. **User**: Stores user account information
   - Attributes: id, first_name, last_name, email (unique), password (hashed), is_admin
   - Relationships: owns places, writes reviews

2. **Place**: Stores place listings
   - Attributes: id, title, description, price, latitude, longitude, owner_id
   - Relationships: owned by user, has reviews, has amenities

3. **Review**: Stores user reviews for places
   - Attributes: id, text, rating (1-5), user_id, place_id
   - Relationships: written by user, belongs to place
   - Constraint: One review per user per place

4. **Amenity**: Stores available amenities
   - Attributes: id, name (unique)
   - Relationships: belongs to places (many-to-many)

5. **Place_Amenity**: Junction table for place-amenity relationship
   - Attributes: place_id, amenity_id (composite primary key)

### Relationships

- **User → Place**: One-to-Many (owns)
- **User → Review**: One-to-Many (writes)
- **Place → Review**: One-to-Many (has)
- **Place ↔ Amenity**: Many-to-Many (includes)

For detailed database diagrams, see:
- `DATABASE_DIAGRAM.md` - Comprehensive ER documentation
- `diagrams/` - Visual diagrams and ORM documentation

---

## Testing the API

### Using cURL

1. **Login to get JWT token**
   ```bash
   curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@example.com", "password": "admin123"}'
   ```

2. **Create a user (Admin only)**
   ```bash
   curl -X POST http://127.0.0.1:5000/api/v1/users/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your-token>" \
     -d '{
       "first_name": "John",
       "last_name": "Doe",
       "email": "john@example.com",
       "password": "password123"
     }'
   ```

3. **Create a place**
   ```bash
   curl -X POST http://127.0.0.1:5000/api/v1/places/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your-token>" \
     -d '{
       "title": "Cozy Apartment",
       "description": "A beautiful place in the city",
       "price": 120.50,
       "latitude": 40.7128,
       "longitude": -74.0060,
       "owner_id": "<user-id>"
     }'
   ```

### Using Postman

1. Import the API documentation from `http://127.0.0.1:5000/api/v1/`
2. Set up environment variable for JWT token
3. Test all endpoints with proper authentication

---

## Development

### Running Tests

```bash
# Run the SQL test queries
cd sql
mysql -u root -p hbnb_db < test_queries.sql
# or for SQLite
sqlite3 ../development.db < test_queries.sql
```

### Configuration

The application supports different configurations for development, testing, and production:

- **Development**: Uses SQLite (`development.db`)
- **Testing**: Uses in-memory SQLite
- **Production**: Configured for MySQL

Edit `app/config.py` to change database settings.

---

## Key Features Implemented

### ✅ Authentication & Authorization
- JWT-based authentication using Flask-JWT-Extended
- Role-based access control (regular users vs. admins)
- Password hashing with Flask-Bcrypt
- Protected endpoints with token validation

### ✅ Database Integration
- SQLAlchemy ORM for database operations
- SQLite for development
- MySQL-ready for production
- Repository pattern for data access
- Automatic database initialization

### ✅ Data Models
- BaseModel with common attributes (id, created_at, updated_at)
- User model with secure password storage
- Place, Review, Amenity models
- Proper relationships and foreign keys
- Data validation and constraints

### ✅ API Endpoints
- RESTful API design
- Swagger/OpenAPI documentation
- CRUD operations for all entities
- Proper HTTP status codes
- Error handling and validation

### ✅ Documentation
- Comprehensive README
- Entity-Relationship diagrams (Mermaid.js)
- SQL scripts with documentation
- API documentation (Swagger UI)
- Code examples and usage guides

---

## Technologies Used

- **Backend Framework**: Flask
- **ORM**: SQLAlchemy
- **Authentication**: Flask-JWT-Extended
- **Password Hashing**: Flask-Bcrypt (bcrypt)
- **Database (Dev)**: SQLite
- **Database (Prod)**: MySQL
- **API Documentation**: Flask-RESTX (Swagger)
- **Diagrams**: Mermaid.js

---

## Contributing

When contributing to this project:

1. Follow the existing code structure
2. Update documentation for any changes
3. Test all endpoints before committing
4. Update database diagrams if schema changes
5. Follow Python PEP 8 style guidelines

---

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError` when running the application
- **Solution**: Ensure you're using the same Python version for both pip and running the app

**Issue**: Database connection errors
- **Solution**: Check that the database file exists or run the setup script

**Issue**: JWT token errors
- **Solution**: Ensure the token is included in the Authorization header as `Bearer <token>`

**Issue**: Permission denied errors
- **Solution**: Verify user roles and authentication status

---

## Future Enhancements

- [ ] Email verification for new users
- [ ] Password reset functionality
- [ ] Booking/Reservation system
- [ ] Payment integration
- [ ] Advanced search and filtering
- [ ] Image upload for places
- [ ] Pagination for list endpoints
- [ ] Rate limiting
- [ ] Caching layer
- [ ] Docker containerization

---

## License

This project is part of the Holberton School curriculum.

---

## Repository

**GitHub**: [holbertonschool-hbnb](https://github.com/faisal-Alazmi/holbertonschool-hbnb)
**Directory**: part3

---

## Contact

For questions or issues, please create an issue in the GitHub repository.

---

**Last Updated**: 2026
**Version**: 1.0.0
**Status**: ✅ Complete
