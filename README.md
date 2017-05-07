# Location-and-Oauth-API

**Add Location**
----
  Add json data about location in Database.

* **URL**

  /post_location

* **Method:**

  `POST`
  
*  **URL Params**

   `None`

* **Data Params**

   **Required:**
  'name, lat, lng '
  **Example: ** '{"name":"bhopal", "lat":"23.258926", "lng":"77.414120" }'
   
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `Successfully Added`
 
* **Error Response:**

  * **Code:** 403 <br />
    **Content:** `{ error : "<error message>" }`
