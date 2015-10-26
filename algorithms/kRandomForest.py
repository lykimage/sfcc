__author__ = 'kunal'
import numpy as np
import pandas as pd
import csv
from sklearn.ensemble import RandomForestClassifier as rfc

# Train Data
trainDf = pd.read_csv('../data/train.csv', header=0, parse_dates=['Dates'])

trainDf['Year'] = trainDf['Dates'].map(lambda x: x.year)
trainDf['Week'] = trainDf['Dates'].map(lambda x: x.week)
trainDf['Hour'] = trainDf['Dates'].map(lambda x: x.hour)

# Change string categories to integer classifiers
# determine all values
Categories = list(enumerate(sorted(np.unique(trainDf['Category']))))
Descriptions = list(enumerate(sorted(np.unique(trainDf['Descript']))))
DaysOfWeeks = list(enumerate(sorted(np.unique(trainDf['DayOfWeek']))))
PdDistricts = list(enumerate(sorted(np.unique(trainDf['PdDistrict']))))
Resolutions = list(enumerate(sorted(np.unique(trainDf['Resolution']))))
# set up dictionaries
CategoriesDict = {name: i for i, name in Categories}
DescriptionsDict = {name: i for i, name in Descriptions}
DaysOfWeeksDict = {name: i for i, name in DaysOfWeeks}
PdDistrictsDict = {name: i for i, name in PdDistricts}
ResolutionsDict = {name: i for i, name in Resolutions}
# Convert all strings to int
trainDf.Category = trainDf.Category.map(lambda x: CategoriesDict[x]).astype(int)
trainDf.Descript = trainDf.Descript.map(lambda x: DescriptionsDict[x]).astype(int)
trainDf.DayOfWeek = trainDf.DayOfWeek.map(lambda x: DaysOfWeeksDict[x]).astype(int)
trainDf.PdDistrict = trainDf.PdDistrict.map(lambda x: PdDistrictsDict[x]).astype(int)
trainDf.Resolution = trainDf.Resolution.map(lambda x: ResolutionsDict[x]).astype(int)

# TODO: Fill missing values if any
# Compute mean of a column and fill missing values
# def computeMean(column):
#     columnName = str(column)
#     meanValue = trainDf[columnName].dropna().mean()
#     if len(trainDf.column[ trainDf.column.isnull()]) > 0:
#         trainDf.loc[(trainDf.column.isnull()), columnName] = meanValue
#
# computeMean(Category)

# select the following columns only
# trainDf = [col for col in trainDf.columns if col in ['Descript', 'DayOfWeek', 'PdDistrict', 'Address']]
# OR :
# select all columns except
# Dates,Category,Descript,DayOfWeek,PdDistrict,Resolution,Address,X,Y,Year,Week,Hour
trainDf = trainDf.drop(['Dates', 'Descript', 'Resolution', 'Address', 'X', 'Y'], axis=1)

# Test data
testDf = pd.read_csv('../data/test.csv', header=0, parse_dates=['Dates'])
testDf['Year'] = testDf['Dates'].map(lambda x: x.year)
testDf['Week'] = testDf['Dates'].map(lambda x: x.week)
testDf['Hour'] = testDf['Dates'].map(lambda x: x.hour)

ids = testDf['Id'].values
# Id,Dates,DayOfWeek,PdDistrict,Address,X,Y,Year,Week,Hour
testDf = testDf.drop(['Id', 'Dates', 'Address', 'X', 'Y'], axis=1)

PdDistricts = list(enumerate(sorted(np.unique(testDf['PdDistrict']))))
DaysOfWeeks = list(enumerate(sorted(np.unique(testDf['DayOfWeek']))))
PdDistrictsDict = {name: i for i, name in PdDistricts}
DaysOfWeeksDict = {name: i for i, name in DaysOfWeeks}
testDf.PdDistrict = testDf.PdDistrict.map(lambda x: PdDistrictsDict[x]).astype(int)
testDf.DayOfWeek = testDf.DayOfWeek.map(lambda x: DaysOfWeeksDict[x]).astype(int)

# Random Forest Algorithm
print list(trainDf.columns.values)
print list(testDf.columns.values)

# back to numpy format
trainData = trainDf.values
testData = testDf.values

print 'Training...'
forest = rfc(n_estimators=25)
forest = forest.fit(trainData[0::,1::], trainData[0::,0])

print 'Predicting...'
output = forest.predict_proba(testData).astype(float)
output = output.tolist()

predictions_file = open("../submissionRF.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["Id",'ARSON','ASSAULT','BAD CHECKS','BRIBERY','BURGLARY','DISORDERLY CONDUCT',
                           'DRIVING UNDER THE INFLUENCE','DRUG/NARCOTIC','DRUNKENNESS','EMBEZZLEMENT','EXTORTION',
                           'FAMILY OFFENSES','FORGERY/COUNTERFEITING','FRAUD','GAMBLING','KIDNAPPING','LARCENY/THEFT',
                           'LIQUOR LAWS','LOITERING','MISSING PERSON','NON-CRIMINAL','OTHER OFFENSES',
                           'PORNOGRAPHY/OBSCENE MAT','PROSTITUTION','RECOVERED VEHICLE','ROBBERY','RUNAWAY',
                           'SECONDARY CODES','SEX OFFENSES FORCIBLE','SEX OFFENSES NON FORCIBLE','STOLEN PROPERTY',
                           'SUICIDE','SUSPICIOUS OCC','TREA','TRESPASS','VANDALISM','VEHICLE THEFT','WARRANTS',
                           'WEAPON LAWS'])
for x in range(len(output)):
    output[x].insert(0, x)
    open_file_object.writerow(output[x])
predictions_file.close()
print 'Done.'
