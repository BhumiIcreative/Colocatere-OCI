# col_property

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* Enhances property management by integrating properties, leases, and contracts with sales, purchases, and project tracking.

---

## Dependencies

### Odoo modules dependencies
| Module                              | Technical Name                          | Why used?|
|---------------------------------------------------------------------------------------------|
| Akawam Link                         | akawam_link                             | Provides integration with Akawam for enhanced functionality.                                |
| Account Project                     | account_project                         | Integrates project management features with accounting operations.                         |                 |
| Invoice Timeline Custom Start Date  | invoice_timeline_custom_start_date      | Customizes invoice timeline with a configurable start date.                                |


### Python library dependenci

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Inherited the 'account.move' model by adding a new fields called "in_deficit","additional_invoice_payment_ref","purchase_contract_id","lease_id" and "lease_partner_ids".

* Defined '_cpt_lease_partner_ids' method for Computes and sets lease partner IDs based on the associated lease.
* Defined 'action_to_post' method for Changes the invoice state to 'to_post' if it is currently in the draft state.

* Defined 'cron_auto_invoice_repayment' for Automatically processes and posts invoices based on due dates within the current month.

* Defined 'action_switch_invoice_into_refund_credit_note' for Switches the invoice into a refund credit note if the document type is suitable.

* Defined 'get_last_day_of_next_month' for Calculates the last day of the next month.

* Inherited the 'project.project' model by adding new fields called "lease_count" (Integer), "property_count" (Integer), "purchase_contract_count" (Integer), "sale_count" (Integer), "purchase_count" (Integer), "in_deficit" (Boolean), "transfer_locked" (Boolean), "seller_id" (Many2one), "cgp_id" (Many2one), "sourcer_id" (Many2one), "subcontractor_id" (Many2one), "decorator_id" (Many2one), "lease_ids" (Many2many), "property_ids" (Many2many), "purchase_contract_ids" (Many2many), "sale_ids" (One2many), "purchase_ids" (One2many), and "agency_col_id" (Many2one).

* Defined _fix_project_id_to_project_ids method for updating the project_ids field for records with a non-empty project_id field. 
* Defined _cpt_count method to compute and set counts for related purchases, contracts, sales, properties, and leases.
* Defined _cpt_in_deficit method to determine if any related properties are in deficit.
* Defined action_view_room method to open the room records related to the current project.

* Defined action_view_property method to open the property records related to the current project.

* Defined action_view_purchase_contracts method to open the purchase contract records related to the current project.

* Defined action_view_leases method to open the lease records related to the current project.

* Defined action_view_sales method to open the sales records related to the current project.

* Defined action_view_purchases method to open the purchase records related to the current project.

* Defined _get_default_currency method to return the default currency for account moves.
* Defined _cpt_name method to compute and set the lease name based on the associated property and room names.
* Added a new model named 'property.commission_line' , which includes the fields "price" (Monetary), "currency_id" (Many2one), "partner_id" (Many2one), and "purchase_contract_id" (Many2one).

* Defined _fix_project_id_to_project_ids method for updating the project_ids field for records with a non-empty project_id field.
* Added a new model named 'property.lease' , which includes the fields "name" (Char), "end_date" (Date), "start_date" (Date), "pricing_id" (Many2one), "project_id" (Many2one), "property_id" (Many2one), "room_id" (Many2one), "lessor_partner_ids" (Many2many), "project_ids" (Many2many), and "tenant_partner_ids" (Many2many).

* Defined _cpt_name method to compute and set the lease name based on the associated property and room names.
* Added a new model named 'property.pricing' , which includes the fields "amount" (Integer), "interval" (Integer), and "interval_type" (Selection).

* Added a new model named 'property.property' , which includes the fields "active" (Boolean), "room_count" (Integer), "lease_count" (Integer), "purchase_contract_count" (Integer), "name" (Char), "area" (Float), "renovated_area" (Float), "in_deficit" (Boolean), "lease_manager_id" (Many2one), "partner_address_id" (Many2one), "project_id" (Many2one), "room_ids" (One2many), "lease_ids" (One2many), "purchase_contract_ids" (One2many), and "project_ids" (Many2many).

* Defined _cpt_count method to compute and set counts for related rooms, leases, and purchase contracts.
* Defined action_view_room method to open the room records related to the current property.

* Defined action_view_leases method to open the lease records related to the current property.

* Defined action_view_purchase_contracts method to open the purchase contract records related to the current property.

* Added a new model named 'property.purchase_contract' , which includes the fields  "amount" (Monetary), "compromise_date" (Date), "is_real_compromise" (Boolean), "is_real_signature" (Boolean), "name" (Char), "owner_type" (Selection), "signature_date" (Date), "currency_id" (Many2one), "project_id" (Many2one), "property_id" (Many2one), "commission_ids" (One2many), "owner_ids" (Many2many), and "project_ids" (Many2many).

* Defined _cpt_owner_type method to compute and set the owner type based on the number of owners.
* Defined _get_default_currency method to return the default currency for account moves.
* Added a new model named 'property.room' , which includes the fields "lease_count" (Integer), "name" (Char), "property_id" (Many2one), and "lease_ids" (One2many).

* Defined action_view_lease method to open lease records associated with the current property and room.

* Defined _get_lease_count method to compute and set the count of associated lease records.
* Inherited the 'purchase.order' model by adding new fields called "project_id" (Many2one) and "purchase_contract_id" (Many2one).

* Override _prepare_invoice method to prepare invoice values by including project and purchase contract information.
* Inherited the 'purchase.order.line' model by adding a new field called "account_analytic_id" (Many2one).

* Defined _cpt_account_analytic_id method to compute and set the analytic account based on the project's analytic account.
* Inherited the 'res.partner' model by adding a new field called "purchase_contract_ids" (Many2many).

* Inherited the 'sale.order' model by adding new fields called "project_id" (Many2one), "purchase_contract_id" (Many2one), and "analytic_account_id" (Many2one).

* Defined _cpt_analytic_account_id method to set the analytic account from the project's analytic account.
* Override _create_invoices method to override the default invoice creation process by setting the project and purchase contract information on the newly created invoices.
* Override _compute_communication method to override the default computation of the communication string by including additional references.
* Override _prepare_invoice_values method to prepare invoice values by including project and purchase contract information. 
* Added an email template for cron exceptions named `col_property.mail_template_exception` to notify about cron job failures.

---
