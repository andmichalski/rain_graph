from func import RainfallFunc

# Executing
file1 = 'Miedzybrodzie_2016_10_26_no00.dbf'
file2 = 'Miedzybrodzie_2017_05_24_no00.dbf'

nlist = RainfallFunc.merge_dbf(file1, file2)
daily_sum = RainfallFunc.rainfall_sum(nlist)
RainfallFunc.write_file(daily_sum)