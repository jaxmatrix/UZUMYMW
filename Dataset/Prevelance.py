import random
import pandas as pd

US_STATES = [
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
    "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
    "VA","WA","WV","WI","WY"
]

US_REGIONS = {
    "Northeast": ["CT","ME","MA","NH","NJ","NY","PA","RI","VT"],
    "Midwest":   ["IL","IN","IA","KS","MI","MN","MO","NE","ND","OH","SD","WI"],
    "South":     ["AL","AR","DE","FL","GA","KY","LA","MD","MS","NC","OK","SC","TN","TX","VA","WV"],
    "West":      ["AK","AZ","CA","CO","HI","ID","MT","NV","NM","OR","UT","WA","WY"]
}

CANCER_TYPES = [
    "Lung Cancer",
    "Breast Cancer",
    "Prostate Cancer",
    "Colorectal Cancer",
    "Leukemia",
    "Lymphoma"
]

def assign_region(state_abbr):
    """
    Return a region name (Northeast, Midwest, South, West) for a given state abbreviation.
    """
    for region, states in US_REGIONS.items():
        if state_abbr in states:
            return region
    return "Unknown"

def create_multi_cancer_prevalence_dataset(
    start_year=2018,
    end_year=2025,
    states=None,
    cancer_types=None
):
    """
    Create a synthetic dataset showing prevalence/incidence/mortality
    for multiple cancer types across U.S. states (and region) over time,
    now including a random 'cancer_stage' (1-4).

    :param start_year:   First year of data
    :param end_year:     Last year of data
    :param states:       A list of state abbreviations. If None, uses all US_STATES.
    :param cancer_types: A list of cancer types to simulate. If None, uses CANCER_TYPES.
    :return: pandas DataFrame with columns:

        [
         'year', 'state', 'region', 'cancer_type', 'cancer_stage',
         'population',
         'prevalence_count', 'prevalence_rate',
         'incidence_count', 'incidence_rate',
         'mortality_count', 'mortality_rate'
        ]
    """
    if states is None:
        states = US_STATES  # all states by default
    if cancer_types is None:
        cancer_types = CANCER_TYPES

    all_rows = []

    for year in range(start_year, end_year + 1):
        for state in states:
            region = assign_region(state)
            
            # Synthetic total population for the state in that year
            population = random.randint(200_000, 40_000_000)

            for cancer in cancer_types:
                # Base ranges vary by cancer
                if cancer == "Lung Cancer":
                    base_incidence_min, base_incidence_max = (500, 6000)
                    base_mort_min,     base_mort_max       = (200, 4500)
                elif cancer == "Breast Cancer":
                    base_incidence_min, base_incidence_max = (1000, 7000)
                    base_mort_min,     base_mort_max       = (300, 3000)
                elif cancer == "Prostate Cancer":
                    base_incidence_min, base_incidence_max = (800, 5000)
                    base_mort_min,     base_mort_max       = (200, 2000)
                elif cancer == "Colorectal Cancer":
                    base_incidence_min, base_incidence_max = (700, 4000)
                    base_mort_min,     base_mort_max       = (200, 1500)
                elif cancer == "Leukemia":
                    base_incidence_min, base_incidence_max = (300, 2000)
                    base_mort_min,     base_mort_max       = (100, 1000)
                elif cancer == "Lymphoma":
                    base_incidence_min, base_incidence_max = (300, 2200)
                    base_mort_min,     base_mort_max       = (100, 800)
                else:
                    # Fallback
                    base_incidence_min, base_incidence_max = (500, 5000)
                    base_mort_min, base_mort_max = (200, 2000)

                # Generate random incidence / mortality
                incidence_count  = random.randint(base_incidence_min, base_incidence_max)
                mortality_count  = random.randint(base_mort_min, min(incidence_count, base_mort_max))

                # For prevalence, assume up to 5x incidence
                prevalence_count = random.randint(incidence_count, incidence_count * 5)

                # Calculate rates per 100k
                prevalence_rate = round((prevalence_count / population) * 100_000, 2)
                incidence_rate  = round((incidence_count  / population) * 100_000, 2)
                mortality_rate  = round((mortality_count  / population) * 100_000, 2)

                # Randomly pick a cancer stage from 1 to 4
                cancer_stage = random.randint(1, 4)

                row = {
                    "year":             pd.to_datetime(str(year) + '-01-01'),
                    "state":            state,
                    "region":           region,
                    "cancer_type":      cancer,
                    "cancer_stage":     cancer_stage,
                    "population":       population,
                    "prevalence_count": prevalence_count,
                    "prevalence_rate":  prevalence_rate,
                    "incidence_count":  incidence_count,
                    "incidence_rate":   incidence_rate,
                    "mortality_count":  mortality_count,
                    "mortality_rate":   mortality_rate
                }
                all_rows.append(row)
    
    df = pd.DataFrame(all_rows)
    return df

# ------------------------------------------------------------------------
# EXAMPLE USAGE:
# multi_cancer_df = create_multi_cancer_prevalence_dataset(start_year=2018, end_year=2025)
# multi_cancer_df.head()
# ------------------------------------------------------------------------
print("EPI BASED DATA ---------------------------------------")
df_epi = create_multi_cancer_prevalence_dataset(start_year=2014, end_year=2021)
print(df_epi.head())