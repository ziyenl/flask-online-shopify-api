from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import CategoryModel, StoreModel, ItemModel
from schema import CategorySchema, CategoryAndItemSchema

blp = Blueprint("Categories", "categories", description="Operations on categories")


@blp.route("/category/<int:category_id>")
class Category(MethodView):
    @blp.response(200, CategorySchema)
    def get(self, category_id):
        """
        Get category info for a category id
        :param category_id: category id
        :return: category
        """
        category = CategoryModel.query.get_or_404(category_id)
        return category

    @blp.response(
        202,
        description="Deletes a category if no item is linked to it.",
        example={"message": "Category deleted."},
    )
    @blp.alt_response(404, description="Category not found.")
    @blp.alt_response(
        400,
        description="Returned if the category is assigned to one or more items. In this case, the category is not deleted.",
    )
    def delete(self, category_id):
        """
        Delete a category if no items are associated with that category
        :param category_id: category id
        :return: str
        """
        category = CategoryModel.query.get_or_404(category_id)

        if not category.items:
            db.session.delete(category)
            db.session.commit()
            return {"message": "Category deleted."}
        abort(
            400,
            message="Could not delete category. Make sure category is not associated with any items, then try again.",  # noqa: E501
        )


@blp.route("/store/<int:store_id>/category")
class CategoriesInStore(MethodView):
    @blp.response(200, CategorySchema(many=True))
    def get(self, store_id):
        """
        Get categories for a given store
        :param store_id: store id
        :return: list of categories
        """
        store = StoreModel.query.get_or_404(store_id)

        return store.categories.all()

    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data, store_id):
        """
        Add a category to a store
        :param category_data: category data
        :param store_id: store id
        :return: category
        """
        if CategoryModel.query.filter(CategoryModel.store_id == store_id).first():
            abort(400, message="A category with that name already exists in that store.")

        category = CategoryModel(**category_data, store_id=store_id)

        try:
            db.session.add(category)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return category


@blp.route("/item/<int:item_id>/category/<int:category_id>")
class LinkCategoryToItem(MethodView):
    @blp.response(201, CategorySchema)
    def post(self, item_id, category_id):
        """
        Link a category to an item
        :param item_id: item id
        :param category_id: category id
        :return: category
        """
        item = ItemModel.query.get_or_404(item_id)
        category = CategoryModel.query.get_or_404(category_id)

        item.categories.append(category)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category for the given item.")

        return category

    @blp.response(200, CategoryAndItemSchema)
    def delete(self, item_id, category_id):
        """
        Unlink category from an item
        :param item_id: item id
        :param category_id: category id
        :return: CategoryAndItemSchema
        """
        item = ItemModel.query.get_or_404(item_id)
        category = CategoryModel.query.get_or_404(category_id)

        item.categories.remove(category)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the category.")

        return {"message": "Item removed from category", "item": item, "category": category}

