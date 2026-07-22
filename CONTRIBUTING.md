# Contributing to Adaptive Explainable Predictive Maintenance

Thank you for your interest in contributing to our open-source industrial AI project!

---

## 🚀 Getting Started

1. **Fork the Repository**: Create your personal fork on GitHub.
2. **Clone Locally**:
   ```bash
   git clone https://github.com/<your-username>/adaptive-explainable-predictuve-maintenance.git
   cd adaptive-explainable-predictuve-maintenance
   ```
3. **Set Up Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## 🛠️ Coding Standards & Verification

All pull requests must pass static quality checks before merging:

1. **PEP8 Formatting & Linting (Ruff)**:
   ```bash
   ruff format src/ tests/
   ruff check src/ tests/
   ```
2. **Static Typing (MyPy)**:
   ```bash
   mypy src/
   ```
3. **Unit Tests (Pytest)**:
   ```bash
   pytest tests/
   ```

---

## 📬 Pull Request Process

1. Create a descriptive feature branch (`git checkout -b feat/your-feature`).
2. Commit your changes with clear conventional commit messages (`feat: ...`, `fix: ...`, `docs: ...`).
3. Ensure all automated GitHub Actions CI checks pass.
4. Open a Pull Request referencing relevant issue IDs.
