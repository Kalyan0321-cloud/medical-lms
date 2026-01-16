"""
Create a demo tenant and user for testing
Command: python create_demo_user.py
"""

from app.database import SessionLocal
from app.models import Tenant, User, UserRole
from app.auth import hash_password
import uuid

db = SessionLocal()

print("Creating demo data...\n")

# Create demo tenant (College)
tenant = Tenant(
    id=uuid.uuid4(),
    name="Demo Medical College",
    domain="demo.medlms.com",
    is_active=True
)
db.add(tenant)
db.commit()
print(f"✅ Tenant created: {tenant.name}")

# Create demo student
student = User(
    id=uuid.uuid4(),
    tenant_id=tenant.id,
    email="student@demo.com",
    password_hash=hash_password("password123"),
    full_name="Demo Student",
    role=UserRole.STUDENT,
    is_active=True
)
db.add(student)
db.commit()
print(f"✅ Student created: {student.email}")

# Create demo faculty
faculty = User(
    id=uuid.uuid4(),
    tenant_id=tenant.id,
    email="faculty@demo.com",
    password_hash=hash_password("password123"),
    full_name="Demo Faculty",
    role=UserRole.FACULTY,
    is_active=True
)
db.add(faculty)
db.commit()
print(f"✅ Faculty created: {faculty.email}")

print("\n🎉 Demo data created successfully!")
print("\nYou can login with:")
print("Email: student@demo.com")
print("Password: password123")
print("\nOr:")
print("Email: faculty@demo.com")
print("Password: password123")

db.close()