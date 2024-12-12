# Django Authentication API

This project is a Django-based API for user authentication, including features like registration, login, token refresh, profile management, password changes, and password reset.

---

## Features

1. **User Registration**: Create a new user with username, email, and password.
2. **Login**: Obtain access and refresh tokens using username and password.
3. **Token Refresh**: Refresh access tokens using a refresh token.
4. **View Personal Data**: Retrieve personal details of the authenticated user.
5. **Profile Update**: Update user profile information (email, first name, and last name).
6. **Change Password**: Change the password of the authenticated user.
7. **Logout**: Blacklist refresh tokens to log out users.
8. **Request Password Reset**: Request a password reset token to be sent to the user's email.
9. **Confirm Password Reset**: Reset the password using a valid token.

---

## Requirements

- Python >= 3.8
- Django >= 4.0
- Django REST Framework
- djangorestframework-simplejwt
- drf-spectacular
- SQLite or any supported database

---

## Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Run the Server**:

   ```bash
   python manage.py runserver
   ```

6. **Access API Documentation**:

   API documentation is available at `/schema/` using DRF Spectacular.

---

## API Endpoints

### Authentication

#### 1. **Register**
   - **Endpoint**: `api/auth/register/`
   - **Method**: POST
   - **Request Body**:

     ```json
     {
       "username": "user123",
       "email": "example@example.com",
       "password": "password123"
     }
     ```
   - **Response**:

     ```json
     {
       "message": "User created successfully",
       "username": "user123",
       "email": "example@example.com",
       "date_joined": "2021-07-16T15:00:00"
     }
     ```

#### 2. **Login**
   - **Endpoint**: `api/auth/login/`
   - **Method**: POST
   - **Request Body**:

     ```json
     {
         "username": "user123",
         "password": "password123"
     }
     ```
   - **Response**:

     ```json
     {
        "access_token": "<access_token>",
        "refresh_token": "<refresh_token>"
     }
     ```




#### 3. **Refresh Token**
   - **Endpoint**: `api/auth/refresh/`
   - **Method**: POST
    - **Request Body**:

     ```json
     {
        "refresh": "<refresh_token>"
     }
     ```
   - **Response**:

     ```json
     {
        "access": "<new_access_token>"
     }
     ```


#### 4. **View Personal Data**
   - **Endpoint**: `api/auth/personal-data/`
   - **Method**: GET
   - **Request headers**:

     ```json
     {
      "Authorization : bearer <access_token>"
     }

- **Response**:

     ```json
     {
        "username": "user123",
        "email": "",
        "first_name": "",
        "last_name": "",
        "date_joined": "2021-07-16T15:00:00",
     }
     ```



#### 5. **Update Profile**
   - **Endpoint**: `api/auth/update-profile/`
   - **Method**: PUT
   - **Request Body**:

     ```json
     {
       "firstName": "John",
       "lastName": "Doe",
       "email": "newemail@example.com"
     }
     ```
     
    
#### 6. **Change Password**
   - **Endpoint**: `api/auth/change-password/`
   - **Method**: PUT
   - **Request Body**:

     ```json
     {
       "old_password": "password123",
       "new_password": "newpassword123",
       "new_password_confirmation": "newpassword123"
     }
     ```

#### 7. **Logout**
   - **Endpoint**: `api/auth/logout/`
   - **Method**: POST
   - **Request Body**:

     ```json
     {
       "refresh_token": "<token>"
     }
     ```

#### 8. **Request Password Reset**
   - **Endpoint**: `api/auth/request-password-reset/`
   - **Method**: POST
   - **Request Body**:

     ```json
     {
       "email": "example@example.com"
     }
     ```

#### 9. **Confirm Password Reset**
   - **Endpoint**: `api/auth/confirm-password-reset/`
   - **Method**: POST
   - **Request Body**:

     ```json
     {
       "token": "<reset_token>",
       "new_password": "newpassword123",
       "new_password_confirmation": "newpassword123"
     }
     ```

---

## Notes

- Ensure to configure your email backend settings in the `settings.py` file to enable password reset emails.
- The project is structured to allow adding more apps, like a `Principal` app for posts and comments, which can be implemented later.
- For demonstration purposes, the database is SQLite but can be configured for any other database system.
