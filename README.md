# Order Total Reconciliation Agent

Reconciles order line extensions, discount, tax, and payable total using integer minor currency units.

## Architecture

```text
JSON payload → domain algorithm → evidence-backed findings → human review
                              └→ OpenAI / CrewAI / Claude Code / Lyzr export surfaces
```

The core implementation is `agent.py` and exposes `analyze(payload)`. Tests include valid, malformed, boundary, and domain-specific cases.

## Run

```bash
python3 agent.py examples/good-input.json
python3 -m unittest discover -s tests -v
python3 tools/audit-order-total-reconciliation-agent.py examples/good-input.json
```

## Limitations

This is arithmetic validation only. It does not determine tax law, refund eligibility, payment settlement, or whether a price is commercially correct.
