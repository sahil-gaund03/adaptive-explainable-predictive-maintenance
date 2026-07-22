#!/usr/bin/env python3
"""
Run Experiments Script.

Executes the evaluation orchestrator for streaming simulation, concept drift injection,
retraining orchestration, and logging to MLflow.
"""

import argparse
import logging
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.orchestration.evaluation import ExperimentOrchestrator
from src.utils.logging_config import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point for running the evaluation experiment."""
    parser = argparse.ArgumentParser(description="Run Adaptive Maintenance Experiments")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/default.yaml",
        help="Path to configuration file.",
    )

    args = parser.parse_args()

    # Initialize logging
    setup_logging()
    logger.info("Starting run_experiments script...")

    config_path = Path(args.config)
    if not config_path.exists():
        logger.error(f"Configuration file not found at {config_path}")
        sys.exit(1)

    try:
        orchestrator = ExperimentOrchestrator(config_path)
        metrics = orchestrator.run_experiment_suite()

        logger.info("\n=== Experiment Summary ===")
        for k, v in metrics.items():
            logger.info(f"  {k}: {v}")

        logger.info("Metrics successfully logged to MLflow.")

    except Exception as e:
        logger.error(f"Error during experiment execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
