# HBnB Evolution – Part 1  
## High-Level Package Diagram

This document describes the high-level architecture of the HBnB Evolution application. The goal of this diagram is to provide a conceptual overview of the system structure and the communication between its main components.

---

## Architecture Overview

The HBnB application follows a **three-layered architecture** that ensures separation of concerns and maintainability.

### 1. Presentation Layer
The Presentation Layer is responsible for handling user interactions with the application. It exposes APIs and services that receive requests from clients and return appropriate responses. This layer does not contain business logic.

### 2. Business Logic Layer
The Business Logic Layer contains the core domain models and the business rules of the application. It includes the main entities such as:
- User
- Place
- Review
- Amenity

This layer also includes the **HBnBFacade**, which acts as a unified interface between the Presentation Layer and the rest of the system.

### 3. Persistence Layer
The Persistence Layer is responsible for data storage and retrieval. It abstracts the database operations using repository components and ensures that the Business Logic Layer does not interact directly with the database.

---

## Facade Pattern

The **Facade Pattern** is implemented through the `HBnBFacade` class.  
All interactions from the Presentation Layer pass through the facade, which:
- Centralizes access to the business logic
- Simplifies communication between layers
- Prevents direct coupling between the Presentation and Persistence layers

---

## Diagram Description

The High-Level Package Diagram illustrates:
- The three main layers of the application
- The key components within each layer
- The communication pathways between layers through the facade

The Presentation Layer communicates exclusively with the Business Logic Layer via the `HBnBFacade`. The Business Logic Layer interacts with the Persistence Layer to perform CRUD operations.

---

## Conclusion

This high-level package diagram provides a clear architectural blueprint for the HBnB Evolution application. It serves as the foundation for the detailed design and implementation phases that follow in the next parts of the project.
