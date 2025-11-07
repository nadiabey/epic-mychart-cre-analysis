# epic-mychart-cre-analysis
Analyzing computer-readable exports from Epic MyChart (mine and my family's, with permission). CREs come in a .zip file that expand into two folders: EHITables (tsv files containing data) and EHITables Schema (htm files containing documentation). 

TSV files were imported into SQL (data-to-sql-db.py) and schema files were compressed into one codebook file (compress-documentation.sh). Exports generally have the same files but tables may be empty and some exports are missing columns for some tables.

Types of identifiers: account ID (billing), patient ID, patient MRN, record ID (claims), etc.

Some significant tables:
* PATIENT, PATIENT_2, PATIENT_3, PATIENT_4, PATIENT_5, PATIENT_6: patient demographics, primary care provider, SSN, Medicare/Medicaid ID, Advanced Directive status, Citzenship, Adoption/Foster status, Alive/Dead status, organ donor status
* ACCOUNT, ACCOUNT_2, ACCOUNT_3: patient info, account type, financial class (insurance type), total/self-pay/insurance balance, payment plan details, propensity to pay, time last viewed billing communications, family size, family income
* CLM_VALUES, CLM_VALUES_2, CLM_VALUES_3, CLM_VALUES_4, CLM_VALUES_5, CLM_VALUE_RECORD: record ID, billing provider NPI/taxonomy, patient MRN, invoice number, total charges, facility type code, frequency code, professional (CMS) or institutional (UB) claim
* CLAIM_INFO: claim and account info, workers comp or commercial claim, entry date, coverage, admit/discharge date
* CL_RMT_SVCE_LN_INF: remittance images with billing codes in format [code type]:[code]:[modifier] (i.e. HC:82627:90)
* COVERAGE_MEMBER_LIST: what patient is in what plan
* ORDER_MED: prescriptions, date ordered, dosage, quantity, refills, order setting (inpatient/outpatient)
* COVERAGE_BENEFITS: OOP max and OOP remaining, deductible met and remaining, coinsurance percent
* DOC_INFORMATION: visit summmaries and references
* EPA_INFO: prior auth
* ORDER_PROC, ORDER_PROC_2, ORDER_PROC_3, ORDER_PROC_4, ORDER_PROC_5, ORDER_PROC_6: procedures ordered and details about provider
* ORDER_RESULTS: results of procedures/tests
* PR_EST_INFO: price estimates

Things I've learned during this:
* Line item charges can often differ for the same billing code.
* There may be multiple remittance images on the same invoice/encounter.
