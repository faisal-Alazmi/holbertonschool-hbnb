# app/services/facade.py
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from datetime import datetime


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ================= USERS =================
    def create_user(self, data):
        user = User(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            password=data.get("password"),
            is_admin=data.get("is_admin", False)
        )
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()
    
    def get_user_by_email(self, email):
        """Get user by email address"""
        users = self.user_repo.get_all()
        for user in users:
            if user.email == email:
                return user
        return None

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(data)
        return user

    # ================= AMENITIES =================
    def create_amenity(self, data):
        if not data.get("name"):
            raise ValueError("Name is required")
        amenity = Amenity(name=data.get("name"))
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(data)
        return amenity

    # ================= PLACES =================
    def create_place(self, data):
        owner = self.user_repo.get(data.get("owner_id"))
        if not owner:
            raise ValueError("Owner not found")

        amenities = [
            self.amenity_repo.get(a_id).id
            for a_id in data.get("amenities", [])
            if self.amenity_repo.get(a_id)
        ]

        place = Place(
            title=data.get("title"),
            description=data.get("description"),
            price=data.get("price"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            owner_id=owner.id,
            amenities=amenities
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.get_place(place_id)
        if not place:
            return None
        place.update(data)
        return place

    # ================= REVIEWS =================
    def create_review(self, data):
        user = self.user_repo.get(data.get("user_id"))
        place = self.place_repo.get(data.get("place_id"))

        if not user:
            raise ValueError("User not found")
        if not place:
            raise ValueError("Place not found")
        if not data.get("text"):
            raise ValueError("Text is required")

        review = Review(
            text=data.get("text"),
            user_id=user.id,
            place_id=place.id
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, data):
        review = self.get_review(review_id)
        if not review:
            return None
        review.update(data)
        return review

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)

    def get_reviews_by_place(self, place_id):
        return [
            r for r in self.review_repo.get_all()
            if r.place_id == place_id
        ]
