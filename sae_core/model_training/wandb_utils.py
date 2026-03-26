from pathlib import Path
from typing import Any, Dict, Optional


def _serialize_for_wandb(value: Any) -> Any:
    """Convert common local types into W&B-friendly config/summary values."""
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): _serialize_for_wandb(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_serialize_for_wandb(v) for v in value]
    return str(value)


def maybe_init_wandb_run(
    *,
    enabled: bool,
    project: Optional[str],
    entity: Optional[str],
    name: str,
    job_type: str,
    config: Optional[Dict[str, Any]] = None,
    tags: Optional[list[str]] = None,
    group: Optional[str] = None,
    notes: Optional[str] = None,
    mode: Optional[str] = None,
) -> Optional[Any]:
    if not enabled:
        return None

    try:
        import wandb
    except ImportError as exc:
        raise RuntimeError(
            "W&B logging requested but `wandb` is not installed in the active environment."
        ) from exc

    init_kwargs: Dict[str, Any] = {
        "project": project,
        "entity": entity,
        "name": name,
        "job_type": job_type,
        "config": _serialize_for_wandb(config or {}),
        "tags": tags or [],
        "group": group,
        "notes": notes,
    }
    if mode is not None:
        init_kwargs["mode"] = mode

    return wandb.init(**init_kwargs)


def maybe_log_final_artifact(
    run: Optional[Any],
    model_dir: Path,
    artifact_name: str,
    metadata: Optional[Dict[str, Any]] = None,
) -> None:
    if run is None:
        return
    try:
        import wandb
    except ImportError:
        return

    artifact = wandb.Artifact(
        name=artifact_name,
        type="sae-model",
        metadata=_serialize_for_wandb(metadata or {}),
    )
    artifact.add_dir(str(model_dir))
    run.log_artifact(artifact)


def maybe_update_wandb_summary(run: Optional[Any], values: Dict[str, Any]) -> None:
    if run is None:
        return
    serialized = _serialize_for_wandb(values)
    for key, value in serialized.items():
        run.summary[key] = value


def finish_wandb_run(run: Optional[Any]) -> None:
    if run is None:
        return
    try:
        run.finish()
    except Exception as exc:
        print(f"W&B finish warning: {exc}")
