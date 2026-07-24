# Information Architecture Plan: AI Maintenance Copilot

**System Architecture:** Enterprise Industry 4.0 Decision Platform  
**Design Philosophy:** Progressive Disclosure & Workflow-Centric Navigation

---

## 1. Complete User Journeys & Mode Separation

```
                              ┌────────────────────────┐
                              │  AI Maintenance        │
                              │  Copilot System        │
                              └───────────┬────────────┘
                                          │
       ┌──────────────────────────────────┼──────────────────────────────────┐
       ▼                                  ▼                                  ▼
🏢 Operations Mode               🔬 Research Mode               🛠️ Developer Mode
(Plant Managers & Operators)    (IEEE Reviewers & Researchers)     (System Admins & Developers)
─────────────────────────       ─────────────────────────────    ───────────────────────────
1. 🏠 Mission Control           1. 📊 Benchmark Performance      1. ⚙️ Simulation Controls
   (Landing Summary & KPIs)        (ROC / PR / Confusion)           (Cost FP/FN Penalty Sliders)
2. 📊 Machine Profiles          2. 📐 Statistical Significance   2. 🔌 Backend API Health (:8000)
   (Telemetry & Root Cause)        (p-values & Cohen's d)       3. 📜 MLflow Tracking URI
3. 📈 Equipment Behavior Story  3. 🧩 Ablation Matrix            4. 🐛 System Debug Traces
   (Plain English Drift Story)  4. 🖼️ Publication Figures        5. 🗂️ Dataset Hash Integrity
```

---

## 2. Progressive Disclosure Rules

To prevent cognitive overload, information is disclosed across 4 progressive tiers:

```
[ Tier 1: Situation ]     -->  Good Morning. Factory Status: Healthy. (Mission Control)
         │
[ Tier 2: Insight ]       -->  Machine #17 has 94% failure risk due to vibration. (Copilot Card)
         │
[ Tier 3: Recommendation]-->  Inspect bearing seal within 24 hours. (Priority Action Stack)
         │
[ Tier 4: Evidence ]      -->  Translated SHAP (+42% Vibration) / Research Mode Metrics.
```

---

## 3. Terminology Mapping Dictionary

| Internal Code Symbol | Exposed in Operations Mode | Exposed in Research Mode | Exposed in Developer Mode |
|:---|:---|:---|:---|
| `concept_drift` | "Changes in Machine Behaviour" | "River ADWIN Drift Window" | `detector.update(residual)` |
| `shap_values` | "Why the AI made this prediction" | "TreeSHAP Attributions" | `explainer.shap_values(X)` |
| `inference` | "Latest Machine Assessment" | "Model Inference Runtime" | `api/v1/predict` |
| `residual_score` | "Prediction Confidence" | "Prequential Residual Error" | `np.abs(y_true - y_pred)` |
| `cost_fp` / `cost_fn` | Hidden (Represented as ROI) | Hidden | "Asymmetric FP/FN Ratio" |
