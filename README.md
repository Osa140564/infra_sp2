# YaMDb Project
The YaMDb project collects user reviews on works (Title). The works are divided into categories: "Books", "Films", "Music". The list of categories (Category) can be expanded.
The works themselves are not stored in YaMDb, you can't watch a movie or listen to music here.
In each category there are works: books, movies or music. For example, in the category "Books" there can be works "Winnie the Pooh and everything-everything-everything" and "Martian Chronicles", and in the category "Music" there can be a song "Recently" by the group "Insects" and the second suite by Bach. A work can be assigned a genre from the preset list (for example, "Fairy Tale", "Rock" or "Arthouse"). New genres can only be created by the administrator.
Grateful or outraged readers leave text reviews to the works and give the work a rating.

# YaMDb API resources
**AUTH**: authentication.

**USERS**: users.

**TITLES**: works that are reviewed (a certain movie, book or song).

**CATEGORIES**: categories (types) of works ("Movies", "Books", "Music").

**GENRES**: genres of works. One work can be linked to several genres.

**REVIEWS**: reviews of works. The review is tied to a specific work.

**COMMENTS**: comments on reviews. The comment is linked to a specific review.

# User registration algorithm
The user sends a POST request with the email parameter to `/api/v1/auth/email/'.
YaMDB sends an email with a confirmation code (confirmation_code) to an email address (a feature in development).
The user sends a POST request with the email and confirmation_code parameters to `/api/v1/auth/token/`, in response to the request he receives a token (JWT token).
These operations are performed once, during user registration. As a result, the user receives a token and can work with the API by sending this token with each request.

# User roles
**Anonymous** — can view descriptions of works, read reviews and comments.

**Authenticated user ** — can read everything, as well as Anonymous, additionally can publish reviews and rate works (films / books / songs), can comment on other people's reviews and give them ratings; can edit and delete their reviews and comments.

**Moderator (moderator)** — the same rights as an Authenticated User plus the right to delete and edit any reviews and comments.

**Admin** — full rights to manage the project and all its contents. Can create and delete works, categories and genres. Can assign roles to users.

**Django Admin** — the same rights as the Administrator role.

# Installation
Clone the repository. Being in the folder with the code, create a virtual environment `python -m venv venv`, activate it (Windows: `source venv\scripts\activate`; Linux/Mac: `sorce venv/bin/activate`), install dependencies `python -m pip install -r requirements.txt `.

To start the development server, from the project directory, run the commands:
``
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
``

The project has been launched and is available at [localhost:8000](http://localhost:8000 /).

# Project in development
You need to finalize sending the code when registering on e-amil and connect the project to Postgres.