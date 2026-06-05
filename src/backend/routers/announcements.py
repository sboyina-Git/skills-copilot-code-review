"""
Announce management endpoints for the High School Management System API
"""

from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from ..database import announcements_collection, teachers_collection

router = APIRouter(
    prefix="/announcements",
    tags=["announcements"]
)


def validate_teacher(teacher_username: Optional[str]) -> None:
    if not teacher_username:
        raise HTTPException(status_code=401, detail="Authentication required for this action")

    teacher = teachers_collection.find_one({"_id": teacher_username})
    if not teacher:
        raise HTTPException(status_code=401, detail="Invalid teacher credentials")


class AnnouncementPayload(BaseModel):
    message: str = Field(..., min_length=5)
    expiration_date: str
    start_date: Optional[str] = None


def parse_date_field(date_value: Optional[str], field_name: str) -> Optional[str]:
    if date_value is None or date_value == "":
        return None
    try:
        datetime.fromisoformat(date_value)
        return date_value
    except ValueError:
        raise HTTPException(status_code=400, detail=f"{field_name} must be a valid YYYY-MM-DD date")


def build_announcement_response(announcement: Dict[str, Any]) -> Dict[str, Any]:
    announcement_id = announcement.get("_id")
    return {"id": announcement_id, **{k: v for k, v in announcement.items() if k != "_id"}}


@router.get("", response_model=List[Dict[str, Any]])
def get_announcements(active: Optional[bool] = False) -> List[Dict[str, Any]]:
    query = {}

    if active:
        today = datetime.utcnow().date().isoformat()
        query["expiration_date"] = {"$gte": today}
        query["$or"] = [
            {"start_date": {"$lte": today}},
            {"start_date": {"$exists": False}},
            {"start_date": None},
            {"start_date": ""}
        ]

    announcements = []
    for announcement in announcements_collection.find(query).sort("expiration_date", 1):
        announcements.append(build_announcement_response(announcement))

    return announcements


@router.post("", response_model=Dict[str, Any])
def create_announcement(payload: AnnouncementPayload, teacher_username: Optional[str] = Query(None)) -> Dict[str, Any]:
    validate_teacher(teacher_username)

    expiration_date = parse_date_field(payload.expiration_date, "Expiration date")
    start_date = parse_date_field(payload.start_date, "Start date")

    now = datetime.utcnow().isoformat()
    announcement_id = str(uuid.uuid4())

    announcement = {
        "_id": announcement_id,
        "message": payload.message.strip(),
        "expiration_date": expiration_date,
        "start_date": start_date,
        "created_at": now,
        "updated_at": now,
    }

    announcements_collection.insert_one(announcement)
    return build_announcement_response(announcement)


@router.put("/{announcement_id}", response_model=Dict[str, Any])
def update_announcement(announcement_id: str, payload: AnnouncementPayload, teacher_username: Optional[str] = Query(None)) -> Dict[str, Any]:
    validate_teacher(teacher_username)

    expiration_date = parse_date_field(payload.expiration_date, "Expiration date")
    start_date = parse_date_field(payload.start_date, "Start date")

    announcement = announcements_collection.find_one({"_id": announcement_id})
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    result = announcements_collection.update_one(
        {"_id": announcement_id},
        {
            "$set": {
                "message": payload.message.strip(),
                "expiration_date": expiration_date,
                "start_date": start_date,
                "updated_at": datetime.utcnow().isoformat(),
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Announcement not found")

    announcement = announcements_collection.find_one({"_id": announcement_id})
    return build_announcement_response(announcement)


@router.delete("/{announcement_id}")
def delete_announcement(announcement_id: str, teacher_username: Optional[str] = Query(None)) -> Dict[str, Any]:
    validate_teacher(teacher_username)

    result = announcements_collection.delete_one({"_id": announcement_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Announcement not found")

    return {"message": "Announcement deleted"}
