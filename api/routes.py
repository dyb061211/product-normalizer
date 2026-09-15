from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
import tempfile
from pathlib import Path
from product_normalizer.service import process_product_files
from product_normalizer.repository import get_runs,get_run,get_run_issues
from ai.listing_service import generate_listing
from ai.schemas import GeneratedListing,ProductInput,AgentRequest,AgentResponse
from ai.agent_service import run_agent
from api.schemas import RAGQueryRequest
from product_normalizer.rag.schemas import RAGResponse
from product_normalizer.rag.service import answer_question

router = APIRouter()

@router.get("/health")
def is_health():
    return {"status": "ok"}

@router.post(
    "/normalize",
    responses={
        400: {"description": "Invalid input file"}
    }
)
async def normalize(
        upc_file:UploadFile=File(...),
        products_file:UploadFile=File(...),
):
    if not upc_file.filename or not products_file.filename:
        raise HTTPException(
            status_code=400,
            detail="上传文件必须包含文件名"
        )
    if not upc_file.filename.lower().endswith(".xlsx") or not products_file.filename.lower().endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="文件必须是xlsx"
        )
    upc_content=await upc_file.read()
    products_content=await products_file.read()
    tmp_dir = tempfile.TemporaryDirectory()
    try:
        tmp_path = Path(tmp_dir.name)
        upc_path = tmp_path / "upc.xlsx"
        products_path = tmp_path / "products.xlsx"
        output_path = tmp_path / "standardized_products.xlsx"
        validation_report_path = tmp_path / "validation_report.xlsx"
        upc_path.write_bytes(upc_content)
        products_path.write_bytes(products_content)
        process_product_files(upc_path, products_path, output_path, validation_report_path,'api',upc_filename=upc_file.filename,products_filename=products_file.filename)
        return FileResponse(
            output_path,
            filename="standardized_products.xlsx",
            background=BackgroundTask(tmp_dir.cleanup)
        )
    except Exception:
        tmp_dir.cleanup()
        raise

@router.get("/runs")
def list_runs(limit:int=10):
    rows=get_runs(limit)
    return rows

@router.get("/run/{run_id}")
def get_run_detail(run_id:int):
    row=get_run(run_id)
    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Run not found"
        )
    return row

@router.get("/runs/{run_id}/issues")
def get_run_issues_list(run_id:int):
    run=get_run(run_id)
    if run is None:
        raise HTTPException(
            status_code=404,
            detail="Run not found"
        )
    return get_run_issues(run_id)

@router.post("/generate-listing",response_model=GeneratedListing)
def generate_listing_api(product:ProductInput):
    listing=generate_listing(product)
    return listing

@router.post("/assistant",response_model=AgentResponse)
def assistant_api(request:AgentRequest):
    answer=run_agent(request.message)
    return AgentResponse(answer=answer)

@router.post("/rag/query",response_model=RAGResponse)
def rag_query(request:RAGQueryRequest)->RAGResponse:
    return answer_question(request.question)