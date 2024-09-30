# account_default_analytic_account_from_project


**Table of Contents**

- Usage
- Dependencies
- Issues & Bugs
- Development

---

* Usage

- Automatically assign and update the analytic account in journal entries and lines based on the associated project.

--- 

* Dependencies

* Odoo modules dependencies

| Module         | Technical Name | Why used?                                                                                        |
|----------------|----------------|--------------------------------------------------------------------------------------------------|
|account_project |Account project | Enhancements to improve project accounting and integration with invoices.                        |

---

* Python library dependencies

- This module doesn't have any python dependencies

---

* Limitations, Issues & Bugs

- This module doesn't have any limitations, issues & bugs

---

* Development

* Enhanced the `account.move` and `account.move.line` models to automatically update the analytic account field based on the project ID in both journal entries and their lines.

---
