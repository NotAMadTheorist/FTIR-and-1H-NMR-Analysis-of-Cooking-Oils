import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from Source_FTIR_HNMR.cls_FTIR_Peak import *

class FTIR_Output:
    listFTIR_Outputs = []
    peakScanRange_High = [800, 1250, 1500, 1800, 2880, 3050]
    peakScanRange_Low = [650, 1100, 1400, 1700, 2800, 2900]
    peakVibrations = ["C-H Rocking", "Ester C-O Stretch", "Alkane C-H Bend", "Carbonyl C=O Stretch",
                      "Alkane C-H Stretch",
                      "Alkene C-H Stretch"]
    numberOfPeaks = len(peakVibrations)
    numberOfSamples = len(listFTIR_Outputs)

    def __init__(self, CSV_FTIRFile, sampleName_Full="", sampleName_Short="", sampleMedium="", plotColor="#5284bd",
                 fraction_CanolaOil=1.00):
        self.CSV_FTIRFile = CSV_FTIRFile
        self.sampleName_Full = sampleName_Full
        self.sampleName_Short = sampleName_Short
        self.sampleMedium = sampleMedium
        self.plotColor = plotColor
        self.fraction_CanolaOil = fraction_CanolaOil

        # Add new FTIR output to the list of all FTIR outputs
        FTIR_Output.listFTIR_Outputs.append(self)
        FTIR_Output.numberOfSamples = len(FTIR_Output.listFTIR_Outputs)

        # Read the CSV files for FTIR data and convert to dataframes
        DF_FTIRColumns = ["Wavenumber", "Percent Transmittance"]
        self.DFSample = pd.read_csv(CSV_FTIRFile, usecols=DF_FTIRColumns)
        self.numberOfPoints = self.DFSample.shape[0]
        self.listFTIRPeaks = []

    @classmethod
    def sortFTIRs(cls):
        cls.listFTIR_Outputs.sort(key = lambda FTIRObj: FTIRObj.fraction_CanolaOil)

    @classmethod
    def setPeakPosition_and_Vibration(cls, peakScanRange_High = (800, 1250, 1500, 1800, 2880, 3050),
                                      peakScanRange_Low=(650, 1100, 1400, 1700, 2800, 2900),
                                      peakVibrations=("C-H Rocking", "Ester C-O Stretch", "Alkane C-H Bend",
                                                      "Carbonyl C=O Stretch", "Alkane C-H Stretch",
                                                      "Alkene C-H Stretch")):
        cls.peakScanRange_High = peakScanRange_High
        cls.peakScanRange_Low = peakScanRange_Low
        cls.peakVibrations = peakVibrations
        cls.numberOfPeaks = len(peakVibrations)

    def plot(self, spacing = 0.15, linewidth = 0.8):
        figure, axis = plt.subplots(figsize=(10, 4.8))
        wavenumberCol = self.DFSample["Wavenumber"]
        transmittanceCol = self.DFSample["Percent Transmittance"]
        axis.plot(wavenumberCol, transmittanceCol, color=self.plotColor, linewidth=linewidth)
        axis.set(xlabel="Wavenumber [cm⁻¹]", ylabel="Transmittance (%)")
        axis.set_title(self.sampleName_Full + " in " + self.sampleMedium + "\n Infrared Spectrum")

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

    @classmethod
    def plotAll(cls, figureTitle = "FTIR Spectra of Cooking Oils in KBr, Liquid", linewidth = 0.8, spacing = 0.15):
        figure, axis = plt.subplots(FTIR_Output.numberOfSamples, 1, figsize=(10, 8.0))
        sampleIndex = 0
        for FTIRObj in cls.listFTIR_Outputs:
            wavenumberCol = FTIRObj.DFSample["Wavenumber"]
            transmittanceCol = FTIRObj.DFSample["Percent Transmittance"]
            axis[sampleIndex].plot(wavenumberCol, transmittanceCol,
                                   color=FTIRObj.plotColor,
                                   linewidth=linewidth)
            if sampleIndex == cls.numberOfSamples - 1:
                axis[sampleIndex].set(xlabel="Wavenumber [cm⁻¹]", ylabel=FTIRObj.sampleName_Short + "\nTransmittance (%)")
            else:
                axis[sampleIndex].set(ylabel=FTIRObj.sampleName_Short + "\nTransmittance (%)")
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
        figure.suptitle(figureTitle)
        plt.show()

    def generatePeaks(self): # Get the relative heights of each peak in the FTIR spectrum of each sample which correspond to a significant vibration.
        transmittanceCol = self.DFSample["Percent Transmittance"]
        initialTrans = transmittanceCol[0]
        peaks_wavenumbers = []
        peaks_transmittance = []
        peaks_heights = []

        for peakIndex in range(FTIR_Output.numberOfPeaks):
            # Narrow down the range where the peak will be found
            upperRange = FTIR_Output.peakScanRange_High[peakIndex]
            lowerRange = FTIR_Output.peakScanRange_Low[peakIndex]
            SelectedDFRange = self.DFSample.loc[self.DFSample["Wavenumber"] >= lowerRange]
            SelectedDFRange = SelectedDFRange.loc[SelectedDFRange["Wavenumber"] <= upperRange]

            # Compute peak-related quantities.
            peakTrans = SelectedDFRange.min().iloc[1]
            peakIndex = SelectedDFRange.idxmin().iloc[1]
            peakWavenumber = SelectedDFRange.loc[peakIndex]["Wavenumber"]
            peakHeight = initialTrans - peakTrans
            peaks_wavenumbers.append(peakWavenumber)
            peaks_transmittance.append(peakTrans)
            peaks_heights.append(peakHeight)

        # Compute relative height of peaks (where the peak from 3050 to 2900 cm(-1) has a relative height of 1)
        baseHeight = peaks_heights[-1]
        peaks_relativeHeights = [height / baseHeight for height in peaks_heights]

        # Generate FTIR peak objects
        for peakIndex in range(FTIR_Output.numberOfPeaks):
            self.listFTIRPeaks.append(FTIR_Peak(peaks_wavenumbers[peakIndex],
                                                peaks_transmittance[peakIndex],
                                                peaks_relativeHeights[peakIndex],
                                                FTIR_Output.peakVibrations[peakIndex]))

    @classmethod
    def generatePeaksAll(cls):
        for FTIRObj in cls.listFTIR_Outputs:
            FTIRObj.generatePeaks()