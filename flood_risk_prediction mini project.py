import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, roc_curve, confusion_matrix,
                             classification_report)

np.random.seed(42)

# ============================================================
# 1. DATA GENERATION
# ============================================================
def generate_data(n=3000):
    df = pd.DataFrame({
        "Rainfall_mm":        np.random.uniform(0, 400, n),
        "River_Level_m":      np.random.uniform(0, 12, n),
        "Soil_Moisture_%":    np.random.uniform(5, 100, n),
        "Humidity_%":         np.random.uniform(30, 100, n),
        "Temperature_C":      np.random.uniform(18, 40, n),
        "Elevation_m":        np.random.uniform(0, 300, n),
        "Drainage_Index":     np.random.uniform(0, 1, n),
        "Population_Density": np.random.uniform(50, 5000, n),
        "Wind_Speed_kmph":    np.random.uniform(0, 90, n),
        "Dam_Release_Cusecs": np.random.uniform(0, 50000, n),
    })
    score = (0.32 * df["Rainfall_mm"] / 400
             + 0.22 * df["River_Level_m"] / 12
             + 0.13 * df["Soil_Moisture_%"] / 100
             + 0.05 * df["Humidity_%"] / 100
             + 0.05 * df["Wind_Speed_kmph"] / 90
             + 0.08 * df["Dam_Release_Cusecs"] / 50000
             - 0.10 * df["Elevation_m"] / 300
             - 0.10 * df["Drainage_Index"]
             + np.random.normal(0, 0.05, n))
    df["Flood"] = (score > 0.40).astype(int)
    # introduce a few missing values to show data cleaning
    for col in ["Soil_Moisture_%", "Humidity_%", "Wind_Speed_kmph"]:
        df.loc[df.sample(frac=0.02).index, col] = np.nan
    return df

data = generate_data()

print("=" * 66)
print("        AI-BASED FLOOD RISK PREDICTION SYSTEM")
print("=" * 66)

# ============================================================
# 2. DATA EXPLORATION & CLEANING
# ============================================================
print(f"\nDataset shape : {data.shape}")
print("\nMissing values before cleaning:")
print(data.isnull().sum()[data.isnull().sum() > 0].to_string())

data = data.fillna(data.median())
print("\nMissing values after cleaning :", int(data.isnull().sum().sum()))

print("\nStatistical summary:")
print(data.describe().T[["mean", "std", "min", "max"]].round(2).to_string())

print("\nClass distribution:")
print(data["Flood"].value_counts().rename({0: "No Flood", 1: "Flood"}).to_string())

print("\nTop correlations with Flood:")
corr = data.corr()["Flood"].drop("Flood").sort_values(ascending=False)
print(corr.round(3).to_string())

# ============================================================
# 3. TRAIN / TEST SPLIT
# ============================================================
X = data.drop("Flood", axis=1)
y = data["Flood"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# ============================================================
# 4. MODEL TRAINING & COMPARISON
# ============================================================
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree":       DecisionTreeClassifier(max_depth=6, random_state=42),
    "KNN":                 KNeighborsClassifier(n_neighbors=7),
    "Random Forest":       RandomForestClassifier(n_estimators=200, random_state=42),
    "Gradient Boosting":   GradientBoostingClassifier(random_state=42),
}

rows = []
for name, m in models.items():
    m.fit(X_train_s, y_train)
    pred = m.predict(X_test_s)
    prob = m.predict_proba(X_test_s)[:, 1]
    cv = cross_val_score(m, X_train_s, y_train, cv=5).mean()
    rows.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, pred),
        "Precision": precision_score(y_test, pred),
        "Recall": recall_score(y_test, pred),
        "F1": f1_score(y_test, pred),
        "AUC": roc_auc_score(y_test, prob),
        "CV(5)": cv,
    })

results = pd.DataFrame(rows).set_index("Model")
print("\n" + "-" * 66)
print("MODEL COMPARISON")
print("-" * 66)
print(results.round(4).to_string())

# ============================================================
# 5. HYPERPARAMETER TUNING
# ============================================================
print("\n" + "-" * 66)
print("HYPERPARAMETER TUNING (Random Forest, GridSearchCV)")
print("-" * 66)
grid = GridSearchCV(
    RandomForestClassifier(random_state=42),
    {"n_estimators": [100, 200], "max_depth": [6, 10, None],
     "min_samples_split": [2, 5]},
    cv=3, scoring="f1", n_jobs=-1)
grid.fit(X_train_s, y_train)
print("Best parameters :", grid.best_params_)
print(f"Best CV F1      : {grid.best_score_:.4f}")

best_model = grid.best_estimator_
best_pred = best_model.predict(X_test_s)
best_prob = best_model.predict_proba(X_test_s)[:, 1]

print(f"\nTuned model accuracy : {accuracy_score(y_test, best_pred) * 100:.2f}%")
print(f"Tuned model AUC      : {roc_auc_score(y_test, best_prob):.4f}")
print("\nConfusion Matrix:\n", confusion_matrix(y_test, best_pred))
print("\nClassification Report:\n",
      classification_report(y_test, best_pred, target_names=["No Flood", "Flood"]))

# ============================================================
# 6. FEATURE IMPORTANCE
# ============================================================
imp = pd.Series(best_model.feature_importances_, index=X.columns).sort_values(ascending=False)
print("Feature Importance:")
for f, v in imp.items():
    print(f"  {f:<20} {'#' * int(v * 60):<25} {v:.3f}")

# ============================================================
# 7. VISUALIZATION DASHBOARD
# ============================================================
fig, ax = plt.subplots(2, 2, figsize=(13, 10))
fig.suptitle("AI-Based Flood Risk Prediction - Dashboard", fontsize=15, fontweight="bold")

imp.sort_values().plot(kind="barh", ax=ax[0, 0], color="#1f77b4")
ax[0, 0].set_title("Feature Importance")

for name, m in models.items():
    fpr, tpr, _ = roc_curve(y_test, m.predict_proba(X_test_s)[:, 1])
    ax[0, 1].plot(fpr, tpr, label=f"{name}")
ax[0, 1].plot([0, 1], [0, 1], "k--")
ax[0, 1].set_title("ROC Curves")
ax[0, 1].set_xlabel("False Positive Rate")
ax[0, 1].set_ylabel("True Positive Rate")
ax[0, 1].legend(fontsize=8)

cm = confusion_matrix(y_test, best_pred)
ax[1, 0].imshow(cm, cmap="Blues")
ax[1, 0].set_title("Confusion Matrix (Tuned RF)")
ax[1, 0].set_xticks([0, 1]); ax[1, 0].set_yticks([0, 1])
ax[1, 0].set_xticklabels(["No Flood", "Flood"]); ax[1, 0].set_yticklabels(["No Flood", "Flood"])
for i in range(2):
    for j in range(2):
        ax[1, 0].text(j, i, cm[i, j], ha="center", va="center", fontsize=14)

ax[1, 1].scatter(data["Rainfall_mm"], data["River_Level_m"], c=data["Flood"],
                 cmap="coolwarm", s=8, alpha=0.6)
ax[1, 1].set_title("Rainfall vs River Level (red = Flood)")
ax[1, 1].set_xlabel("Rainfall (mm)")
ax[1, 1].set_ylabel("River Level (m)")

plt.tight_layout()
plt.savefig("flood_dashboard.png", dpi=120)
print("\nDashboard saved as flood_dashboard.png")

# ============================================================
# 8. RISK PREDICTION FOR NEW LOCATIONS
# ============================================================
def risk_level(p):
    if p < 0.30: return "LOW"
    if p < 0.60: return "MEDIUM"
    if p < 0.85: return "HIGH"
    return "SEVERE"

def predict_flood(values):
    sample = pd.DataFrame([values], columns=X.columns)
    p = best_model.predict_proba(scaler.transform(sample))[0][1]
    return p, risk_level(p)

# order: Rain, River, Soil, Humidity, Temp, Elev, Drain, Pop, Wind, Dam
locations = {
    "Chennai Coastal Area": (320, 9.5, 90, 92, 28, 8,   0.2, 4500, 60, 30000),
    "Hill Station Village": (120, 2.0, 50, 70, 22, 250, 0.8, 300,  15, 2000),
    "River Bank Town":      (280, 10.5, 85, 88, 30, 20, 0.3, 2800, 45, 40000),
    "Dry Plateau Region":   (30,  1.0, 15, 40, 36, 200, 0.7, 150,  10, 500),
    "Suburban Colony":      (180, 6.0, 65, 78, 31, 60,  0.5, 3200, 30, 12000),
    "Delta Farmland":       (230, 8.0, 80, 85, 29, 15,  0.4, 900,  40, 25000),
}

print("\n" + "=" * 66)
print("FLOOD RISK PREDICTION FOR NEW LOCATIONS")
print("=" * 66)
print(f"{'Location':<24}{'Probability':<14}{'Risk Level'}")
print("-" * 66)
preds = {}
for loc, vals in locations.items():
    p, lvl = predict_flood(vals)
    preds[loc] = (p, lvl)
    print(f"{loc:<24}{p * 100:>6.1f}%      {lvl}")

# ============================================================
# 9. ALERT & ACTION SYSTEM
# ============================================================
actions = {
    "SEVERE": "Immediate evacuation. Alert disaster response team.",
    "HIGH":   "Evacuation advisory. Open relief camps.",
    "MEDIUM": "Stay alert. Monitor river and dam levels.",
    "LOW":    "No action needed.",
}
print("\nALERTS & RECOMMENDED ACTIONS:")
for loc, (p, lvl) in preds.items():
    print(f"  [{lvl:<6}] {loc:<22} -> {actions[lvl]}")

# ============================================================
# 10. SUMMARY
# ============================================================
print("\n" + "=" * 66)
print("SUMMARY")
print("=" * 66)
print(f"Total records        : {len(data)}")
print(f"Features used        : {X.shape[1]}")
print(f"Best algorithm       : Random Forest (tuned)")
print(f"Final accuracy       : {accuracy_score(y_test, best_pred) * 100:.2f}%")
print(f"Final AUC score      : {roc_auc_score(y_test, best_prob):.4f}")
print(f"Most important factor: {imp.index[0]}")
