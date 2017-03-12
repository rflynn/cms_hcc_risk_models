/* dump coefficients file (C2214O5P) to csv and sas7bdat */
filename inc "/folders/myfolders/sasuser.v94/2017/C2214O5P";
libname incoef "/folders/myfolders/sasuser.v94/2017";
proc cimport data=incoef.C2214O5P infile=inc;
run;

proc export data=incoef.C2214O5P
    outfile='/folders/myfolders/sasuser.v94/2017/C2214O5P.csv'
    dbms=csv
    replace;
run;



/* dump format file (F221690P) to csv and sas7bdat */
filename inf "/folders/myfolders/sasuser.v94/2017/F221690P";
libname cmshccfm "/folders/myfolders/sasuser.v94/2017";
proc cimport library=cmshccfm infile=inf;
run;

proc format lib=cmshccfm.formats cntlout=cmshccfm.F221690P;
  select a-zzzzzzzz  $a-$zzzzzzzz;
run;


proc export data=cmshccfm.F221690P
    outfile='/folders/myfolders/sasuser.v94/2017/F221690P.csv'
    dbms=csv
    replace;
run;




