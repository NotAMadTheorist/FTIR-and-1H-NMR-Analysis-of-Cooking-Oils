from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent.parent
path_FTIRCanolaOil = ROOT_DIR / "Instrument Output Files" / "FTIR Instrument Outputs" / "FTIR_CanolaOil.csv"
path_FTIRPalmOil = ROOT_DIR / "Instrument Output Files" / "FTIR Instrument Outputs" / "FTIR_PalmOil.csv"
path_FTIR2C1PMix = ROOT_DIR / "Instrument Output Files" / "FTIR Instrument Outputs" / "FTIR_2Canola_1Palm_Mixture.csv"
path_FTIR1C2PMix = ROOT_DIR / "Instrument Output Files" / "FTIR Instrument Outputs" / "FTIR_1Canola_2Palm_Mixture.csv"
path_ProgOutput_FTIR = ROOT_DIR / "Program Output Files" / "FTIR Program Outputs"
path_OutFTIR_CorrelProc = path_ProgOutput_FTIR / "FTIR_AllPeakCorrelations (procedural).csv"
path_OutFTIR_CorrelOOP = path_ProgOutput_FTIR / "FTIR_AllPeakCorrelations (OOP).csv"

path_RawText_NMRCanolaOil = ROOT_DIR / "Instrument Output Files" / "1H-NMR Instrument Outputs" / "RawText_1H-NMR_CanolaOil.txt"
path_RawText_NMRPalmOil = ROOT_DIR / "Instrument Output Files" / "1H-NMR Instrument Outputs" / "RawText_1H-NMR_PalmOil.txt"
path_RawText_NMR2C1PMix = ROOT_DIR / "Instrument Output Files" / "1H-NMR Instrument Outputs" / "RawText_1H-NMR_2Canola_1Palm_Mixture.txt"
path_NMRCanolaOil = ROOT_DIR / "Instrument Output Files" / "1H-NMR Instrument Outputs" / "1H-NMR_CanolaOil.csv"
path_NMRPalmOil = ROOT_DIR / "Instrument Output Files" / "1H-NMR Instrument Outputs" / "1H-NMR_PalmOil.csv"
path_NMR2C1PMix = ROOT_DIR / "Instrument Output Files" / "1H-NMR Instrument Outputs" / "1H-NMR_2Canola_1Palm_Mixture.csv"
path_ProgOutput_HNMR = ROOT_DIR / "Program Output Files" / "1H-NMR Program Outputs"
path_OutNMR_CorrelAllProc = path_ProgOutput_HNMR / "1H-NMR_AllPeakCorrelations (procedural).csv"
path_OutNMR_CorrelSigProc = path_ProgOutput_HNMR / "1H-NMR_SigPeakCorrelations (procedural).csv"


