from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.session import get_db
from app.models.user import User
from app.core.response import success_response

router = APIRouter(tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(payload: dict, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.get("email")).first()

    # ❌ duplicate user fix
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(payload.get("password"))

    user = User(
        email=payload.get("email"),
        hashed_password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return success_response(
        data={"id": user.id, "email": user.email},
        message="User registered successfully"
    )