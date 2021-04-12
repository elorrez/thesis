#

# 1. doing the analysis
# run_gc_analysis

from analysis_run_gc import write_ouput_analysis

inpath = "C:/EVA/THESIS/data/full_dataset_absolute/"
outpath = "C:/EVA/THESIS/data/analyse_test_6/"

write_ouput_analysis(inpath,outpath)

# Analyse test 1 - 4: result doesn't make sense (linear analysis returns R² = 1
# Analyse test 5: results make  more sense, but R² < 0 --> possible?
# Analuse test 6: absolute anomalies
#2. Visualize results
# FILE: plot_gc_output.py