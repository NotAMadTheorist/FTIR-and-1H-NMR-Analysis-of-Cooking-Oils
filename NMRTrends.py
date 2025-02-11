import pandas as pd
import os
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats.mstats import pearsonr

# This program compares the peak areas of analogous peaks in the 1H-NMR spectra of Canola Oil, Palm Oil, and their
# ...respective mixtures in 2:1 and 1:2 mass ratios, respectively by plotting bar charts.

# Assign variables to the paths of CSV files to use
path_Source = os.path.dirname(__file__)
path_NMRCanolaOil = os.path.join(path_Source, "1H-NMR_CanolaOil.csv")
path_NMRPalmOil = os.path.join(path_Source, "1H-NMR_PalmOil.csv")
path_NMR2C1PMix = os.path.join(path_Source, "1H-NMR_2Canola_1Palm_Mixture.csv")

# Paths are arranged from most saturated to least saturated oils on average.
path_NMRSamples = [path_NMRPalmOil, path_NMR2C1PMix, path_NMRCanolaOil]
names_NMRSamples = ['PO', '2C:1P', 'CO']
colors_NMRSamples = ['#f34f1c', '#ffba01','#7fbc00']
percentCanola_NMRSamples = [0.00,  1.0308/(0.5125+1.0308), 1.00]

# Create data frames for the oil samples
DFColumns = ["Peak Number","Range High δ","Range Low δ","%Peak Area"]
dataFrames_NMRSamples = [pd.read_csv(path, usecols=DFColumns) for path in path_NMRSamples]
numberOfSamples = len(path_NMRSamples)
numberOfPeaks = dataFrames_NMRSamples[0].shape[0]

# Group the peak areas that are analogous to each other, and
# Get the average high and low range values for the chemical shifts of each group of analogous peaks in 2 s.f.
peakAreas_Grouped = []
highShifts_Grouped = []
lowShifts_Grouped = []
for peakIndex in range(numberOfPeaks):
    group = []
    highShifts = []
    lowShifts = []
    for DFSample in dataFrames_NMRSamples:
        group.append(DFSample.iat[peakIndex, 3])
        highShifts.append(DFSample.iat[peakIndex, 1])
        lowShifts.append(DFSample.iat[peakIndex, 2])
    peakAreas_Grouped.append(group)
    highShifts_Grouped.append(round(sum(highShifts)/numberOfSamples, 2))
    lowShifts_Grouped.append(round(sum(lowShifts)/numberOfSamples, 2))

# Create individual bar charts of the peak areas for each group of analogous peaks
# Summarize by showing 5 x 2 subplots at a time
maxNumber_subplots = 5
peakIndex = 0
rowPeakIndex = 0
colPeakIndex = 0

while peakIndex < numberOfPeaks:
    figure, axis = plt.subplots(2, maxNumber_subplots, figsize=(11.0, 6.0))
    while rowPeakIndex < 2:
        while colPeakIndex < maxNumber_subplots:
            # Create a subplot for selected group of analogous peaks
            axis[rowPeakIndex, colPeakIndex].bar(names_NMRSamples, peakAreas_Grouped[peakIndex], color=colors_NMRSamples)
            axis[rowPeakIndex, colPeakIndex].set_title(f'{lowShifts_Grouped[peakIndex]} to {highShifts_Grouped[peakIndex]} δ')
            if colPeakIndex == 0:
                axis[rowPeakIndex, colPeakIndex].set(ylabel = '% Peak Area')
            peakIndex += 1
            colPeakIndex += 1
        colPeakIndex = 0
        rowPeakIndex += 1
    rowPeakIndex = 0
    plt.subplots_adjust(hspace=3.0, bottom=0.29, right=0.90)
    figure.tight_layout(pad=1.5)
    plt.show()

# Create combined bar chart of the peak areas for each group of analogous peaks
# Create a dataframe where each row represents a peak
DFCombinedBar_List = []
DFCombinedBar_Columns = ["Range of Chemical Shift (δ)"] + names_NMRSamples
for peakIndex in range(numberOfPeaks):
    peakRange = f'{lowShifts_Grouped[peakIndex]:.1f}-{highShifts_Grouped[peakIndex]:.1f}'
    DFRow = [peakRange] + peakAreas_Grouped[peakIndex]
    DFCombinedBar_List.append(DFRow)
DFCombinedBar = pd.DataFrame(DFCombinedBar_List, columns=DFCombinedBar_Columns)
DFCombinedBar.plot(x='Range of Chemical Shift (δ)',
                   logy=True,
                   kind='bar',
                   stacked=False,
                   title='Variation of H-NMR Peak Areas with Oil Type',
                   figsize=(11.0, 8.0),
                   colormap=LinearSegmentedColormap.from_list("mycmap", colors_NMRSamples),
                   position=1.0)
plt.ylabel("% Peak Area")
plt.legend(loc='upper left')
plt.subplots_adjust(bottom=0.33)
plt.grid()
plt.show()

# Create combined bar chart of the relative ratios of protons showing up for each peak
# Again, create the corresponding dataframe first.
DFCombinedBar_List = []
DFCombinedBar_Columns = ["Range of Chemical Shift (δ)"] + names_NMRSamples
for peakIndex in range(numberOfPeaks):
    peakRange = f'{lowShifts_Grouped[peakIndex]:.1f}-{highShifts_Grouped[peakIndex]:.1f}'
    minimumArea = min(peakAreas_Grouped[peakIndex])
    ratioProtons = [peakArea/minimumArea for peakArea in peakAreas_Grouped[peakIndex]]
    DFRow = [peakRange] + ratioProtons
    DFCombinedBar_List.append(DFRow)
DFCombinedBar = pd.DataFrame(DFCombinedBar_List, columns=DFCombinedBar_Columns)
DFCombinedBar.plot(x='Range of Chemical Shift (δ)',
                   kind='bar',
                   stacked=False,
                   title='Variation of Proton Ratios per Peak with Oil Type',
                   figsize=(11.0, 8.0),
                   colormap=LinearSegmentedColormap.from_list("mycmap", colors_NMRSamples),
                   position=1.0)
plt.ylabel("Relative Ratio")
plt.legend(loc='upper left')
plt.subplots_adjust(bottom=0.33)
plt.grid()
plt.show()

# For each peak, compute the Pearson correlation coefficient between mass %canola oil and peak areas
# ... then save the summarized correlation data as a CSV file
DFPeakCorrelation_List = []
DFPeakCorrelation_Columns = (["Peak Number", "Range of Chemical Shift (δ)"]
                             + [f'{x} ({y:.1%} CO)' for x, y in zip(names_NMRSamples, percentCanola_NMRSamples)]
                             + ["Pearson Coefficient", "p-value", "Significant? (p < 5%)", "Trend"])
for peakIndex in range(numberOfPeaks):
    peakNumber = peakIndex + 1
    peakRange = f'{lowShifts_Grouped[peakIndex]:.2f}-{highShifts_Grouped[peakIndex]:.2f}'
    peakAreas = peakAreas_Grouped[peakIndex]
    percentCanola = percentCanola_NMRSamples
    pearsonResults = pearsonr(percentCanola, peakAreas)
    pearsonCoeff, pValue = pearsonResults
    boolSignificance = pValue < 0.05
    if not boolSignificance:
        signTrend = "Trend not significant"
    else:
        if pearsonCoeff > 0:
            signTrend = "Positive trend (+)"
        else:
            signTrend = "Negative trend (-)"
    DFRow = ([peakNumber, peakRange] + peakAreas_Grouped[peakIndex]
             + [pearsonCoeff, pValue, boolSignificance, signTrend])
    DFPeakCorrelation_List.append(DFRow)
DFPeakCorrelation = pd.DataFrame(DFPeakCorrelation_List, columns=DFPeakCorrelation_Columns)
DFPeakCorrelation.to_csv("1H-NMR_AllPeakCorrelations.csv", index=False)

# Another file containing only the significant correlations is saved.
DFSignificantCorr = DFPeakCorrelation.loc[DFPeakCorrelation["Significant? (p < 5%)"] == True]
DFSignificantCorr.to_csv("1H-NMR_SigPeakCorrelations.csv", index=False)

