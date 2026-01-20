HBnB – Part 2: RESTful API
Description

This project is part of the Holberton School HBnB series.
In Part 2, a RESTful API is implemented using Flask and Flask-RESTx to manage users, places, amenities, and reviews with an in-memory persistence layer.

The API follows REST principles and provides full CRUD functionality with proper validation and HTTP status codes.

Technologies Used

Python 3.13

Flask

Flask-RESTx

UUID

In-memory repositories

cURL for testing

Project Structure
part2/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   │       └── __init__.py
│   ├── models/
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── persistence/
│   │   └── repository.py
│   └── services/
│       └── facade.py
├── run.py
└── README.md

Installation and Run
Install dependencies
pip install flask flask-restx

Run the application
python3 run.py


The API will be available at:

http://127.0.0.1:5000


Swagger documentation:

http://127.0.0.1:5000/api/v1/

API Endpoints
Users
Method	Endpoint	Description
POST	/api/v1/users/	Create a user
GET	/api/v1/users/	Retrieve all users
GET	/api/v1/users/<id>	Retrieve user by ID
PUT	/api/v1/users/<id>	Update user
Places
Method	Endpoint	Description
POST	/api/v1/places/	Create a place
GET	/api/v1/places/	Retrieve all places
GET	/api/v1/places/<id>	Retrieve place by ID
PUT	/api/v1/places/<id>	Update place

Note: owner_id must reference an existing user.

Reviews
Method	Endpoint	Description
POST	/api/v1/reviews/	Create a review
GET	/api/v1/reviews/	Retrieve all reviews
GET	/api/v1/reviews/<id>	Retrieve review by ID
PUT	/api/v1/reviews/<id>	Update review
DELETE	/api/v1/reviews/<id>	Delete review

Note: user_id and place_id must reference existing entities.

Amenities
Method	Endpoint	Description
POST	/api/v1/amenities/	Create an amenity
GET	/api/v1/amenities/	Retrieve all amenities
GET	/api/v1/amenities/<id>	Retrieve amenity by ID
PUT	/api/v1/amenities/<id>	Update amenity
Example Requests
Create a User
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "123456"
}'

Create a Place
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Beach House",
  "price": 200,
  "latitude": 36.77,
  "longitude": -119.41,
  "owner_id": "<USER_ID>",
  "amenities": []
}'

Expected HTTP Status Codes

201 Created

200 OK

400 Bad Request

404 Not Found

204 No Content

Notes

Data is stored in memory only and will be lost when the server restarts.

.pyc files are automatically generated and should not be committed.

The API uses UUIDs as identifiers.
