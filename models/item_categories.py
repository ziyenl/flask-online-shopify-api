from db import db


class ItemsCategories(db.Model):
    __tablename__ = "items_categories"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))