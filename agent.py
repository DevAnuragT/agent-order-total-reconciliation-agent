
#!/usr/bin/env python3
"""Deterministic, local-only passport implementation."""
import json
import math
import sys
from pathlib import Path

DOMAIN = 'Order Total Reconciliation Agent'

def _num(value, name, findings):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        findings.append(f"{name}: must be a finite number")
        return 0
    return value

def analyze(payload):
    if not isinstance(payload, dict):
        raise ValueError("payload must be an object")
    findings = []
    items = payload.get("items"); currency = payload.get("currency")
    if not isinstance(currency, str) or len(currency) != 3 or not currency.isalpha(): raise ValueError("three-letter currency is required")
    if not isinstance(items, list) or not items: raise ValueError("items must be a non-empty list")
    ids=set(); subtotal=0
    for item in items:
        if not isinstance(item, dict): raise ValueError("each item must be an object")
        if not isinstance(item.get("id"), str) or not item["id"] or item["id"] in ids: findings.append("line identifiers must be unique and non-empty")
        ids.add(item.get("id")); unit=_num(item.get("unit_minor"), "unit_minor", findings); qty=_num(item.get("quantity"), "quantity", findings)
        if int(unit)!=unit or int(qty)!=qty or unit<0 or qty<=0: findings.append("unit price and quantity must be nonnegative integer minor units; quantity must be positive")
        subtotal += int(unit)*int(qty)
    discount=_num(payload.get("discount_minor"), "discount_minor", findings); tax=_num(payload.get("tax_minor"), "tax_minor", findings); total=_num(payload.get("total_minor"), "total_minor", findings)
    if any(int(x)!=x or x<0 for x in (discount,tax,total)): findings.append("discount, tax, and total must be nonnegative integer minor units")
    if discount>subtotal: findings.append("discount exceeds subtotal")
    if subtotal-int(discount)+int(tax) != int(total): findings.append(f"total mismatch expected={subtotal-int(discount)+int(tax)} actual={int(total)}")
    return {"domain": DOMAIN, "status": "needs-review" if findings else "ready", "findings": findings}

if __name__ == "__main__":
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    payload = json.loads(source.read_text(encoding="utf-8") if source else sys.stdin.read())
    print(json.dumps(analyze(payload), indent=2, sort_keys=True))
