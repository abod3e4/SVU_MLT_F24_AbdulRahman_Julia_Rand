from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from services.prediction import predict_loan_status
from services.request_store import add_request, remove_request_by_id,load_requests
from services.eda import generate_eda_summary
from services.model_utils import get_model_metrics
from services.eda import analyze_data_issues
from services.model_utils import predict_with_probability



router = APIRouter()

class LoanRequest(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str

@router.post("/predict")
def predict(request: LoanRequest):
    result = predict_with_probability(request.dict())
    return result

@router.post("/add-request")
def add_loan_request(request: LoanRequest):
    result = predict_with_probability(request.dict())
    prediction = predict_loan_status(request)
    data = request.dict()
    data.update(result)
    data["prediction"] = prediction
    added = add_request(data)
    return {"message": "Request added", "data": added}

@router.delete("/remove-request/{request_id}")
def delete_loan_request(request_id: str):
    success = remove_request_by_id(request_id)
    if not success:
        raise HTTPException(status_code=404, detail="Request not found")
    return {"message": f"Request with ID {request_id} removed"}


@router.get("/all-requests")
def get_all_requests():
    data = load_requests()
    return {"count": len(data), "requests": data}

@router.get("/eda-summary")
def eda_summary():
    return generate_eda_summary()