from app import create_app, db
from flask_migrate import Migrate, upgrade

app = create_app('development')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)


if __name__ == '__main__':
    # upgrade()
    app.run(host="0.0.0.0", debug=True)
