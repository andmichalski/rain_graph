from func import RainfallFunc
from graph import Draw

# Executing
list_dbfs = RainfallFunc.find_dbf_files()
nlist = RainfallFunc.merge_all_dbf(list_dbfs)
daily_sum = RainfallFunc.rainfall_sum(nlist)

# Write list file (additional function)
# RainfallFunc.write_file(daily_sum)

Draw.plot_rainfall(daily_sum)