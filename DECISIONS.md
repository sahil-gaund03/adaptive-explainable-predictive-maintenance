# Architectural & Research Decisions (DECISIONS.md)

This file tracks the key technical and methodology decisions made during the R&D cycle.

## D1: Combination Novelty Scope
- **Status**: Approved
- **Decided on**: 2026-07-21
- **Context**: Resolves the scope of R&D for an undergraduate paper.
- **Decision**: Focus on the system-level integration of cost-sensitive classification, ensemble consensus drift detection, and counterfactual explanation stability. No new algorithms will be designed from scratch.
- **Rationale**: Combining these individually verified methods into a unified framework addressing dynamic drift settings constitutes high novelty for ICTAI/IJCNN conferences.

## D2: Drift Simulation Protocol
- **Status**: Approved
- **Decided on**: 2026-07-21
- **Context**: The Scania APS dataset lacks temporal/timestamp data.
- **Decision**: Simulate abrupt and gradual concept drift by shuffling the dataset, treating it as a stream, and injecting scaled standard deviation shifts ($\delta$) into the top-k most important features (based on SHAP baseline values) at midpoint index ($t_d=30000$).
- **Rationale**: Standard method in drift detection literature when genuine chronological sensor drift is unavailable.

## D3: Retraining Strategy
- **Status**: Approved
- **Decided on**: 2026-07-21
- **Context**: Full vs. incremental model updates.
- **Decision**: Primary retraining strategy is incremental (adding estimators to XGBoost with reduced learning rate). Baseline comparison uses sliding window retraining from scratch.
- **Rationale**: Compares training overhead and knowledge retention (avoiding catastrophic forgetting).

## D4: Scope Exclusions
- **Status**: Approved
- **Decided on**: 2026-07-21
- **Context**: Reducing risk of scope creep.
- **Decision**: Exclude deep learning, causal inference, and uncertainty quantification. Demote Streamlit dashboard to Tier 3 (optional).
- **Rationale**: Keeps execution timeline focused strictly on publication-critical deliverables.
