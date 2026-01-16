from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.models import User
from app.auth import get_current_user, verify_password, hash_password

router = APIRouter(prefix="/users", tags=["Users"])


# Request/Response models
class UpdateProfileRequest(BaseModel):
    phone: Optional[str] = None
    bio: Optional[str] = None


class ProfileResponse(BaseModel):
    id: str
    full_name: str
    email: str
    phone: Optional[str]
    bio: Optional[str]


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


# 1. PUT /users/profile - Update user profile
@router.put("/profile", response_model=ProfileResponse)
def update_profile(
    profile_data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update phone and bio of current user
    """
    # Update phone if provided
    if profile_data.phone is not None:
        current_user.phone = profile_data.phone
    
    # Update bio if provided
    if profile_data.bio is not None:
        current_user.bio = profile_data.bio
    
    # Save changes to database
    db.commit()
    db.refresh(current_user)
    
    return ProfileResponse(
        id=str(current_user.id),
        full_name=current_user.full_name,
        email=current_user.email,
        phone=current_user.phone,
        bio=current_user.bio
    )


# 2. PUT /users/change-password - Change password
@router.put("/change-password")
def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    """
    # Check if current password is correct
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Hash new password
    new_password_hash = hash_password(password_data.new_password)
    
    # Update password
    current_user.password_hash = new_password_hash
    
    # Save to database
    db.commit()
    
    return {"message": "Password changed successfully"}