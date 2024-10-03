# E-commerce Platform API

## Project Description

This project is a Django-based RESTful API for an e-commerce platform, designed to manage orders, products, customers, and sellers with a focus on performance and scalability. The application includes background task scheduling using Celery and a management command for bulk product import from Excel files.

## Key Features

- **User Management:**
  - Customer and Seller Profiles: Linked to the Django User model.
  - Basic Token Authentication: For secure API access.

- **Product Management:**
  - CRUD Operations: Create, read, update, and delete products.
  - Validation: Prevents duplicate product creation.
  - Bulk Import: Import products from Excel files using a management command.

- **Order Management:**
  - CRUD Operations: Manage orders with associations to customers, sellers, and products.
  - Filtering and Searching: Filter orders by product and search using `icontains`.
  - Pagination and Sorting: Supports ascending, descending, and top 5 sorting.
  - Permissions: Customers can only view their own orders.

- **API Logging:**
  - Automatic Logging: Logs all API calls using a custom mixin.

- **Performance Optimizations:**
  - Efficient Queries: Uses `select_related` and `prefetch_related` for database queries.
  - Caching: Implements caching strategies for frequently accessed data.

- **Background Tasks:**
  - Celery Integration: Runs scheduled tasks, including a daily product import task at 2:30 PM.

## Technical Stack

- **Django & Django REST Framework:** For building the API.
- **Celery:** For background task scheduling.
- **Pandas:** For data processing during product import.
- **PostgreSQL:** As the database backend.
- **Redis:** As the Celery broker and result backend.

## Development Practices

- **Git Version Control:** With a meaningful commit history and branch-based workflow.
- **Comprehensive Test Suite:** For all major components.
- **Detailed Documentation:** Including setup instructions and API usage.

## Models

- **Orders:** 
  - `customer (ForeignKey to Customer)`
  - `seller (ForeignKey to Seller)`
  - `products (ManyToMany to Product)`
  - `amount (DecimalField)`

- **Customer:**
  - `name (CharField)`
  - `mobile (CharField)`
  - `user (ForeignKey to User)`

- **Seller:**
  - `name (CharField)`
  - `mobile (CharField)`
  - `user (ForeignKey to User)`

- **Product:**
  - `name (CharField)`
  - `amount (DecimalField)`

- **PlatformApiCall:**
  - `user (ForeignKey to User)`
  - `requested_url (URLField)`
  - `requested_data (TextField)`
  - `response_data (TextField)`

## Instructions for Deployment

1. **Clone the Repository:**
   ```
   git clone https://github.com/Ultronoss/codezen-backend-assignments.git
   cd ecommerce
   ```

2. **Create a Virtual Environment and install dependencies**
```
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
```

3. **Set Up the Database:**
```
python manage.py makemigrations
python manage.py migrate
```

4. **Run the Development Server:**
``` python manage.py runserver```

5. **Set Up Celery:**
        ***Run Redis Server:***
        `sudo service redis-server start`
```celery -A ecommerce worker -l info --pool=solo```
```celery -A ecommerce beat --loglevel=info```

6. **Import product from Excel:**
```python manage.py import_products api/Product_data.xlsx```


**Additional Features**
- Management Command for Bulk Import: Uses Pandas to read data from Excel files and ensures no duplicate entries.
- Celery Task Scheduling: Configured to run the import task daily at 2:30 PM using a cron job.

**API Endpoints**

- ## User Management

    - POST `/api/auth/login/`: Authenticate a user and obtain a token.
    - POST `/api/auth/logout/`: Log out a user and invalidate the token.

- ## Customer Management

    - POST `/api/customers/register/`: Register a new customer.
    - GET `/api/customers/`: List all customers (Admin only).
    - GET `/api/customers/{id}/`: Retrieve a specific customer by ID.
    - POST `/api/customers/`: Create a new customer profile (Admin only).
    - PUT `/api/customers/{id}/`: Update an existing customer profile (Admin only).
    - DELETE `/api/customers/{id}/`: Delete a customer profile (Admin only).

- ## Seller Management

    - POST `/api/sellers/register/`: Register a new seller.
    - GET `/api/sellers/`: List all sellers (Admin only).
    - GET `/api/sellers/{id}/`: Retrieve a specific seller by ID.
    - POST `/api/sellers/`: Create a new seller profile (Admin only).
    - PUT `/api/sellers/{id}/`: Update an existing seller profile (Admin only).
    - DELETE `/api/sellers/{id}/`: Delete a seller profile (Admin only).

- ## Product Management

    - GET `/api/products/`: List all products with filtering and pagination.
    - GET `/api/products/{id}/`: Retrieve a specific product by ID.
    - POST` /api/products/`: Create a new product.
    - PUT `/api/products/{id}/`: Update an existing product.
    - DELETE `/api/products/{id}/`: Delete a product.

- ## Order Management

    - GET `/api/orders/`: List all orders with filtering, searching, and pagination.
    - GET `/api/orders/{id}/`: Retrieve a specific order by ID.
    - POST `/api/orders/`: Create a new order.
    - PUT `/api/orders/{id}/`: Update an existing order.
    - DELETE `/api/orders/{id}/`: Delete an order.

- ## API Logging

    - GET `/api/logs/`: List all API logs (Admin only).
    - GET `/api/logs/{id}/`: Retrieve a specific log entry by ID.

- ## Bulk Import

    - POST `/api/products/import/`: Trigger the management command for bulk product import (Admin only).

Made by Raj Mishra