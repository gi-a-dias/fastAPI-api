
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI(title="Items API")

# Dados de exemplo armazenados em memória
items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"}
]


# Modelo dos dados recebidos pela API
class ItemIn(BaseModel):
    name: str


# Procura um item pelo ID
def find_item(item_id: int):
    return next(
        (item for item in items if item["id"] == item_id),
        None
    )


# Redireciona a página inicial para a documentação Swagger
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


# GET - Listar todos os itens
@app.get("/items")
def get_items():
    return {"items": items}


# GET - Buscar um item pelo ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = find_item(item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {"item": item}


# POST - Criar um novo item
@app.post("/items", status_code=201)
def create_item(payload: ItemIn):
    new_id = max(
        (item["id"] for item in items),
        default=0
    ) + 1

    new_item = {
        "id": new_id,
        "name": payload.name
    }

    items.append(new_item)

    return {"item": new_item}


# PUT - Atualizar um item existente
@app.put("/items/{item_id}")
def update_item(item_id: int, payload: ItemIn):
    item = find_item(item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    item["name"] = payload.name

    return {"item": item}


# DELETE - Excluir um item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    item = find_item(item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    items.remove(item)

    return {"result": True}
