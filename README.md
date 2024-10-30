# mayim



## Project Structure
```
mayim/ 
├── backend/ 
│   ├── app/ 
│   │   ├── __init__.py 
│   │   ├── models.py 
│   │   ├── routes.py 
│   │   └── ... 
│   ├── run.py 
│   ├── requirements.txt 
│   └── ... 
├── frontend/ 
│   ├── public/ 
│   ├── src/ 
│   │   ├── components/ 
│   │   ├── services/ 
│   │   ├── App.js 
│   │   ├── index.js 
│   │   └── ... 
│   ├── package.json 
│   └── ... 
├── .env 
├── .gitignore 
├── README.md 
└── ...
```

## Installation

### Prerequisites

- Python 3.12
- Node.js and npm

### Backend Setup

1. **Create a Python virtual environment**:
    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment**:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

3. **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Frontend Setup

Navigate to the frontend directory and install dependencies:
```bash
cd frontend
npm install
```

## Startup

### Backend Startup

Navigate to the backend directory and run the backend server:
```bash
cd backend
python run.py
```

### Frontend Startup

Navigate to the frontend directory and start the frontend development server:
```bash
cd frontend
npm start
```

## Environment Variables

Ensure you have a `.env` file in the root directory with the necessary content. Copy example.env and rename it to ".env". Add your own API keys as needed.

## Additional Information

- **Virtual Environment**: It's recommended to use a Python virtual environment to manage dependencies and avoid conflicts with other projects.
- **Node.js**: Ensure you have Node.js and npm installed on your system. You can download them from [nodejs.org](https://nodejs.org/).
- **Environment Variables**: The `.env` file should contain the necessary API keys and database connection strings for the project.

By following these instructions, you should be able to set up and run the Mayim project successfully. If you encounter any issues, please refer to the documentation or seek help from the project maintainers.
