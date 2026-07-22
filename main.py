from fastapi import FastAPI
import uvicorn

from auth.router import router
from users.users_router import user_router
from products.product_router import product_router
from cartitems.basket_router import b_router



app = FastAPI()

app.include_router(router=router)
app.include_router(router=product_router)
app.include_router(router=user_router)
app.include_router(router=b_router)


@app.get("/")
async def root():
    return {
        "message": "hello"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)