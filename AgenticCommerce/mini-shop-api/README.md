# Mini Shop API

A lightweight FastAPI-based product management system demonstrating RESTful API design principles and serving as a foundation for agentic commerce applications.

## Overview

Mini Shop API provides a simple yet robust backend for managing product catalogs. Built with FastAPI and Pydantic, it offers type-safe endpoints for creating and retrieving products, making it ideal for AI agents and automated commerce systems to interact with product data programmatically.

## Features

- **Product Creation**: POST endpoint for adding new products with automatic ID generation
- **Product Retrieval**: GET endpoint for fetching all products in the catalog
- **Type Safety**: Pydantic models ensure data validation and structured responses
- **RESTful Design**: Standard HTTP methods and status codes
- **Comprehensive Testing**: Full test suite using pytest and FastAPI TestClient
- **Agentic-Ready**: Structured API suitable for AI agent interactions

## Project Structure

```
.
├── main.py           # FastAPI application and route handlers
├── models.py         # Pydantic data models (ProductIn, ProductOut)
├── test_api.py       # Comprehensive test suite
└── requirements.txt  # Project dependencies
```

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
fastapi dev main.py
```

The API will be available at `http://localhost:8000`

Access interactive API documentation at `http://localhost:8000/docs`

## API Endpoints

### GET `/`
Welcome endpoint returning API information.

**Response:**
```json
{
  "message": "Welcome to Mini Shop API"
}
```

### POST `/products`
Create a new product in the catalog.

**Request Body:**
```json
{
  "name": "Apple",
  "description": "macbook",
  "price": 42.00,
  "currency": "USD",
  "inventory": 2000,
  "category": "Electronics"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Apple",
  "description": "macbook",
  "price": 42.00,
  "currency": "USD",
  "inventory": 2000,
  "category": "Electronics"
}
```

### GET `/products`
Retrieve all products from the catalog.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Apple",
    "description": "macbook",
    "price": 42.00,
    "currency": "USD",
    "inventory": 2000,
    "category": "Electronics"
  }
]
```

## Data Models

### ProductIn
Input model for creating products:
- `name`: Product name (string)
- `description`: Product description (string)
- `price`: Product price (float)
- `currency`: Currency code (string)
- `inventory`: Stock quantity (integer)
- `category`: Product category (string)

### ProductOut
Output model including system-generated fields:
- All ProductIn fields plus:
- `id`: Unique product identifier (integer, auto-generated)

## Testing

Run the test suite:
```bash
pytest test_api.py -v
```
