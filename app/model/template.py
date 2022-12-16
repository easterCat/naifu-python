from datetime import datetime

from app import db


class BaseTemplate(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(120), default="")
    preview = db.Column(db.Text(300), default="")
    prompt = db.Column(db.Text(3000), nullable=False)
    prompt_zh = db.Column(db.Text(3000), default="")
    n_prompt = db.Column(db.Text(3000), default="")
    n_prompt_zh = db.Column(db.Text(3000), default="")
    step = db.Column(db.String(60), default="")
    sampler = db.Column(db.String(80), default="")
    scale = db.Column(db.String(60), default="")
    seed = db.Column(db.String(60), default="")
    skip = db.Column(db.String(60), default="")
    size = db.Column(db.String(60), default="")
    model = db.Column(db.Text(300), default="")
    path = db.Column(db.Text(300), default="")
    desc = db.Column(db.Text(300), default="")
    like = db.Column(db.Integer, default=0)
    like_address = db.Column(db.Text(3000), default="")
    category = db.Column(db.String(80), default="")
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    template_from = db.Column(db.String(30), default="")
    key_word = db.Column(db.String(30), default="")
    key_word2 = db.Column(db.String(30), default="")
    file1 = db.Column(db.Text(300), default="")
    file2 = db.Column(db.Text(300), default="")
    file3 = db.Column(db.Text(300), default="")

    def __init__(self, *args, **kwargs):
        self.set_args(**kwargs)

    def set_args(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_json(self):
        if "/original_i2i/" in self.preview:
            minify_preview = self.preview.replace(
                "/original_i2i/", "/min_original_i2i/"
            )
        elif "/original_20221209/" in self.preview:
            minify_preview = self.preview.replace(
                "/original_20221209/", "/min_original_20221209/"
            )
        elif "/chi_tu/" in self.preview:
            minify_preview = self.preview.replace("/chi_tu/", "/min_chi_tu/")
        else:
            minify_preview = self.preview.replace("/original/", "/min_original/")

        json_data = {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if c.name != "like_address"
        }
        json_data["minify_preview"] = minify_preview
        return json_data


class TemplateHan(BaseTemplate):
    __tablename__ = "template_han"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TemplateChitu(BaseTemplate):
    __tablename__ = "template_chitu"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TemplateTest(BaseTemplate):
    __tablename__ = "template_test"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TemplateStable(BaseTemplate):
    __tablename__ = "template_stable"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TemplateNoval(BaseTemplate):
    __tablename__ = "template_noval"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
