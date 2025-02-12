import pandas as pd
import os
from matplotlib import pyplot as plt
from scipy.stats.mstats import pearsonr
from matplotlib.ticker import MultipleLocator
from matplotlib.colors import LinearSegmentedColormap

# This program plots and compares the FTIR spectra of Canola Oil, Palm Oil, and their respective mixtures in 2:1
# ...and 1:2 mass ratios, respectively, in KBr. FTIR absorption data was obtained via IRAffinity spectrometer.

# Assign variables to the paths of CSV files to use
path_Source = os.path.dirname(__file__)
path_FTIRCanolaOil = os.path.join(path_Source, "FTIR_CanolaOil.csv")
path_FTIRPalmOil = os.path.join(path_Source, "FTIR_PalmOil.csv")
path_FTIR2C1PMix = os.path.join(path_Source, "FTIR_2Canola_1Palm_Mixture.csv")
path_FTIR1C2PMix = os.path.join(path_Source, "FTIR_1Canola_2Palm_Mixture.csv")

# Paths are arranged from most saturated to least saturated oils on average.
path_FTIRSamples = [path_FTIRPalmOil, path_FTIR1C2PMix, path_FTIR2C1PMix, path_FTIRCanolaOil]
names_FTIRSamples = ["PO", "1C:2P", "2C:1P", "CO"]
fullNames_FTIRSamples = ["Palm Oil",
                         "1:2 Mixture of Canola and Palm Oils",
                         "2:1 Mixture of Canola and Palm Oils",
                         "Canola Oil"]
nameAppend = " in KBr, liquid\n Infrared Spectrum"
colors_FTIRSamples = ['#f34f1c', '#5284bd', '#dba207','#80ba06']
percentCanola_FTIRSamples = [0.00, 0.5046/(0.5046+1.0088), 1.0308/(0.5125+1.0308), 1.00]
numberOfSamples = len(names_FTIRSamples)

# Read the CSV files for FTIR data and convert to dataframes
DF_FTIRColumns = ["Wavenumber", "Percent Transmittance"]
DF_FTIRSamples = []
for pathSample in path_FTIRSamples:
    DFSample = pd.read_csv(pathSample, usecols=DF_FTIRColumns)
    DF_FTIRSamples.append(DFSample)
numberOfPoints = DF_FTIRSamples[0].shape[0]

# Plot the FTIR Spectrum of each oil individually
spacing = 0.15
linewidth = 0.8
for fullName, color, percentCanola, DFSample in zip(fullNames_FTIRSamples, colors_FTIRSamples, percentCanola_FTIRSamples,
                                                    DF_FTIRSamples):
    figure, axis = plt.subplots(figsize=(10, 4.8))
    wavenumberCol = DFSample["Wavenumber"]
    transmittanceCol = DFSample["Percent Transmittance"]
    axis.plot(wavenumberCol, transmittanceCol, color=color, linewidth=linewidth)
    axis.set(xlabel="Wavenumber [cm⁻¹]", ylabel="Transmittance (%)")
    axis.set_title(fullName + nameAppend)

    # Set the limits for the y-axis
    ymax, ymin = max(transmittanceCol), min(transmittanceCol)
    yrange = ymax - ymin
    axis.set_ylim(ymin - spacing * yrange, ymax + spacing * yrange)

    # Set the limits for the x-axis; orient x-axis in reverse direction
    xmax, xmin = max(wavenumberCol), min(wavenumberCol)
    axis.set_xlim(xmax, xmin)

    # Properly position the x and y axes
    axis.xaxis.set_minor_locator(MultipleLocator(100))
    axis.yaxis.set_minor_locator(MultipleLocator(2))
    plt.show()

# Plot the FTIR spectra of all four oils, in order of increasing degree of unsaturation
figure, axis = plt.subplots(numberOfSamples, 1, figsize=(10, 8.0))
sampleIndex = 0
linewidth = 0.8
spacing = 0.15
for shortName, color, percentCanola, DFSample in zip(names_FTIRSamples, colors_FTIRSamples, percentCanola_FTIRSamples,
                                                    DF_FTIRSamples):
    wavenumberCol = DFSample["Wavenumber"]
    transmittanceCol = DFSample["Percent Transmittance"]
    axis[sampleIndex].plot(wavenumberCol, transmittanceCol,
                           color=color,
                           linewidth=linewidth)
    if sampleIndex == numberOfSamples-1:
        axis[sampleIndex].set(xlabel="Wavenumber [cm⁻¹]", ylabel= shortName + "\nTransmittance (%)")
    else:
        axis[sampleIndex].set(ylabel=shortName + "\nTransmittance (%)")
    # Set the limits for the y-axis
    ymax, ymin = max(transmittanceCol), min(transmittanceCol)
    yrange = ymax - ymin
    axis[sampleIndex].set_ylim(ymin - spacing * yrange, ymax + spacing * yrange)

    # Set the limits for the x-axis; orient x-axis in reverse direction
    xmax, xmin = max(wavenumberCol), min(wavenumberCol)
    axis[sampleIndex].set_xlim(xmax, xmin)

    # Position the x and y axes properly
    axis[sampleIndex].xaxis.set_minor_locator(MultipleLocator(100))
    axis[sampleIndex].yaxis.set_minor_locator(MultipleLocator(2))
    sampleIndex += 1
plt.subplots_adjust(bottom=0.15, right=0.90, hspace=0.45)
figure.suptitle("FTIR Spectra of Cooking Oils in KBr, Liquid")
plt.show()


# Get the relative heights of each peak in the FTIR spectrum of each sample which correspond to a significant vibration
# ... then correlate their relative heights to the mass% of canola oil.
# 3050 - 2900  (Alkene C-H stretch)
# 2880 - 2800  (Alkane C-H stretch)
# 1800 - 1700  (Carbonyl C=O stretch)
# 1500 - 1400  (Alkane C-H bend)
# 1250 - 1100  (Ester C-O stretch)
# 800 - 650 (C-H stretching / rocking)
scanRangeHigh = [800, 1250, 1500, 1800, 2880, 3050]
scanRangeLow = [650, 1100, 1400, 1700, 2800, 2900]
peakVibrations = ["C-H Rocking", "Ester C-O Stretch", "Alkane C-H Bend", "Carbonyl C=O Stretch", "Alkane C-H Stretch",
                  "Alkene C-H Stretch"]
numberOfPeaks = 6

initial_transmittance = []
peaks_wavenumbers = []
peaks_transmittance = []
peaks_heights = []
peaks_relativeHeights = []

for DFSample in DF_FTIRSamples:
    wavenumberCol = DFSample["Wavenumber"]
    transmittanceCol = DFSample["Percent Transmittance"]
    initialTrans = transmittanceCol[0]
    initial_transmittance.append(initialTrans)

    samplePeaks_wavenumbers = []
    samplePeaks_transmittance = []
    samplePeaks_heights = []
    for peakIndex in range(numberOfPeaks):
        # Narrow down the range where the peak will be found
        upperRange = scanRangeHigh[peakIndex]
        lowerRange = scanRangeLow[peakIndex]
        SelectedDFRange = DFSample.loc[DFSample["Wavenumber"] >= lowerRange]
        SelectedDFRange = SelectedDFRange.loc[SelectedDFRange["Wavenumber"] <= upperRange]

        # Compute peak-related quantities and add to the growing list
        peakTrans = SelectedDFRange.min()[1]
        peakIndex = SelectedDFRange.idxmin()[1]
        peakWavenumber = SelectedDFRange.loc[peakIndex]["Wavenumber"]
        peakHeight = initialTrans - peakTrans
        samplePeaks_wavenumbers.append(peakWavenumber)
        samplePeaks_transmittance.append(peakTrans)
        samplePeaks_heights.append(peakHeight)

    # Compute relative height of peaks (where the peak from 3050 to 2900 cm(-1) has a relative height of 1)
    baseHeight = samplePeaks_heights[-1]
    samplePeaks_relativeHeights = [height/baseHeight for height in samplePeaks_heights]

    # Append to the list of peaks for all samples
    peaks_wavenumbers.append(samplePeaks_wavenumbers)
    peaks_transmittance.append(samplePeaks_transmittance)
    peaks_heights.append(samplePeaks_heights)
    peaks_relativeHeights.append(samplePeaks_relativeHeights)

# Construct a dataframe summarizing the wavenumbers, transmittance, and relative heights of peaks per sample
# ... where each row represents a peak and the peak from 3050 to 2900 cm(-1) has a relative height of 1
DFPeakCorrelation_List = []
DFPeakCorrelation_Columns = ((["Peak Number", "Peak Range (cm⁻¹)", "Type of Vibration", "Average Peak Wavenumber (cm⁻¹)"]
                             + [f"Relative Height in {x} ({y:.1%} CO)" for x, y in zip(names_FTIRSamples,
                                                                                        percentCanola_FTIRSamples)])
                             + ["Pearson Coefficient", "p-value", "Significant? (p < 5%)", "Trend"])
for peakIndex in range(numberOfPeaks):
    peakNumber = peakIndex + 1
    peakRange = f'{scanRangeLow[peakIndex]}-{scanRangeHigh[peakIndex]}'
    typeVibration = peakVibrations[peakIndex]
    peakWavenumbers = []
    relativeHeights = []
    for sampleIndex in range(numberOfSamples):
        peakWavenumbers.append(peaks_wavenumbers[sampleIndex][peakIndex])
        relativeHeights.append(peaks_relativeHeights[sampleIndex][peakIndex])
    averageWavenumber = sum(peakWavenumbers)/numberOfSamples
    pearsonResults = pearsonr(percentCanola_FTIRSamples, relativeHeights)
    pearsonCoeff, pValue = pearsonResults
    boolSignificance = pValue < 0.05
    if not boolSignificance:
        signTrend = "Trend not significant"
    else:
        if pearsonCoeff > 0:
            signTrend = "Positive trend (+)"
        else:
            signTrend = "Negative trend (-)"
    DFRow = ([peakNumber, peakRange, typeVibration, averageWavenumber] + relativeHeights
             + [pearsonCoeff, pValue, boolSignificance, signTrend])
    DFPeakCorrelation_List.append(DFRow)

DFPeakCorrelation = pd.DataFrame(DFPeakCorrelation_List, columns=DFPeakCorrelation_Columns)
DFPeakCorrelation.to_csv("FTIR_AllPeakCorrelations.csv", index=False)


# Create a combined bar chart summarizing the relative heights of each peak where the peak from 3050 to 2900 cm(-1)
# ... has a relative height of 1
DFCombinedBar_List = []
DFCombinedBar_Columns = ["FTIR Peak#\n (Av. Wavenumber [cm⁻¹])"] + [f"{x} ({y:.1%} CO)" for x, y in zip(names_FTIRSamples,
                                                                                        percentCanola_FTIRSamples)]
peakNumberCol = DFPeakCorrelation["Peak Number"]
avWavenumberCol = DFPeakCorrelation["Average Peak Wavenumber (cm⁻¹)"]
barNames = []
for peakIndex in range(numberOfPeaks):
    barName = f"Peak #{peakNumberCol[peakIndex]}\n ({avWavenumberCol[peakIndex]:.0f})"
    barNames.append(barName)
DFCombinedBar_List.append(barNames)
for sampleIndex in range(numberOfSamples):
    relHeightsCol = DFPeakCorrelation.iloc[:, 4+sampleIndex]
    DFCombinedBar_List.append(list(relHeightsCol))

DFCombinedBar = pd.DataFrame(DFCombinedBar_List).transpose().set_axis(DFCombinedBar_Columns, axis=1)
DFCombinedBar.plot(x='FTIR Peak#\n (Av. Wavenumber [cm⁻¹])',
                   kind='bar',
                   stacked=False,
                   title='Variation of FTIR Relative Peak Heights with Oil Type',
                   figsize=(11.0, 8.0),
                   colormap=LinearSegmentedColormap.from_list("mycmap", colors_FTIRSamples),
                   position=1.0)
plt.ylabel("Relative Peak Height")
plt.ylim(top=1.5)
plt.legend(loc='upper left')
plt.subplots_adjust(bottom=0.33)
plt.grid()
plt.show()