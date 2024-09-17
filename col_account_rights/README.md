# col_account_rights

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

* Usage

* This module implements a custom access control system for accounting users, featuring five distinct access levels.
---

* Dependencies

* Odoo modules dependencies
| Module                              | Technical Name                       | Why used?                                                |
|-------------------------------------|--------------------------------------|---------------------------------------------------------------------------------------------|
| Accounting                          | account_accountant                   | Provides core accounting features.                       |
| Assets Management                   | account_asset                        | Manages accounting assets and depreciation.              | 
| Account Automatic Transfer          | account_auto_transfer                | Automates account transfers.                             |
| Account payment term by product     | account_payment_term_by_product      | Enables payment terms based on productsdate.             |
| Accounting Reports                  | account_reports                      | Offers advanced accounting reporting features.           |
| SEPA Credit Transfer                | account_sepa                         | Enables SEPA payment processing.                         |
| SEPA Direct Debit                   | account_sepa_direct_debit            | Provides SEPA direct debit functionality for handling payments.                                                                                                                               |
| Analytic Accounting Enterprise      |analytic_enterprise                   | Adds advanced analytic accounting features.              |
|  Col expense report import          |col_expense_report_import             |Imports expense reports into the system.                  |
|Col payment import                   |col_payment_import                    |Facilitates importing payment data.                       |
|Invoice timeline - Custom start date on 1st or 15      |invoice_timeline_custom_start_date    |Allows custom start dates for invoice timelines.                                                                                                                              |
|Invoice timeline - Purchase          |invoice_timeline_purchase             |Integrates purchase orders with custom invoice timeline   |
|Invoice timeline - Sale              |invoice_timeline_sale	             |Integrates sales orders with custom invoice timelines.    |
|Project                              |project                               |Adds project management features integrated with accounting.|
|Purchase                             |purchase                              |Manages procurement and purchase orders.                  |
|SMS                                  |sms                                   |Enables SMS communication capabilities.                   |
|Snail Mail Follow-Up                 |snailmail_account_followup            |Automates follow-up letters for outstanding invoices via snail mail.                                                                                                                                   |
|France - Accounting                  |l10n_fr                               |Adds French accounting standards.                         |
|Belgium - Accounting                 |l10n_be                               |Adds Belgian accounting standards.

* Python library dependenci

* This module doesn't have any python dependencies

---

* Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Implemented the account.group_account_invoice group with access to general ledger, partner ledger, and finance entries.
* Implemented the group_col_account_invoice_expense group, inheriting from Level 1, and added access to expense report import functionality.
* Implemented the group_col_account_partner group, inheriting from Level 2, with access to a broader range of accounting menus and reports, but excluding certain restricted accounts.
* Implemented the account.group_account_user group, inheriting from Level 3, with comprehensive access to all accounting functionalities and reports.
* Implemented the account.group_account_manager group with the highest level of access, including configuration options for accounting and invoicing.
* Rule 1: Restrict access to certain accounts and payment types.
* Rule 2: Expanded access to partner bank data and limited account payment visibility.
* Rule 3: Provided access to a comprehensive view of accounting journals.
* Rule 4: Allowed full access to all accounting entries and assets.
* Rule 5: Assigned access rights for complete configuration control over accounting and invoicing settings.

---
