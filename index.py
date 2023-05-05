from dotenv import load_dotenv
load_dotenv()

from app import app
from database.db import db

from utils.auth import signToken


if __name__ == "__main__":
    print(signToken({"id": 1, "role": "admin"}))
    app.run(debug=True)
