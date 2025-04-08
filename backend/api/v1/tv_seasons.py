from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from services.tv_season_service import get_tv_season_service, TVSeasonService
from models.tv_season import TVSeason, TVSeasonCreate, TVSeasonUpdate

router = APIRouter(prefix="/tv-seasons", tags=["tv-seasons"])

@router.post("/", response_model=TVSeason)
async def create_tv_season(tv_season: TVSeasonCreate, tv_season_service: TVSeasonService = Depends(get_tv_season_service)):
    return await tv_season_service.create_tv_season(tv_season)

@router.get("/{tv_season_id}", response_model=TVSeason)
async def get_tv_season(tv_season_id: str, tv_season_service: TVSeasonService = Depends(get_tv_season_service)):
    tv_season = await tv_season_service.get_tv_season(tv_season_id)
    if not tv_season:
        raise HTTPException(status_code=404, detail="TV season not found")
    return tv_season

@router.get("/show/{show_id}", response_model=List[TVSeason])
async def get_tv_seasons_by_show(
    show_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    tv_season_service: TVSeasonService = Depends(get_tv_season_service)
):
    return await tv_season_service.get_tv_seasons_by_show(show_id, skip=skip, limit=limit)

@router.put("/{tv_season_id}", response_model=TVSeason)
async def update_tv_season(
    tv_season_id: str,
    tv_season: TVSeasonUpdate,
    tv_season_service: TVSeasonService = Depends(get_tv_season_service)
):
    updated_tv_season = await tv_season_service.update_tv_season(tv_season_id, tv_season)
    if not updated_tv_season:
        raise HTTPException(status_code=404, detail="TV season not found")
    return updated_tv_season

@router.delete("/{tv_season_id}")
async def delete_tv_season(tv_season_id: str, tv_season_service: TVSeasonService = Depends(get_tv_season_service)):
    success = await tv_season_service.delete_tv_season(tv_season_id)
    if not success:
        raise HTTPException(status_code=404, detail="TV season not found")
    return {"message": "TV season deleted successfully"} 