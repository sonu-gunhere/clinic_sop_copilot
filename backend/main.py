from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from backend.routers import assistant, sop, web, cite

app = FastAPI(title="Clinic SOP Copilot")

# Mount static + templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Include routers
app.include_router(sop.router, prefix="/sop", tags=["SOP"])
app.include_router(web.router, prefix="/web", tags=["Web"])
app.include_router(cite.router, prefix="/cite", tags=["Citation"])
app.include_router(assistant.router, prefix="/assistant", tags=["Assistant"])


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
