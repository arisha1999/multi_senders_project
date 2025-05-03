from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_items():
    return [{"id": 1, "name": "Item A"}, {"id": 2, "name": "Item B"}]

@router.get("/{item_id}")
def get_item(item_id: int):
    return {"id": item_id, "name": f"Item {item_id}"}
