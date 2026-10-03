from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from ..dependencies import get_current_user
from ..models import User


router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request},
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request},
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"request": request},
    )


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "user": user,
        },
    )


@router.get("/history-page", response_class=HTMLResponse)
def history_page(
    request: Request,
    user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "request": request,
            "user": user,
        },
    )


@router.get("/planner/{planner}", response_class=HTMLResponse)
def planner_page(
    request: Request,
    planner: str,
    user: User = Depends(get_current_user),
):
    if planner not in {"home", "party", "jewelry"}:
        return RedirectResponse(url="/")

    return templates.TemplateResponse(
        request=request,
        name="planner.html",
        context={
            "request": request,
            "planner": planner,
            "user": user,
        },
    )


@router.get(
    "/recommendations/{recommendation_id}",
    response_class=HTMLResponse,
)
def recommendations_page(
    request: Request,
    recommendation_id: int,
    user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(
        request=request,
        name="recommendations.html",
        context={
            "request": request,
            "recommendation_id": recommendation_id,
            "user": user,
        },
    )