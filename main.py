from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from services.cost_engine import calculate_ec2_cost
from services.policy_engine import check_cost_policy
from services.cost_engine import calculate_ec2_cost


app = FastAPI(
    title="CloudCostOps",
    description="Cloud cost optimization platform",
    version="0.1.0"
)


class EC2Resource(BaseModel):
    instance_type: str
    quantity: int = 1


class CostEstimateRequest(BaseModel):
    resources: list[EC2Resource]

class CostGateRequest(BaseModel):
    current_monthly_cost: float = Field(ge=0)
    max_increase: float = Field(default=100.0, ge=0)
    resources: list[EC2Resource]


@app.get("/")
def root():
    return {
        "application": "CloudCostOps",
        "version": "0.1.0",
        "message": "Cloud cost optimization starts here"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/estimate")
def estimate_cost(request: CostEstimateRequest):

    results = []
    total_cost = 0

    for resource in request.resources:

        try:
            result = calculate_ec2_cost(
                resource.instance_type,
                resource.quantity
            )

            results.append(result)

            total_cost += result["monthly_cost"]

        except ValueError as error:

            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

    return {
        "currency": "USD",
        "monthly_cost": round(total_cost, 2),
        "resources": results
    }


class CostPolicyRequest(BaseModel):
    current_monthly_cost: float = Field(ge=0)
    proposed_monthly_cost: float = Field(ge=0)
    max_increase: float = Field(default=100.0, ge=0)


@app.post("/policy/check")
def check_policy(request: CostPolicyRequest):
    return check_cost_policy(
        current_monthly_cost=request.current_monthly_cost,
        proposed_monthly_cost=request.proposed_monthly_cost,
        max_increase=request.max_increase,
    )


@app.post("/cost-gate")
def cost_gate(request: CostGateRequest):
    results = []
    proposed_monthly_cost = 0.0

    for resource in request.resources:
        try:
            result = calculate_ec2_cost(
                resource.instance_type,
                resource.quantity,
            )
        except ValueError as error:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )

        results.append(result)
        proposed_monthly_cost += result["monthly_cost"]

    policy = check_cost_policy(
        current_monthly_cost=request.current_monthly_cost,
        proposed_monthly_cost=proposed_monthly_cost,
        max_increase=request.max_increase,
    )

    return {
        "currency": "USD",
        "estimated_resources": results,
        "policy_result": policy,
    }
