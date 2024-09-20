# invoice_timeline_purchase

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* Integrates invoice timeline templates with purchase orders, allowing automatic 
  invoice creation based on selected timeline templates.

---

## Dependencies

### Odoo modules dependencies

| Module           | Technical Name   | Why used?                                                                                        |
|------------------|------------------|--------------------------------------------------------------------------------------------------|
| invoice_timeline | invoice_timeline | Provides the foundational functionality for managing account timeline templates.
| purchase         | purchase         | Allows integration of timeline templates with purchase orders.
                                     

### Python library dependency

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Added a new field use_on_purchase to indicate if the timeline template should be used for purchase orders.
* Added a field invoice_timeline_template_id to select an invoice timeline template and methods to create invoices from the timeline.
* Added methods to link purchase lines to invoice lines and to retrieve data for invoice creation.

---
 