Documentationb API:

Stateless. It means that each request from a client to the server contains all the information necessary to understand and process the request. The sever does not store any client state.

Uses the HTTP protocol. HTTP provides a set of standardized methods (GET, POST, PUT, DELETE) for interacting with resources (data in the server). It use also status codes; e.g. 200 = successful,  201 = resource created, 400 = error,  404 = resource not found, etc.

It is about resources.  It uses a resource identifier usually embedded in the URL (Uniform Resource Locator), the service path.
Example:

    * http//service.com/books/  GET : get a list of books.
    


