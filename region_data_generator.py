import pandas as pd
import json
import os
import zipfile

FIRST_YEAR = 2010
LAST_YEAR = 2022

zone = "E"
data_directory = f"data/regions/{zone}"

COMBUSTIBLES = {
    1: "Chauffage urbain",
    2: "Gaz de ville/réseau",
    3: "Fioul (mazout)",
    4: "Électricité",
    5: "Gaz bouteille/citerne",
    6: "Autre"
}

TYPES_LOGEMENTS = {
    1: "Maison individuelle",
    2: "Appartement",
    3: "Autre"
}

fioul_par_annee_emmenagement = {}
fioul_par_type_logement = {}
fioul_par_annee_et_type = {}

for year in range(FIRST_YEAR, LAST_YEAR + 1):
    zip_path = f"{data_directory}/{year}.zip"
    
    if year < 2016:
        file_name = f"FD_LOGEMTZ{zone}_{year}.txt"
    else:
        file_name = f"FD_LOGEMTZ{zone}_{year}.csv"
        
    with zipfile.ZipFile(zip_path, 'r') as z:
        with z.open(file_name) as f:
            df = pd.read_csv(f, sep=';', usecols=["CMBL", "IPONDL", "AEMM", "TYPL"])

    df["CMBL"] = pd.to_numeric(df["CMBL"], errors="coerce")
    
    if pd.api.types.is_string_dtype(df["IPONDL"]):
        df["IPONDL"] = df["IPONDL"].str.replace(",", ".")
    df["IPONDL"] = pd.to_numeric(df["IPONDL"], errors="coerce")
    df["AEMM"] = pd.to_numeric(df["AEMM"], errors="coerce")
    df["TYPL"] = pd.to_numeric(df["TYPL"], errors="coerce")

    df_fioul = df[df["CMBL"] == 3].copy()

    fioul_par_annee_emmenagement[year] = {}
    for annee_emm in df_fioul["AEMM"].unique():
        if not pd.isna(annee_emm):
            count = df_fioul.loc[df_fioul["AEMM"] == annee_emm, "IPONDL"].sum()
            fioul_par_annee_emmenagement[year][int(annee_emm)] = count

    fioul_par_type_logement[year] = {}
    for type_log in df_fioul["TYPL"].unique():
        if not pd.isna(type_log):
            count = df_fioul.loc[df_fioul["TYPL"] == type_log, "IPONDL"].sum()
            fioul_par_type_logement[year][int(type_log)] = count

    fioul_par_annee_et_type[year] = {}
    for annee_emm in df_fioul["AEMM"].unique():
        if not pd.isna(annee_emm):
            fioul_par_annee_et_type[year][int(annee_emm)] = {}
            for type_log in df_fioul["TYPL"].unique():
                if not pd.isna(type_log):
                    mask = (df_fioul["AEMM"] == annee_emm) & (df_fioul["TYPL"] == type_log)
                    count = df_fioul.loc[mask, "IPONDL"].sum()
                    fioul_par_annee_et_type[year][int(annee_emm)][int(type_log)] = count

results_dir = f'results/{zone}'
os.makedirs(results_dir, exist_ok=True)

with open(f'{results_dir}/fioul_par_annee_emmenagement.json', 'w', encoding='utf-8') as f:
    json.dump(fioul_par_annee_emmenagement, f, indent=2, ensure_ascii=False)

with open(f'{results_dir}/fioul_par_type_logement.json', 'w', encoding='utf-8') as f:
    json.dump(fioul_par_type_logement, f, indent=2, ensure_ascii=False)