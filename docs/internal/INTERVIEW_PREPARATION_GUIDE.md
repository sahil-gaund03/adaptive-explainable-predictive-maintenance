# INTERVIEW PREPARATION GUIDE

This guide provides model answers based on the Predictive Maintenance project for various interview domains.

## HR Questions (Selection of 30)
*Focus: Behavioral, teamwork, and project management.*
1. **Tell me about a challenging project.** -> Discuss the Scania APS project, focusing on balancing academic rigor with industrial cost constraints.
2. **How do you handle competing priorities?** -> Discuss balancing model accuracy with explainability (SHAP) and inference latency.
3. **Describe a time you failed.** -> Discuss initial attempts using SMOTE that failed to reduce actual costs, leading to the threshold optimization breakthrough.
*(Answers structure for HR: Use STAR method - Situation (Imbalance), Task (Reduce Cost), Action (Asymmetric thresholding), Result (69.4% cost reduction)).*
*(Questions 4-30: Standard behavioral covering communication of SHAP results to non-technical stakeholders, handling deployment issues, and open-source contribution).*

## Machine Learning Questions (Selection of 50)
*Focus: Imbalanced data, tree ensembles, and cost-sensitive learning.*
1. **Q: Why does standard binary cross-entropy fail on imbalanced data?**
   **A:** It optimizes for overall accuracy. With 98% negative class, the model minimizes loss by predicting negative everywhere, missing the crucial positive class.
2. **Q: Compare XGBoost, LightGBM, and CatBoost.**
   **A:** XGBoost grows trees level-wise, LightGBM grows leaf-wise (faster, prone to overfit), CatBoost uses symmetric trees and handles categorical features natively.
3. **Q: What is the difference between hard and soft voting?**
   **A:** Hard voting uses majority class labels. Soft voting averages class probabilities, which is essential for applying custom decision thresholds ($\tau^*$).
4. **Q: How does SMOTE distort empirical priors?**
   **A:** Generating synthetic minority samples changes the base rate (e.g., from 1% to 50%). When predicting on true distributions, the model outputs uncalibrated, overconfident probabilities.
*(Questions 5-50: Cover ROC vs PR curves, calibration (Platt scaling), Gini impurity vs Entropy, gradient boosting math, cross-validation strategies for time-series vs tabular data).*

## Python Questions (Selection of 30)
*Focus: Tooling, pandas, and software design.*
1. **Q: How do you handle missing data in Pandas efficiently?**
   **A:** Vectorized operations like `df.fillna(df.median())` rather than iterating. In ML pipelines, use `sklearn.impute.SimpleImputer`.
2. **Q: What are decorators and how did you use them?**
   **A:** Functions that modify other functions. Used in FastAPI for routing (`@app.post`) and Streamlit for caching (`@st.cache_resource`).
3. **Q: What is the GIL and does it affect your models?**
   **A:** The Global Interpreter Lock prevents multiple native threads from executing Python bytecodes simultaneously. ML libraries like XGBoost bypass the GIL using C++ backends.
*(Questions 4-30: Cover iterators, generators (useful for streaming data to ADWIN), context managers, Pydantic validation, and multiprocessing).*

## Software Engineering Questions (Selection of 30)
*Focus: MLOps, Docker, and Architecture.*
1. **Q: Explain your Docker Compose architecture.**
   **A:** Orchestrates multiple microservices: a FastAPI backend serving the model, a Streamlit frontend for the UI, and an MLflow server for metric tracking, ensuring isolated but communicative networks.
2. **Q: How do you handle state in a REST API?**
   **A:** REST is stateless. For ML, the model artifact is loaded into memory on startup, and each request is treated independently. Drift detection requires external state stores (e.g., Redis) if distributed.
3. **Q: What is the purpose of Pydantic in FastAPI?**
   **A:** It enforces strict type hinting and data validation at runtime, rejecting malformed JSON payloads before they hit the ML model.
*(Questions 4-30: Cover CI/CD, Git workflows, unit testing vs integration testing, API versioning, and latency optimization).*

## Research Methodology Questions (Selection of 30)
*Focus: Experimental design and statistics.*
1. **Q: Why use a paired t-test over an independent t-test for CV folds?**
   **A:** Because the models are evaluated on the exact same folds (paired data), controlling for the variance introduced by the specific data split.
2. **Q: What does a Cohen's d of 3.42 indicate?**
   **A:** A massive effect size. A value > 0.8 is considered large. 3.42 means the means are separated by over 3 standard deviations.
3. **Q: How did you ensure construct validity?**
   **A:** By directly utilizing the canonical $10/$500 cost matrix provided by the Scania APS challenge, ensuring our optimization metric mirrored reality.
*(Questions 4-30: Cover null hypothesis formulations, non-parametric alternatives, ablation study designs, and addressing internal/external validity threats).*

## Explainable AI (XAI) Questions (Selection of 20)
*Focus: SHAP, LIME, and Interpretability.*
1. **Q: What are Shapley values theoretically?**
   **A:** A concept from cooperative game theory that fairly distributes the total payout (prediction) among players (features) based on their marginal contributions.
2. **Q: TreeSHAP vs KernelSHAP?**
   **A:** TreeSHAP exploits the internal structure of tree ensembles for exact, fast computation. KernelSHAP is model-agnostic but relies on slow, perturbation-based approximation.
3. **Q: How does a waterfall plot differ from a summary plot?**
   **A:** Waterfall explains a *single local prediction* by showing how features push the base value to the final output. Summary plots show *global* feature importance across the dataset.
*(Questions 4-20: Cover DiCE counterfactuals, fidelity vs interpretability tradeoff, and adversarial robustness of explanations).*

## Concept Drift Questions (Selection of 20)
*Focus: Streaming data and adaptation.*
1. **Q: Define virtual vs real concept drift.**
   **A:** Virtual drift is a change in $P(X)$ without changing decision boundaries. Real drift is a change in $P(y|X)$, which degrades model accuracy.
2. **Q: How does ADWIN dynamically adjust its window?**
   **A:** It grows the window when the distribution is stable to increase statistical confidence, and shrinks it rapidly when a significant mean difference is detected.
3. **Q: Why monitor residuals instead of feature distributions?**
   **A:** Monitoring 163 features causes false alarms (virtual drift). Monitoring the error residual $e_t = |y_t - \hat{y}_t|$ ensures we only trigger retraining when predictive performance actually degrades.
*(Questions 4-20: Cover Page-Hinkley, prequential evaluation limits, catastrophic forgetting, and gradual vs sudden drift).*

*(Note: The above serves as the master blueprint for answering interview questions derived from the APS Predictive Maintenance Project, specifically tailored to demonstrate deep competence in both theory and engineering implementation).*
