import random
from datetime import datetime, timedelta
import pandas as pd

# ------------------------------------------------
# 1. Dictionaries to Customize Gene Expression
# ------------------------------------------------

# Baseline expression ranges for each disease & gene.
# Each tuple is (min_value, max_value).
DISEASE_GENE_BASE = {
    "Breast Cancer": {
        "EGFR":  (5,  8),
        "KRAS":  (4,  7),
        "BRAF":  (5,  10),
        "PIK3CA":(6,  11)
    },
    "Lung Cancer": {
        "EGFR":  (10, 15),
        "KRAS":  (8,  14),
        "BRAF":  (5,  9),
        "PIK3CA":(7,  10)
    },
    "Colorectal Cancer": {
        "EGFR":  (4,  7),
        "KRAS":  (9,  14),
        "BRAF":  (7,  12),
        "PIK3CA":(6,  9)
    },
    "Prostate Cancer": {
        "EGFR":  (4,  6),
        "KRAS":  (5,  8),
        "BRAF":  (3,  6),
        "PIK3CA":(5,  8)
    },
    "Leukemia": {
        "EGFR":  (5,  8),
        "KRAS":  (5,  9),
        "BRAF":  (5,  9),
        "PIK3CA":(4,  7)
    },
    "Lymphoma": {
        "EGFR":  (6,  9),
        "KRAS":  (5,  8),
        "BRAF":  (6,  10),
        "PIK3CA":(5,  9)
    }
}

# Multipliers for each stage (1 through 4).
STAGE_MULTIPLIERS = {
    1: 1.0,
    2: 1.1,
    3: 1.2,
    4: 1.3
}

GENE_LIST = ["EGFR", "KRAS", "BRAF", "PIK3CA"]

# ------------------------------------------------
# 2. Generate & Update Gene Expression
# ------------------------------------------------

def generate_initial_gene_expression(disease, stage):
    """
    Generate a new dictionary of gene expressions for a patient
    given their 'disease' and 'stage' using the baseline ranges
    and applying a stage multiplier.
    """
    gene_expression = {}
    disease_bases = DISEASE_GENE_BASE.get(disease, DISEASE_GENE_BASE["Breast Cancer"])
    stage_multiplier = STAGE_MULTIPLIERS.get(stage, 1.0)
    
    for gene_name in GENE_LIST:
        base_range = disease_bases.get(gene_name, (5, 10))
        val = random.uniform(base_range[0], base_range[1])
        gene_expression[gene_name] = round(val * stage_multiplier, 2)
    
    return gene_expression

def update_gene_expression(old_expression, disease, stage, variation=2):
    """
    Update an existing expression dictionary to reflect stage progression
    and random drift. The new stage multiplier is applied on top of the old value.
    """
    stage_multiplier = STAGE_MULTIPLIERS.get(stage, 1.0)
    
    new_expr = {}
    for gene_name, old_val in old_expression.items():
        drift = random.uniform(-variation, variation)
        new_val = (old_val + drift) * stage_multiplier
        new_expr[gene_name] = round(new_val, 2)
    
    return new_expr

# ------------------------------------------------
# 3. Other Utility Functions
# ------------------------------------------------

def random_date(start_year=2021, end_year=2025):
    start_dt = datetime(start_year, 1, 1)
    end_dt = datetime(end_year, 12, 31)
    delta = end_dt - start_dt
    random_days = random.randrange(delta.days + 1)
    return start_dt + timedelta(days=random_days)

def generate_patient_name():
    first_names = ["John", "Jane", "Mary", "Michael", "Sarah", "David", 
                   "Anna", "Peter", "Linda", "James"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", 
                  "Miller", "Davis", "Martinez", "Wilson"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_gender():
    return random.choice(["Male", "Female", "Other"])

def generate_diagnosis():
    diagnoses = [
        "Breast Cancer",
        "Lung Cancer",
        "Colorectal Cancer",
        "Prostate Cancer",
        "Leukemia",
        "Lymphoma"
    ]
    return random.choice(diagnoses)

def generate_treatment_type():
    treatments = [
        "Chemotherapy",
        "Targeted Therapy",
        "Immunotherapy",
        "Hormonal Therapy",
        "Combination Therapy"
    ]
    return random.choice(treatments)

def generate_ethnicity():
    ethnicities = [
        "Hispanic or Latino",
        "Not Hispanic or Latino",
        "African American",
        "Asian",
        "White",
        "Unknown"
    ]
    return random.choice(ethnicities)

def generate_us_location():
    us_states = [
        "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
        "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
        "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
        "VA","WA","WV","WI","WY"
    ]
    return random.choice(us_states)

def generate_treatment_history():
    possible_treatments = [
        "Surgery",
        "Radiotherapy",
        "Previous Chemotherapy",
        "Previous Immunotherapy",
        "Hormonal Therapy"
    ]
    num_treatments = random.randint(0, 3)
    return random.sample(possible_treatments, num_treatments)

def generate_adverse_events():
    possible_events = [
        "Nausea",
        "Fatigue",
        "Neutropenia",
        "Neuropathy",
        "Alopecia",
        "Anemia",
        "Diarrhea",
        "Rash"
    ]
    num_events = random.randint(0, 4)
    return random.sample(possible_events, num_events)

def generate_comorbidities():
    possible_comorbidities = [
        "Hypertension",
        "Diabetes",
        "Hyperlipidemia",
        "Obesity",
        "Chronic Kidney Disease",
        "Depression",
        "Coronary Artery Disease"
    ]
    num_co = random.randint(0, 3)
    return random.sample(possible_comorbidities, num_co)

def generate_treatment_outcome():
    """
    Randomly assign a final treatment outcome for each cycle,
    including the possibility of 'Discontinued'.
    """
    # We add 'Discontinued' as a possible event with some probability.
    # You can tune these probabilities as needed.
    outcomes = [
        "Complete Response",
        "Partial Response",
        "Stable Disease",
        "Progressive Disease",
        "Death",
        "Discontinued"
    ]
    return random.choice(outcomes)

DRUGS_BY_STAGE = {
    1: ["Doxorubicin", "Cyclophosphamide", "Paclitaxel"],
    2: ["Carboplatin", "Cisplatin", "Pembrolizumab"],
    3: ["Trastuzumab", "Erlotinib", "Bevacizumab"],
    4: ["Gemcitabine", "Vincristine", "Irinotecan"]
}

def generate_cycle_drugs_for_stage(disease_stage):
    possible_drugs = DRUGS_BY_STAGE.get(disease_stage, [])
    if not possible_drugs:
        return []
    num_drugs = random.randint(1, min(3, len(possible_drugs)))
    return random.sample(possible_drugs, num_drugs)

THERAPY_SEGMENT_BY_STAGE = {
    1: "First-line Therapy",
    2: "Second-line Therapy",
    3: "Third-line Therapy",
    4: "Fourth-line Therapy"
}

# ------------------------------------------------
# 4. Generate Treatment Cycles
# ------------------------------------------------

def generate_treatment_cycles(disease, start_date, num_cycles=4, cycle_gap_days=21, date_of_death=None):
    """
    Generate a list of dictionaries for each cycle:
        - cycle_number
        - cycle_date
        - disease_stage (1->4, only progresses)
        - therapy_segment
        - drugs_used
        - gene_expression (tailored to disease & stage)
        - treatment_outcome
        - Discontinuation case: if outcome == 'Discontinued', we stop generating new cycles.

    If date_of_death is provided, we end if the next cycle date >= date_of_death
    or if outcome is 'Death'.
    """
    cycles = []
    # Start disease stage at 1 or 2
    disease_stage = random.randint(1, 2)
    gene_expression = generate_initial_gene_expression(disease, disease_stage)

    for cycle_num in range(1, num_cycles + 1):
        # Check if the patient has died (date_of_death) before starting this cycle
        if date_of_death and start_date >= date_of_death:
            break
        
        outcome = generate_treatment_outcome()
        
        cycle_info = {
            "cycle_number": cycle_num,
            "cycle_date": start_date.strftime("%Y-%m-%d"),
            "disease_stage": disease_stage,
            "therapy_segment": THERAPY_SEGMENT_BY_STAGE[disease_stage],
            "drugs_used": generate_cycle_drugs_for_stage(disease_stage),
            "gene_expression": gene_expression,
            "treatment_outcome": outcome
        }
        cycles.append(cycle_info)
        
        # Advance the date for the next cycle (if any)
        start_date += timedelta(days=cycle_gap_days)
        
        # Update gene expression for next cycle
        next_stage = min(disease_stage + 1, 4)
        gene_expression = update_gene_expression(gene_expression, disease, next_stage)
        
        # Increase disease_stage if not already 4
        if disease_stage < 4:
            disease_stage += 1
        
        # If outcome is Death -> no further cycles
        if outcome == "Death":
            date_of_death = start_date
            break
        
        # If outcome is Discontinued -> no further cycles, but patient is still alive
        if outcome == "Discontinued":
            # We won't set date_of_death, but we stop generating cycles anyway
            break

    return cycles, date_of_death

# ------------------------------------------------
# 5. Main Patient Generation
# ------------------------------------------------

def generate_patient_info(num_patients=5):
    """
    Generate a list of patient dictionaries. For each patient:
      - Basic demographics & diagnosis
      - Possibly truncated cycles if 'Death' or 'Discontinued' occurs
      - OS/PFS
      - Disease- & stage-specific gene expression
    """
    patients_data = []
    
    for i in range(1, num_patients + 1):
        patient_id = f"PT{i:03d}"
        name = generate_patient_name()
        age = random.randint(25, 85)
        gender = generate_gender()
        diagnosis = generate_diagnosis()
        treatment_type = generate_treatment_type()
        
        ethnicity = generate_ethnicity()
        location = generate_us_location()
        treatment_history = generate_treatment_history()
        adverse_events = generate_adverse_events()
        comorbidities = generate_comorbidities()
        number_of_hospitalizations = random.randint(0, 3)
        
        os_months = random.randint(6, 60)
        pfs_months = random.randint(3, min(os_months - 1, 24))
        
        first_cycle_date = random_date(2021, 2024)
        planned_cycles = random.randint(3, 6)
        
        # Generate cycles
        cycle_data, date_of_death = generate_treatment_cycles(
            disease=diagnosis,
            start_date=first_cycle_date,
            num_cycles=planned_cycles,
            cycle_gap_days=21
        )
        
        actual_cycle_count = len(cycle_data)
        
        patient_dict = {
            "patient_id": patient_id,
            "name": name,
            "age": age,
            "gender": gender,
            "ethnicity": ethnicity,
            "location": location,
            "diagnosis": diagnosis,
            "treatment_type": treatment_type,
            "treatment_history": treatment_history,
            "adverse_events": adverse_events,
            "comorbidities": comorbidities,
            "number_of_hospitalizations": number_of_hospitalizations,
            "os_months": os_months,
            "pfs_months": pfs_months,
            "date_of_death": date_of_death,
            "number_of_cycles": actual_cycle_count,
            "cycles": cycle_data
        }
        patients_data.append(patient_dict)
    
    return patients_data

# ------------------------------------------------
# 6. DataFrame Constructors
# ------------------------------------------------

def create_rwe_table(patients_data):
    """
    RWE Table (wide format for genes):
      - One row per (patient_id, cycle_number, cycle_date, drug_name)
      - Columns for each gene in GENE_LIST (EGFR, KRAS, BRAF, PIK3CA).
    """
    rwe_rows = []
    for patient in patients_data:
        for cycle in patient["cycles"]:
            for drug in cycle["drugs_used"]:
                row = {
                    "patient_id":     patient["patient_id"],
                    "cycle_number":   cycle["cycle_number"],
                    "cycle_date":     cycle["cycle_date"],
                    "drug_name":      drug,
                    "disease_stage":  cycle["disease_stage"],
                    "therapy_segment":cycle["therapy_segment"],
                    "treatment_outcome": cycle["treatment_outcome"]
                }
                # Flatten each gene expression into its own columns
                for gene_name, expr_value in cycle["gene_expression"].items():
                    row[gene_name] = expr_value

                rwe_rows.append(row)
    return pd.DataFrame(rwe_rows)

def create_tcga_table(patients_data):
    """
    TCGA Table (wide format, 1 row per patient/cycle).
    """
    tcga_rows = []
    for patient in patients_data:
        for cycle in patient["cycles"]:
            row_dict = {
                "patient_id": patient["patient_id"],
                "cycle_number": cycle["cycle_number"],
                "cycle_date": cycle["cycle_date"]
            }
            for gene_name, expr_value in cycle["gene_expression"].items():
                row_dict[gene_name] = expr_value
            tcga_rows.append(row_dict)
    return pd.DataFrame(tcga_rows)

def create_ehr_table(patients_data):
    """
    EHR Table:
      - One row per patient/cycle
      - Includes demographic/clinical data, disease_stage, therapy_segment,
        plus drugs in a single comma-separated column.
    """
    ehr_rows = []
    for patient in patients_data:
        adverse_events_str = ", ".join(patient["adverse_events"])
        treatment_history_str = ", ".join(patient["treatment_history"])
        comorbidities_str = ", ".join(patient["comorbidities"])
        
        for cycle in patient["cycles"]:
            drug_string = ", ".join(cycle["drugs_used"])
            ehr_rows.append({
                "patient_id":    patient["patient_id"],
                "name":          patient["name"],
                "age":           patient["age"],
                "gender":        patient["gender"],
                "ethnicity":     patient["ethnicity"],
                "location":      patient["location"],
                "diagnosis":     patient["diagnosis"],
                "treatment_type":patient["treatment_type"],
                "treatment_history":      treatment_history_str,
                "adverse_events":         adverse_events_str,
                "comorbidities":          comorbidities_str,
                "number_of_hospitalizations": patient["number_of_hospitalizations"],
                "date_of_death": patient["date_of_death"],
                "cycle_number": cycle["cycle_number"],
                "cycle_date":   cycle["cycle_date"],
                "disease_stage":cycle["disease_stage"],
                "therapy_segment": cycle["therapy_segment"],
                "treatment_outcome": cycle["treatment_outcome"],
                "drugs_used":    drug_string
            })
    return pd.DataFrame(ehr_rows)

def create_patient_registry_table(patients_data):
    """
    Patient Registry Table:
      - One row per patient
    """
    registry_rows = []
    for patient in patients_data:
        cycle_dates = [c["cycle_date"] for c in patient["cycles"]]
        cycle_dates_sorted = sorted(cycle_dates)
        
        final_outcome = "No Treatment"
        if patient["cycles"]:
            final_outcome = patient["cycles"][-1]["treatment_outcome"]
        
        first_cycle = cycle_dates_sorted[0] if cycle_dates_sorted else None
        last_cycle = cycle_dates_sorted[-1] if cycle_dates_sorted else None
        
        adverse_events_str = ", ".join(patient["adverse_events"])
        treatment_history_str = ", ".join(patient["treatment_history"])
        comorbidities_str = ", ".join(patient["comorbidities"])
        
        registry_rows.append({
            "patient_id":     patient["patient_id"],
            "name":           patient["name"],
            "age":            patient["age"],
            "gender":         patient["gender"],
            "ethnicity":      patient["ethnicity"],
            "location":       patient["location"],
            "diagnosis":      patient["diagnosis"],
            "treatment_type": patient["treatment_type"],
            "treatment_history": treatment_history_str,
            "adverse_events":    adverse_events_str,
            "comorbidities":     comorbidities_str,
            "number_of_hospitalizations": patient["number_of_hospitalizations"],
            "final_outcome":   final_outcome,
            "date_of_death":   patient["date_of_death"],
            "number_of_cycles":patient["number_of_cycles"],
            "first_cycle_date": first_cycle,
            "last_cycle_date":  last_cycle,
            "os_months":       patient["os_months"],
            "pfs_months":      patient["pfs_months"]
        })
    return pd.DataFrame(registry_rows)

def create_claims_table(patients_data):
    """
    Claims Table:
      - One row per patient/cycle
      - Columns for cost_of_treatment, cost_of_diagnostics, etc.
    """
    procedure_codes = ["CPT-1234", "CPT-5678", "CPT-9012", "CPT-3456"]
    claims_rows = []
    claim_id_counter = 1000
    
    for patient in patients_data:
        for cycle in patient["cycles"]:
            proc_code = random.choice(procedure_codes)
            drug_string = ", ".join(cycle["drugs_used"])
            
            cost_of_treatment = round(random.uniform(500, 5000), 2)
            cost_of_diagnostics = round(random.uniform(200, 2000), 2)
            
            total_bill = round(cost_of_treatment + cost_of_diagnostics, 2)
            coverage_fraction = random.uniform(0.5, 0.9)
            paid_by_insurance = round(total_bill * coverage_fraction, 2)
            paid_by_patient = round(total_bill - paid_by_insurance, 2)
            
            claims_rows.append({
                "claim_id": claim_id_counter,
                "patient_id": patient["patient_id"],
                "date_of_service": cycle["cycle_date"],
                "drugs_administered": drug_string,
                "procedure_code": proc_code,
                "cost_of_treatment": cost_of_treatment,
                "cost_of_diagnostics": cost_of_diagnostics,
                "total_bill": total_bill,
                "paid_by_insurance": paid_by_insurance,
                "paid_by_patient": paid_by_patient
            })
            
            claim_id_counter += 1
    
    return pd.DataFrame(claims_rows)

# ------------------------------------------------
# 7. High-Level "Run" Function
# ------------------------------------------------

def generate_all_tables(num_patients=5):
    """
    Generates all the synthetic data tables (RWE, TCGA, EHR, Registry, Claims)
    for the specified number of patients, and returns them as DataFrames.
    
    Example usage:
        rwe_df, tcga_df, ehr_df, registry_df, claims_df = generate_all_tables(10)
    """
    patients_data = generate_patient_info(num_patients)
    
    rwe_df       = create_rwe_table(patients_data)
    tcga_df      = create_tcga_table(patients_data)
    ehr_df       = create_ehr_table(patients_data)
    registry_df  = create_patient_registry_table(patients_data)
    claims_df    = create_claims_table(patients_data)
    
    return rwe_df, tcga_df, ehr_df, registry_df, claims_df


df_rwe, df_tcga, df_ehr, df_registry, df_claims = generate_all_tables(num_patients=600)

print(df_rwe.head())
print(df_tcga.head())
print(df_ehr.head())
print(df_registry.head())
print(df_claims.head())