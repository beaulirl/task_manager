# Task Manager API

This manager helps to track your tasks.

It supports the following methods:

## Creating task
### `POST` /api/v1/tasks/

**Post params**

**Required:**
* `'task_maker'`
* `'task_author'`
* `'status'`
* `'project'`

**Success Response:**

* **Code:** 201

**Error Response:**

  * **Code:** 400 Bad Request <br />
  * **Content:** `'Error: no such field `field_name` in post params'`

  OR

  * **Code:** 400 Bad Request <br />
  * **Content:** `'Error: there is no task name in post params.'`

  OR

  * **Code:** 400 Bad Request <br />
  * **Content:** `'Error: there is no `field_name` with such name.'`

## Updating task (update status and task_maker)
### `PUT` /api/v1/tasks/:task_id

**PUT params**

* `'task_maker'`
* `'status'`

**Success Response:**

* **Code:** 200

**Error Response:**

  * **Code:** 400 Bad Request <br />
  * **Content:** `'Error: there is no task with id ":id"'`

  OR

  * **Code:** 400 Bad Request <br />
  * **Content:** `'Error: there is no such "field_name"'`

## Deleting task
### `DELETE` /api/v1/tasks/:task_id

**Success Response:**

* **Code:** 200

## Adding comment
### `POST` /api/v1/tasks/:task_id/comments/

**POST params**
**Required:**
* `'comment'`


**Success Response:**

* **Code:** 201

**Error Response:**

  * **Code:** 400 Bad Request <br />
  * **Content:** `'Error: there is no comment in post params'`

  OR

  * **Code:** 400 Bad Request <br />
  * **Content:** `'Error: there is no task with id ":id"'`

## Getting task info
### `GET` /api/v1/tasks/:task_id

**Success Response:**

* **Code:** 200 <br />
* **Content:** `{"task_id": 1, "comments": ["1 comment", "2 comment"], "descriptions": ["Main description", "Not main description"], "task_author": "Anna", "task_status": "Done", "task_maker": "Elena"}`

**Error Response:**

  * **Code:** 400 Bad Request <br />
  * **Content:** `'Error: there is no task with id ":id"'`

## Getting task info with filters
### `GET` /api/v1/tasks/:task_id?status=:status&task_author=:author&task_maker=:maker&project=:project

**GET params**
* `status=[string]`
* `task_author=[string]`
* `task_maker=[string]`
* `project=[string]`


**Success Response:**

* **Code:** 200

**Error Response:**

  * **Code:** 400 Bad Request <br />
  * **Content:** `'Error: wrong get params'`
