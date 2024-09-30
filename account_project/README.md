# account_project

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* Enhancements to improve project accounting and integration with invoices.

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

* Inherited the 'account.move' model by adding a new field called "Project"
* Inherited the 'project.project' model by adding a new field called "Invoices count" and smart button "Invoices"
* Inherited the form of 'account.move' to add 'project' field
* Inherited the form of 'project.project' to add smart button of invoice
---
