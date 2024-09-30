# account_payment_block_partner


**Table of Contents**

- Usage
- Dependencies
- Issues & Bugs
- Development

---

* Usage

- Implement payment restrictions based on partner settings by blocking or warning users during processing. This involves displaying error messages, hiding validation buttons, and showing relevant warnings.

--- 


* Dependencies

* Odoo modules dependencies

| Module         | Technical Name | Why used?                                                                                        |
|----------------|----------------|--------------------------------------------------------------------------------------------------|
|                |                |                                                                                                  |

---

* Python library dependencies

- This module doesn't have any python dependencies

---

* Limitations, Issues & Bugs

- This module doesn't have any limitations, issues & bugs

---

* Development

* Inherited `account.move` model to overwrite method`action_register_payment`,used to checks partner payment restrictions.
* Inherited `account.payment` model and used to manage partner payment warnings
* Inherited `account.payment.register` model
* Inherited `res.config.settings` model
* Inherited `res.partner` model ,used to payment warning fields to the partner form, visible only to users with the appropriate group permissions.

---
