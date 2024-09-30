# invoice_timeline

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* Create invoice with time interval.

---

## Dependencies

### Odoo modules dependencies

| Module  | Technical Name | Why used?                                                                                        |
|---------|----------------|--------------------------------------------------------------------------------------------------|
| account | account        | for add account timeline templates related functionality.
| sale    | sale           | provides sale order related functionality.

### Python library dependenci

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Inherited the 'account.move' model by adding a new field called "timeline_sequence" and "account_timeline_template_id"

* Added a new model named 'account.timeline.template', which includes the fields "active", "invoice_count", "name", "sequence", "used_on", "invoice_ids", and "line_ids".

* Added a new model named 'account.timeline.template.line', which includes the fields "interval","interval_type","percent","product_categ_id" and "template_id".

* Inherited 'account.move.date.update' for update timeline sequence.

* Added a new wizard named 'account.move.date.update.line', which includes the fields "invoice_date_due","new_invoice_date_due","writable","invoice_id" and "wizard_id".

* Inherited 'script.wizard', which includes the fields "account_timeline_template_id" and "line_ids".

* Defined '_cpt_timeline_sequence' for Computes and assigns a sequence number to each invoice within its associated timeline template based on due dates.
* Defined 'action_update_invoice_date' for Opens a wizard to update invoice due dates based on the current timeline template.

* Defined _cpt_invoice_count: Computes and updates the number of invoices associated with each timeline template.
* 
* Defined action_view_invoices: Opens a view showing the invoices associated with the current record.
* 
* Defined _check_line_sum: Validates that the sum of percentages for each product category equals 100 and raises a UserError if it does not.
* 
* Defined _group_lines_by_categ_id: Groups lines by their product category, excluding specified categories, and returns a dictionary of grouped lines.
* 
* Defined _get_invoiceable_lines_by_date: Groups invoiceable lines by date based on the given start date and returns a dictionary of lines categorized by date.
* 
* Defined create_invoices: Creates invoices with specified lines and optional start date, updating invoice details and generating multiple invoice records based on the provided lines and default values.
* 
* Defined _cpt_sequence: Computes the sequence based on the interval and interval type, multiplying by 31 if the interval type is 'month'.
* 
* Defined _check_percent_constraints: Ensures the 'percent' field value is within the valid range of 0 to 100.
* 
* Defined _get_date: Computes a list of dates starting from date_start, incrementing based on line intervals.
* 
* Override reverse_moves: Reverses account moves and updates the timeline sequence based on the original moves.
* 
* Defined _cpt_writable: Computes the writable field based on the state of the related invoice, setting it to True if the invoice state is 'draft' or 'to_post'.
* 
* Defined compute_date: Computes the date using the wizard and opens the wizard view.
* 
* Defined confirm: Updates invoice dates based on new due dates from writable lines and adjusts related invoice line dates.
* 
* Defined _compute_date: Computes and updates new invoice due dates based on the base line date and timeline template.
---
 