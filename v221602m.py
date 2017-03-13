"""
 * set the following parameters:
 *      INP      - SAS input person dataset
 *      IND      - SAS input diagnosis dataset
 *      OUTDATA  - SAS output dataset
 *      IDVAR    - name of person id variable (HICNO for medicare data)
 *      KEEPVAR  - variables to keep in the output dataset
 *      SEDITS   - a switch that controls whether to perform MCE edits
 *                 on ICD9 and ICD10: 1-YES, 0-NO
 *      DATE_ASOF- reference date to calculate age. Set to February 1
 *                 of the payment year for consistency with CMS

 %V2216O2M(INP      =IN1.PERSON,
           IND      =IN2.DIAG,
           OUTDATA  =OUT.PERSON,
           IDVAR    =HICNO,
           KEEPVAR  =HICNO &INPUTVARS &SCOREVARS &DEMVARS
                     &HCCV22_list79 &CCV22_list79,
           SEDITS   =1,
           DATE_ASOF="1FEB2016"D);


"""

import pandas
import datetime
import formats
import v221602p
import v22h79l1
import v22i0ed1
import agesexv2
import regression_variables as rv

# input
#===================================================================
INP = pandas.read_csv('input/2017/person.csv', parse_dates=['DOB'])
IND = pandas.read_csv('input/2017/diag.csv')
IDVAR = 'HICNO'

# merge person and diag data (one row per person/diag
inpind = pandas.merge(INP, IND, on=IDVAR)
inpind = inpind.sort_values(IDVAR)


KEEPVAR = [IDVAR] + rv.INPUTVARS + rv.SCOREVARS + \
          rv.DEMVARS + rv.HCCV22_list79 + rv.CCV22_list79
SEDITS = True
DATE_ASOF = datetime.date(2016, 2, 1)

# read regression coefficients
fname = 'cms_models/2017/cms_hcc_v2216_79_02/C2214O5P.csv'
hcccoefn = pandas.read_csv(fname)

# read formats file
fname = 'cms_models/2017/cms_hcc_v2216_79_02/F221690P.csv'
hcc_formats = formats.HccFormats(fname)



# loop over patients
for hicno in inpind['HICNO'].unique():

    # get rows from inpind for this patient
    ptrows = inpind.loc[inpind['HICNO']==hicno, :]

    # get demographic data from ptrows
    dob = ptrows.iloc[0]['DOB']
    sex = ptrows.iloc[0]['SEX']

    # calculate age
    agef = DATE_ASOF.year - dob.year
    agef_edit = agef

    orec = ptrows.iloc[0]['OREC']

    # create demographics regression variables
    disabl, origds, cell, necell = agesexv2.create_demographic_regression_variables(
        agef_edit, sex, orec)


    # initialize C and HCC arrays
    # these are just flags.  we use N_CC + 1 so that
    # we can use 1-based indexing (or simply say C[i] == 1
    # means the i'th condition code is true. C[0] and HCC[0]
    # will always be zero
    C = [0] * (rv.N_CC + 1)
    HCC = [0] * (rv.N_CC + 1)

    # loop over diagnoses and assign CCs
    for ii, row in ptrows.iterrows():
        print()

        diag = row['DIAG']
        diag_type = row['DIAG_TYPE']
        print('ii={}, hicno={}, diag={}, diag_type={}'.format(
            ii, hicno, diag, diag_type))

        # initial value
        cc = 9999
        print('initial cc={}'.format(cc))

        if diag_type == 9:
            # do ICD-9-CM edit stuff
            cc = v22i9ed1.icd9_edits(cc, agef_edit, sex, diag, SEDITS, hcc_formats)
            print('after ICD-9 edits cc={}'.format(cc))
            if cc != -1 and cc != 9999:
                if 1 <= cc <= rv.N_CC:
                    C[cc] = 1

            # assign condition category
            elif cc == 9999:
                # primary assignment
                cc = hcc_formats.cc_pri_assignment(diag, diag_type)
                print('after primary cc={}'.format(cc))
                if 1 <= cc <= rv.N_CC:
                    C[cc] = 1
                # duplicate assignment
                cc = hcc_formats.cc_dup_assignment(diag, diag_type)
                print('after duplicate cc={}'.format(cc))
                if 1 <= cc <= rv.N_CC:
                    C[cc] = 1


        if diag_type == 0:
            # do ICD-10-CM edit stuff
            cc = v22i0ed1.icd10_edits(cc, agef_edit, sex, diag, SEDITS, hcc_formats)
            print('after ICD-10 edits cc={}'.format(cc))
            if cc != -1 and cc != 9999:
                if 1 <= cc <= rv.N_CC:
                    C[cc] = 1

            # assign condition category
            elif cc == 9999:
                # primary assignment
                cc = hcc_formats.cc_pri_assignment(diag, diag_type)
                print('after primary cc={}'.format(cc))
                if 1 <= cc <= rv.N_CC:
                    C[cc] = 1
                # duplicate assignment
                cc = hcc_formats.cc_dup_assignment(diag, diag_type)
                print('after duplicate cc={}'.format(cc))
                if 1 <= cc <= rv.N_CC:
                    C[cc] = 1
                # secondary assignment
                cc = hcc_formats.cc_sec_assignment(diag, diag_type)
                print('after secondary cc={}'.format(cc))
                if 1 <= cc <= rv.N_CC:
                    C[cc] = 1
