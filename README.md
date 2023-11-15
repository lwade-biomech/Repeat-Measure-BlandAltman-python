Python Script for Repeat measures bland-altman analysis

INPUT: All data points (difference between methods), organised into long format (columns=[participants, variables])

OUTPUT: 
    - Data - Original pandas Dataframe of data in long format
    - obsv - Number of observations per participant
    - bias - Mean difference between two methods
    - SD - Repeat measures Bland-altman SD that accounts for multiple values per participant
    - LOA_L - Repeat measures Bland-altman lower limits of agreement
    - LOA_U - Repeat measures Bland-altman upper limits of agreement
    -CommonSense - Outputs the % of values that sit within the RBA LOA lower and upper limits.
                    This value should be close to 0.95 (95% CI)

Running this script directly will use example data (difference between two methods) provided alongside this code.
This will also occur if the main() function is run without an input (e.g. data, obsv, bias, SD, LOA_L, LOA_U, commonSense = main()). 
This example data is the same as the data provided in our published manuscript, so users can follow along with 
the steps outlined in the appendix. Example data is the observed difference between a
a marker-based motion capture system, and a markerless motion capture system, for the left
ankle joint in the sagittal plane during one stride of walking.

If using this code, please cite: WADE, L., NEEDHAM, L., EVANS, M., MCGUIGAN, P., COLYER, S., COSKER, D. & BILZON, J. 2023. Examination of 2D frontal and sagittal markerless motion capture: Implications for markerless applications. PLOS ONE, 18, e0293917.)
Please report any issues with this code using github or emailing lw2175@bath.ac.uk


