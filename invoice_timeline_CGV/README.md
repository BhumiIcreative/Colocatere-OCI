# invoice_timeline_CGV

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

* Usage

* This module automatically populates the "oci_cgv" field with relevant data.

---

* Dependencies

* Odoo modules dependencies

| Module         | Technical Name | Why used?                                                                                        |
|----------------|----------------|--------------------------------------------------------------------------------------------------|
|Accounting	 |  account	  |Used for managing invoices, payments, and financial transactions.                                 |
|Sales           |  sale          |Required for managing sales orders and quotations, as well as invoicing sales transactions.       |
|Invoice Timeline|invoice_timeline|Adds functionality for scheduling and managing invoice timelines.                                 |
|Invoice timeline - Sale / Col property |invoice_timeline_sale_col_property	|Integrates sales and invoice timeline features with COL property data.

---

* Python library dependenci

* This module doesn't have any python dependencies

---

* Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

* Development

* Inherited the `account.timeline.template` and add `oci_note_cgv` field.
* Inherited the `sale.order` and add `oci_cgv` field.

---
