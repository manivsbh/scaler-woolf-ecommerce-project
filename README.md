# Django REST Framework E-commerce Application

This is a backend e-commerce application built with Django REST Framework, integrating key High-Level Design (HLD) components such as Elasticsearch for product search, Redis for cart caching, and Kafka for event-driven communication between services.

## Table of Contents

- [Features](#features)
- [HLD Components Integrated](#hld-components-integrated)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Running External Services](#running-external-services)
- [Running the Django Application](#running-the-django-application)
- [API Endpoints & Testing](#api-endpoints--testing)
  - [User Management](#user-management)
  - [Product Catalog](#product-catalog)
  - [Cart & Checkout](#cart--checkout)
  - [Order Management](#order-management)
  - [Payment](#payment)
  - [Elasticsearch Search](#elasticsearch-search)
  - [Redis Caching](#redis-caching)
  - [Kafka Events](#kafka-events)

## Features

*   **User Management:** User registration, secure login (JWT authentication), profile viewing and modification, and password reset functionality.
*   **Product Catalog:** Browse products by category, view detailed product information, and search for products.
*   **Cart & Checkout:** Add products to a shopping cart, review cart contents, and proceed to checkout to create an order.
*   **Order Management:** View order history and track order status.
*   **Payment:** Simulate payment processing and record transactions.

## HLD Components Integrated

This application demonstrates the integration of the following HLD components:

*   **Elasticsearch:** Used for fast and relevant product search.
*   **Redis:** Implemented for caching user cart data to improve performance.
*   **Kafka:** Utilized as a message broker for asynchronous communication, publishing events for user registration, cart updates, order creation, and payment processing.

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

*   **Python 3.x**
*   **pip** (Python package installer)
*   **Django**
*   **Django REST Framework**
*   **Elasticsearch** (version compatible with `django-elasticsearch-dsl` v8.x, e.g., 8.x)
*   **Redis**
*   **Kafka**
*   **Zookeeper** (Kafka's dependency)
*   **`python-dotenv`**: For managing environment variables locally.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>/ecommerce
    ```
    (Replace `<repository_url>` and `<repository_name>` with your actual repository details)

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    # If requirements.txt is not present, install manually:
    # pip install django djangorestframework djangorestframework-simplejwt django-redis django-elasticsearch-dsl elasticsearch kafka-python Faker django-filter python-dotenv stripe
    ```

3.  **Configure Environment Variables (`.env` file):**
    Create a file named `.env` in the `ecommerce/` directory (where `manage.py` is located) with your sensitive credentials. **DO NOT commit this file to Git.**
    ```
    # Stripe API Keys (Use your actual test keys here)
    STRIPE_PUBLISHABLE_KEY="pk_test_YOUR_PUBLISHABLE_KEY"
    STRIPE_SECRET_KEY="sk_test_YOUR_SECRET_KEY"

    # Elasticsearch Credentials
    ES_USERNAME="your_elasticsearch_username"
    ES_PASSWORD="your_elasticsearch_password"

    # Other sensitive settings can go here
    # SECRET_KEY="your_django_secret_key"
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Populate Initial Data (Optional, for testing):**
    To quickly populate your database with mock users, categories, and products:
    ```bash
    python manage.py populate_data
    ```

## Running External Services

Ensure all required external services are running before starting the Django application.

*   **Start Elasticsearch:** Follow the official Elasticsearch documentation for your operating system.
*   **Start Redis:** Follow the official Redis documentation for your operating system.
*   **Start Zookeeper & Kafka:** Follow the official Kafka documentation. Typically, you start Zookeeper first, then Kafka.

    Example (Linux/macOS, assuming Kafka is installed in `/opt/kafka`):
    ```bash
    # Start Zookeeper
    /opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties &

    # Start Kafka
    /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties &
    ```

## Running the Django Application

Navigate to the `ecommerce` directory (where `manage.py` is located) and run the development server:

```bash
python manage.py runserver
```

The server will typically run on `http://127.0.0.1:8000/`.

## API Endpoints & Testing

You can use `curl` or a tool like Postman/Insomnia to test the API endpoints. Remember to replace `YOUR_ACCESS_TOKEN` with a valid JWT obtained from the login endpoint.

### User Management

*   **Register User:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword", "email": "test@example.com"}' http://127.0.0.1:8000/api/users/register/
    ```
*   **Login (Get JWT Token):**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpassword"}' http://127.0.0.1:8000/api/users/token/
    ```
    (Copy the `access` token from the response)
*   **User Profile (Requires Authentication):**
    ```bash
    curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://127.0.0.1:8000/api/users/profile/
    ```
*   **Password Reset (Browser-based):**
    Navigate to `http://127.0.0.1:8000/api/users/password_reset/` in your browser. Enter the user's email. The reset link will be printed to your Django server's console.

### Product Catalog

*   **Create Category:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "Electronics"}' http://127.0.0.1:8000/api/categories/
    ```
*   **Create Product:**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"name": "Laptop", "description": "A powerful laptop", "price": "1200.00", "category": 1}' http://127.0.0.1:8000/api/products/
    ```
*   **List Products:**
    ```bash
    curl http://127.0.0.1:8000/api/products/
    ```
*   **Filter Products by Category:**
    ```bash
    curl "http://127.0.0.1:8000/api/products/?category=1"
    ```

### Cart & Checkout

*   **Add to Cart (Requires Authentication):**
    ```bash
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"product_id": 1, "quantity": 1}' http://127.0.0.1:8000/api/cart/add/
    ```
*   **View Cart (Requires Authentication):**
    ```bash
    curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://127.0.0.1:8000/api/cart/
    ```
*   **Create Order from Cart (Requires Authentication):**
    ```bash
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://127.0.0.1:8000/api/orders/create/
    ```

### Order Management

*   **List Orders (Requires Authentication):**
    ```bash
    curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://127.0.0.1:8000/api/orders/
    ```

### Payment

*   **Process Payment (Requires Authentication, Stripe Integration):**
    ```bash
    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"order_id": <YOUR_ORDER_ID>, "payment_method_id": "pm_card_visa"}' http://127.0.0.1:8000/api/payments/process/
    ```
    (Replace `order_id` with an actual order ID. `pm_card_visa` is a test payment method ID for basic testing. In a real frontend, this would be dynamically generated by Stripe.js.)

### Elasticsearch Search

1.  **Build Elasticsearch Index:**
    Navigate to the `ecommerce` directory and run:
    ```bash
    python manage.py search_index --rebuild
    ```
2.  **Search Products:**
    ```bash
    curl "http://127.0.0.1:8000/api/products/search/?q=Laptop"
    ```

### Redis Caching

1.  **Ensure Redis server is running.**
2.  **View Cart (first time):**
    ```bash
    curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://127.0.0.1:8000/api/cart/
    ```
    This will fetch from DB and cache in Redis.
3.  **View Cart (subsequent times):**
    ```bash
    curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://127.0.0.1:8000/api/cart/
    ```
    This should be faster as it's served from Redis.
4.  **Verify in Redis CLI:**
    ```bash
    redis-cli
    keys *
    get cart_<user_id> # e.g., get cart_1
    ```
    Adding/removing items from the cart will invalidate the cache.

### Kafka Events

1.  **Ensure Kafka and Zookeeper are running.**
2.  **Start Kafka Consumer:**
    Open a new terminal, navigate to the `ecommerce` directory, and run:
    ```bash
    python manage.py kafka_consumer
    ```
3.  **Trigger Events:** Perform actions via the API (e.g., register a new user, add to cart, create an order, process a payment). You should see corresponding messages appear in the terminal where the `kafka_consumer` is running.

---

Feel free to contribute to this project!