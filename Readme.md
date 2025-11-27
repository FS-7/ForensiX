1. Running Frontend (Flask)
   * cd web/react
   * npm i
   * npx shadcn@latest init
   * npm run dev

2. Running Backend (Flask)
   * cd web/flask   
   * Create a .env file
     * SESSION_KEY = "5c69b50571378eb1abc5443160fcd87800cd1b0c2e482606e1735cea2d2b5f3c"
     * UPLOAD_FOLDER = (uploaded files location)
     * DB_LOCATION = (Main DB location)
     * EXTRACTED_FILES_LOCATION = (Extracted files location)
     * EXT_DB_LOCATION = (Files database)
     * AI_URL = (URL to flask AI models server)

   * Create a virtual environment
     * virtualenv .venv
     * .venv\Scripts\activate.bat
     * pip install -r requirements.txt
     * flask run (optional: --debug for debugging)

3. Running AI models (Flask)
   * Requirements: 16GB Ram
   * Paging File: 100GB Storage
   * cd web/flask_ai
   
   * Create a .env file
     * HF_TOKEN

   * Create a virtual environment
     * virtualenv .venv
     * .venv\Scripts\activate.bat
     * pip install -r requirements.txt
     * flask run --port 5001
