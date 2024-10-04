import requests

BASE_URL = 'http://localhost:8000/api/'  # Adjust this URL as needed

# Authentication
def get_token(username, password):
    response = requests.post(f'{BASE_URL}auth/', data={'username': username, 'password': password})
    return response.json()['token']

# Customer Registration
def register_customer():
    data = {
        "user": {
            "username": "newcustomer",
            "email": "newcustomer@example.com",
            "password": "securepassword"
        },
        "name": "New Customer",
        "mobile": "1234567890"
    }
    response = requests.post(f'{BASE_URL}register/customer/', json=data)
    return response.json()

# Seller Registration
def register_seller():
    data = {
        "user": {
            "username": "newseller",
            "email": "newseller@example.com",
            "password": "securepassword"
        },
        "name": "New Seller",
        "mobile": "9876543210"
    }
    response = requests.post(f'{BASE_URL}register/seller/', json=data)
    return response.json()

# Customer operations
def customer_operations(token):
    headers = {'Authorization': f'Token {token}'}
    
    # List customers
    response = requests.get(f'{BASE_URL}customers/', headers=headers)
    print("List customers:", response.json())
    
    # Get specific customer
    customer_id = 1  # Replace with actual ID
    response = requests.get(f'{BASE_URL}customers/{customer_id}/', headers=headers)
    print(f"Get customer {customer_id}:", response.json())

# Seller operations
def seller_operations(token):
    headers = {'Authorization': f'Token {token}'}
    
    # List sellers
    response = requests.get(f'{BASE_URL}sellers/', headers=headers)
    print("List sellers:", response.json())
    
    # Get specific seller
    seller_id = 1  # Replace with actual ID
    response = requests.get(f'{BASE_URL}sellers/{seller_id}/', headers=headers)
    print(f"Get seller {seller_id}:", response.json())

# Product operations
def product_operations(token):
    headers = {'Authorization': f'Token {token}'}
    
    # List products
    response = requests.get(f'{BASE_URL}products/', headers=headers)
    print("List products:", response.json())
    
    # Create a new product
    new_product = {
        "name": "New Product",
        "amount": 19.99
    }
    response = requests.post(f'{BASE_URL}products/', json=new_product, headers=headers)
    print("Create product:", response.json())

# Order operations
def order_operations(token):
    headers = {'Authorization': f'Token {token}'}
    
    # List orders
    response = requests.get(f'{BASE_URL}orders/', headers=headers)
    print("List orders:", response.json())
    
    # Create a new order
    new_order = {
        "products": [1, 2],  # Replace with actual product IDs
        "total_amount": 39.98
    }
    response = requests.post(f'{BASE_URL}orders/', json=new_order, headers=headers)
    print("Create order:", response.json())

# API Call logging
def api_call_logging(token):
    headers = {'Authorization': f'Token {token}'}
    
    # List API calls
    response = requests.get(f'{BASE_URL}api-calls/', headers=headers)
    print("List API calls:", response.json())

# Main execution
if __name__ == "__main__":
    # Register a new customer and seller
    customer = register_customer()
    seller = register_seller()
    
    # Get authentication token (use registered user's credentials)
    token = get_token("newcustomer", "securepassword")
    
    # Perform operations
    customer_operations(token)
    seller_operations(token)
    product_operations(token)
    order_operations(token)
    api_call_logging(token)