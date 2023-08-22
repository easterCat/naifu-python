import os

from dotenv import load_dotenv

from app import create_app, db

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

config_name = os.getenv("FLASK_CONFIG", "development")
app = create_app(config_name)

print("当前环境 = > ", app.config["ENV"])


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)


def main():
    if app.config["ENV"] == "production":
        from waitress import serve

        serve(app, host="0.0.0.0", port=5000)
    else:
        app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
