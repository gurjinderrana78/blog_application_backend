# Blog Backend

This is a Django-based backend for a blog application, providing APIs for managing posts, comments, and likes. The application also includes JWT-based authentication.

## Features

- JWT Authentication for secure access
- CRUD operations for blog posts
- CRUD operations for comments on posts
- Like and unlike functionality for posts
- Pagination support for retrieving posts

## Installation

1. **Clone the repository**
    ```sh
    git clone https://github.com/gurjinderrana78/blog_application_backend.git
    cd blog_backend
    ```

2. **Create and activate a virtual environment**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Apply migrations**
    ```sh
    python manage.py migrate
    ```

5. **Run the development server**
    ```sh
    python manage.py runserver
    ```

## API Endpoints

### Authentication
- **Obtain Token**
    ```
    POST /login/token/
    ```
    Request Body:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```
    Response:
    ```json
    {
        "access": "access_token",
        "refresh": "refresh_token"
    }
    ```

- **Refresh Token**
    ```
    POST /login/token/refresh/
    ```
    Request Body:
    ```json
    {
        "refresh": "refresh_token"
    }
    ```
    Response:
    ```json
    {
        "access": "new_access_token"
    }
    ```

### Posts
- **Get All Posts and its like count and if logged in liked by current user or not**
    ```
    GET /posts/
    ```
    Query Parameters:
    - `page`: Page number (default: 1)
    - `page_size`: Number of posts per page (default: 10)
    
    Headers(Optional Parameters):
    ```http
    Authorization: Bearer <access_token>
    ```

- **Get Specific Post**
    ```
    GET /posts/<int:id>/
    ```

- **Create Post**
    ```
    POST /posts/
    ```
    Request Body:
    ```json
    {
        "post_title": "Post title",
        "post_content": "Post content"
    }
    ```
    Headers:
    ```http
    Authorization: Bearer <access_token>
    ```

- **Update Post**
    ```
    PUT /posts/<int:id>/
    ```
    Request Body:
    ```json
    {
        "post_title": "Updated title",
        "post_content": "Updated content"
    }
    ```
    Headers:
    ```http
    Authorization: Bearer <access_token>
    ```

- **Delete Post**
    ```
    DELETE /posts/<int:id>/
    ```
    Headers:
    ```http
    Authorization: Bearer <access_token>
    ```

### Comments
- **Get Comments for a Specific Post**
    ```
    GET /comments/<int:id>/
    ```

- **Create Comment**
    ```
    POST /comments/
    ```
    Request Body:
    ```json
    {
        "post_id": post_id,
        "comment_content": "Comment content",
        "author_name": "author_name",

    }
    ```
    Headers:
    ```http
    Authorization: Bearer <access_token>
    ```

- **Delete Comment**
    ```
    DELETE /comments/<int:id>/
    ```
    Headers:
    ```http
    Authorization: Bearer <access_token>
    ```

### Likes
- **Like or Unlike a Post**
    ```
    POST /like/<int:post_id>/
    ```
    Headers:
    ```http
    Authorization: Bearer <access_token>
    ```

## Pagination

All paginated endpoints return a response in the following format:
```json
{
    "data": [...],
    "pagination": {
        "total_pages": total_pages,
        "current_page": current_page,
        "has_prev": true_or_false,
        "has_next": true_or_false
    }
}
