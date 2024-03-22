from fastapi import APIRouter, Request
from app.emailscrapper.ghc_email_scrapper import ghc_open_shift_scraping, ghc_shifts_json
from app.config import schemas  
import json

sub_router = APIRouter()

@sub_router.post("/id-medical/api/v1/ghc/openShifts")
def ghcShifts(ghcScema:schemas.GHCSchema, headers:Request ):
    resp = ghc_shifts_json()
    resp = json.loads(resp)
    return resp 