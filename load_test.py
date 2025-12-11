import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os

plt.style.use('seaborn-v0_8')

# Types de combustibles
COMBUSTIBLES = {
    1: "Chauffage urbain",
    2: "Gaz de ville/réseau",
    3: "Fioul (mazout)",
    4: "Électricité",
    5: "Gaz bouteille/citerne",
    6: "Autre"
}

# Types de logements
TYPES_LOGEMENTS = {
    1: "Maison individuelle",
    2: "Appartement",
    3: "Autre"
}

directory = "data/melun/"

# =============================================================================
# ANALYSE DES LOGEMENTS AU FIOUL PAR ANNÉE D'EMMÉNAGEMENT ET TYPE
# =============================================================================

fioul_par_annee_emmenagement = {}
fioul_par_type_logement = {}
fioul_par_annee_et_type = {}

for year in range(2010, 2022):
    file = f"{directory}/melun_{year}.csv"
    df = pd.read_csv(file, sep=';', usecols=["CMBL", "IPONDL", "AEMM", "TYPL"])

    # Conversion en numérique
    df["CMBL"] = pd.to_numeric(df["CMBL"], errors="coerce")
    df["IPONDL"] = pd.to_numeric(df["IPONDL"], errors="coerce")
    df["AEMM"] = pd.to_numeric(df["AEMM"], errors="coerce")
    df["TYPL"] = pd.to_numeric(df["TYPL"], errors="coerce")

    # Filtrer uniquement les logements au fioul
    df_fioul = df[df["CMBL"] == 3].copy()

    # Logements au fioul par année d'emménagement
    fioul_par_annee_emmenagement[year] = {}
    for annee_emm in df_fioul["AEMM"].unique():
        if not pd.isna(annee_emm):
            count = (df_fioul[df_fioul["AEMM"] == annee_emm]["IPONDL"]).sum()
            fioul_par_annee_emmenagement[year][int(annee_emm)] = count

    # Logements au fioul par type de logement
    fioul_par_type_logement[year] = {}
    for type_log in df_fioul["TYPL"].unique():
        if not pd.isna(type_log):
            count = (df_fioul[df_fioul["TYPL"] == type_log]["IPONDL"]).sum()
            fioul_par_type_logement[year][int(type_log)] = count

    # Logements au fioul par année d'emménagement ET type de logement
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

# Sauvegarde des données
os.makedirs('results', exist_ok=True)

with open('results/fioul_par_annee_emmenagement.json', 'w', encoding='utf-8') as f:
    json.dump(fioul_par_annee_emmenagement, f, indent=2, ensure_ascii=False)

with open('results/fioul_par_type_logement.json', 'w', encoding='utf-8') as f:
    json.dump(fioul_par_type_logement, f, indent=2, ensure_ascii=False)

# =============================================================================
# GRAPHIQUES - FIOUL PAR ANNÉE D'EMMÉNAGEMENT
# =============================================================================

print("=" * 60)
print("LOGEMENTS AU FIOUL PAR ANNÉE D'EMMÉNAGEMENT")
print("=" * 60)

# Préparation des données pour le graphique cumulatif
all_annees_emm = set()
for year_data in fioul_par_annee_emmenagement.values():
    all_annees_emm.update(year_data.keys())
all_annees_emm = sorted([a for a in all_annees_emm if a >= 1950])

# Création du DataFrame cumulatif
df_fioul_emm_cumul = pd.DataFrame(index=all_annees_emm)
for year in range(2010, 2022):
    year_data = fioul_par_annee_emmenagement.get(year, {})
    counts = [year_data.get(annee, 0) for annee in all_annees_emm]
    df_fioul_emm_cumul[year] = counts

# Graphique 1 : Heatmap des logements au fioul par année d'emménagement
plt.figure(figsize=(16, 10))
im = plt.imshow(df_fioul_emm_cumul.T, cmap='YlOrRd', aspect='auto',
                extent=[min(all_annees_emm), max(all_annees_emm), 2021, 2010])
plt.colorbar(label='Nombre de logements au fioul (pondéré)')
plt.xlabel('Année d\'emménagement')
plt.ylabel('Année de l\'enquête')
plt.title(
    'Logements au fioul par année d\'emménagement\n(Melun, 2010-2021)', fontsize=14)
plt.gca().invert_yaxis()  # Pour avoir 2010 en haut, 2021 en bas
plt.tight_layout()
plt.show()

# Graphique 2 : Distribution des logements au fioul par année d'emménagement (2021)
if 2021 in fioul_par_annee_emmenagement:
    data_2021 = fioul_par_annee_emmenagement[2021]
    annees_emm_2021 = sorted(
        [k for k in data_2021.keys() if k >= 1950 and data_2021[k] > 0])
    counts_2021 = [data_2021[k] for k in annees_emm_2021]

    plt.figure(figsize=(14, 8))
    plt.bar(annees_emm_2021, counts_2021, alpha=0.7,
            color='red', edgecolor='darkred')
    plt.title(
        'Logements au fioul par année d\'emménagement\n(Enquête 2021 - Melun)', fontsize=14)
    plt.xlabel('Année d\'emménagement')
    plt.ylabel('Nombre de logements au fioul (pondéré)')
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Graphique 3 : Évolution des logements au fioul par période d'emménagement
# Regroupement par décennies
decennies = ['1950-1959', '1960-1969', '1970-1979', '1980-1989',
             '1990-1999', '2000-2009', '2010-2019', '2020-2021']

fioul_par_decennie = {dec: [] for dec in decennies}
years_survey = list(range(2010, 2022))

for year in years_survey:
    data = fioul_par_annee_emmenagement.get(year, {})
    for decennie in decennies:
        start, end = map(int, decennie.split('-'))
        total_decennie = sum(data.get(annee, 0) for annee in data.keys()
                             if start <= annee <= end)
        fioul_par_decennie[decennie].append(total_decennie)

plt.figure(figsize=(14, 8))
for decennie in decennies:
    plt.plot(years_survey, fioul_par_decennie[decennie],
             marker='o', linewidth=2, label=decennie)

plt.title('Évolution des logements au fioul par décennie d\'emménagement\n(Melun, 2010-2021)', fontsize=14)
plt.xlabel('Année de l\'enquête')
plt.ylabel('Nombre de logements au fioul (pondéré)')
plt.grid(True, alpha=0.3)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
           title='Décennie d\'emménagement')
plt.xticks(years_survey)
plt.tight_layout()
plt.show()

# =============================================================================
# GRAPHIQUES - FIOUL PAR TYPE DE LOGEMENT
# =============================================================================

print("\n" + "=" * 60)
print("LOGEMENTS AU FIOUL PAR TYPE DE LOGEMENT")
print("=" * 60)

# Préparation des données
fioul_par_type_combined = {}
for type_log in TYPES_LOGEMENTS.keys():
    fioul_par_type_combined[type_log] = []
    for year in range(2010, 2022):
        data = fioul_par_type_logement.get(year, {})
        fioul_par_type_combined[type_log].append(data.get(type_log, 0))

# Graphique 4 : Évolution des logements au fioul par type de logement
plt.figure(figsize=(12, 8))
for type_log, counts in fioul_par_type_combined.items():
    type_name = TYPES_LOGEMENTS[type_log]
    plt.plot(range(2010, 2022), counts, marker='o', linewidth=2,
             label=type_name, markersize=6)

plt.title('Évolution des logements au fioul par type de logement\n(Melun, 2010-2021)', fontsize=14)
plt.xlabel('Année')
plt.ylabel('Nombre de logements au fioul (pondéré)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.xticks(range(2010, 2022))
plt.tight_layout()
plt.show()

# Graphique 5 : Répartition des logements au fioul par type (2021)
if 2021 in fioul_par_type_logement:
    data_2021_types = fioul_par_type_logement[2021]
    labels = [TYPES_LOGEMENTS.get(k, f"Type {k}")
              for k in data_2021_types.keys()]
    sizes = [data_2021_types[k] for k in data_2021_types.keys()]
    total_2021 = sum(sizes)

    # Calcul des pourcentages
    percentages = [f'{s/total_2021*100:.1f}%' for s in sizes]

    plt.figure(figsize=(10, 8))
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    wedges, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.1f%%',
                                       colors=colors, startangle=90)

    # Amélioration de l'affichage des pourcentages
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    plt.title(f'Répartition des logements au fioul par type de logement\n(Enquête 2021 - Total: {total_2021:.0f} logements)',
              fontsize=14)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

# Graphique 6 : Stacked area - Évolution cumulée par type
df_fioul_types = pd.DataFrame(fioul_par_type_combined)
df_fioul_types.index = range(2010, 2022)
df_fioul_types.columns = [TYPES_LOGEMENTS[col]
                          for col in df_fioul_types.columns]

plt.figure(figsize=(14, 8))
plt.stackplot(df_fioul_types.index, df_fioul_types.T,
              labels=df_fioul_types.columns, alpha=0.8)
plt.title('Évolution cumulée des logements au fioul par type de logement\n(Melun, 2010-2021)', fontsize=14)
plt.xlabel('Année')
plt.ylabel('Nombre de logements au fioul (pondéré)')
plt.grid(True, alpha=0.3)
plt.legend(title='Type de logement')
plt.xticks(range(2010, 2022))
plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("RÉSUMÉ DES ANALYSES")
print("=" * 60)

# Statistiques récapitulatives
total_fioul_2021 = sum(fioul_par_type_logement[2021].values(
)) if 2021 in fioul_par_type_logement else 0
print(f"Nombre total de logements au fioul en 2021 : {total_fioul_2021:.0f}")

if 2021 in fioul_par_type_logement:
    print("\nRépartition par type de logement en 2021 :")
    for type_log, count in fioul_par_type_logement[2021].items():
        type_name = TYPES_LOGEMENTS.get(type_log, f"Type {type_log}")
        pourcentage = (count / total_fioul_2021 *
                       100) if total_fioul_2021 > 0 else 0
        print(f"  {type_name}: {count:.0f} logements ({pourcentage:.1f}%)")

print("\nDonnées sauvegardées dans le dossier 'results/' :")
print("- fioul_par_annee_emmenagement.json")
print("- fioul_par_type_logement.json")
