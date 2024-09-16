# akawam_link

**Table of Contents**

* Usage
* Dependencies
* Issues & Bugs
* Development

---

## Usage

* This module Usage a connector for integrating with the Akawam web service, enabling the ability to send and receive data between Odoo and the Akawam platform.

---

## Dependencies

### Odoo modules dependencies

| Module         | Technical Name | Why used?                                                                                        |
|----------------|----------------|--------------------------------------------------------------------------------------------------|
|Script tools    |script_tools    |Provides utility functions for generating record references and handling scripts.                 |
---

### Python library dependenci

* This module doesn't have any python dependencies

---

## Limitations, Issues & Bugs

* This module doesn't have any limitations, issues & bugs

---

## Development

* Implemented a model akawam.ws.call to log web service calls, storing details such as the Akawam ID, data sent, response received, and call duration.
* Implemented a method call to send data to the Akawam platform, handling POST and PATCH requests based on the existence of an Akawam ID.

---
