from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body, FastAPI
from mysql.connector import connect, Error
from config.cors import origins
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
    allow_origins=origins,
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

# # save item to cart
# @app.post("/cart/add")
# async def get_one_design(design_id: int) -> DesignBaseModel:
#     with sql.cursor() as db_connection:
#         return get_design(sql.cursor(buffered=True), sql.cursor(buffered=True), design_id, False)