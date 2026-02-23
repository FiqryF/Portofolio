from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from projects import router as projects_router
from hero import router as hero_router
from about import router as about_router
from skills import router as skills_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(projects_router, prefix="/api/projects")
app.include_router(hero_router, prefix="/api/hero")
app.include_router(about_router, prefix="/api/about")
app.include_router(skills_router, prefix="/api/skills")

@app.get("/")
def root():
    return {"message": "Backend running"}
