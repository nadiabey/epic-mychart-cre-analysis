"""
created 11/6/25
the 2026 proposed hospital price transparency rule requires hospitals to disclose the 
10th percentile, median, and 90th percentile price for all offered services in standard 
charge machine-readable files using remittance data. if the calculated median/percentile is not a real price, 
the value must be replaced with the closest real price. this uses remittance tables from epic to estimate these 
benchmarks for each unique billing code.

not taken into consideration: facility type (FAC_CODE_VAL in CL_RMT_CLM_INFO), payor (link INV_NUM to INV_BASIC_INFO which has CVG_ID which can probably be linked somewhere)

update 11/13/25: facility and payor added
"""
import pandas as pd, sqlite3, re, numpy as np


# function to get nearest value
def nearest(listy, val):
    return listy[np.absolute(listy-val).argmin()]


# open db
conn = sqlite3.connect('atriumrecords2.db')
# get remittance image id, code, line item amount, and amount paid toward claim from one table
# get invoice number and facility type from other table
# some remittances have charges removed or insurance denied so drop those
remit = pd.read_sql("select cvg_id, mailing_name, image_id, inv_no, fac_code_val, proc_identifier, prov_payment_amt "
                    "from inv_basic_info join (select rmt.image_id, inv_no, fac_code_val, proc_identifier, "
                    "prov_payment_amt from cl_rmt_svce_ln_inf as rmt join cl_rmt_clm_info as clm on rmt.image_id = "
                    "clm.image_id where inv_no not in (select inv_no from cl_rmt_clm_info where clm_stat_cd_c_name = "
                    "'Reversal of previous payment' or clm_stat_cd_c_name = 'Denied')) as claim on "
                    "inv_basic_info.inv_num = claim.inv_no", conn)
conn.close()
# force all column names to uppercase
remit.columns = [col.upper() for col in remit.columns]
# payment columns are strings so change to floats
remit['PROV_PAYMENT_AMT'] = remit['PROV_PAYMENT_AMT'].astype(float)
# transform code column into three columns (code type, code, modifier)
codes = [re.split(r'[:>]+', code) for code in remit['PROC_IDENTIFIER']]
code_type = []
code = []
modifier = []
for cd in codes:
    code_type.append(cd[0])
    code.append(cd[1])
    mod = "" if len(cd) < 3 else cd[2]  # empty column if no modifier else modifier
    modifier.append(mod)
# set new columns
remit['code_type'] = code_type
remit['code'] = code
remit['modifier'] = modifier
# simplify columns
new_cols = remit[['MAILING_NAME', 'FAC_CODE_VAL', 'code_type', 'code', 'modifier', 'PROV_PAYMENT_AMT']]
# calculate percentiles and claim counts
stats = new_cols.groupby(['MAILING_NAME', 'FAC_CODE_VAL', 'code_type', 'code', 'modifier'], as_index=False).describe([.1, .5, .9])
# group prices
prices = new_cols.groupby(['MAILING_NAME', 'FAC_CODE_VAL', 'code_type', 'code', 'modifier'], as_index=False)['PROV_PAYMENT_AMT'].apply(list)
# check if 10th/median/90th percentile values are real prices
for i in range(len(stats)):
    payments = prices.iloc[i]['PROV_PAYMENT_AMT'] # list of prices
    # store current values and if current values don't match list, calculate new value
    ten = stats.iloc[i]['PROV_PAYMENT_AMT']['10%']
    perc10 = ten if ten in payments else nearest(payments, ten)
    median = stats.iloc[i]['PROV_PAYMENT_AMT']['50%']
    perc50 = median if median in payments else nearest(payments, median)
    ninety = stats.iloc[i]['PROV_PAYMENT_AMT']['90%']
    perc90 = ninety if ninety in payments else nearest(payments, ninety)
    # replace values in table
    stats.loc[i, ('PROV_PAYMENT_AMT', '10%')], stats.loc[i, ('PROV_PAYMENT_AMT', '50%')], stats.loc[i, ('PROV_PAYMENT_AMT', '90%')] = perc10, perc50, perc90
