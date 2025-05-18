# E-commerce Backend API

This is a backend API for a basic e-commerce platform built with FastAPI and PostgreSQL. It covers all the essential features you’d expect for managing users and products, with a focus on simplicity and security.

## What’s Inside?

#### User Authentication:
Secure login and registration using JWT tokens. Tokens are stored in HTTP-only cookies for safety, and there’s a refresh token system to keep users logged in smoothly without constant re-authentication.

#### Product Management:
Admins can add, update, and delete products. Each product has a name, price, stock quantity, and can optionally have an image. Uploaded images are stored on the server with unique names, and their paths are saved in the database. The API returns the image paths so frontends can display product photos.

#### Order Products:
Users can order products that are available. They can updated, delete(Cancel) their order.

#### Cart:
Users can add products to their carts and order all of them (who's stock is available) directly from their cart.

#### Clean Data Handling:
Uses Pydantic models for input validation and output formatting. Prevents duplicate products for the same user, and ensures all product details are valid before saving.

#### Database Setup:
PostgreSQL is used with SQLAlchemy ORM for easy database management. Models represent users and products with proper relationships.

#### API Design:
Modular routes with FastAPI’s dependency injection make the code clean and maintainable. Proper error handling returns clear messages on failures. Includes docstring for every endpoint and functions.

#### Why This Project?
This backend serves as a solid foundation for a simple e-commerce platform or as a learning project to understand user authentication, file uploads, and REST API design with FastAPI.


## Getting Started
1. Prerequisites
2. Python 3.9+
3. PostgreSQL database up and running
4. pip for installing dependencies

## Installation
Clone the repo:
<pre>
-git clone https://github.com/aryanpal-7/E-commerce.git
-cd E-commerce
</pre>


## Create and activate a virtual environment (recommended):
<pre>
-python -m venv venv
-source venv/bin/activate   # On Windows: venv\Scripts\activate
</pre>
## Install the dependencies:
<pre>
-pip install -r requirements.txt
</pre>
## Run database migrations (if using Alembic or your migration tool):
<pre>
-alembic upgrade head
</pre>
## Start the FastAPI server:
<pre>
-uvicorn app.main:app --reload
</pre>
## Using the API
Open your browser and navigate to:
<pre>
http://127.0.0.1:8000/docs
</pre>
This will open the Swagger UI where you can test all the API endpoints interactively.


# Work In Progress
