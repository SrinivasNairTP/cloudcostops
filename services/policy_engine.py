
def check_cost_policy(
    current_monthly_cost: float,
    proposed_monthly_cost: float,
    max_increase: float = 100.0,
):
    increase = proposed_monthly_cost - current_monthly_cost
    excess_over_limit = max(0, increase - max_increase)

    passed = increase <= max_increase

    return {
        "policy": "maximum_monthly_cost_increase",
        "currency": "USD",
        "current_monthly_cost": round(current_monthly_cost, 2),
        "proposed_monthly_cost": round(proposed_monthly_cost, 2),
        "monthly_increase": round(increase, 2),
        "increase_percentage": round(
            (increase / current_monthly_cost * 100)
            if current_monthly_cost > 0 else 0,
            2,
        ),
        "maximum_allowed_increase": round(max_increase, 2),
        "excess_over_limit": round(excess_over_limit, 2),
        "status": "PASS" if passed else "FAIL",
        "message": (
            f"Cost policy passed. Monthly cost increases by ${increase:.2f}."
            if passed
            else (
                f"Cost increases by ${increase:.2f} per month, "
                f"which exceeds the allowed increase of "
                f"${max_increase:.2f} by ${excess_over_limit:.2f}."
            )
        ),
    }
