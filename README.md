# Contents

[Assessment Backend Developer](#Assessment-Backend-Developer)  
[APIDocs](#API-Documentation)  


## Assessment Backend Developer

**Dear candidate,**

It's great that you are taking our test. Through this test, we aim to assess your knowledge of Python, FastAPI, REST APIs, and self-sufficiency. We use this test for both inexperienced and experienced Python developers. It's important that you demonstrate an understanding of the core elements of Python, including the correct use of SOLID principles, exception handling, OOP, decorators, and package management. Additionally, inheritance is crucial as long as it is functional within the test application. Of course, it's important that you work in an organized and structured manner.

**To begin, we ask the following:**

- Create a publicly accessible git repository.
- Make clean interim commits so that the steps you have taken can be traced from your commits.
- Use FastAPI.
- Use Pydantic.
- Adhere to best practices for Python.
- Provide comments in your code to explain why you make certain choices. For this test, there are no "too many" comments as long as they clarify your thought process.
- Create a REST API for a simple task list. The API should support basic operations such as retrieving all tasks, retrieving a specific task, adding a new task, and updating/removing an existing task.

**We expect the following from you:**

- An endpoint for searching tasks.
- Support for pagination, filtering, and sorting.
- Unit testing.
- Authentication.

**Assessment criteria:**

- Structure and organization (40%)
- Re-usability and performance (30%)
- Code quality and best practices (30%)

## API-Documentation

## Description

FastAPI TODO server version 0.1.0

## Paths

### /api/token

#### POST

**Summary:** Get Access Token

**Description:**

Create Bearer token for API authorization

**Notes on access-token:**

* An access token is valid for 120 minutes

**Usage:**

headers: {"Authorization": "Bearer token"}

**Parameters:**

| Name        | In    | Description                              | Required | Type   |
|-------------|-------|------------------------------------------|----------|--------|
| grant_type  | query | Grant Type                               | true     | string |
| username    | query | Username                                 | true     | string |
| password    | query | Password                                 | true     | string |
| scope       | query | Scope                                    |          | string |
| client_id   | query | Client Id                                |          | string |
| client_secret | query | Client Secret                           |          | string |

**Responses:**

| Status Code | Description       |
|-------------|-------------------|
| 200         | Successful Response |
| 422         | Validation Error  |

### /api/users/create

#### POST

**Summary:** Users Create

**Description:**

Create a new user in the database

**Notes:**

Only admin users are allowed to create new users

**Parameters:**

| Name        | In    | Description                              | Required | Type   |
|-------------|-------|------------------------------------------|----------|--------|
| username    | body  | Username                                 | true     | string |
| email       | body  | Email                                    | true     | string |
| full_name   | body  | Full Name                                | true     | string |
| disabled    | body  | Disabled                                 |          | boolean |
| is_admin    | body  | Is Admin                                 |          | boolean |
| clear_password | body  | Clear Password                        | true     | string |

**Responses:**

| Status Code | Description       |
|-------------|-------------------|
| 200         | Successful Response |
| 422         | Validation Error  |

### /api/users/delete

#### DELETE

**Summary:** Users Delete

**Description:**

Remove a user from the database

**Notes:**

* Only admin users are allowed to remove a user from the database
* It's not allowed to remove oneself

**Parameters:**

| Name        | In    | Description                              | Required | Type   |
|-------------|-------|------------------------------------------|----------|--------|
| username    | query | Username                                 | true     | string |

**Responses:**

| Status Code | Description       |
|-------------|-------------------|
| 200         | Successful Response |
| 422         | Validation Error  |

### /api/todos

#### GET

**Summary:** Get All

**Description:**

Get all todos from database, filter and sort results

 * filter on (a part of the) title
 * sort by: id, title, description or due_date

**Parameters:**

| Name        | In    | Description                              | Required | Type   |
|-------------|-------|------------------------------------------|----------|--------|
| page        | query | Page                                     | true     | integer|
| page_size   | query | Page Size                                | true     | integer|
| title       | query | Title                                    |          | string |
| sort_by     | query | Sort By                                  |          | string |

**Responses:**

| Status Code | Description       |
|-------------|-------------------|
| 200         | Successful Response |
| 422         | Validation Error  |

#### POST

**Summary:** Post

**Description:**

Create new todo

**Responses:**

| Status Code | Description       |
|-------------|-------------------|
| 200         | Successful Response |
| 422         | Validation Error  |

### /api/todos/{_id}

#### GET

**Summary:** Get

**Description:**

Get todo from database by id

**Parameters:**

| Name        | In    | Description                              | Required | Type   |
|-------------|-------|------------------------------------------|----------|--------|
| _id         | path  |  Id                                      | true     | integer|

**Responses:**

| Status Code | Description       |
|-------------|-------------------|
| 200         | Successful Response |
| 422         | Validation Error  |

#### PUT

**Summary:** Put

**Description:**

Update todo

**Parameters:**

| Name        | In    | Description                              | Required | Type   |
|-------------|-------|------------------------------------------|----------|--------|
| _id         | path  |  Id                                      | true     | integer|

**Responses:**

| Status Code | Description       |
|-------------|-------------------|
| 200         | Successful Response |
| 422         | Validation Error  |

#### DELETE

**Summary:** Delete

**Description:**

Delete todo

**Parameters:**

| Name        | In    | Description                              | Required | Type   |
|-------------|-------|------------------------------------------|----------|--------|
| _id         | path  |  Id                                      | true     | integer|

**Responses:**

| Status Code | Description       |
|-------------|-------------------|
| 200         | Successful Response |
| 422         | Validation Error  |

## Components

### Schemas

#### Body_get_access_token_api_token_post

| Name         | Type   | Description               | Required |
|--------------|--------|---------------------------|----------|
| grant_type   | string | Grant Type                | true     |
| username     | string | Username                  | true     |
| password     | string | Password                  | true     |
| scope        | string | Scope                     |          |
| client_id    | string | Client Id                 |          |
| client_secret| string | Client Secret             |          |

#### HTTPValidationError

| Name         | Type   | Description               | Required |
|--------------|--------|---------------------------|----------|
| detail       | array  | Detail                    |          |

#### NewUser

| Name         | Type    | Description              | Required |
|--------------|---------|--------------------------|----------|
| username     | string  | Username                 | true     |
| email        | string  | Email                    | true     |
| full_name    | string  | Full Name                | true     |
| disabled     | boolean | Disabled                 |          |
| is_admin     | boolean | Is Admin                 |          |
| clear_password | string | Clear Password          | true     |

#### SortByFields

| Name         | Type   | Description              | Required |
|--------------|--------|--------------------------|----------|
|              | string |                          |          |

#### ToDoListModelPaginated

| Name         | Type    | Description              | Required |
|--------------|---------|--------------------------|----------|
| page         | integer | Page                     | true     |
| page_size    | integer | Page Size                | true     |
| pages        | integer | Pages                    | true     |
| result       | array   | Result                   | true     |

#### ToDoModel

| Name         | Type    | Description              | Required |
|--------------|---------|--------------------------|----------|
| id           | integer | Id                       |          |
| title        | string  | Title                    | true     |
| description  | string  | Description              | true     |
| due_date     | string  | Due

 Date                 | true     |
| completed    | boolean | Completed                |          |

#### Token

| Name         | Type    | Description              | Required |
|--------------|---------|--------------------------|----------|
| access_token | string  | Access Token             | true     |
| token_type   | string  | Token Type               | true     |

#### User

| Name         | Type    | Description              | Required |
|--------------|---------|--------------------------|----------|
| username     | string  | Username                 | true     |
| email        | string  | Email                    |          |
| full_name    | string  | Full Name                |          |
| disabled     | boolean | Disabled                 |          |
| is_admin     | boolean | Is Admin                 |          |

#### ValidationError

| Name         | Type    | Description              | Required |
|--------------|---------|--------------------------|----------|
| loc          | array   | Location                 | true     |
| msg          | string  | Message                  | true     |
| type         | string  | Error Type               | true     |

### Security Schemes

#### OAuth2PasswordBearer

| Type         | Description                |
|--------------|----------------------------|
| oauth2       |                            |
| flows        |                            |

