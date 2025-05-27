from fastapi import FastAPI, Request, Form, Depends, HTTPException, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, StudentID, aboutBooks, Transaction, Fine
from sqlalchemy import func, cast, Date, distinct, extract
from datetime import date, timedelta, datetime
from fastapi.responses import JSONResponse
from decimal import Decimal
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

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

#---------------------------------DashBoard/Home--------------------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    session = SessionLocal()
    count = session.query(aboutBooks).count()
    return_count = session.query(func.count(Transaction.transaction_id)).filter(Transaction.return_date == None).scalar()
    total_amt_unpaid = session.query(func.sum(Fine.amount)).filter(Fine.paid_status == 'Not Paid').scalar()
    today = date.today()
    book_add_count = session.query(func.count(aboutBooks.book_id)).filter(cast(aboutBooks.added_at, Date) == today).scalar()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)          # Sunday
    
    week_borrowed_count = session.query(func.count(distinct(Transaction.user_id)))\
        .filter(Transaction.issue_date >= start_of_week)\
        .filter(Transaction.issue_date <= end_of_week)\
        .scalar()


    session.close()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,"book_count": count,"returned_books_count": return_count, "total_unpaid": total_amt_unpaid, "Book_added" : book_add_count, "book_per_week" : week_borrowed_count 
    })
    

@app.post("/issue-book")
async def issue_book(
    user_id: str = Form(...),
    book_id: int = Form(...),
    issue_date: date = Form(...),
    due_date: date = Form(...),
    db: Session = Depends(get_db)
):
    try:
        new_transaction = Transaction(
            user_id=user_id,
            book_id=book_id,
            issue_date=issue_date,
            due_date=due_date,
            return_date=None
        )
        
        db.add(new_transaction)
        db.commit()

        db.refresh(new_transaction)
        transaction_id = new_transaction.transaction_id

        return JSONResponse(
            content={
                "success": True,
                "message": f"Transaction Success!! Your Transaction ID is {transaction_id}!"
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": "BookID/ UserID is Wrong "},
            status_code=400
        )
    
#------------------Fine status update from manage Fine Management----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/return_book")
async def return_books(
    transaction_id = Form(...),
    return_date: date = Form(...),
    db: Session = Depends(get_db)
    ):
    try:
        transaction = db.query(Transaction).filter(
            Transaction.transaction_id == transaction_id
        ).first()

        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction_ID not found")

        transaction.return_date = return_date

        db.commit()
        fine_amount = Decimal(0)
        if return_date > transaction.due_date:
            days_overdue = (return_date - transaction.due_date).days
            fine_amount = Decimal(days_overdue * 5)

            new_fine = Fine(
                transaction_id=transaction_id,
                amount=fine_amount,
                paid_status='Not Paid'
            )
            db.add(new_fine)
            db.commit()
        
        return JSONResponse(
            content={"success": True, "message": "Book return successfully!! Fine: {0}".format(fine_amount)}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            content={"success": False, "message": "Invalid TransactionID"},
            status_code=400
        )

# @app.get("/test")
# def test():
#     print("DEBUG: Test route worked!")  # Check terminal
#     session = SessionLocal()
#     count = session.query(aboutBooks).count()
#     issued_books_count = session.query(func.count(Transaction.transaction_id)).filter(Transaction.return_date == None).scalar()

#     session.close()
#     print("Books not return Count: ", issued_books_count)
#     return {"Books not return: ": issued_books_count}

@app.get("/books", response_class= HTMLResponse)
def booksDetail(request: Request):
    return templates.TemplateResponse("books.html", {"request": request})

@app.get("/users", response_class= HTMLResponse)
def usersDetail(request: Request):
    return templates.TemplateResponse("users.html", {"request": request})

#----------------------------- Manage Books-----------------------------------------------------------
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    category: str
    publisher: str
    quantity: int

class BookResponse(BookCreate):
    book_id: int
    added_at: datetime

@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate):
    db = SessionLocal()
    try:
        db_book = aboutBooks(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

# Update your read_books endpoint for better error reporting
@app.get("/books/", response_model=list[BookResponse])
def read_books():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1")).fetchall()
        books = db.query(aboutBooks).all()
        return books
    except Exception as e:
        print(f"Database error: {str(e)}")  # Check terminal for actual error
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )
    finally:
        db.close()

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    db = SessionLocal()
    book = db.query(aboutBooks).filter(aboutBooks.book_id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    try:
        db.delete(book)
        db.commit()
        return {"message": "Book deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()