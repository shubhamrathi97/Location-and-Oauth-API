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
  `name, lat, lng `
  
  **Example:** `{"name":"bhopal", "lat":"23.258926", "lng":"77.414120" }`
   
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `Successfully Added`
 
* **Error Response:**

  * **Code:** 403 <br />
    **Content:** `{ error : "<error message>" }`


**Get location using postgres method**
----
  Get data of location in radius of 5kms of given location. Used earth_distance and cube extension in postgres

* **URL**

  /get_using_postgres/:lat/:lng

* **Method:**

  `GET`
  
*  **URL Params**

   `lat, lng`

* **Data Params**
    `None`
   
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"name": "bhopal accurate"},{"name": "bhopal accurate 2"}]`
 
 
**Get location using mathematical computation**
----
  Get data of location in radius of 5kms of given location. Used custom logic to get data

* **URL**

  /get_using_self/:lat/:lng

* **Method:**

  `GET`
  
*  **URL Params**

   `lat, lng`

* **Data Params**
    `None`
   
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `[{"name": "bhopal accurate"},{"name": "bhopal accurate 2"}]`
