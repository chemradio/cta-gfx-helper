from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/")
async def temp_form():
    """Unused at the moment"""
    with open("./base_html/index.html") as index_html:
        data = index_html.read()
    return Response(content=data, media_type="text/html")
