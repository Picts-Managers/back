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

# Project: REST API

# PICTSMANAGER

PICTSMANAGER is a mobile application designed to facilitate the management and sharing of pictures. It includes features such as taking, storing, tagging, and handling pictures. The application organizes pictures into albums, each of which has an owner and a list of people who can view it.

## Requirements

### Usability-Driven Features

-   The application stores only pictures' names and associated IDs. Pictures, metadata, and other information are stored on a distant back server and can be retrieved and updated with specific requests.
-   Pictures taken from the phone camera need to be compressed before being stored, with a compromise between performance and quality.
-   The user who creates an album becomes its only owner and also owns all the pictures it contains. Ownership cannot be shared, transferred, or resigned.
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

# 📁 Collection: Auth

## Auth Login

This endpoint allows users to log in and obtain an access token.

-   Method: POST
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /auth/login

### Request Body

-   Type: Raw (application/json)

| Key      | **Type** | Description                         | **Required** |
| -------- | -------- | ----------------------------------- | ------------ |
| login    | string   | The user's login username or email. | true         |
| password | string   | The user's login password.          | true         |

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| Key          | **Type** | Description                                                 |
| ------------ | -------- | ----------------------------------------------------------- |
| access_token | string   | The user's Bearer token that he can use to perform request. |

## Auth Register

This endpoint allows users to register and obtain an access token.

-   Method: POST
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /auth/register

### Request Body

-   Type: Raw (application/json)

| Key      | **Type** | Description          | **Required** |
| -------- | -------- | -------------------- | ------------ |
| email    | string   | The user's email.    | true         |
| username | string   | The user's username. | true         |
| password | string   | The user's password. | true         |

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| Key          | **Type** | Description                                                 |
| ------------ | ----------------------------------------------------------- | -------- |
| access_token | string   | The user's Bearer token that he can use to perform request. |

# 📁 Collection: Users

## Users Me

This endpoint allows a user to retrieve the informations of his account.

-   Method: GET
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /users/me
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| Key      | **Type** | Description          |
| -------- | -------- | -------------------- |
| id       | string   | The user's id.       |
| email    | string   | The user's email.    |
| username | string   | The user's username. |

## Update User Profile

This endpoint allows users to update their profile information.

-   Method: PATCH
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /users/me
-   Authentication: Bearer token required

### Request Body

-   Type: Raw (application/json)

| **Key**  | **Type** | **Description**               | **Required** |
| -------- | -------- | ----------------------------- | ------------ |
| username | string   | The user's new username.      | false        |
| email    | string   | The user's new email address. | false        |

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| **Key**  | **Type** | **Description**                   |
| -------- | -------- | --------------------------------- |
| id       | string   | The user's unique identifier.     |
| username | string   | The user's updated username.      |
| email    | string   | The user's updated email address. |

## Method: PUT

> ```
> {{base_url}}/users/me
> ```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

## End-point: Delete my account

## Delete Album

This endpoint allows users to delete an existing album.

-   Method: DELETE
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /albums/
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| **Field** | **Type** | **Description**                                           |
| --------- | -------- | --------------------------------------------------------- |
| message   | string   | A message confirming the successful deletion of the user. |

# 📁 Collection: Albums

## End-point: Get my albums

## Get Albums

This endpoint retrieves a list of albums owned by the user.

-   Method: GET
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /albums
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

The response body will be a JSON object with an "albums" field containing a list of objects, each representing an album with the following attributes:

```json
{
    "albums": [
        {
            "id": "string",
            "owner_id": "string",
            "title": "string",
            "cover_id": "string",
            "viewers_ids": ["string"],
            "pictures_ids": ["string"]
        },
        ...
    ]
}

```

## Get Album by ID

This endpoint retrieves information about a specific album identified by its ID.

-   Method: GET
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /albums/`album_id`
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| **Key**      | **Type**         | **Description**                                                            |
| ------------ | ---------------- | -------------------------------------------------------------------------- |
| id           | string           | The unique identifier of the album.                                        |
| owner_id     | string           | The unique identifier of the owner of the album.                           |
| title        | string           | The title of the album.                                                    |
| cover_id     | string           | The unique identifier of the cover picture of the album.                   |
| viewers_ids  | array of strings | List of unique identifiers of users who have permission to view the album. |
| pictures_ids | array of strings | List of unique identifiers of pictures in the album.                       |

## Get Shared Albums

This endpoint retrieves a list of albums shared with the user.

-   Method: GET
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /albums/shared
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

The response body will be a JSON object with an "albums" field containing a list of objects, each representing an album shared with the user with the following attributes:

```json
{
    "albums": [
        {
            "id": "string",
            "owner_id": "string",
            "title": "string",
            "cover_id": "string",
            "viewers_ids": ["string"],
            "pictures_ids": ["string"]
        },
        ...
    ]
}

```

## Get Picture from Album

This endpoint retrieves a picture from a specific album identified by its ID.

-   Method: GET
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /albums/`album_id`/`picture_id`
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: image/\* (MIME type of the image)

#### Response Body

The response body will be the image file itself.

## Get Low-Resolution Picture from Album

This endpoint retrieves a low-resolution version of a picture from a specific album identified by its ID.

-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /albums/`album_id`/`picture_id`/low
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: image/\* (MIME type of the image)

#### Response Body

The response body contains the low-resolution image file in a 200x200 format.

## Create Album

This endpoint allows users to create a new album.

-   Method: POST
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /albums
-   Authentication: Bearer token required

### Request Body

-   Content-Type: application/json

#### Request Body Schema

| **Field** | **Type** | **Description**        | **Required** |
| --------- | -------- | ---------------------- | ------------ |
| name      | string   | The name of the album. | true         |

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| **Field**    | **Type**          | **Description**                                                            |
| ------------ | ----------------- | -------------------------------------------------------------------------- |
| id           | string            | The unique identifier of the created album.                                |
| owner_id     | string            | The unique identifier of the owner of the album.                           |
| title        | string            | The title of the album.                                                    |
| cover_id     | string (optional) | The unique identifier of the cover picture of the album, if available.     |
| viewers_ids  | array of strings  | List of unique identifiers of users who have permission to view the album. |
| pictures_ids | array of strings  | List of unique identifiers of pictures in the album.                       |

## Add Picture to Album

This endpoint allows users to add an already uploaded image to an existing album.

-   Method: PATCH
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /albums/`album_id`
-   Authentication: Bearer token required

### Request Body

-   Content-Type: application/json

#### Request Body Schema

| **Field**  | **Type** | **Description**                            | **Constraints**                                |
| ---------- | -------- | ------------------------------------------ | ---------------------------------------------- |
| picture_id | string   | The ID of the picture to add to the album. | Must adhere to specified pattern (isObjectId). |

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| **Field**    | **Type**          | **Description**                                                            |
| ------------ | ----------------- | -------------------------------------------------------------------------- |
| id           | string            | The unique identifier of the updated album.                                |
| owner_id     | string            | The unique identifier of the owner of the album.                           |
| title        | string            | The title of the album.                                                    |
| cover_id     | string (optional) | The unique identifier of the cover picture of the album, if available.     |
| viewers_ids  | array of strings  | List of unique identifiers of users who have permission to view the album. |
| pictures_ids | array of strings  | List of unique identifiers of pictures in the album.                       |

## Upload Image to Album

This endpoint allows users to upload an image to an existing album.

-   Method: PATCH
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /albums/upload/`album_id`
-   Authentication: Bearer token required

### Request Body

-   Content-Type: multipart/form-data

#### Request Body Parameters

| **Parameter** | **Type** | **Description**                        |
| ------------- | -------- | -------------------------------------- |
| file          | file     | The image file to upload to the album. |

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| **Field**    | **Type**          | **Description**                                                            |
| ------------ | ----------------- | -------------------------------------------------------------------------- |
| id           | string            | The unique identifier of the updated album.                                |
| owner_id     | string            | The unique identifier of the owner of the album.                           |
| title        | string            | The title of the album.                                                    |
| cover_id     | string (optional) | The unique identifier of the cover picture of the album, if available.     |
| viewers_ids  | array of strings  | List of unique identifiers of users who have permission to view the album. |
| pictures_ids | array of strings  | List of unique identifiers of pictures in the album.                       |

## Share Album

This endpoint allows users to share an album with other users.

-   Method: PATCH
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /albums/`album_id`/share
-   Authentication: Bearer token required

### Request Body

-   Content-Type: application/json

#### Request Body Schema

| **Field** | **Type** | **Description**                      |
| --------- | -------- | ------------------------------------ |
| user_id   | string   | The user ID to share the album with. |

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| **Field**    | **Type** | **Description**                                                            |
| ------------ | -------- | -------------------------------------------------------------------------- |
| id           | string   | The unique identifier of the album.                                        |
| owner_id     | string   | The unique identifier of the owner of the album.                           |
| title        | string   | The title of the album.                                                    |
| cover_id     | string   | The unique identifier of the cover picture of the album.                   |
| viewers_ids  | array    | List of unique identifiers of users who have permission to view the album. |
| pictures_ids | array    | List of unique identifiers of pictures in the album.                       |
| shared_with  | array    | List of unique identifiers of users the album is shared with.              |

## Delete Album

This endpoint allows users to delete an existing album.

-   Method: DELETE
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /albums/
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| **Field** | **Type** | **Description**                                            |
| --------- | -------- | ---------------------------------------------------------- |
| message   | string   | A message confirming the successful deletion of the album. |

# 📁 Collection: Pictures

## End-point: Get my pictures

## Get Pictures

This endpoint retrieves a list of pictures.

-   Method: GET
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /pictures
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

```json
{
    "pictures": [
        {
            "id": "string",
            "filename": "string",
            "owner_id": "string",
            "date": "string",
            "location": {
                "latitude": "string",
                "longitude": "string"
            },
            "viewers_ids": ["string"]
        },
        ...
    ]
}

```

## Get Picture by ID

This endpoint retrieves the picture identified by its ID.

-   Method: GET
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /pictures/`picture_id`
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: image/jpeg (or appropriate image format)

## Get Low-Resolution Picture by ID

This endpoint retrieves a low-resolution version of a specific picture identified by its ID.

-   Method: GET
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /pictures/`picture_id`/low
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: image/jpeg (or appropriate image format)

## Upload Picture

This endpoint allows users to upload a picture.

-   Method: POST
-   Base URL: [[http://localhost:3000](http://localhost:3000)](<http://localhost:3000](http://localhost:3000)>)
-   Path: /pictures/upload
-   Authentication: Bearer token required

### Request Body

-   Content-Type: multipart/form-data

#### Request Body Parameters

| **Parameter** | **Type** | **Description**           |
| ------------- | -------- | ------------------------- |
| file          | file     | The image file to upload. |

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| **Field**          | **Type** | **Description**                                                                               |
| ------------------ | -------- | --------------------------------------------------------------------------------------------- |
| id                 | string   | The unique identifier of the uploaded picture.                                                |
| filename           | string   | The filename of the uploaded picture.                                                         |
| owner_id           | string   | The unique identifier of the owner of the picture.                                            |
| date               | string   | The date the picture was uploaded. If not provided, it defaults to the current date and time. |
| location           | object   | The coordinates of the location where the picture was taken. (Optional)                       |
| location.latitude  | string   | The latitude of the location.                                                                 |
| location.longitude | string   | The longitude of the location.                                                                |
| viewers_ids        | array    | List of unique identifiers of users who have permission to view the picture.                  |

## Share Picture

This endpoint allows users to share a picture with other users.

-   Method: PATCH
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /pictures/`picture_id`/share
-   Authentication: Bearer token required

### Request Body

-   Content-Type: application/json

#### Request Body Parameters

| **Parameter** | **Type** | **Description**                        |
| ------------- | -------- | -------------------------------------- |
| user_email       | string   | The email of the user to share the picture with. |

### Response

-   Status: 200
-   Content-Type: image/jpeg (or appropriate image format)

The response will contain the shared picture.

## Delete Picture

This endpoint allows users to delete a specific picture.

-   Method: DELETE
-   Base URL: [http://localhost:3000](http://localhost:3000)
-   Path: /pictures/`picture_id`
-   Authentication: Bearer token required

### Response

-   Status: 200
-   Content-Type: application/json

#### Response Body

| **Field** | **Type** | **Description**                                              |
| --------- | -------- | ------------------------------------------------------------ |
| message   | string   | A message confirming the successful deletion of the picture. |
