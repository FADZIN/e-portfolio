from sqlalchemy import Column, Integer, String, Text
from database import Base

# Requirement: Personal Information & Objective
class PersonalInfo(Base):
    __tablename__ = "personal_info"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    objective = Column(Text)
    profile_pic = Column(String(255))
    about_me = Column(Text)  # Add this line

# Requirement: Education (The one causing the error)
class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String(255))
    year = Column(String(100))
    description = Column(Text)

# Requirement: Skills
class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    level = Column(String(50))

# Add these as well to avoid future errors:
class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(255))
    position = Column(String(255))
    duration = Column(String(100))
    description = Column(Text)  # Add this line!

class Award(Base):
    __tablename__ = "awards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    year = Column(Integer)  # Ensure this line exists!

class Reference(Base):
    __tablename__ = "references"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    contact = Column(String(255))
    relationship = Column(String(255))  # <--- THIS LINE IS MISSING OR TYPOED