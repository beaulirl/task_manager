# Task Manager Api

This manager helps to track your tasks.

It supports the following methods:

## Creating task

**URL**
/api/v1/tasks/

**Method**
`POST`

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
    **Content:** ``

  OR

  * **Code:** 401 UNAUTHORIZED <br />
    **Content:** `{ error : 'Error: there is no task name in post params.' }`

