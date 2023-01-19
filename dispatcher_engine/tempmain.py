from fastapi import FastAPI, Response

from api_routers import add_order_react

app = FastAPI()
app.include_router(add_order_react.router, prefix="/react")


@app.get("/")
async def read_root():
    """Unused at the moment"""
    with open("./base_html/index.html") as index_html:
        data = index_html.read()
    return Response(content=data, media_type="text/html")
