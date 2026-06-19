from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any

from services.ats_service import ATSService
from services.workflow_service import WorkflowService
from auth.security import verify_token

router = APIRouter()
from services.workflow_service import WorkflowService

workflow_service = WorkflowService()

@router.post("/analyze")
async def analyze_candidates(
    user=Depends(verify_token)
):
    try:

        result = await workflow_service.process()

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )