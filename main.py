from fastapi import FastAPI, Request, Depends, Form, responses
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
import shutil
import os
from fastapi import File, UploadFile

app = FastAPI()

# Creates tables in MySQL
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 1. PERSONAL INFO (Home Page) ---
@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    personal = db.query(models.PersonalInfo).first()
    return templates.TemplateResponse("index.html", {"request": request, "personal": personal})

# --- 2. PROFESSIONAL OBJECTIVE ---
@app.get("/objective")
def view_objective(request: Request, db: Session = Depends(get_db)):
    personal = db.query(models.PersonalInfo).first()
    return templates.TemplateResponse("objective.html", {"request": request, "personal": personal})

# --- 3. EDUCATION ---
@app.get("/education")
def view_education(request: Request, db: Session = Depends(get_db)):
    education = db.query(models.Education).all()
    return templates.TemplateResponse("education.html", {"request": request, "education": education})

# --- 4. WORK EXPERIENCE ---
@app.get("/experience")
def view_experience(request: Request, db: Session = Depends(get_db)):
    experience = db.query(models.Experience).all()
    return templates.TemplateResponse("experience.html", {"request": request, "experience": experience})

# --- 5. AWARDS & HONOURS ---
@app.get("/awards")
def view_awards(request: Request, db: Session = Depends(get_db)):
    awards = db.query(models.Award).all()
    return templates.TemplateResponse("awards.html", {"request": request, "awards": awards})

# --- 6. SKILLS ---
@app.get("/skills")
def view_skills(request: Request, db: Session = Depends(get_db)):
    skills = db.query(models.Skill).all()
    return templates.TemplateResponse("skills.html", {"request": request, "skills": skills})

# --- 7. REFERENCES ---
@app.get("/references")
def view_references(request: Request, db: Session = Depends(get_db)):
    references = db.query(models.Reference).all()
    return templates.TemplateResponse("references.html", {"request": request, "references": references})

# --- LOGIN PAGE ---
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# --- LOGIN ACTION ---
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    # You can change 'admin' and '1234' to whatever you like
    if username == "admin" and password == "12345":
        response = responses.RedirectResponse(url="/admin", status_code=303)
        # We set a simple cookie to 'remember' the login
        response.set_cookie(key="is_logged_in", value="true")
        return response
    else:
        return responses.RedirectResponse(url="/login?error=Invalid+Credentials", status_code=303)

# --- LOGOUT ACTION ---
@app.get("/logout")
def logout():
    # Create a redirect response back to the home page
    response = responses.RedirectResponse(url="/", status_code=303)
    # Delete the login cookie to lock the admin panel
    response.delete_cookie(key="is_logged_in")
    return response

# --- UPDATED ADMIN PROTECTOR ---
@app.get("/admin")
def admin_page(request: Request, db: Session = Depends(get_db)):
    # Check if the user has the 'logged_in' cookie
    if request.cookies.get("is_logged_in") != "true":
        return responses.RedirectResponse(url="/login")
        
    return templates.TemplateResponse("admin.html", {
        "request": request, 
        "personal": db.query(models.PersonalInfo).first(), 
        "skills": db.query(models.Skill).all(),
        "education": db.query(models.Education).all(),
        "experience": db.query(models.Experience).all(),
        "awards": db.query(models.Award).all(),
        "references": db.query(models.Reference).all()
    })

# --- CRUD OPERATIONS (ADD) ---
@app.post("/admin/personal/update")
async def update_personal(
    name: str = Form(...), 
    obj: str = Form(...), 
    email: str = Form(...), 
    phone: str = Form(...), 
    address: str = Form(...), 
    about_me: str = Form(...), # Add this parameter
    profile_pic: UploadFile = File(None), # Add this
    db: Session = Depends(get_db)
):
    personal = db.query(models.PersonalInfo).first()
    filename = personal.profile_pic if personal else None

    # Handle file upload
    if profile_pic and profile_pic.filename:
        filename = profile_pic.filename
        file_path = os.path.join("static/images", filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(profile_pic.file, buffer)

    if not personal:
        personal = models.PersonalInfo(full_name=name, objective=obj, email=email, phone=phone, address=address, about_me=about_me, profile_pic=filename)
        db.add(personal)
    else:
        personal.full_name, personal.objective, personal.email, personal.phone, personal.address, personal.about_me, personal.profile_pic = name, obj, email, phone, address, about_me, filename
        
    db.commit()
    return responses.RedirectResponse(url="/admin#personal", status_code=303)

# --- UPDATE EDUCATION ---
@app.post("/admin/education/update/{edu_id}")
def update_education(edu_id: int, institution: str = Form(...), year: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    edu = db.query(models.Education).filter(models.Education.id == edu_id).first()
    if edu:
        edu.institution, edu.year, edu.description = institution, year, description
        db.commit()
    return responses.RedirectResponse(url="/admin#education", status_code=303)

# --- UPDATE EXPERIENCE ---
@app.post("/admin/experience/update/{exp_id}")
def update_experience(exp_id: int, company: str = Form(...), position: str = Form(...), duration: str = Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    exp = db.query(models.Experience).filter(models.Experience.id == exp_id).first()
    if exp:
        exp.company, exp.position, exp.duration, exp.description = company, position, duration, description
        db.commit()
    return responses.RedirectResponse(url="/admin#experience", status_code=303)

# --- UPDATE SKILL ---
@app.post("/admin/skill/update/{skill_id}")
def update_skill(skill_id: int, name: str = Form(...), level: str = Form(...), db: Session = Depends(get_db)):
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if skill:
        skill.name, skill.level = name, level
        db.commit()
    return responses.RedirectResponse(url="/admin#skills", status_code=303)

# --- UPDATE AWARD ---
@app.post("/admin/award/update/{award_id}")
def update_award(award_id: int, title: str = Form(...), year: str = Form(...), db: Session = Depends(get_db)):
    award = db.query(models.Award).filter(models.Award.id == award_id).first()
    if award:
        award.title = title
        award.year = year
        db.commit()
    return responses.RedirectResponse(url="/admin#awards", status_code=303)

# --- UPDATE REFERENCE ---
@app.post("/admin/reference/update/{ref_id}")
def update_reference(ref_id: int, name: str = Form(...), contact: str = Form(...), relationship: str = Form(...), db: Session = Depends(get_db)):
    ref = db.query(models.Reference).filter(models.Reference.id == ref_id).first()
    if ref:
        ref.name = name
        ref.contact = contact
        ref.relationship = relationship
        db.commit()
    return responses.RedirectResponse(url="/admin#references", status_code=303)

@app.post("/admin/skill/add")
def add_skill(name: str = Form(...), level: str = Form(...), db: Session = Depends(get_db)):
    db.add(models.Skill(name=name, level=level))
    db.commit()
    return responses.RedirectResponse(url="/admin#skills", status_code=303)

@app.post("/admin/education/add")
def add_education(institution: str = Form(...), year: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    db.add(models.Education(institution=institution, year=year, description=description))
    db.commit()
    return responses.RedirectResponse(url="/admin#education", status_code=303)

@app.post("/admin/experience/add")
def add_experience(company: str = Form(...), position: str = Form(...), duration: str = Form(...), description: str = Form(None), db: Session = Depends(get_db)):
    new_exp = models.Experience(company=company, position=position, duration=duration, description=description)
    db.add(new_exp)
    db.commit()
    return responses.RedirectResponse(url="/admin#experience", status_code=303)

@app.post("/admin/award/add")
def add_award(title: str = Form(...), year: str = Form(...), db: Session = Depends(get_db)):
    db.add(models.Award(title=title, year=year))
    db.commit()
    return responses.RedirectResponse(url="/admin#awards", status_code=303)

@app.post("/admin/reference/add")
def add_reference(
    name: str = Form(...), 
    contact: str = Form(...), 
    relationship: str = Form(...), 
    db: Session = Depends(get_db)
):
    # 'relationship' here must match 'relationship' in models.py
    new_ref = models.Reference(name=name, contact=contact, relationship=relationship)
    db.add(new_ref)
    db.commit()
    return responses.RedirectResponse(url="/admin#references", status_code=303)

# --- CRUD OPERATIONS (DELETE) ---
@app.get("/admin/skill/delete/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(models.Skill).get(skill_id)
    if skill: db.delete(skill); db.commit()
    return responses.RedirectResponse(url="/admin#skills", status_code=303)

@app.get("/admin/education/delete/{edu_id}")
def delete_education(edu_id: int, db: Session = Depends(get_db)):
    edu = db.query(models.Education).get(edu_id)
    if edu: db.delete(edu); db.commit()
    return responses.RedirectResponse(url="/admin#education", status_code=303)

@app.get("/admin/experience/delete/{exp_id}")
def delete_experience(exp_id: int, db: Session = Depends(get_db)):
    exp = db.query(models.Experience).get(exp_id)
    if exp: db.delete(exp); db.commit()
    return responses.RedirectResponse(url="/admin#experience", status_code=303)

@app.get("/admin/award/delete/{award_id}")
def delete_award(award_id: int, db: Session = Depends(get_db)):
    award = db.query(models.Award).get(award_id)
    if award: db.delete(award); db.commit()
    return responses.RedirectResponse(url="/admin#awards", status_code=303)

@app.get("/admin/reference/delete/{ref_id}")
def delete_reference(ref_id: int, db: Session = Depends(get_db)):
    ref = db.query(models.Reference).get(ref_id)
    if ref: db.delete(ref); db.commit()
    return responses.RedirectResponse(url="/admin#references", status_code=303)

@app.get("/report")
def generate_report(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("report.html", {
        "request": request,
        "personal": db.query(models.PersonalInfo).first(),
        "education": db.query(models.Education).all(),
        "experience": db.query(models.Experience).all(),
        "awards": db.query(models.Award).all(),
        "skills": db.query(models.Skill).all(),
        "references": db.query(models.Reference).all()
    })