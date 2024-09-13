# invoice_timeline

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* Create invoice with time interval.

---

## Dependencies

### Odoo modules dependencies

| Module  | Technical Name | Why used?                                                                                        |
|---------|----------------|--------------------------------------------------------------------------------------------------|
| account | account        | for add account timeline templates related functionality

### Python library dependenci

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Inherited the 'account.move' model by adding a new field called "timeline_sequence" and "account_timeline_template_id"
* Added a new model named 'account.timeline.template', which includes the fields "active", "invoice_count", "name", "sequence", "used_on", "invoice_ids", and "line_ids".
* Added a new model named 'account.timeline.template.line', which includes the fields "interval","interval_type","percent","product_categ_id" and "template_id".
* Inherited 'account.move.date.update' for update timeline sequence.
* Added a new wizard named 'account.move.date.update.line', which includes the fields "invoice_date_due","new_invoice_date_due","writable","invoice_id" and "wizard_id".
* Inherited 'script.wizard', which includes the fields "account_timeline_template_id" and "line_ids"
---
 