# akawam_web_service

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* This module is used to automatically create records in the Akawam ws call when triggered by the "Sync to Akawam" button or corresponding server action.

---

## Dependencies

### Odoo modules dependencies

| Module         | Technical Name | Why used?                                                                                        |
|----------------|----------------|--------------------------------------------------------------------------------------------------|
|COL Property    |col_property    |Provides utility functions for generating record references and handling scripts.|

---

### Python library dependenci

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Inherited the `account.move` model to sync various invoice types (maintenance, location, timeline) and handle reversed entries. Sync is triggered automatically during record creation or updates for linked projects.
* Inherited the `account.payment` model to sync tenant and owner payments based on reconciled invoices, tenant contracts, and payment events (creation, modification, or posting).

---
