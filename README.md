# BusTicketSystem

## Overview
BusTicketSystem is a backend API built with Django to handle user registration and booking of bus tickets. It provides endpoints for user authentication, allowing two types of users: admin and normal users. Admin users have the ability to manage bus routes and bus information, while normal users can access available trips and book tickets.

## Features
- **User Registration and Authentication:** Users can register for accounts and log in securely to access the booking system.
- **Admin Dashboard:** Admin users have access to an admin dashboard to manage bus routes and bus information.
- **Booking Management:** Normal users can search for available trips and book tickets for their desired journeys.
- **Role-based Access Control:** Differentiate between admin and normal users, with different permissions and access levels.

## Technologies Used
- **Backend Framework:** Django (Django corsheaders already installed and configured for simple frontend connections)
- **Database:** MySQL (with Django ORM)
- **Caching:** Redis
- **Dependency Management:** pip with requirements.txt
- **Version Control:** Git

## Installation and Configuration
**Bsure that you have installed python, redis, mysql on your system and have basic understanding of django**
1. Clone the repository:
git clone https://github.com/Genocadio/BusTicketSystem.git

2. Navigate to the project directory:
cd ./BusTicketSystem/busticket
3. Install dependencies:
pip install -r requirements.txt
4. Create a new mysql database and configure it in database secition in settings.py file in '**busticket\busticket\settings.py**'
5. Run the server:
python manage.py runserver

use the available local host link to access the ApI
here it will be **http://127.0.0.1:8000/**
so we will start testing different routes

## The project layout
- /busticket
- |__bookings  **:app to handle the bookings for trips**
- |__buses  **:app to handle buses and routes(trips available)**
- |__busticket  **:main project directory**
- |__users **:app to handle users**
## Using the API
lets start with user handling, this is done in users app to access users routes there are at:  
**/users/**
- Most routes  in the users app require authentication using a JSON Web Token (JWT). You can obtain a JWT by logging in with a registered user's email and password. Refer to the LoginView documentation for details. Include the JWT in the request header as "**Authorization: Bearer <access_token>**".
### Permissions:

Certain endpoints have specific permission requirements enforced using Django REST Framework permissions. These permissions are:

1. IsAuthenticated: User must be logged in with a valid JWT.
2. IsAdminUser: User must be an admin user.
3. IsNormalUser: User must be a normal user.

### Endpoints:  
1. ### Register (POST /register)  
- **/user/register**  
- Description: Registers a new user.  
- Request Data: JSON object containing:  
- email (string): User's email address (required)  
- name (string): User's name (required)  
- password (string): User's password (required)  
- user_type (string, optional): User type ("normal" or "admin"). Defaults to "normal".  
- Permissions: None (no authentication required)  
- Response: JSON object containing the newly created user's information (serialized using UserSerializer).  


2. ### Login (POST /login)
- **/users/login**  
- Description: Logs in a user and returns access and refresh tokens.  
- Request Data: JSON object containing:  
- email (string): User's email address (required)  
- password (string): User's password (required)  
- Permissions: None (no authentication required)  
- Response: JSON object containing:  
- message (string): "Login successful"  
- access_token (string): JWT access token  
- refresh_token (string): JWT refresh token (used to obtain new access tokens)  


3. ### User Information (GET /user)
- **/user/user** 
- Description: Retrieves information about the currently logged-in user.
- Permissions: IsAuthenticated
- Response: JSON object containing the logged-in user's information (serialized using UserSerializer).
4. ### Delete User (DELETE /user/<email>)
- **/users/user/<email>**
- Description: Deletes a user by email address.
- Permissions: IsAuthenticated, IsAdminUser (user performing the deletion must be an admin)
- Request Path: Replace <email> with the email address of the user to be deleted.
- Response: Empty response with status code 204 (No Content) upon successful deletion.
5. ### Update User Information (PUT /user)
- **/users/user**
- Description: Updates information about the currently logged-in user
- Permissions: IsAuthenticated (for updating own information)
- Request Data: JSON object containing fields to be updated (e.g., email, name, password, user_type).
- Response: JSON object containing the updated user's information (serialized using UserSerializer).
6. ### Logout (POST /logout)
- **/users/logout**
- Description: Logs out the currently logged-in user.
- Permissions: IsAuthenticated
- Response: JSON object containing:
- message (string): "Logout successful"
7. ### Get All Users (GET /users)
- **/users/users**
- Description: Retrieves information about all registered users.
- Permissions: IsAdminUser
- Response: JSON array containing information for all users (serialized using UserSerializer).

Now we can go on buses and routes/trips handling,  this can be done by using the **/buses** route

- Most routes  in the buses app require authentication using a JSON Web Token (JWT). You can obtain a JWT by logging in with a registered user's email and password. Refer to the LoginView documentation for details. Include the JWT in the request header as "**Authorization: Bearer <access_token>**".
### Permissions:
Certain endpoints have specific permission requirements enforced using Django REST Framework permissions. These permissions are:

1. IsAuthenticated: User must be logged in with a valid JWT.
2. IsAdminUser: User must be an admin user.

### Endpoints:

1. ### Route List (GET /buses/routes)
- **/buses/routes**
- Description: Retrieves a list of all available routes.

- Permissions: IsAdminUser, IsAuthenticated (admin or authenticated user)

- Response: JSON array containing information for all routes (serialized using RouteSerializer).

2. ### Route Detail (DELETE /buses/routes/<route_id>)
- **/buses/routes/<route_id>**
- Description: Delete a single route matching a specific id.

- Permissions: IsAdminUser, IsAuthenticated

- Request Path: Replace <route_id> with the actual ID of the route you want to retrieve.

- Response: 204 No Content

3. ### Bus Detail (DELETE /buses/buses/<bus_id)
- **/buses/buses/<bus_id>**
- Description: Delete a single bus
- Permissions: IsAdmin, IsAuthenticated
- Request:  Replace <bus_id> with the id of the bus you want to delete.
- Response: 204 No Content
4. ### Trip Detail (DELETE /buses/trips/<trip_id>)
-**/buses/trips/<tip_id>**
- Description: Delete a single trip
- Permissions: IsAdmin, IsAuthenticated
- Request: Replace <trip_id> with the id of the trip you want to delete.
- Response: 204 No Content

5. ### Create Route (POST /buses/routes)
- **/buses/routes**
- Description: Creates a new route with provided details.

- Permissions: IsAdminUser (admin user only)
- Request Data: JSON object containing route information
- Response: JSON object containing information for the newly created route


6. ### Create Route (DELETE /buses/routes)
- **/buses/routes**
- Description: Deletes all routes from database.
- Permissions: IsAdminUser (admin user only)
- Response: 204 no content


7. ### Create Route (GET /buses/buses)
- **/buses/buses**
- Description: gets all buses from database.
- Permissions: IsAdminUser (admin user only)
- Response: JSON object containing information for the available buses


8. ### Create Route (POST /buses/buses)
- **/buses/buses**
- Description: Adds a bus to the database.
- Permissions: IsAdminUser (admin user only)
- Request: Json with information for bus (basename and seats count)
- Response: JSON object containing information for the added bus

9. ### Create Route (DELETE /buses/buses)
- **/buses/buses**
- Description: Deletes all buses from database.
- Permissions: IsAdminUser (admin user only)
- Response: 204 no content
10. ### Create Route (GET /buses/trips)
- **/buses/trips**
- Description: gets all trips from database.
- Permissions: IsAdminUser (admin user only)
- Response: JSON object containing information for the available trips


11. ### Create Route (POST /buses/trips)
- **/buses/trips**
- Description: Adds a trip to the database.
- Permissions: IsAdminUser (admin user only)
- Request: Json with information for trip (bus and route id, deperture and arrival time)
- Response: JSON object containing information for the added bus

12. ### Create Route (DELETE /buses/trips)
- **/buses/trips**
- Description: Deletes all trips from database.
- Permissions: IsAdminUser (admin user only)
- Response: 204 no content


Now we can go on booking handling,  this can be done by using the **/bookings** route

- Most routes  in the bookings app require authentication using a JSON Web Token (JWT). You can obtain a JWT by logging in with a registered user's email and password. Refer to the LoginView documentation for details. Include the JWT in the request header as "**Authorization: Bearer <access_token>**".
This app requires redis to wrok
### Permissions:
Certain endpoints have specific permission requirements enforced using Django REST Framework permissions. These permissions are:

1. IsAuthenticated: User must be logged in with a valid JWT.


### Endpoints:

1. ### Route List (GET /bookings/bookings)
- **/bookings/bookings**
- Description: Retrieves a list of all available bookings.

- Permissions: IsAuthenticated

- Response: JSON array containing information for all routes (serialized using RouteSerializer).

2. ### Route Detail (DELETE /bookings/bookings)
- **/buses/bookings**
- Description: Delete a single booking matching a specific id.

- Permissions: IsAuthenticated

- Request: Json with the bookings id from database

- Response: 204 No Content

3. ### Bus Detail (POST /bookings/booking/<int:booking_id>)
- **/bookings/booking/<int:booking_id>**
- Description: Add a single booking to database
- Permissions: IsAuthenticated
- Request:  replace <int:booking_id> withbooking id from database
- Response: Json with the added booking info