## Summary

Describe the change and why it is needed.

## Validation

- [ ] `finsec-eval validate --dataset datasets/v0.2/cases.jsonl`
- [ ] `python scripts/build_v0_2_dataset.py` leaves generated copies unchanged
- [ ] `python -m unittest discover -s tests -v`
- [ ] Generated schema still matches the committed schema.

## Dataset and safety checks

- [ ] No real secrets, personal data, customer information, financial records,
      or confidential institutional details are included.
- [ ] New or changed cases have provenance, expected behavior, severity, and
      review status.
- [ ] Critical failures remain visible and cannot be hidden by aggregate scores.
- [ ] Licensing is compatible with the file or dataset being changed.

## Review notes

List any semantic judgments, open questions, or independent review still
required.
