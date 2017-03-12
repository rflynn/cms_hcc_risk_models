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


# input
#===================================================================
INP = pandas.read_csv('input/2017/person.csv', parse_dates=['DOB'])
IND = pandas.read_csv('input/2017/diag.csv')

# merge person and diag data (one row per person/diag
inpind = pandas.merge(INP, IND, on='HICNO')
inpind = inpind.sort_values('HICNO')

IDVAR = 'HICNO'
KEEPVAR = [IDVAR] + v221602p.INPUTVARS + v221602p.SCOREVARS + \
          v221602p.DEMVARS + v221602p.HCCV22_list79 + v221602p.CCV22_list79
SEDITS = True
DATE_ASOF = datetime.date(2016, 2, 1)

# read regression coefficients
fname = 'cms_models/2017/cms_hcc_v2216_79_02/C2214O5P.csv'
hcccoefn = pandas.read_csv(fname)

# read formats file
fname = 'cms_models/2017/cms_hcc_v2216_79_02/F221690P.csv'
hcc_formats = formats.HccFormats(fname)



N_CC=201 #max # of HCCs

# %**********************************************************************
# * step2: define internal macro variables
# **********************************************************************;

# %* age/sex variables for Community Aged regression;
AGESEXVA = [
    'F65_69','F70_74','F75_79','F80_84','F85_89','F90_94','F95_GT',
    'M65_69','M70_74','M75_79','M80_84','M85_89','M90_94','M95_GT',
]

# %* age/sex variables for Community Disabled regression;
AGESEXVD = [
    'F0_34','F35_44','F45_54','F55_59','F60_64',
    'M0_34','M35_44','M45_54','M55_59','M60_64',
]

# %* diagnostic categories necessary to create interaction variables;
DIAG_CAT = [
    'CANCER','DIABETES','CHF','CARD_RESP_FAIL','gCopdCF','RENAL',
    'SEPSIS','PRESSURE_ULCER','gSubstanceAbuse','gPsychiatric'
]

# %*orig disabled interactions for Community Aged regressions;
ORIG_INT = ['OriginallyDisabled_Female', 'OriginallyDisabled_Male']

# %*interaction variables for Community Aged regressions;
INTERRACC_VARSA = [
    'HCC47_gCancer', 'HCC85_gDiabetesMellit', 'HCC85_gCopdCF', 'HCC85_gRenal',
    'gRespDepandArre_gCopdCF', 'HCC85_HCC96',
]

# %*interaction variables for Community Disabled regressions;
INTERRACC_VARSD = [
    'HCC47_gCancer', 'HCC85_gDiabetesMellit', 'HCC85_gCopdCF', 'HCC85_gRenal',
    'gRespDepandArre_gCopdCF', 'HCC85_HCC96', 'gSubstanceAbuse_gPsychiatric',
]

# %*variables for Community Aged regressions ;
COMM_REGA = AGESEXVA + ORIG_INT + v221602p.HCCV22_list79 + INTERRACC_VARSA

# %*variables for Community Disabled regressions ;
COMM_REGD = AGESEXVD + v221602p.HCCV22_list79 + INTERRACC_VARSD

# %* age/sex variables for Insititutional regression;
AGESEXV = [
    'F0_34','F35_44','F45_54','F55_59','F60_64','F65_69',
    'F70_74','F75_79','F80_84','F85_89','F90_94','F95_GT',
    'M0_34','M35_44','M45_54','M55_59','M60_64','M65_69',
    'M70_74','M75_79','M80_84','M85_89','M90_94','M95_GT',
]

# %*interaction variables for Institutional regression;
INTERRACI_VARS = [
    'DISABLED_HCC85',       'DISABLED_PRESSURE_ULCER',
    'DISABLED_HCC161',      'DISABLED_HCC39',
    'DISABLED_HCC77',       'DISABLED_HCC6',
    'CHF_gCopdCF',
    'gCopdCF_CARD_RESP_FAIL',
    'SEPSIS_PRESSURE_ULCER',
    'SEPSIS_ARTIF_OPENINGS',
    'ART_OPENINGS_PRESSURE_ULCER',
    'DIABETES_CHF',
    'gCopdCF_ASP_SPEC_BACT_PNEUM',
    'ASP_SPEC_BACT_PNEUM_PRES_ULC',
    'SEPSIS_ASP_SPEC_BACT_PNEUM',
    'SCHIZOPHRENIA_gCopdCF',
    'SCHIZOPHRENIA_CHF',
    'SCHIZOPHRENIA_SEIZURES',
]


# %*variables for Institutional regression;
INST_REG = AGESEXV + ['LTIMCAID', 'ORIGDS'] + INTERRACI_VARS + v221602p.HCCV22_list79

# %*age/sex variables for non-ORIGDS New Enrollee and SNP New Enrollee interactions;
NE_AGESEXV = [
      'NEF0_34',   'NEF35_44',  'NEF45_54',  'NEF55_59',  'NEF60_64',
      'NEF65',     'NEF66',     'NEF67',     'NEF68',     'NEF69',
      'NEF70_74',  'NEF75_79',  'NEF80_84',
      'NEF85_89',  'NEF90_94',  'NEF95_GT',
      'NEM0_34',   'NEM35_44',  'NEM45_54',  'NEM55_59',  'NEM60_64',
      'NEM65',     'NEM66',     'NEM67',     'NEM68',     'NEM69',
      'NEM70_74',  'NEM75_79',  'NEM80_84',
      'NEM85_89',  'NEM90_94',  'NEM95_GT',
]

# %*age/sex variables for ORIGDS New Enrollee and SNP New Enrollee interactions;
ONE_AGESEXV = [
      'NEF65',     'NEF66',     'NEF67',     'NEF68',     'NEF69',
      'NEF70_74',  'NEF75_79',  'NEF80_84',
      'NEF85_89',  'NEF90_94',  'NEF95_GT',
      'NEM65',     'NEM66',     'NEM67',     'NEM68',     'NEM69',
      'NEM70_74',  'NEM75_79',  'NEM80_84',
      'NEM85_89',  'NEM90_94',  'NEM95_GT',
]


# %*variables for New Enrollee and SNP New Enrollee regression;
NE_REG = [
    'NMCAID_NORIGDIS_NEF0_34',       'NMCAID_NORIGDIS_NEF35_44',
    'NMCAID_NORIGDIS_NEF45_54',      'NMCAID_NORIGDIS_NEF55_59',
    'NMCAID_NORIGDIS_NEF60_64',      'NMCAID_NORIGDIS_NEF65',
    'NMCAID_NORIGDIS_NEF66',         'NMCAID_NORIGDIS_NEF67',
    'NMCAID_NORIGDIS_NEF68',         'NMCAID_NORIGDIS_NEF69',
    'NMCAID_NORIGDIS_NEF70_74',      'NMCAID_NORIGDIS_NEF75_79',
    'NMCAID_NORIGDIS_NEF80_84',      'NMCAID_NORIGDIS_NEF85_89',
    'NMCAID_NORIGDIS_NEF90_94',      'NMCAID_NORIGDIS_NEF95_GT',

    'NMCAID_NORIGDIS_NEM0_34',       'NMCAID_NORIGDIS_NEM35_44',
    'NMCAID_NORIGDIS_NEM45_54',      'NMCAID_NORIGDIS_NEM55_59',
    'NMCAID_NORIGDIS_NEM60_64',      'NMCAID_NORIGDIS_NEM65',
    'NMCAID_NORIGDIS_NEM66',         'NMCAID_NORIGDIS_NEM67',
    'NMCAID_NORIGDIS_NEM68',         'NMCAID_NORIGDIS_NEM69',
    'NMCAID_NORIGDIS_NEM70_74',      'NMCAID_NORIGDIS_NEM75_79',
    'NMCAID_NORIGDIS_NEM80_84',      'NMCAID_NORIGDIS_NEM85_89',
    'NMCAID_NORIGDIS_NEM90_94',      'NMCAID_NORIGDIS_NEM95_GT',

    'MCAID_NORIGDIS_NEF0_34',        'MCAID_NORIGDIS_NEF35_44',
    'MCAID_NORIGDIS_NEF45_54',       'MCAID_NORIGDIS_NEF55_59',
    'MCAID_NORIGDIS_NEF60_64',       'MCAID_NORIGDIS_NEF65',
    'MCAID_NORIGDIS_NEF66',          'MCAID_NORIGDIS_NEF67',
    'MCAID_NORIGDIS_NEF68',          'MCAID_NORIGDIS_NEF69',
    'MCAID_NORIGDIS_NEF70_74',       'MCAID_NORIGDIS_NEF75_79',
    'MCAID_NORIGDIS_NEF80_84',       'MCAID_NORIGDIS_NEF85_89',
    'MCAID_NORIGDIS_NEF90_94',       'MCAID_NORIGDIS_NEF95_GT',

    'MCAID_NORIGDIS_NEM0_34',        'MCAID_NORIGDIS_NEM35_44',
    'MCAID_NORIGDIS_NEM45_54',       'MCAID_NORIGDIS_NEM55_59',
    'MCAID_NORIGDIS_NEM60_64',       'MCAID_NORIGDIS_NEM65',
    'MCAID_NORIGDIS_NEM66',          'MCAID_NORIGDIS_NEM67',
    'MCAID_NORIGDIS_NEM68',          'MCAID_NORIGDIS_NEM69',
    'MCAID_NORIGDIS_NEM70_74',       'MCAID_NORIGDIS_NEM75_79',
    'MCAID_NORIGDIS_NEM80_84',       'MCAID_NORIGDIS_NEM85_89',
    'MCAID_NORIGDIS_NEM90_94',       'MCAID_NORIGDIS_NEM95_GT',

    'NMCAID_ORIGDIS_NEF65',          'NMCAID_ORIGDIS_NEF66',
    'NMCAID_ORIGDIS_NEF67',          'NMCAID_ORIGDIS_NEF68',
    'NMCAID_ORIGDIS_NEF69',          'NMCAID_ORIGDIS_NEF70_74',
    'NMCAID_ORIGDIS_NEF75_79',       'NMCAID_ORIGDIS_NEF80_84',
    'NMCAID_ORIGDIS_NEF85_89',       'NMCAID_ORIGDIS_NEF90_94',
    'NMCAID_ORIGDIS_NEF95_GT',

    'NMCAID_ORIGDIS_NEM65',          'NMCAID_ORIGDIS_NEM66',
    'NMCAID_ORIGDIS_NEM67',          'NMCAID_ORIGDIS_NEM68',
    'NMCAID_ORIGDIS_NEM69',          'NMCAID_ORIGDIS_NEM70_74',
    'NMCAID_ORIGDIS_NEM75_79',       'NMCAID_ORIGDIS_NEM80_84',
    'NMCAID_ORIGDIS_NEM85_89',       'NMCAID_ORIGDIS_NEM90_94',
    'NMCAID_ORIGDIS_NEM95_GT',

    'MCAID_ORIGDIS_NEF65',           'MCAID_ORIGDIS_NEF66',
    'MCAID_ORIGDIS_NEF67',           'MCAID_ORIGDIS_NEF68',
    'MCAID_ORIGDIS_NEF69',           'MCAID_ORIGDIS_NEF70_74',
    'MCAID_ORIGDIS_NEF75_79',        'MCAID_ORIGDIS_NEF80_84',
    'MCAID_ORIGDIS_NEF85_89',        'MCAID_ORIGDIS_NEF90_94',
    'MCAID_ORIGDIS_NEF95_GT',

    'MCAID_ORIGDIS_NEM65',           'MCAID_ORIGDIS_NEM66',
    'MCAID_ORIGDIS_NEM67',           'MCAID_ORIGDIS_NEM68',
    'MCAID_ORIGDIS_NEM69',           'MCAID_ORIGDIS_NEM70_74',
    'MCAID_ORIGDIS_NEM75_79',        'MCAID_ORIGDIS_NEM80_84',
    'MCAID_ORIGDIS_NEM85_89',        'MCAID_ORIGDIS_NEM90_94',
    'MCAID_ORIGDIS_NEM95_GT',
    ]

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

    # initialize C and HCC arrays
    # these are just flags.  we use N_CC + 1 so that
    # we can use 1-based indexing (or simply say C[i] == 1
    # means the i'th condition code is true. C[0] and HCC[0]
    # will always be zero
    C = [0] * (N_CC + 1)
    HCC = [0] * (N_CC + 1)

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
                if 1 <= cc <= N_CC:
                    C[cc] = 1

            # assign condition category
            elif cc == 9999:
                # primary assignment
                cc = hcc_formats.cc_pri_assignment(diag, diag_type)
                print('after primary cc={}'.format(cc))
                if 1 <= cc <= N_CC:
                    C[cc] = 1
                # duplicate assignment
                cc = hcc_formats.cc_dup_assignment(diag, diag_type)
                print('after duplicate cc={}'.format(cc))
                if 1 <= cc <= N_CC:
                    C[cc] = 1


        if diag_type == 0:
            # do ICD-10-CM edit stuff
            cc = v22i0ed1.icd10_edits(cc, agef_edit, sex, diag, SEDITS, hcc_formats)
            print('after ICD-10 edits cc={}'.format(cc))
            if cc != -1 and cc != 9999:
                if 1 <= cc <= N_CC:
                    C[cc] = 1

            # assign condition category
            elif cc == 9999:
                # primary assignment
                cc = hcc_formats.cc_pri_assignment(diag, diag_type)
                print('after primary cc={}'.format(cc))
                if 1 <= cc <= N_CC:
                    C[cc] = 1
                # duplicate assignment
                cc = hcc_formats.cc_dup_assignment(diag, diag_type)
                print('after duplicate cc={}'.format(cc))
                if 1 <= cc <= N_CC:
                    C[cc] = 1
                # secondary assignment
                cc = hcc_formats.cc_sec_assignment(diag, diag_type)
                print('after secondary cc={}'.format(cc))
                if 1 <= cc <= N_CC:
                    C[cc] = 1
