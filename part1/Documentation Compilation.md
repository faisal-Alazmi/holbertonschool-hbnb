1. Introduction
1.1 Purpose of This Document
This technical document provides a comprehensive architectural and design blueprint for the HBnB Evolution application, a simplified AirBnB-like platform. It serves as a reference for the implementation phases of the project by clearly describing the system structure, core business entities, and interaction flows.
1.2 Scope
This document includes:
A high-level architectural overview of the system
A detailed class diagram for the Business Logic layer
Sequence diagrams illustrating API interaction flows
Explanatory notes explaining design decisions and data flow
2. High-Level Architecture
2.1 Architectural Overview
HBnB Evolution follows a layered architecture composed of three main layers:
Presentation Layer
Exposes RESTful APIs
Handles HTTP requests and responses
Acts as a facade to the Business Logic layer
Business Logic Layer
Contains domain models and core business rules
Validates data and enforces application constraints
Persistence Layer
Responsible for data storage and retrieval
Abstracts database operations from business logic
This separation ensures maintainability, scalability, and testability.

2.2 High-Level Package Diagram
<img width="838" height="539" alt="high digram" src="https://github.com/user-attachments/assets/dea131af-b426-4835-becc-252a796ce9f6" />
Explanation
The Presentation Layer communicates only with the Business Logic layer.
The Business Logic layer coordinates all operations and delegates data storage to the Persistence layer.
The Persistence layer does not communicate directly with the Presentation layer.


3. Business Logic Layer – Class Diagram
3.1 Overview
The Business Logic layer contains the core entities:
User
Place
Review
Amenity
Each entity:
Has a unique identifier
Tracks creation and update timestamps
Encapsulates business rules relevant to its domain

3.2 Class Diagram
<img width="349" height="575" alt="class" src="https://github.com/user-attachments/assets/4f4f485a-869c-47a0-8c1b-6049cc72ad5c" />

3.3 Design Rationale
User–Place relationship ensures ownership of listings.
Place–Review relationship allows feedback from multiple users.
Many-to-many Place–Amenity relationship provides flexibility in property features.
CRUD methods are included to support API operations.
Timestamps support audit and traceability requirements.


4. API Interaction Flow – Sequence Diagrams
This section illustrates how the layers interact to fulfill API requests.

4.1 User Registration
Description
Handles new user creation with validation and persistence.
<img width="5235" height="3815" alt="Untitled diagram-2025-12-22-155938" src="https://github.com/user-attachments/assets/1c35f97c-ad49-4636-acb5-795f38bab414" />

4.2 Place Creation
Description
Allows a user to create a new place listing.
<img width="5190" height="3815" alt="Untitled diagram-2025-12-22-155437" src="https://github.com/user-attachments/assets/2a63e4f2-3877-40c3-80ef-f1da01a234bc" />

4.3 Review Submission
Description
Allows users to submit reviews for places.
<img width="5295" height="3995" alt="Untitled diagram-2025-12-22-155833" src="https://github.com/user-attachments/assets/77a6fa3b-4d88-495c-a549-ad0c64684871" />


4.4 Fetching a List of Places
Description
Retrieves available places based on optional filters.
<img width="4760" height="2445" alt="Untitled diagram-2025-12-22-155119" src="https://github.com/user-attachments/assets/a8d23e99-5e03-4bf8-8a94-e600a5d08019" />

5. Conclusion
This technical document defines the architecture, business entities, and interaction flows of the HBnB Evolution application. By combining UML diagrams with explanatory notes, it provides a clear and reliable reference for the implementation phases.
The layered design ensures:
Clean separation of concerns
Maintainable and extensible codebase
Alignment with industry best practices
