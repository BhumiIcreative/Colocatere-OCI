# invoice_timeline_custom_start_date

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* Create invoices with custom time intervals by defining a timeline template with specific start dates and intervals,
then use the template to generate invoices with computed dates.

---

## Dependencies

### Odoo modules dependencies

| Module           | Technical Name   | Why used?                                                                                        |
|------------------|------------------|--------------------------------------------------------------------------------------------------|
| invoice_timeline | invoice_timeline | Provides the foundational functionality for managing account timeline templates.

### Python library dependency

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Inherited the 'account.timeline.template' model by adding a new field called "room_min" and "room_max".
* Inherited the 'account.timeline.template.line' Extended functionality to adjust the date calculation based on custom logic, 
  including handling monthly intervals and recursive date generation.

---
 