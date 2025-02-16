# Code Refactor Web App

This is a simple web application that takes code as input and returns refactored code.

## Features

- Refactor Python code by removing unused imports.
- Simple web interface for input and output.

## Installation

1. Clone the repository:

   ```
   git clone <https://github.com/yourusername/code-refactor.git>
   cd code-refactor
   ```

Install dependencies:

```
pip install -r requirements.txt
```

Run the application:

```
python app.py
```

Open your browser and go to:

```
<http://127.0.0.1:5000>
```

Running with Docker
Build and run the Docker container:

```
docker-compose up --build
```

Open your browser and go to:

```
<http://localhost:5000>
```

Testing
Run the tests with:

```
python -m unittest test_backend.py
```