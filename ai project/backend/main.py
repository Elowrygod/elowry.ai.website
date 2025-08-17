from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def get_zapros():
    return {"hellow: world"}

items =  {
    1: {"item1":" 1"},
    2: {"item2":" 2"},
    3: {"item3":" 3"},   
}

@app.get("/item/{item_id}")
def get_item(item_id: int):
    item = items.get(item_id)

    if item is None:
        return {"error"}, 404
    return item