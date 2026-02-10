# HBnB ER Diagram - Quick Reference

## Simple Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "has"
    PLACE }o--o{ AMENITY : "includes"

    USER {
        string id PK
        string first_name
        string last_name
        string email UK
        string password
        boolean is_admin
    }

    PLACE {
        string id PK
        string title
        string description
        float price
        float latitude
        float longitude
        string owner_id FK
    }

    REVIEW {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
    }

    AMENITY {
        string id PK
        string name UK
    }

    PLACE_AMENITY {
        string place_id PK_FK
        string amenity_id PK_FK
    }
```

## Relationship Summary

- **User → Place**: One user owns many places
- **User → Review**: One user writes many reviews
- **Place → Review**: One place has many reviews
- **Place ↔ Amenity**: Many-to-many through PLACE_AMENITY

## Key Constraints

- User email must be unique
- Amenity name must be unique
- Review rating: 1-5
- One review per user per place
- All foreign keys cascade on delete
