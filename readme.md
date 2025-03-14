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
10. **Post Management**: Create, retrieve, update, and delete blog posts.
11. **Comment Management**: Create, update, and delete comments on posts.

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
   git clone https://github.com/NicolasThompsonW/ApiDjangoRest
   cd ApiDjangoRest
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

### Blog Posts

#### 1. **Get All Posts**
   - **Endpoint**: `api/posts/`
   - **Method**: GET
   - **Query Parameters**:
     - `page`: Page number for pagination.
     - `search`: Search term for filtering by author's username.
   - **Response**:

     ```json
     {
       "count": 100,
       "next": "http://example.com/api/posts/?page=2",
       "previous": null,
       "results": [
         {
           "id": "1",
           "title": "Post title",
           "content": "Post content",
           "author": "user123",
           "created_at": "2021-07-16T15:00:00",
           "updated_at": "2021-07-16T15:00:00",
           "comments": []
         }
       ]
     }
     ```

#### 2. **Create a Post**
   - **Endpoint**: `api/posts/`
   - **Method**: POST
   - **Request Body**:

     ```json
     {
       "title": "Post title",
       "content": "Post content"
     }
     ```
   - **Response**:

     ```json
     {
       "id": "1",
       "title": "Post title",
       "content": "Post content",
       "author": "user123",
       "created_at": "2021-07-16T15:00:00",
       "updated_at": "2021-07-16T15:00:00"
     }
     ```

#### 3. **Get a Post**
   - **Endpoint**: `api/posts/{id}/`
   - **Method**: GET
   - **Response**:

     ```json
     {
       "id": "1",
       "title": "Post title",
       "content": "Post content",
       "author_username": "user123",
       "created_at": "2021-07-16T15:00:00",
       "updated_at": "2021-07-16T15:00:00",
       "comments": [
         {
           "id": "1",
           "content": "Comment content",
           "author": "commenter123",
           "post": 1,
           "created_at": "2021-07-16T15:30:00",
           "updated_at": "2021-07-16T15:30:00"
         }
       ]
     }
     ```

#### 4. **Update a Post**
   - **Endpoint**: `api/posts/{id}/`
   - **Method**: PUT
   - **Request Body**:

     ```json
     {
       "title": "Updated post title",
       "content": "Updated post content"
     }
     ```
   - **Response**:

     ```json
     {
       "id": "1",
       "title": "Updated post title",
       "content": "Updated post content",
       "author": "user123",
       "created_at": "2021-07-16T15:00:00",
       "updated_at": "2021-07-16T15:00:00"
     }
     ```

#### 5. **Delete a Post**
   - **Endpoint**: `api/posts/{id}/`
   - **Method**: DELETE
   - **Response**:

     ```json
     {
       "message": "Post deleted successfully"
     }
     ```

### Comments

#### 1. **Create a Comment**
   - **Endpoint**: `api/comments/`
   - **Method**: POST
   - **Request Body**:

     ```json
     {
       "content": "Comment content",
       "post": 1
     }
     ```
   - **Response**:

     ```json
     {
       "id": "1",
       "content": "Comment content",
       "post": 1,
       "author": "commenter123",
       "created_at": "2021-07-16T15:30:00",
       "updated_at": "2021-07-16T15:30:00"
     }
     ```

#### 2. **Update a Comment**
   - **Endpoint**: `api/comments/{id}/`
   - **Method**: PUT
   - **Request Body**:

     ```json
     {
       "content": "Updated comment content"
     }
     ```
   - **Response**:

     ```json
     {
       "id": "1",
       "content": "Updated comment content",
       "post": 1,
       "author": "commenter123",
       "created_at": "2021-07-16T15:30:00",
       "updated_at": "2021-07-16T15:30:00"
     }
     ```

#### 3. **Delete a Comment**
   - **Endpoint**: `api/comments/{id}/`
   - **Method**: DELETE
   - **Response**:

     ```json
     {
       "message": "Comment deleted successfully"
     }
     ```

---

## Notes

- Ensure to configure your email backend settings in the `settings.py` file to enable password reset emails.
- The project is structured to allow adding more apps, like a `Principal` app for posts and comments, which can be implemented later.
- For demonstration purposes, the database is SQLite but can be configured for any other database system.

## Usage

- API access available at `http://localhost:8000/api/`
- Documentation available at `http://localhost:8000/api/docs/swagger`

## Contributing

If you want to contribute to this project and make it better, your help is very welcome. Here are some ways you can contribute:

1. Clone the repository and make your changes.
2. Create a new branch: `git checkout -b feature/nueva-funcionalidad`.
3. Commit your changes: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin feature/nueva-funcionalidad`.
5. Submit a pull request.

## Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Consulta el archivo LICENSE para más detalles.
