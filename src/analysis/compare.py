"""Matched-seed P0 vs P1 comparison: per-seed change, then average change and range across 5 seeds."""


def compare_policies(p0_metrics, p1_metrics):
    """Compute P1 minus P0 for each metric.

    Args:
        p0_metrics: dict from compute_metrics for P0
        p1_metrics: dict from compute_metrics for P1

    Returns:
        dict of metric_name -> change (P1 - P0)
    """
    changes = {}
    for key in p0_metrics:
        if isinstance(p0_metrics[key], (int, float)) and isinstance(p1_metrics.get(key), (int, float)):
            changes[key] = p1_metrics[key] - p0_metrics[key]
    return changes


def aggregate_comparisons(comparisons_list):
    """Compute mean and range of changes across multiple seeds.

    Args:
        comparisons_list: list of dicts from compare_policies (one per seed)

    Returns:
        dict with 'mean' and 'range' sub-dicts for each metric
    """
    if not comparisons_list:
        return {}

    keys = comparisons_list[0].keys()
    result = {'mean': {}, 'range': {}, 'per_seed': comparisons_list}

    for key in keys:
        values = [c[key] for c in comparisons_list if key in c and isinstance(c[key], (int, float))]
        if values:
            result['mean'][key] = sum(values) / len(values)
            result['range'][key] = {
                'min': min(values),
                'max': max(values),
                'spread': max(values) - min(values),
            }

    return result
