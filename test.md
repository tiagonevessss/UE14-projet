```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file = "data/melun/melun_2010.csv"
df = pd.read_csv(file, sep=';', usecols=["CMBL", "IPONDL", "AEMM", "TYPL"])

# Conversion en numérique
df["CMBL"] = pd.to_numeric(df["CMBL"], errors="coerce")
df["IPONDL"] = df["IPONDL"].str.replace(",", ".")
df["IPONDL"] = pd.to_numeric(df["IPONDL"], errors="coerce")
df["AEMM"] = pd.to_numeric(df["AEMM"], errors="coerce")
df["TYPL"] = pd.to_numeric(df["TYPL"], errors="coerce")

# Filtrer uniquement les logements au fioul
df_fioul = df[df["CMBL"] == 3].copy()
```

```python
df_fioul["IPONDL"]
```

```python

```
