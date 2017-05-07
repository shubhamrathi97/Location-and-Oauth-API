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
    
    
 **Add OAuth Details**
----
  Add json data of client in Database.

* **URL**

  /add_oauth

* **Method:**

  `POST`
  
*  **URL Params**

   `None`

* **Data Params**

   **Required:**
  `client_id, client_secret, redirect_uri `
  
  **Example:** `{"client_id":"ASDSfjdsfhj121432423","client_secret":"147652268+2665235421","redirect_uri":"www.shubhamrathi.me"}`
   
* **Success Response:**

  * **Code:** 201 <br />
    **Content:** `Successfully Added`
 
* **Error Response:**

  * **Code:** 403 <br />
    **Content:** `{ error : "<error message>" }`
    
    
 **Get Authorization Token**
----
 This is the default for Authorization Code grant. A successful response is 302 Found, which triggers a redirect to the redirect_uri. The response parameters are embedded in the query component (the part after ?) of the redirect_uri in the Location header.

* **URL**
  /oauth/authorize
  `Example: localhost:5000/oauth/authorize?response_type=code&client_id=123456789&redirect_uri=localhost.com&scope=read`
* **Method:**

  `GET`
  
*  **URL Params**
    **Required:**
   `response_type, client_id, redirect_uri, scope`

* **Data Params**
  `none`
  
* **Success Response:**

  * **Code:** 302 <br />
    **Content:** `http://<:redirect uri>/callback?code=<:authorization code>`
 
* **Error Response:**

  * **Code:** 400 <br />
    **Content:** `{ error : "invalid client_id" }`
    
  * **Code:** 400 <br />
    **Content:** `{ error : "invalid redirect_uri" }`



 **Get Access Token**
----
The Token endpoint is used by the client in order to get an access token or a refresh token. It is used by all grant types, except for Implicit grant (since an access token is issued directly).

In the Authorization Code grant, the client exchanges the authorization code it got from the Authorization endpoint for an access token.

* **URL**
  /oauth/token
  `Example: localhost:5000/oauth/token?client_id=12345645&client_secret=4585sd54das5a&grant_type=authorization_code&code=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnRfaWQiOiIxMjM0NTY3ODkifQ.pSnldg0lX4gom3nf_Cey04X3xYdSF2xGukQEkPKGwhY&redirect_uri=www.shubhamrathi.me`

* **Method:**

  `GET`
  
*  **URL Params**
    **Required:**
   `grant_type, code, client_id, client_secret, redirect_uri`

* **Data Params**
  `none`
  
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `  { "access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnRfaWQiOiIxMjM0NTY0NSIsImV4cCI6MTQ5NDEyODkzNCwiaWF0IjoxNDk0MTI4OTM0LCJ0eXBlIjoiYWNjZXNzIn0.IsLqkBcAM4Gk8yXWhg-kXpWZMA8pRYMkRWM7SsTJNQA","expires_in": "300000","refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnRfaWQiOiIxMjM0NTY0NSIsImV4cCI6MTQ5NDEyODkzNCwiaWF0IjoxNDk0MTI4OTM0LCJ0eXBlIjoicmVmcmVzaCJ9.xCv9QosOfjSQ_LvjBdFFmYDSPyMFtWkzJcEul6pJwIM","token_type": "Basic"}`
 
* **Error Response:**

  * **Code:** 400 <br />
    **Content:** `{ error : "invalid client_id" }`
    
  * **Code:** 400 <br />
    **Content:** `{ error : "invalid redirect_uri" }`
  
  * **Code:** 400 <br />
    **Content:** `{ error : "invalid client_secret" }`

