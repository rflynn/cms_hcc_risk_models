"""
 %MACRO V22H79H1; /* HIERARCHIES */;
 %**********************************************************************
 ***********************************************************************

 1  MACRO NAME:      V22H79H1
 2  PURPOSE:         HCC HIERARCHIES: version 22 of HCCs
                     only 79 CMS HCCs are included
 3  COMMENT:         it is assumed that:
                      -MAX number of CCs are placed into global macro
                       variable N_CC in the main program:
                      -the following arrays are set in the main program
                       ARRAY C(&N_CC)  CC1-CC&N_CC
                       ARRAY HCC(&N_CC) HCC1-HCC&N_CC
                      -format ICD to CC creates only 79 out of &N_CC CMS
                       CCs

 **********************************************************************;
"""


# map priority of HCC codes
HCC_HIER_DICT = {
    8: [9, 10, 11, 12],            # /*Neoplasm 1 */
    9: [10, 11, 12],               # /*Neoplasm 2 */
    10: [11, 12],                  # /*Neoplasm 3 */
    11: [12],                      # /*Neoplasm 4 */
    17: [18, 19],                  # /*Diabetes 1 */
    18: [19],                      # /*Diabetes 2 */
    27: [28, 29, 80],              # /*Liver 1 */
    28: [29],                      # /*Liver 2 */
    46: [48],                      # /*Blood 1 */
    54: [55],                      # /*SA1 */
    57: [58],                      # /*Psychiatric 1 */
    70: [71, 72, 103, 104, 169],   # /*Spinal 1 */
    71: [72, 104, 169],            # /*Spinal 2 */
    72: [169],                     # /*Spinal 3 */
    82: [83, 84],                  # /*Arrest 1 */
    83: [84],                      # /*Arrest 2 */
    86: [87, 88],                  # /*Heart 2 */
    87: [88],                      # /*Heart 3 */
    99: [100],                     # /*CVD 1 */
    103: [104],                    # /*CVD 5 */
    106: [107, 108, 161, 189],     # /*Vascular 1 */
    107: [108],                    # /*Vascular 2 */
    110: [111, 112],               # /*Lung 1 */
    111: [112],                    # /*Lung 2 */
    114: [115],                    # /*Lung 5 */
    134: [135, 136, 137],          # /*Kidney 3 */
    135: [136, 137],               # /*Kidney 4 */
    136: [137],                    # /*Kidney 5 */
    157: [158, 161],               # /*Skin 1 */
    158: [161],                    # /*Skin 2 */
    166: [80, 167],                # /*Injury 1 */
}


def impose_hierarchy(C, HCC):

    # first copy the C array into the HCC array
    for i in range(len(C)):
        HCC[i] = C[i]

    # now impose the hiearchy
    for itop, izeros in HCC_HIER_DICT.items():
        if HCC[itop] == 1 and C[i] == 1:
            for izero in izeros:
                HCC[izero] = 0

    return HCC
