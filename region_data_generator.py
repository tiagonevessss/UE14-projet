import pandas as pd
import json
import os

FIRST_YEAR = 2010
LAST_YEAR = 2022

# A, B, C, D ou E
zone = "A"
data_directory = f"data/regions/{zone}"

# types de combustibles
COMBUSTIBLES = {
    1: "Chauffage urbain",
    2: "Gaz de ville/réseau",
    3: "Fioul (mazout)",
    4: "Électricité",
    5: "Gaz bouteille/citerne",
    6: "Autre"
}

# types de logements
TYPES_LOGEMENTS = {
    1: "Maison individuelle",
    2: "Appartement",
    3: "Autre"
}

# =============================================================================
# ANALYSE DES LOGEMENTS AU FIOUL PAR ANNÉE D'EMMÉNAGEMENT ET TYPE
# =============================================================================

fioul_par_annee_emmenagement = {}
fioul_par_type_logement = {}
fioul_par_annee_et_type = {}

for year in range(FIRST_YEAR, LAST_YEAR+1):
    file = f"{data_directory}/{year}.csv"
    df = pd.read_csv(file, sep=';', usecols=["CMBL", "IPONDL", "AEMM", "TYPL"])

    # conversion en numérique
    df["CMBL"] = pd.to_numeric(df["CMBL"], errors="coerce")
    # pour les années 2010/2011, le poids utilisait des ","
    if pd.api.types.is_string_dtype(df["IPONDL"].dtypes):
        df["IPONDL"] = df["IPONDL"].str.replace(",", ".")
    df["IPONDL"] = pd.to_numeric(df["IPONDL"], errors="coerce")
    df["AEMM"] = pd.to_numeric(df["AEMM"], errors="coerce")
    df["TYPL"] = pd.to_numeric(df["TYPL"], errors="coerce")

    # logements qui utilisent du fioul
    df_fioul = df[df["CMBL"] == 3].copy()

    # logements au fioul / année d'emménagement
    fioul_par_annee_emmenagement[year] = {}
    for annee_emm in df_fioul["AEMM"].unique():
        if not pd.isna(annee_emm):
            count = (df_fioul[df_fioul["AEMM"] == annee_emm]["IPONDL"]).sum()
            fioul_par_annee_emmenagement[year][int(annee_emm)] = count

    # logements au fioul / type de logement
    fioul_par_type_logement[year] = {}
    for type_log in df_fioul["TYPL"].unique():
        if not pd.isna(type_log):
            count = (df_fioul[df_fioul["TYPL"] == type_log]["IPONDL"]).sum()
            fioul_par_type_logement[year][int(type_log)] = count

    # logements au fioul / année d'emménagement et type de logement
    fioul_par_annee_et_type[year] = {}
    for annee_emm in df_fioul["AEMM"].unique():
        if not pd.isna(annee_emm):
            fioul_par_annee_et_type[year][int(annee_emm)] = {}
            for type_log in df_fioul["TYPL"].unique():
                if not pd.isna(type_log):
                    count = ((df_fioul["AEMM"] == annee_emm) &
                             (df_fioul["TYPL"] == type_log) * df_fioul["IPONDL"]).sum()
                    fioul_par_annee_et_type[year][int(
                        annee_emm)][int(type_log)] = count

# sauvegarde des données
results_dir = f'results/{zone}'
os.makedirs(results_dir, exist_ok=True)

with open(f'{results_dir}/fioul_par_annee_emmenagement.json', 'w', encoding='utf-8') as f:
    json.dump(fioul_par_annee_emmenagement, f, indent=2, ensure_ascii=False)

with open(f'{results_dir}/fioul_par_type_logement.json', 'w', encoding='utf-8') as f:
    json.dump(fioul_par_type_logement, f, indent=2, ensure_ascii=False)
