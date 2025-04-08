from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from services.tv_show_service import get_tv_show_service, TVShowService
from models.tv_show import TVShow, TVShowCreate, TVShowUpdate

router = APIRouter(prefix="/tv-shows", tags=["tv-shows"])

@router.post("/", response_model=TVShow)
async def create_tv_show(tv_show: TVShowCreate, tv_show_service: TVShowService = Depends(get_tv_show_service)):
    return await tv_show_service.create_tv_show(tv_show)

@router.get("/{tv_show_id}", response_model=TVShow)
async def get_tv_show(tv_show_id: str, tv_show_service: TVShowService = Depends(get_tv_show_service)):
    tv_show = await tv_show_service.get_tv_show(tv_show_id)
    if not tv_show:
        raise HTTPException(status_code=404, detail="TV show not found")
    return tv_show

@router.get("/", response_model=List[TVShow])
async def get_tv_shows(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    title: Optional[str] = None,
    status: Optional[str] = None,
    tv_show_service: TVShowService = Depends(get_tv_show_service)
):
    return await tv_show_service.get_tv_shows(skip=skip, limit=limit, title=title, status=status)

@router.put("/{tv_show_id}", response_model=TVShow)
async def update_tv_show(
    tv_show_id: str,
    tv_show: TVShowUpdate,
    tv_show_service: TVShowService = Depends(get_tv_show_service)
):
    updated_tv_show = await tv_show_service.update_tv_show(tv_show_id, tv_show)
    if not updated_tv_show:
        raise HTTPException(status_code=404, detail="TV show not found")
    return updated_tv_show

@router.delete("/{tv_show_id}")
async def delete_tv_show(tv_show_id: str, tv_show_service: TVShowService = Depends(get_tv_show_service)):
    success = await tv_show_service.delete_tv_show(tv_show_id)
    if not success:
        raise HTTPException(status_code=404, detail="TV show not found")
    return {"message": "TV show deleted successfully"} 