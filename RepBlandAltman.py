# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 13:19:21 2023

@author: Logan Wade

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
the steps outlined in the appendix. Example data is the observed difference between a marker-based motion capture system, 
and a markerless motion capture system, for the left ankle joint in the sagittal plane during one stride of walking, 
with up to 10 stride performed per person and each stride normalised to 101 points. Thus the total number of observations 
for each participant may differ (strides x 101 data points).

If using this code, please cite: WADE, L., NEEDHAM, L., EVANS, M., MCGUIGAN, P., COLYER, S., COSKER, D. & BILZON, J. 2023. Examination of 2D frontal and sagittal markerless motion capture: Implications for markerless applications. PLOS ONE, 18, e0293917.)

    Please report any issues with this code using github or emailing lw2175@bath.ac.uk
    """


import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols



def observations(data): # Identify how many ovservation were obtained for each participant
    participants = pd.unique(data['participants'])
    obsv = np.zeros(len(participants), dtype='int64')
    for count, p in enumerate(participants):
        obsv[count] = np.sum(data['participants'].str.count(p))
    
    return obsv


def ANOVA_MS(data):
    model = ols('variables ~ participants', data = data).fit()
    anova_result = sm.stats.anova_lm(model, typ=2)
    MS_between = anova_result['sum_sq']['participants'] / anova_result['df']['participants']
    MS_within = anova_result['sum_sq']['Residual'] / anova_result['df']['Residual']
    
    return MS_between, MS_within


##Calculate Variance and SD from ANOVA results
def RBA_SD(obsv, MS_between, MS_within):
    diff_accrossSubjects = MS_between - MS_within
    diff_withinSubject = MS_within
    
    #formula is ((sum(mi)^2) - sum(mi^2)) / (n - 1) * sum(mi)
    #where m is the number of observations for participant i
    #see appendix of published manuscript for indepth explanation of these steps below : WADE, L., NEEDHAM, L., EVANS, M., MCGUIGAN, P., COLYER, S., COSKER, D. & BILZON, J. 2023. Examination of 2D frontal and sagittal markerless motion capture: Implications for markerless applications. PLOS ONE, 18, e0293917.)
    num_observations = ( ( np.square( obsv.sum() ) ) - np.sum( np.square(obsv) ) ) / ( (len(obsv) - 1) * obsv.sum() )

    varianceHetro = diff_accrossSubjects / num_observations
    
    totalVariance = varianceHetro + diff_withinSubject
    
    SD = np.sqrt(totalVariance)
    
    return (SD)


def RBA_values(data, SD):
    bias = data['variables'].mean()
    LOA_L = bias - (SD * 1.96)
    LOA_U = bias + (SD * 1.96)

    return bias, LOA_L, LOA_U



#Find out how many SD are outside the LOA
def commonSenseTesting(data, LOA_L, LOA_U):   
    commonSense = (data['variables'] > LOA_L) & (data['variables'] < LOA_U)
    length = len(data['variables'])
    commonSense = sum(commonSense==True) / length

    return commonSense

       
def main(*args):
    
    #example data
    if 'data' in locals():
        pass
    else:
        #load in example data with using the dataset included with this code
        data = pd.read_csv('ExampleArray_SagittalankleAngle.csv')
        data = data.drop('Unnamed: 0', axis=1)
    
    #calculate number of observations per participant
    obsv = observations(data)
    
    #calcualte MS between participant and within participant values from One Way ANOVA
    MS_between, MS_within = ANOVA_MS(data)
    
    #calculate SD using Repeat Measures Bland-Altman formula
    SD = RBA_SD(obsv, MS_between, MS_within)
    
    #Calculate bias and limits of agreement
    bias, LOA_L, LOA_U = RBA_values(data, SD)
    
    #Perform common sense testing to ensure 95% of the values align with expected 95% CI of LOA upper and lower
    commonSense = commonSenseTesting(data, LOA_L, LOA_U)
    
    return data, obsv, bias, SD, LOA_L, LOA_U, commonSense



if __name__ == '__main__':
    #data, obsv, SD = main(data) #runs code on new data
    data, obsv, bias, SD, LOA_L, LOA_U, commonSense = main() #runs code on example data (same dataset as in published paper WADE, L., NEEDHAM, L., EVANS, M., MCGUIGAN, P., COLYER, S., COSKER, D. & BILZON, J. 2023. Examination of 2D frontal and sagittal markerless motion capture: Implications for markerless applications. PLOS ONE, 18, e0293917.)
    print('Bias:', bias)
    print('SD:', SD)
    print('LOA:', LOA_L, '-', LOA_U)
