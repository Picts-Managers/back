## Requirements

### Usability-Driven Features

-   The application stores only pictures' names and associated IDs. Pictures, metadata, and other information are stored on a distant back server and can be retrieved and updated with specific requests.
-   Pictures taken from the phone camera need to be compressed before being stored, with a compromise between performance and quality.
-   The user who creates an album becomes its only owner and owns all the pictures it contains. Ownership cannot be shared, transferred, or resigned.
-   Only the owner of a picture/album can modify/delete it.
-   Users can only see pictures/albums they own or have been granted access to.
-   Implementation of a research engine without external libraries.
-   The application should be reactive, with no lag when accessing pictures.

### Technical Requirements

-   Architecture designed with scalability in mind.
-   Use of efficient algorithms and database models.
-   Containerization of services with Docker and orchestration with Docker Compose.
-   Automation of the construction of the mobile application and the back-end within containers.
-   Comprehensive documentation including Software Architecture Specification and Software Qualification.
-   Implementation of a testing policy.
-   Logging of all errors and important messages in a clear manner.
-   Optimized for Python 3.11.

## Usage

To run the application in production, follow these steps:

1. Clone this repository.
2. Navigate to the project directory.
3. Fill in the `.env` file with the required environment variables. You can use the `.env.example` file as a template.
4. `docker-compose up --build` to build and start the services.
5. The application is now running on `localhost:3000` you can use reverse proxy engine like nginx or apache to handle http/https.

To run the application in development, follow these steps:

1. Clone this repository.
2. Navigate to the project directory.
3. Fill in the `.env` file with the required environment variables. You can use the `.env.example` file as a template.
4. `python main.py` to build and start the services.
5. The application is now running on `localhost:3000`, you will found a complete swagger on `localhost:3000/`.
