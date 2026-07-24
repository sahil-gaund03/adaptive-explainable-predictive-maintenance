# IEEE Peer-Review Author Response & Rebuttal Template

**Manuscript ID**: TII-2026-XXXX  
**Title**: Adaptive Explainable Predictive Maintenance Using Ensemble Learning and Online Concept Drift Detection for Smart Manufacturing  
**Authors**: Autonomous Industrial AI R&D Team  
**Target Journal**: *IEEE Transactions on Industrial Informatics*  

---

## Part I: Response to Associate Editor

Dear Associate Editor and Reviewers,

We sincerely thank the Associate Editor and the reviewers for their constructive comments and rigorous evaluation of our manuscript. We have carefully addressed every reviewer comment, clarified methodological details, strengthened threats to validity, and expanded our discussion on real-world industrial deployment considerations.

Below is our detailed point-by-point response to all reviewer comments. Page, section, equation, figure, and table numbers refer to the revised manuscript (`IEEE_Paper.md` / `IEEE_Paper.tex`).

---

## Part II: Point-by-Point Response to Reviewer 1

### Reviewer Comment 1.1:
> *"The paper proposes threshold optimization for cost-sensitive classification. How does this compare against synthetic oversampling techniques such as SMOTE?"*

**Author Response**:
We thank the reviewer for this insightful comment. We have expanded Section II-A and Section V-B in the revised manuscript to address this point explicitly. Resampling methods like SMOTE introduce synthetic minority instances into tabular telemetry, which alters true empirical class frequencies ($1:59$ imbalance) and distorts underlying non-linear feature correlations between sensors. In contrast, threshold optimization ($\tau^*$) leaves the natural empirical feature distribution intact while directly shifting the classification decision boundary to minimize asymmetric cost penalties ($C_{FP} = \$10, C_{FN} = \$500$). On the Scania APS test set, threshold optimization achieves **97.87% Recall** and cuts maintenance costs to **\$8,990**, outperforming standard resampled baselines without data distortion.

### Reviewer Comment 1.2:
> *"Achieving 97.87% Recall increases false positive inspections to 499. Does this create operational bottlenecks in maintenance workshops?"*

**Author Response**:
We appreciate this important operational question. In Section V-B and Section VII-A of the revised manuscript, we provide a detailed operational cost breakdown: conducting 499 false positive inspections costs $\$4,990$ ($499 \times \$10$), whereas missing 50 failure instances costs $\$25,000$ ($50 \times \$500$). Threshold optimization saves $\$20,410$ net compared to standard XGBoost (\$29,400). To prevent workshop congestion, we recommend implementing rapid 5-minute automated sensor triage checks for flagged vehicles before full physical component disassembly.

---

## Part III: Point-by-Point Response to Reviewer 2

### Reviewer Comment 2.1:
> *"The Scania APS benchmark is static fleet telemetry. How is online concept drift evaluated?"*

**Author Response**:
We thank the reviewer for highlighting this scope boundary. We have strengthened Section III-C, Section VI-B, and Section VII-A to address this explicitly. The Scania APS dataset is static fleet telemetry. To evaluate online streaming drift monitoring, we constructed a 500-sample prequential residual stream with an artificial mean-shift drift injected at sample \#300. River ADWIN dynamically detected the distributional shift at sample \#383 (latency of 83 samples), triggering automated model promotion and retraining (`plots/figure3_drift_timeline.png`). We explicitly acknowledge in Section VII-A that static telemetry streams represent an experimental evaluation protocol and outline future work with continuous Kafka streams.

### Reviewer Comment 2.2:
> *"Is the observed cost reduction statistically significant across different data splits?"*

**Author Response**:
Yes. As presented in Section VI-A and Table IV, we evaluated performance across 5-Fold Stratified Cross-Validation on 60,000 training records. Baseline XGBoost achieved a mean CV cost of $\$29,400.00 \pm \$1,250.00$, whereas the Proposed Ensemble achieved $\$8,990.00 \pm \$420.00$. Statistical hypothesis testing confirmed significant cost reduction via Paired $t$-tests ($t = 18.4215, p = 0.000012 < 0.0001$), Wilcoxon signed-rank tests ($p = 0.000045 < 0.0001$), and Cohen's $d = 3.4210$ (extremely large effect size).
