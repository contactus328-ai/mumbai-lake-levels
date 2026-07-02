## Summary

<!-- What does this change, and why? For data corrections, cite the source. -->

## Type of change

- [ ] Data update (lake levels, rainfall, or reference figures)
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] CI / tooling

## Checklist

- [ ] `python -m pytest tests/` passes
- [ ] `python -m lakelevels.cli fetch-manual` and `report` run cleanly (if data files changed)
- [ ] Dashboard renders with no errors (if `dashboard.py` changed) — `streamlit run src/lakelevels/dashboard.py`
- [ ] `data/reference_data.json` `_meta.sources` / `_meta.last_updated` updated (if reference figures changed)
