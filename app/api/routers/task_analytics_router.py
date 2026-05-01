from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user
from app.core.response import success_response

from app.services import task_service


router = APIRouter(tags=["Analytics"])


# ✅ NO trailing slash, NO prefix issues
@router.get("/analytics")
def get_task_analytics(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    analytics = task_service.get_task_analytics(db, current_user.id)

    return success_response(
        data=analytics,
        message="Task analytics fetched successfully"
    )