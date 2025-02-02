import pandas as pd
import random, math
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Provided data
CANCER_TYPES = [
    "Breast Cancer",
    "Lung Cancer",
    "Colorectal Cancer",
    "Prostate Cancer",
    "Leukemia",
    "Lymphoma"
]

DRUGS_BY_STAGE = {
    1: ["Doxorubicin", "Cyclophosphamide", "Paclitaxel"],
    2: ["Carboplatin", "Cisplatin", "Pembrolizumab"],
    3: ["Trastuzumab", "Erlotinib", "Bevacizumab"],
    4: ["Gemcitabine", "Vincristine", "Irinotecan"]
}

COMPETITORS = ["PharmaA", "PharmaB", "PharmaC"]

def two_phase_curve(t, peak_month, L, k_grow, k_decay):
    """
    A piecewise function:
    - For t < peak_month: logistic growth from near 0 to ~L by the peak.
    - For t >= peak_month: exponential decay from ~L down toward 0.

    Parameters
    ----------
    t           : int (month index, e.g. 0..N-1)
    peak_month  : int (the month index at which sales reach ~peak)
    L           : float (peak sales level)
    k_grow      : float (growth rate for logistic up)
    k_decay     : float (exponential decay rate after peak)
    """
    if t < peak_month:
        # Logistic growth up to L by peak_month
        # We'll set a logistic midpoint at half of peak_month so we get near L by t=peak_month
        x0 = peak_month / 2.0
        return L / (1.0 + math.exp(-k_grow*(t - x0)))
    else:
        # Exponential decay from L at t=peak_month onward
        tprime = t - peak_month
        return L * math.exp(-k_decay * tprime)

def generate_competitor_sales_data_scurve_with_decline(
    start_month="2023-01",
    end_month="2023-12"
):
    """
    Generate monthly competitor sales data for each 
    (competitor, cancer_type, stage, drug) combination over a date range,
    using a 2-phase S-curve: logistic growth then exponential decline.

    Columns in the output DataFrame:
      - month (YYYY-MM)
      - competitor
      - cancer_type
      - stage
      - drug
      - sales
    """

    # Parse start/end into datetime objects
    start_date = datetime.strptime(start_month, "%Y-%m")
    end_date   = datetime.strptime(end_month,   "%Y-%m")
    
    # Build list of months in [start_date, end_date]
    months = []
    current_date = start_date
    while current_date <= end_date:
        months.append(current_date)
        current_date += relativedelta(months=1)
    
    num_months = len(months)

    # For each competitor, define random parameters for the 2-phase curve:
    # - peak_month  (somewhere between 30%..70% of the total months)
    # - L          (peak sales, e.g. 3000..15000)
    # - k_grow     (growth rate, e.g. 0.2..1.0)
    # - k_decay    (decay rate, e.g. 0.05..0.3)
    competitor_params = {}
    for comp in COMPETITORS:
        peak_m   = random.randint(int(num_months*0.3), int(num_months*0.7))
        L        = random.uniform(3000, 15000) 
        k_grow   = random.uniform(0.2, 1.0)
        k_decay  = random.uniform(0.05, 0.3)
        competitor_params[comp] = (peak_m, L, k_grow, k_decay)

    rows = []
    for month_idx, dt in enumerate(months):
        month_str = dt.strftime("%Y-%m")
        for comp in COMPETITORS:
            # Evaluate base curve for competitor at this month
            peak_m, L, k_grow, k_decay = competitor_params[comp]
            base_value = two_phase_curve(
                t=month_idx,
                peak_month=peak_m,
                L=L,
                k_grow=k_grow,
                k_decay=k_decay
            )
            
            # Now for each (cancer_type, stage, drug)
            for ctype in CANCER_TYPES:
                for stage, drug_list in DRUGS_BY_STAGE.items():
                    for drug in drug_list:
                        # Variation factor so not all (ctype,stage,drug) are identical
                        var_factor = random.uniform(0.8, 1.2)
                        sales = base_value * var_factor

                        # Add random noise (± 5%)
                        noise = random.uniform(-0.05, 0.05) * sales
                        sales += noise
                        # Ensure no negative
                        if sales < 0:
                            sales = 0
                        
                        sales = int(round(sales))

                        row = {
                            "month": month_str,
                            "competitor": comp,
                            "cancer_type": ctype,
                            "stage": stage,
                            "drug": drug,
                            "sales": sales
                        }
                        rows.append(row)
    
    df = pd.DataFrame(rows)
    return df


# =======================
# Example usage
# =======================

df_sales = generate_competitor_sales_data_scurve_with_decline(
    start_month="2014-01", 
    end_month="2024-06"
)

print("Sample competitor sales data (growth + decline curve):")
print(df_sales.head(20))
print(f"\nTotal rows = {len(df_sales)}")

    # You can pivot, plot, or export the DataFrame as needed.
