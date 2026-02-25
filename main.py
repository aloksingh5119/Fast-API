from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# -----------------------------
# CORS Middleware (IMPORTANT)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Helper Function
# -----------------------------
def patients_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data


# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {"message": "Hello Patients"}


# -----------------------------
# Get All Patients
# -----------------------------
@app.get("/patients")
def get_all_patients():
    return patients_data()


# -----------------------------
# Get Single Patient
# -----------------------------
@app.get("/patients/{patient_id}")
def get_single_patient(
    patient_id: str = Path(..., description="Patient ID required", example="P001")
):
    data = patients_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(status_code=404, detail="Patient not found")


# -----------------------------
# Sort Patients
# -----------------------------
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort by height, weight, bmi"),
    order: str = Query("asc", description="Sort order: asc or desc"),
):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Select from {valid_fields}"
        )

    if order not in ['asc', 'desc']:
        raise HTTPException(
            status_code=400,
            detail="Order must be 'asc' or 'desc'"
        )

    data = patients_data()

    reverse_order = True if order == "desc" else False

    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=reverse_order
    )

    return sorted_data


# -----------------------------
# Delete Patient
# -----------------------------
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):
    data = patients_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]

    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)

    return {"message": "Patient deleted successfully"}