PRICING = {
    "t3.micro": 7.59,
    "t3.small": 15.18,
    "t3.medium": 30.37,
    "t3.large": 60.74,
    "m5.large": 70.08,
}


def calculate_ec2_cost(instance_type: str, quantity: int = 1):
    if instance_type not in PRICING:
        raise ValueError(
            f"Pricing not available for instance type: {instance_type}"
        )

    monthly_cost = PRICING[instance_type] * quantity

    return {
        "service": "EC2",
        "instance_type": instance_type,
        "quantity": quantity,
        "monthly_cost": round(monthly_cost, 2),
    }