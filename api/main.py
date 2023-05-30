from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from mysql.connector import connect, Error

from model.Payload.create import new_payment
from model.Payload.payload import NewPayloadBody
from model.Cart.remove import DropFromCartBody, remove_from_cart
from model.Cart.cart import CartBaseModel, CartResponse
from model.Cart.get import CartCountBaseModel, users_cart_count, get_cart
from model.Cart.add import cart_add_design, AddToCartBaseModel, AddToCartBody
from config.main import cors_origins
from model.Category.category import get_category, CategoryResult
from model.Design.design import get_design, DesignBaseModel

sql = 0

try:
    sql = connect(host="localhost",user='root',password='toor', database='mky')
except Error as e:
    print(e)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# get category + breadcrumbs
@app.get("/catalog/{category_id}")
async def get_category_by_id(category_id:int) -> CategoryResult:
    with sql.cursor() as db_connection:
        return get_category(db_connection, category_id)


# get one item
@app.get("/design/{design_id}")
async def get_one_design(design_id: int) -> DesignBaseModel:
    return get_design(sql.cursor(buffered=True), sql.cursor(buffered=True), design_id, False)


# save item to cart
@app.post("/cart/add")
async def add_to_cart(data: AddToCartBody) -> AddToCartBaseModel:
    session_key = cart_add_design(sql, data)
    return session_key


# get cart count
@app.get("/cart/count/{session_key}")
async def cart_count(session_key: str) -> CartCountBaseModel:
    return users_cart_count(sql, session_key)


# get cart count
@app.get("/cart/{session_key}")
async def get_cart_data(session_key: str) -> CartBaseModel:
    if session_key == 'false':
        return CartResponse([]).asdict()

    return get_cart(sql.cursor(), session_key)


# get cart countasdf
@app.post("/cart/remove")
async def drop_from_cart(data: DropFromCartBody) -> CartBaseModel:
    result = remove_from_cart(sql, data.session, data.cart_id)
    if result:
        return get_cart(sql.cursor(), data.session)



# create payment
@app.post("/payment/new")
async def create_payment(data: NewPayloadBody):
    return new_payment(sql, data)

