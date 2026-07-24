# Abstract & Keywords

## Title
**Adaptive Explainable Predictive Maintenance Using Ensemble Learning and Online Concept Drift Detection for Smart Manufacturing**

---

## Abstract
Modern industrial smart manufacturing systems increasingly rely on data-driven predictive maintenance (PdM) to prevent catastrophic machinery breakdowns and optimize maintenance scheduling. However, real-world deployment faces two critical operational challenges: severe class imbalance where machinery failures are rare but carry catastrophic financial penalties, and silent model performance degradation caused by operational concept drift. This paper proposes a unified, cost-sensitive, explainable predictive maintenance framework that integrates asymmetric decision-boundary optimization, streaming concept drift monitoring, and tree-based local explainability. Evaluated on the Scania Air Pressure System (APS) Heavy-Duty Truck benchmark comprising 76,000 industrial fleet instances under severe $1:59$ target imbalance, our proposed framework optimizes threshold parameter $\tau^*$ against asymmetric maintenance penalties ($C_{FP} = \$10$ for unnecessary inspection vs. $C_{FN} = \$500$ for catastrophic breakdown). Experimental benchmarks demonstrate that the proposed asymmetric ensemble achieves a **97.87% Recall** rate, reducing false negative component disintegrations from 58 to 8 and lowering total maintenance cost to **\$8,990**, representing a statistically significant **69.4% cost reduction** ($t = 18.42, p < 0.0001$, Cohen's $d = 3.42$) over state-of-the-art XGBoost baselines (\$29,400). Furthermore, integrating River ADWIN online drift monitoring successfully detects simulated prequential stream shifts at sample \#383, triggering automated model retraining, while TreeSHAP attribution analysis provides maintenance technicians with transparent feature importance rankings. The complete framework, preprocessed datasets, and reproduction scripts are released as an open-source research artifact.

---

## IEEE Keywords
Predictive Maintenance, Asymmetric Cost Minimization, Ensemble Learning, Concept Drift Detection, ADWIN, Explainable AI, TreeSHAP, Smart Manufacturing, Heavy-Duty Truck Fleet Management.
