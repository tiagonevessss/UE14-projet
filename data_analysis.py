import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn-v0_8')

# types de combustibles
COMBUSTIBLES = {
    1: "Chauffage urbain",
    2: "Gaz de ville/réseau",
    3: "Fioul (mazout)",
    4: "Électricité",
    5: "Gaz bouteille/citerne",
    6: "Autre"
}

directory = "data/melun/"

# =============================================================================
# ANALYSE DU FIOUL
# =============================================================================

counts_fioul = {}
total_logements = {}

for year in range(2010, 2022):
    file = f"{directory}/melun_{year}.csv"
    df = pd.read_csv(file, sep=';')
    df["CMBL"] = pd.to_numeric(df["CMBL"], errors="coerce")

    counts_fioul[year] = (df["CMBL"] == 3).sum()
    total_logements[year] = len(df)

# df pour le fioul
result_fioul = pd.DataFrame.from_dict(counts_fioul, orient='index', columns=[
                                      "Nombre de logements au fioul"])
result_fioul["Total logements"] = pd.Series(total_logements)
result_fioul["Pourcentage fioul"] = (
    result_fioul["Nombre de logements au fioul"] / result_fioul["Total logements"] * 100).round(2)

# graphe 1 : nombre absolu de logements au fioul
plt.figure(figsize=(12, 8))
plt.plot(result_fioul.index, result_fioul["Nombre de logements au fioul"],
         marker='o', linewidth=2, markersize=6, color='red', label='Logements au fioul')
plt.title('Evolution du nombre de logements utilisant le fioul\n(Melun, 2010-2021)', fontsize=14)
plt.xlabel('Année')
plt.ylabel('Nombre de logements')
plt.grid(True, alpha=0.3)
plt.legend()
plt.xticks(result_fioul.index)
plt.tight_layout()
plt.show()

# graph 2 : pourcentage de logements au fioul
plt.figure(figsize=(12, 8))
plt.plot(result_fioul.index, result_fioul["Pourcentage fioul"],
         marker='s', linewidth=2, markersize=6, color='darkred', label='% de logements au fioul')
plt.title('Evolution en pourcentage des logements utilisant le fioul', fontsize=14)
plt.xlabel('Année')
plt.ylabel('Pourcentage (%)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.xticks(result_fioul.index)
plt.tight_layout()
plt.show()

# =============================================================================
# ANALYSE DE TOUS LES COMBUSTIBLES
# =============================================================================

counts_by_cmbl = {}
total_by_year = {}

for year in range(2010, 2022):
    file = f"{directory}/melun_{year}.csv"
    df = pd.read_csv(file, sep=';')
    df["CMBL"] = pd.to_numeric(df["CMBL"], errors="coerce")

    counts = df["CMBL"].value_counts().sort_index()
    counts_by_cmbl[year] = counts
    total_by_year[year] = len(df)


result_complet = pd.DataFrame.from_dict(counts_by_cmbl, orient='index')
result_complet = result_complet.fillna(0)


result_complet.columns = [COMBUSTIBLES.get(
    col, f"Inconnu ({col})") for col in result_complet.columns]


result_pourcentage = (result_complet.div(
    pd.Series(total_by_year), axis=0) * 100).round(2)

# graphe 3 : évolution en pourcentage
plt.figure(figsize=(14, 8))
plt.stackplot(result_pourcentage.index, result_pourcentage.T,
              labels=result_pourcentage.columns, alpha=0.8)
plt.title('Répartition proportionnelle des combustibles (%)', fontsize=14)
plt.xlabel('Année')
plt.ylabel('Pourcentage (%)')
plt.grid(True, alpha=0.3)
plt.legend(title='Type de combustible',
           bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(result_pourcentage.index)
plt.tight_layout()
plt.show()
