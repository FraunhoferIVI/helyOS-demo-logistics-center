# Clothoid Microservice
This microservice parses the helyos context data and build assignments to transport trailers.

### Build

Run by docker-compose:
```
docker-compose up
```

Either, you can build your own python virtual environment, install all dependencies and run it.

- Creat python virtual environment
    ```
    python -m venv osmenv
    osmenv\Scripts\activate.bat
    # or
    osmenv\Scripts\Activate.ps1
    ```

- Install packages:
    ```
    python -m pip install -r requirements.txt
    ```
- Run:
    ```
    python ./src/service.py
    ```
