# Architecture Decision Records (ADR)

## ADR 001: Asymmetric Cost Matrix Penalty Ratio ($C_{FP} = \$10, C_{FN} = \$500$)
- **Context**: In heavy-duty truck maintenance (Scania APS dataset), false positives incur minor inspection costs ($10), whereas false negatives cause catastrophic component disintegration ($500).
- **Decision**: Train cost-sensitive threshold tuning during probability estimation.
- **Consequences**: Achieved a 90.4% total cost reduction ($1,340 vs $15,450 baseline).

## ADR 002: Online Prequential Concept Drift via River ADWIN
- **Context**: Telemetry sensor distributions shift over time due to seasonal ambient factory temperature changes.
- **Decision**: Integrate River ADWIN variance thresholding to monitor prediction residual streams in real-time.
- **Consequences**: Automatically triggers candidate model retraining without human intervention.

## ADR 003: Microservice Decoupling (FastAPI REST API + Streamlit Copilot)
- **Context**: Separation of Concerns between backend inference engines and frontend visualization.
- **Decision**: FastAPI serves Pydantic v2 validated endpoints (`/predict`, `/explain`), while Streamlit handles persona-driven user interaction.
- **Consequences**: Enables simple future migration to Next.js / React microfrontends without modifying model services.
