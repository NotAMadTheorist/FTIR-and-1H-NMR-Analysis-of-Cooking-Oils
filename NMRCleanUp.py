import os

# This program changes the CSV files containing data on the 1H-NMR spectra of Canola Oil, Palm Oil, and their
# ...respective mixtures in 2:1 and 1:2 mass ratios, respectively by converting spaces to delimiting commas.

# Assign variables to the paths of CSV files to use
path_Source = os.path.dirname(__file__)
path_NMRCanolaOil = os.path.join(path_Source, "1H-NMR_CanolaOil.csv")
path_NMRPalmOil = os.path.join(path_Source, "1H-NMR_PalmOil.csv")
path_NMR2C1PMix = os.path.join(path_Source, "1H-NMR_2Canola_1Palm_Mixture.csv")

# Read through each file
paths_NMR = [path_NMRCanolaOil,
             path_NMRPalmOil,
             path_NMR2C1PMix]
for path_NMR in paths_NMR:
    with open(path_NMR, 'r', encoding='UTF-8') as file:
        lines_NMRData = file.readlines()
    newColumns = ['Peak Number', 'Range High δ', 'Range Low δ', '%Peak Area', '\n']
    newLine_columns = ','.join(newColumns)
    newLines_NMRData = [newLine_columns]
    for line in lines_NMRData[1:]:
        newLines_NMRData.append(','.join([x for x in line.split(" ") if len(x) != 0]))
    with open(path_NMR, 'w', encoding='UTF-8') as file:
        file.writelines(newLines_NMRData)





path_OIITrial1 = os.path.join(path_Source, "JesuitasSanguyoUy_OrangeII_IR_Trial1.csv")
path_OIITrial2 = os.path.join(path_Source, "JesuitasSanguyoUy_OrangeII_IR_Trial2.csv")
path_ParaRed = os.path.join(path_Source, "AbayaYuag_ParaRed.csv")
path_INBenzene = os.path.join(path_Source, "AbayaYuag_1-Iodo-4-nitrobenzene.csv")

# Plan:
# 1. Read through the line of each file
# 2.

