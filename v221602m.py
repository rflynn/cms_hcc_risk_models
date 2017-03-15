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
import v22h79h1
import agesexv2
import regression_variables as rv

# input
#===================================================================
INP = pandas.read_csv('input/2017/person.csv', parse_dates=['DOB'])
IND = pandas.read_csv('input/2017/diag.csv')

OUTDATA = None
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
#======================================================================
for hicno in inpind['HICNO'].unique():

    # get rows from inpind for this patient
    ptrows = inpind.loc[inpind['HICNO']==hicno, :]

    # get demographic data from ptrows
    dob = ptrows.iloc[0]['DOB']
    sex = ptrows.iloc[0]['SEX']
    ltimcaid = ptrows.iloc[0]['LTIMCAID']
    nemcaid = ptrows.iloc[0]['NEMCAID']
    orec = ptrows.iloc[0]['OREC']

    # calculate age
    agef = DATE_ASOF.year - dob.year
    agef_edit = agef

    # initialize dummy variable dictionary
    dumvars = {}
    dumvars['LTIMCAID'] = ltimcaid
    dumvars['NEMCAID'] = nemcaid

    # create demographic regression variables
    disabl, origds, cell, necell = agesexv2.create_demographic_regression_variables(
        agef_edit, sex, orec)

    dumvars['DISABL'] = disabl
    dumvars['ORIGDS'] = origds
    for k,v in cell.items():
        dumvars[k] = v
    for k,v in necell.items():
        dumvars[k] = v

    # initialize C and HCC arrays
    # these are just flags.  we use N_CC + 1 so that
    # we can use 1-based indexing (or simply say C[i] == 1
    # means the i'th condition code is true. C[0] and HCC[0]
    # will always be zero
    C = [0] * (rv.N_CC + 1)
    HCC = [0] * (rv.N_CC + 1)

    # loop over diagnoses and assign CCs
    #======================================================================
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

    # calculate regression variables
    #======================================================================

    # %*interaction;
    OriginallyDisabled_Female = origds * int(sex==2)
    OriginallyDisabled_Male   = origds * int(sex==1)

    dumvars['OriginallyDisabled_Female'] = OriginallyDisabled_Female
    dumvars['OriginallyDisabled_Male'] = OriginallyDisabled_Male

    # %* NE interactions;
    NE_ORIGDS       = int(agef>=65) * int(orec==1)
    NMCAID_NORIGDIS = int(nemcaid <=0 and NE_ORIGDS <=0)
    MCAID_NORIGDIS  = int(nemcaid > 0 and NE_ORIGDS <=0)
    NMCAID_ORIGDIS  = int(nemcaid <=0 and NE_ORIGDS > 0)
    MCAID_ORIGDIS   = int(nemcaid > 0 and NE_ORIGDS > 0)

    dumvars['NMCAID_NORIGDIS'] = NMCAID_NORIGDIS
    dumvars['MCAID_NORIGDIS'] = MCAID_NORIGDIS
    dumvars['NMCAID_ORIGDIS'] = NMCAID_ORIGDIS
    dumvars['MCAID_ORIGDIS'] = MCAID_ORIGDIS

    #%INTER(PVAR =  NMCAID_NORIGDIS,  RLIST = &NE_AGESEXV );
    #%INTER(PVAR =  MCAID_NORIGDIS,   RLIST = &NE_AGESEXV );
    #%INTER(PVAR =  NMCAID_ORIGDIS,   RLIST = &ONE_AGESEXV);
    #%INTER(PVAR =  MCAID_ORIGDIS,    RLIST = &ONE_AGESEXV);
    for key in rv.NE_AGESEXV:
        dumvars['NMCAID_NORIGDIS_{}'.format(key)] = NMCAID_NORIGDIS * dumvars[key]
    for key in rv.NE_AGESEXV:
        dumvars['MCAID_NORIGDIS_{}'.format(key)] = MCAID_NORIGDIS * dumvars[key]
    for key in rv.ONE_AGESEXV:
        dumvars['NMCAID_ORIGDIS_{}'.format(key)] = NMCAID_ORIGDIS * dumvars[key]
    for key in rv.ONE_AGESEXV:
        dumvars['MCAID_ORIGDIS_{}'.format(key)] = MCAID_ORIGDIS * dumvars[key]

    # impose hierarchy
    HCC = v22h79h1.impose_hierarchy(C, HCC)

    # %************************
    # * interaction variables
    # *************************;

    # %*diagnostic categories;
    dumvars['CANCER']          = max(HCC[8], HCC[9], HCC[10], HCC[11], HCC[12])
    dumvars['DIABETES']        = max(HCC[17], HCC[18], HCC[19])
    dumvars['CARD_RESP_FAIL']  = max(HCC[82], HCC[83], HCC[84])
    dumvars['CHF']             = HCC[85]
    dumvars['gCopdCF']         = max(HCC[110], HCC[111], HCC[112])
    dumvars['RENAL']           = max(HCC[134], HCC[135], HCC[136], HCC[137])
    dumvars['SEPSIS']          = HCC[2]
    dumvars['gSubstanceAbuse'] = max(HCC[54], HCC[55])
    dumvars['gPsychiatric']    = max(HCC[57], HCC[58])

    # %*community models interactions ;
    dumvars['HCC47_gCancer']                = HCC[47]*dumvars['CANCER']
    dumvars['HCC85_gDiabetesMellit']        = HCC[85]*dumvars['DIABETES']
    dumvars['HCC85_gCopdCF']                = HCC[85]*dumvars['gCopdCF']
    dumvars['HCC85_gRenal']                 = HCC[85]*dumvars['RENAL']
    dumvars['gRespDepandArre_gCopdCF']      = dumvars['CARD_RESP_FAIL']*dumvars['gCopdCF']
    dumvars['HCC85_HCC96']                  = HCC[85]*HCC[96]
    dumvars['gSubstanceAbuse_gPsychiatric'] = dumvars['gSubstanceAbuse']*dumvars['gPsychiatric']

    # %*institutional model;
    dumvars['PRESSURE_ULCER'] = max(HCC[157], HCC[158]) # /*10/19/2012*/
    dumvars['CHF_gCopdCF']                  = dumvars['CHF']*dumvars['gCopdCF']
    dumvars['gCopdCF_CARD_RESP_FAIL']       = dumvars['gCopdCF']*dumvars['CARD_RESP_FAIL']
    dumvars['SEPSIS_PRESSURE_ULCER']        = dumvars['SEPSIS']*dumvars['PRESSURE_ULCER']
    dumvars['SEPSIS_ARTIF_OPENINGS']        = dumvars['SEPSIS']*(HCC[188])
    dumvars['ART_OPENINGS_PRESSURE_ULCER']  = (HCC[188])*dumvars['PRESSURE_ULCER']
    dumvars['DIABETES_CHF']                 = dumvars['DIABETES']*dumvars['CHF']
    dumvars['gCopdCF_ASP_SPEC_BACT_PNEUM']  = dumvars['gCopdCF']*(HCC[114])
    dumvars['ASP_SPEC_BACT_PNEUM_PRES_ULC'] = (HCC[114])*dumvars['PRESSURE_ULCER']
    dumvars['SEPSIS_ASP_SPEC_BACT_PNEUM']   = dumvars['SEPSIS']*(HCC[114])
    dumvars['SCHIZOPHRENIA_gCopdCF']        = (HCC[57])*dumvars['gCopdCF']
    dumvars['SCHIZOPHRENIA_CHF']            = (HCC[57])*dumvars['CHF']
    dumvars['SCHIZOPHRENIA_SEIZURES']       = (HCC[57])*(HCC[79])

    dumvars['DISABLED_HCC85']          = dumvars['DISABL']*(HCC[85])
    dumvars['DISABLED_PRESSURE_ULCER'] = dumvars['DISABL']*dumvars['PRESSURE_ULCER']
    dumvars['DISABLED_HCC161']         = dumvars['DISABL']*(HCC[161])
    dumvars['DISABLED_HCC39']          = dumvars['DISABL']*(HCC[39])
    dumvars['DISABLED_HCC77']          = dumvars['DISABL']*(HCC[77])
    dumvars['DISABLED_HCC6']           = dumvars['DISABL']*(HCC[6])

    # add the HCC variables to dumvars
    for ii in rv.CC_NUMS:
        key = 'HCC{}'.format(ii)
        dumvars[key] = HCC[ii]

    # calculate risk scores
    #======================================================================
    hcc_risk_scores = {}

    # community models
    #----------------------------------------------------------------------
    risk_score = 0.0
    for var in rv.COMM_REGA:
        risk_score += dumvars[var] * hcccoefn['{}_{}'.format('CNA', var)][0]
    hcc_risk_scores['CNA'] = risk_score

    risk_score = 0.0
    for var in rv.COMM_REGD:
        risk_score += dumvars[var] * hcccoefn['{}_{}'.format('CND', var)][0]
    hcc_risk_scores['CND'] = risk_score

    risk_score = 0.0
    for var in rv.COMM_REGA:
        risk_score += dumvars[var] * hcccoefn['{}_{}'.format('CFA', var)][0]
    hcc_risk_scores['CFA'] = risk_score

    risk_score = 0.0
    for var in rv.COMM_REGD:
        risk_score += dumvars[var] * hcccoefn['{}_{}'.format('CFD', var)][0]
    hcc_risk_scores['CFD'] = risk_score

    risk_score = 0.0
    for var in rv.COMM_REGA:
        risk_score += dumvars[var] * hcccoefn['{}_{}'.format('CPA', var)][0]
    hcc_risk_scores['CPA'] = risk_score

    risk_score = 0.0
    for var in rv.COMM_REGD:
        risk_score += dumvars[var] * hcccoefn['{}_{}'.format('CPD', var)][0]
    hcc_risk_scores['CPD'] = risk_score

    # institutional model
    #----------------------------------------------------------------------
    risk_score = 0.0
    for var in rv.INST_REG:
        risk_score += dumvars[var] * hcccoefn['{}_{}'.format('INS', var)][0]
    hcc_risk_scores['INS'] = risk_score

    # new enrollees model
    #----------------------------------------------------------------------
    risk_score = 0.0
    for var in rv.NE_REG:
        risk_score += dumvars[var] * hcccoefn['{}_{}'.format('NE', var)][0]
    hcc_risk_scores['NE'] = risk_score

    # new enrollees model
    #----------------------------------------------------------------------
    risk_score = 0.0
    for var in rv.NE_REG:
        risk_score += dumvars[var] * hcccoefn['{}_{}'.format('SNPNE', var)][0]
    hcc_risk_scores['SNPNE'] = risk_score

    # OUTPUT
    #----------------------------------------------------------------------
    print()
    print('hcc_risk_scores: ', hcc_risk_scores)
