# invoice_timeline_sale_col_property

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* This module extends 'sale.order' to automatically select invoice timeline templates based on project properties, streamlining invoice management for purchases linked to specific projects.

---

## Dependencies

### Odoo modules dependencies

| Module         | Technical Name | Why used?                                                                                        |
|----------------|----------------|--------------------------------------------------------------------------------------------------|
|COL Property    |col_property    |Provides utility functions for generating record references and handling scripts.                 |
|Invoice timeline - Sale|invoice_timeline_sale | Provides  allow setting a custom start date with room minimum and maximum constraints for templates. |

---

### Python library dependenci

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Inherited the 'sale.order' model to include a computed field 'invoice_timeline_template_id', which selects the appropriate invoice timeline template based on project properties such as room count.
* Implemented logic within '_cpt_invoice_timeline_template_id' to dynamically search for and assign an invoice timeline template that matches the room count of properties associated with a project.
* Extended the '_create_invoices_from_timeline_default_value' method to include additional context for project and sale contract details when creating invoices.
---
