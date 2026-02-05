from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="Restaurant Management System")

class Dish(BaseModel):
    id: str
    name: str
    price: float

class OrderItem(BaseModel):
    dish_id: str
    quantity: int

class Order(BaseModel):
    id: str
    items: List[OrderItem]
    total: Optional[float] = None

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
DISH_FILE = os.path.join(DATA_DIR, "dishes.txt")
ORDER_FILE = os.path.join(DATA_DIR, "orders.txt")

for file in [DISH_FILE, ORDER_FILE]:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            pass

@app.post("/dishes", response_model=Dish)
def add_dish(dish: Dish):
    with open(DISH_FILE, 'r+', encoding='utf-8') as f:
        lines = f.read().splitlines()
        for line in lines:
            if line.startswith(f"{dish.id},"):
                raise HTTPException(status_code=400, detail="Dish ID already exists")
        f.write(f"{dish.id},{dish.name},{dish.price}\n")
    return dish

@app.get("/dishes", response_model=List[Dish])
def get_dishes():
    dishes = []
    with open(DISH_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            did, name, price = line.strip().split(',')
            dishes.append(Dish(id=did, name=name, price=float(price)))
    return dishes

@app.post("/orders", response_model=Order)
def create_order(order: Order):
    dish_list = get_dishes()
    dish_map = {d.id: d.price for d in dish_list}
    total = 0.0
    for item in order.items:
        if item.dish_id not in dish_map:
            raise HTTPException(status_code=404, detail=f"Dish {item.dish_id} not found")
        total += dish_map[item.dish_id] * item.quantity
    order.total = round(total, 2)
    with open(ORDER_FILE, 'a', encoding='utf-8') as f:
        item_str = ';'.join([f"{i.dish_id}:{i.quantity}" for i in order.items])
        f.write(f"{order.id},{item_str},{order.total}\n")
        return order

@app.get("/orders", response_model=List[Order])
def get_orders():
    orders = []
    with open(ORDER_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            oid, items_str, total = line.strip().split(',')
            items = []
            for s in items_str.split(';'):
                did, q = s.split(':')
                items.append(OrderItem(dish_id=did, quantity=int(q)))
            orders.append(Order(id=oid, items=items, total=float(total)))
    return orders

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)