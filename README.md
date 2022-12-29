# fraud-detection-in-subsidy-applications
 whether the companies submitting subsidy applications to government have been suspected of fraud or commited fraud in the past.
This article tells the procedure to check whether the companies submitting subsidy applications to government have been suspected of fraud or commited fraud in the past.

## Comparing chamber of commerce (KVK) numbers
One of the possibility is to check whether the applicant company is bankrupt while it is applying for a subsidy. The list of bankrupted companies with their chamber of commerce number, (KVK for short) can be downloaded from https://www.faillissementen.com/ as ‘faillissement_database.xlsx’.
Give name to the dataframe dff columns: ‘ORG_NAME’, ‘ORG_KVK’ where company info and number information is, respectively.

Compare the Chamber of Commerce numbers of the companies listed in the database of the government, ‘government_database.xlsx’ against the Chamber of Commerce numbers of companies listed in bankruptcy register.

The dataframe df should contain column names: ‘REFERENCE’, ‘ORG_NAME’, ‘ORG_STREET NAME’, ‘ORG_HOUSE NUMBER’, ‘ORG_ZIPCODE’, ‘ORG_CITY’, ‘ORG_IBAN’, ‘CP_FIRST NAME’, ‘CP_LAST NAME’, ‘CP_EMAIL ‘, ‘CP_PHONE’

## Check multiple submissions
Companies/institutions may not be allowed to submit multiple applications to multiple rounds or subsidies. For those reasons, we can perform a check for duplicate information such as Chamber of Commerce number; PO box / address; signatory; IBAN account number; e-mail address; phone number.

We can also verify that no private email addresses (such as Hotmail.com, live.nl, gmail.com, etc.) and no Foreign bank account numbers are used in the application.
