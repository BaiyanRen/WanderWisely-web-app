from flaskr.main import app
import os


port = int(os.environ.get('PORT', 33507))


if __name__ == "__main__":
        app.run(port=port)