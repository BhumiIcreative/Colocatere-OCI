# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

COMPANY = {
    "SARL_COLOCATERE": 2,  # ID for SARL Colocatère (Property Management)
    "SAS_GROUPE_COLOCATERE": 1,  # ID for SAS Groupe Colocatère (Sales)
}

JOURNAUX = {
    "FACTURES_CLIENTS": 1,  # Sales Invoice in SAS Groupe Colocatère
    "FACTURES_FOURNISSEURS": 2,  # Purchase Invoice in SAS Groupe Colocatère
    "REVERSEMENT": 33,  # Purchase Invoice from Property Owners in SARL Colocatère
    "QUITTANCE": 34,  # Rental Invoice to Tenants in SARL Colocatère
    "FRAIS_DE_DOSSIER_LOCATAIRE": 37,  # File Fees Invoice in SARL Colocatère
    "ASSURANCES_PROPRIETAIRE_GLI_PNO": 38,  # Insurance Invoice in SARL Colocatère
    "FACTURES_CLIENTS_SARL": 23,  # Sales Invoice in SARL Colocatère
}

PAYMENT_TYPE = {
    "manual": 1,  # Manual Payment
    "batch_payment": 0,  # Batch Payment
    "electronic": 1,  # Electronic Payment
    "sepa_ct": 1,  # SEPA Credit Transfer
    "sdd": 6,  # SEPA Direct Debit
}
