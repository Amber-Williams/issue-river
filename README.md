# River
An app to help teams with bugs, features and fixes

### Set up
1. run `source venv/bin/activate` to activate the projects virtual environment
2. run `pip install -r requirements.txt` to install package dependencies
3. create `.env` file that contains the same variables as `.env.example`

### Running the application
1. `uvicorn app.main:app --reload`
2. (optional) visit  http://127.0.0.1:8000/docs to see endpoint docs

### Testing
Run `python3 -m pytest`