from Source_FTIR_HNMR.rootDir import (path_RawText_NMRCanolaOil, path_RawText_NMRPalmOil, path_RawText_NMR2C1PMix,
                                      path_NMRCanolaOil, path_NMRPalmOil, path_NMR2C1PMix)

# This program changes the CSV files containing data on the 1H-NMR spectra of Canola Oil, Palm Oil, and their
# ...respective mixtures in 2:1 and 1:2 mass ratios, respectively by converting spaces to delimiting commas.

# Read through each file
paths_RT_NMR = [path_RawText_NMRCanolaOil,
                path_RawText_NMRPalmOil,
                path_RawText_NMR2C1PMix]
paths_NMR = [path_NMRCanolaOil,
             path_NMRPalmOil,
             path_NMR2C1PMix]
for path_NMR, path_RT_NMR in zip(paths_NMR, paths_RT_NMR):
    with open(path_RT_NMR, 'r', encoding='UTF-8') as file:
        lines_NMRData = file.readlines()
    newColumns = ['Peak Number', 'Range High δ', 'Range Low δ', '%Peak Area']
    newLine_columns = ','.join(newColumns) + "\n"
    newLines_NMRData = [newLine_columns]
    for line in lines_NMRData[1:]:
        newLines_NMRData.append(','.join([x for x in line.split(" ") if len(x) != 0]))
    with open(path_NMR, 'w', encoding='UTF-8') as file:
        file.writelines(newLines_NMRData)


