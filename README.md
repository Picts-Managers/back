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

## Usage

To run the application, follow these steps:

1. Clone this repository.
2. Navigate to the project directory.
3. Run `docker-compose up` to start the services.
4. Access the application through the provided endpoints or the mobile application interface.
