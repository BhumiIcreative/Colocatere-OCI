# account_anomaly

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* Add a Checkbox to Identify Anomalies in Journal Entries

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

* Inherited the 'account.move' model by adding a new field called "anomaly"
* Inherited the form and tree views of 'account.move' for customer invoices and vendor bills.
* Added a filter to display only entries marked as anomalies.

---
