import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os

plt.style.use('seaborn-v0_8')

zone = "A"
results_dir = f'results/{zone}'

FIRST_YEAR = 2010
LAST_YEAR = 2022

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

with open(f'{results_dir}/fioul_par_annee_emmenagement.json', 'r', encoding='utf-8') as f:
    data_raw = json.load(f)
    fioul_par_annee_emmenagement = {
        int(k): {int(ki): vi for ki, vi in v.items()} for k, v in data_raw.items()}

with open(f'{results_dir}/fioul_par_type_logement.json', 'r', encoding='utf-8') as f:
    data_raw_type = json.load(f)
    fioul_par_type_logement = {
        int(k): {int(ki): vi for ki, vi in v.items()} for k, v in data_raw_type.items()}

print("=" * 60)
print("LOGEMENTS AU FIOUL PAR ANNÉE D'EMMÉNAGEMENT")
print("=" * 60)

all_annees_emm = set()
for year_data in fioul_par_annee_emmenagement.values():
    all_annees_emm.update(year_data.keys())
all_annees_emm = sorted([a for a in all_annees_emm if a >= 1950])

df_fioul_emm_cumul = pd.DataFrame(index=all_annees_emm)
for year in range(FIRST_YEAR, LAST_YEAR):
    year_data = fioul_par_annee_emmenagement.get(year, {})
    counts = [year_data.get(annee, 0) for annee in all_annees_emm]
    df_fioul_emm_cumul[year] = counts

plt.figure(figsize=(16, 10))
plt.imshow(df_fioul_emm_cumul.T, cmap='YlOrRd', aspect='auto',
           extent=[min(all_annees_emm), max(all_annees_emm), LAST_YEAR - 1, FIRST_YEAR])
plt.colorbar(label='Nombre de logements au fioul (pondéré)')
plt.xlabel('Année d\'emménagement')
plt.ylabel('Année de l\'enquête')
plt.title(
    f'Logements au fioul par année d\'emménagement\n(Zone {zone}, {FIRST_YEAR}-{LAST_YEAR - 1})', fontsize=14)
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

current_analysis_year = LAST_YEAR - 1
if current_analysis_year in fioul_par_annee_emmenagement:
    data_last_year = fioul_par_annee_emmenagement[current_analysis_year]
    annees_emm_last = sorted(
        [k for k in data_last_year.keys() if k >= 1950 and data_last_year[k] > 0])
    counts_last = [data_last_year[k] for k in annees_emm_last]

    plt.figure(figsize=(14, 8))
    plt.bar(annees_emm_last, counts_last, alpha=0.7,
            color='red', edgecolor='darkred')
    plt.title(
        f'Logements au fioul par année d\'emménagement\n(Enquête {current_analysis_year} - Zone {zone})', fontsize=14)
    plt.xlabel('Année d\'emménagement')
    plt.ylabel('Nombre de logements au fioul (pondéré)')
    plt.grid(True, alpha=0.3, axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

decennies = ['1950-1959', '1960-1969', '1970-1979', '1980-1989',
             '1990-1999', '2000-2009', '2010-2019', '2020-2021']

fioul_par_decennie = {dec: [] for dec in decennies}
years_survey = list(range(FIRST_YEAR, LAST_YEAR))

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

plt.title(
    f'Évolution des logements au fioul par décennie d\'emménagement\n(Zone {zone}, {FIRST_YEAR}-{LAST_YEAR - 1})', fontsize=14)
plt.xlabel('Année de l\'enquête')
plt.ylabel('Nombre de logements au fioul (pondéré)')
plt.grid(True, alpha=0.3)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
           title='Décennie d\'emménagement')
plt.xticks(years_survey)
plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("LOGEMENTS AU FIOUL PAR TYPE DE LOGEMENT")
print("=" * 60)

fioul_par_type_combined = {}
for type_log in TYPES_LOGEMENTS.keys():
    fioul_par_type_combined[type_log] = []
    for year in range(FIRST_YEAR, LAST_YEAR):
        data = fioul_par_type_logement.get(year, {})
        fioul_par_type_combined[type_log].append(data.get(type_log, 0))

plt.figure(figsize=(12, 8))
for type_log, counts in fioul_par_type_combined.items():
    type_name = TYPES_LOGEMENTS[type_log]
    plt.plot(range(FIRST_YEAR, LAST_YEAR), counts, marker='o', linewidth=2,
             label=type_name, markersize=6)

plt.title(
    f'Évolution des logements au fioul par type de logement\n(Zone {zone}, {FIRST_YEAR}-{LAST_YEAR - 1})', fontsize=14)
plt.xlabel('Année')
plt.ylabel('Nombre de logements au fioul (pondéré)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.xticks(range(FIRST_YEAR, LAST_YEAR))
plt.tight_layout()
plt.show()

if current_analysis_year in fioul_par_type_logement:
    data_last_types = fioul_par_type_logement[current_analysis_year]
    labels = [TYPES_LOGEMENTS.get(k, f"Type {k}")
              for k in data_last_types.keys()]
    sizes = [data_last_types[k] for k in data_last_types.keys()]
    total_last = sum(sizes)

    plt.figure(figsize=(10, 8))
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    wedges, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.1f%%',
                                       colors=colors, startangle=90)

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    plt.title(f'Répartition des logements au fioul par type de logement\n(Enquête {current_analysis_year} - Total: {total_last:.0f} logements)',
              fontsize=14)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

df_fioul_types = pd.DataFrame(fioul_par_type_combined)
df_fioul_types.index = range(FIRST_YEAR, LAST_YEAR)
df_fioul_types.columns = [TYPES_LOGEMENTS[col]
                          for col in df_fioul_types.columns]

plt.figure(figsize=(14, 8))
plt.stackplot(df_fioul_types.index, df_fioul_types.T,
              labels=df_fioul_types.columns, alpha=0.8)
plt.title(
    f'Évolution cumulée des logements au fioul par type de logement\n(Zone {zone}, {FIRST_YEAR}-{LAST_YEAR - 1})', fontsize=14)
plt.xlabel('Année')
plt.ylabel('Nombre de logements au fioul (pondéré)')
plt.grid(True, alpha=0.3)
plt.legend(title='Type de logement')
plt.xticks(range(FIRST_YEAR, LAST_YEAR))
plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("RÉSUMÉ DES ANALYSES")
print("=" * 60)

total_fioul_last = sum(fioul_par_type_logement[current_analysis_year].values(
)) if current_analysis_year in fioul_par_type_logement else 0
print(
    f"Nombre total de logements au fioul en {current_analysis_year} : {total_fioul_last:.0f}")

if current_analysis_year in fioul_par_type_logement:
    print(f"\nRépartition par type de logement en {current_analysis_year} :")
    for type_log, count in fioul_par_type_logement[current_analysis_year].items():
        type_name = TYPES_LOGEMENTS.get(type_log, f"Type {type_log}")
        pourcentage = (count / total_fioul_last *
                       100) if total_fioul_last > 0 else 0
        print(f"  {type_name}: {count:.0f} logements ({pourcentage:.1f}%)")
