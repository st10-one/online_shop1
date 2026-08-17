from fastapi import FastAPI
import uvicorn

from auth.router import router
from users.users_router import user_router
from products.product_router import product_router
from orders.orders_router import orders_router
from cartitems.cartitems_router import b_router
from admin.admin_router import a_router


app = FastAPI(title="Online Shop")

app.include_router(router=router)
app.include_router(router=product_router)
app.include_router(router=user_router)
app.include_router(router=b_router)
app.include_router(router=orders_router)
app.include_router(router=a_router)


@app.get("/")
async def root():
    return {
        "message": "hello"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)