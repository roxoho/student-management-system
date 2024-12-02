import uvicorn
from app.routes import app
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    port = int(os.getenv("PORT", 10000))

    uvicorn.run(app, host="0.0.0.0", port=port)