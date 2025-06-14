import pandas as pd
from scipy.stats.mstats import pearsonr
from Source_FTIR_HNMR.cls_FTIR_Output import FTIR_Output
from Source_FTIR_HNMR.rootDir import path_OutFTIR_CorrelOOP

class FTIR_CorrelationAnalysis:
    def __init__(self, listFTIR_Outputs = [], lambdaKey = lambda FTIRObj: FTIRObj.fraction_CanolaOil):
        self.listFTIR_Outputs = listFTIR_Outputs.copy()
        self.listFTIR_Outputs.sort(key = lambdaKey)
        self.numberOfSamples = len(self.listFTIR_Outputs)
        self.numberOfPeaks = FTIR_Output.numberOfPeaks
        self.lambdaKey = lambdaKey
        self.peakScanRange_High = FTIR_Output.peakScanRange_High
        self.peakScanRange_Low = FTIR_Output.peakScanRange_Low
        self.peakVibrations = FTIR_Output.peakVibrations

    def generateCorrelations(self):
        # Construct a dataframe summarizing the wavenumbers, transmittance, and relative heights of peaks per sample
        # ... where each row represents a peak and the peak from 3050 to 2900 cm(-1) has a relative height of 1
        DFPeakCorrelation_List = []
        names_FTIRSamples = [FTIRObj.sampleName_Short for FTIRObj in self.listFTIR_Outputs]
        percentCanola_FTIRSamples = [FTIRObj.fraction_CanolaOil for FTIRObj in self.listFTIR_Outputs]
        DFPeakCorrelation_Columns = (
                    (["Peak Number", "Peak Range (cm⁻¹)", "Type of Vibration", "Average Peak Wavenumber (cm⁻¹)"]
                     + [f"Relative Height in {x} ({y:.1%} CO)" for x, y in zip(names_FTIRSamples,
                                                                               percentCanola_FTIRSamples)])
                    + ["Pearson Coefficient", "p-value", "Significant? (p < 5%)", "Trend"])
        for peakIndex in range(self.numberOfPeaks):
            peakNumber = peakIndex + 1
            peakRange = f'{self.peakScanRange_Low[peakIndex]}-{self.peakScanRange_High[peakIndex]}'
            typeVibration = self.peakVibrations[peakIndex]
            peakWavenumbers = []
            relativeHeights = []
            for sampleIndex in range(self.numberOfSamples):
                peakWavenumbers.append(self.listFTIR_Outputs[sampleIndex].listFTIRPeaks[peakIndex].wavenumber)
                relativeHeights.append(self.listFTIR_Outputs[sampleIndex].listFTIRPeaks[peakIndex].relativeHeight)
            averageWavenumber = sum(peakWavenumbers) / self.numberOfSamples
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
        self.DFPeakCorrelation = DFPeakCorrelation

    def saveCorrelations(self, FTIR_OutputDir, CSVFileName=path_OutFTIR_CorrelOOP):
        self.DFPeakCorrelation.to_csv(FTIR_OutputDir / CSVFileName, index=False)
