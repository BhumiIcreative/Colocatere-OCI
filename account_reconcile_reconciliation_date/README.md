# account_reconcile_reconciliation_date

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* To track the latest reconciliation date for fully reconciled entries.

---

## Dependencies

### Odoo modules dependencies

| Module         | Technical Name | Why used?                                                                                        |
|----------------|----------------|--------------------------------------------------------------------------------------------------|
---

### Python library dependenci

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Inherited the `account.move.line` model to add a new field called **"reconciliation_date"**.
* Inherited the `account.full.reconcile` model by adding a computed field **"latest_reconciliation_date"**, and used it to automatically update the **"reconciliation_date"** on related entries.
* Inherited the tree view of `account.move.line` to display the **"reconciliation_date"**.

---
