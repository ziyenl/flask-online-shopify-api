from marshmallow import Schema, fields


class BaseStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class BaseItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class BaseCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class StoreSchema(BaseStoreSchema):
    items = fields.List(fields.Nested(BaseItemSchema()), dump_only=True)


class ItemSchema(BaseItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(BaseStoreSchema(), dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


# Each category belongs to a store and can contain multiple items
class CategorySchema(BaseCategorySchema):
    store_id = fields.Int(load_only=True)
    items = fields.List(fields.Nested(BaseItemSchema()), dump_only=True)
    store = fields.Nested(BaseStoreSchema(), dump_only=True)


class CategoryAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    category = fields.Nested(CategorySchema)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) # never sent back to client
