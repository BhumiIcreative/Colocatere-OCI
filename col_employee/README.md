# col_employee

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* Used the col employee module payments to be linked to employee-specific accounts, separate from the usual payable accounts and better tracking of employee-related payments, such as expense reimbursements or salary payments.

---

## Dependencies

### Odoo modules dependencies

| Module         | Technical Name | Why used?													|
--------------------------------------------------------------------------------------------------|
|COL Property    |col_property    |Manages property leases, contracts, and integrates with sales, purchases, and project tracking.   |
---

### Python library dependenci

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Inherited the 'account.paymnet' model to use employee-specific accounts if "use_employee_account" is enabled, otherwise defaults to the standard account.
* Inherited the 'res.partner' model to automatically update or create properties for employee accounts.
---
