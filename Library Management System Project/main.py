from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, StudentID
from passlib.hash import bcrypt

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "error": None})

@app.get("/login", response_class=HTMLResponse)
def admin_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/sLogin", response_class=HTMLResponse)
def user_login(request: Request):
    return templates.TemplateResponse("sLogin.html", {"request": request})

@app.post("/sLogin", response_class=HTMLResponse)
def login(request: Request, user_id: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    std = db.query(StudentID).filter(StudentID.user_id == user_id, StudentID.password == password).first()
    if std:
        return RedirectResponse("/landing_page", status_code=HTTP_302_FOUND)
    return templates.TemplateResponse("sLogin.html", {"request": request, "error": "Invalid username or password"})

@app.get("/landing_page", response_class=HTMLResponse)
def LandingPage(request: Request):
    return templates.TemplateResponse("landing_page.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if user:
        return RedirectResponse("/dashboard", status_code=HTTP_302_FOUND)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})



@app.get("/books", response_class= HTMLResponse)
def booksDetail(request: Request):
    return templates.TemplateResponse("books.html", {"request": request})

@app.get("/users", response_class= HTMLResponse)
def usersDetail(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})

