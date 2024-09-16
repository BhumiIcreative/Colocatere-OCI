# invoice_timeline_sale

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* Integrates invoice timeline templates with sale orders, enabling the creation of invoices based on defined time intervals.

---

## Dependencies

### Odoo modules dependencies

| Module             | Technical Name     | Why used?                                                                                        |
|--------------------|--------------------|--------------------------------------------------------------------------------------------------|
| invoice_timeline   | invoice_timeline   | Provides the foundational functionality for managing account timeline templates.
| sale_management    | sale_management    | Facilitates the integration of timeline templates with sale orders.
                                     

### Python library dependency

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Added a new field 'Use on sale' to indicate if the timeline template should be used for sale orders.
* Added a field 'invoice_timeline_template_id' to select an invoice timeline template and methods to create invoices from the timeline.
* Added methods to link purchase lines to invoice lines and to retrieve data for invoice creation.
* Added 'create_invoices_from_timeline_default_value' for default values used for creating invoices from the timeline.
* Added '_create_invoices_from_timeline' for Creates invoices for each sale order based on the selected timeline template.
---
 