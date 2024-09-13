# col_expense_report_import

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* User can create the vendor bills by importing the  expense report with filetype as csv.

---

## Dependencies

### Odoo modules dependencies

| Module           | Technical Name   | Why used?                                                                                        |
|------------------|------------------|--------------------------------------------------------------------------------------------------|
| col_employee | col_employee | Used field reference to add custom field after it.
| script_tools | script_tools | Model used in creating vendor bill record
| account_accountant | account_accountant | Used the menu as reference

### Python library dependency

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Updated folder structure.
* Replaced sql constrain with api constrain for property field.
* Added validation for Invalid file import.
* Updated fields and logics for analytic account.
---
 