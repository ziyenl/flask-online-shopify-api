from db import db


# Each store can contain multiple categories e.g. mammal, reptile
# Each item can contain multiple categories e.g. black fur, regular grooming
# Each category can contain multiple items e.g. dog category contains chihuahua, labrador etc
class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    store_id = db.Column(db.Integer(), db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates="categories")
    items = db.relationship("ItemModel", back_populates="categories", secondary="items_categories")