/* take output from HCUP's CCS mapping program that matches HCPCS codes to buckets https://hcup-us.ahrq.gov/toolssoftware/ccs_svcsproc/ccscpt_license.jsp
and sum up all the claims then add group labels*/

* input file containing ccs groups and number of claims;
data input;
set epic.code_buckets;
run;

* import HCUP reference file;
proc import datafile='/home/u61030821/epic/CCS_Services_Procedures_v2025-1_052425.csv' out=prelabels dbms=csv replace;
getnames=no;
datarow=3;
run;

* drop the column containing hcpcs codes;
data prelabels2 (rename=(VAR2=ccs VAR3=ccs_label));
set prelabels(drop=VAR1);
run;

* group by ccs number;
proc sort data=labels dupout=removed noduprecs;
by ccs;
run;

* create new data table;
proc sql;
create table code_groups as
select cpt_ccs1, ccs_label, total_claims from (select cpt_ccs1, sum(claim_count) as total_claims from input group by cpt_ccs1) as tab1 left join labels on tab1.cpt_ccs1 = labels.ccs;
quit;

* export;
proc export data=code_groups outfile='/home/u61030821/epic/epic_claims_ccs_groups.csv';
run;
