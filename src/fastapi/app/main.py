from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, relationship, declarative_base
import uuid
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/shopping_list.db") 
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ShoppingList(Base):
    __tablename__ = "shopping_lists"
    id = Column(String, primary_key=True, index=True)
    items = relationship("Item", back_populates="shopping_list", cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = "items"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    shopping_list_id = Column(String, ForeignKey("shopping_lists.id"))
    shopping_list = relationship("ShoppingList", back_populates="items")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create-list")
def create_list(db: Session = Depends(get_db)):
    new_list = ShoppingList(id=str(uuid.uuid4()))
    db.add(new_list)
    db.commit()
    return {"list_id": new_list.id}

@app.get("/list/{list_id}/items")
def get_items(list_id: str, db: Session = Depends(get_db)):
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping List not found")
    print(shopping_list.items)
    return [{"name": x.name, "id": x.id} for x in shopping_list.items]

@app.post("/list/{list_id}/add-item")
def add_item(list_id: str, name: str, db: Session = Depends(get_db)):
    shopping_list = db.query(ShoppingList).filter(ShoppingList.id == list_id).first()
    if not shopping_list:
        raise HTTPException(status_code=404, detail="Shopping List not found")
    new_item = Item(id=str(uuid.uuid4()), name=name, shopping_list_id=list_id)
    db.add(new_item)
    db.commit()
    return {"message": "Item added"}

@app.delete("/list/{list_id}/delete-item/{item_id}")
def delete_item(list_id: str, item_id: str, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id, Item.shopping_list_id == list_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}

# PWA Service Worker
@app.get("/service-worker.js")
def service_worker(request: Request):
    return templates.TemplateResponse("service_worker.js", {"request": request}, media_type="application/javascript")
