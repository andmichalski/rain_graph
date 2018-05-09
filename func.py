import unittest
from dbfread import DBF
import datetime
from collections import OrderedDict


class RainfallFunc:

    # Function to calculate daliy rainfall from list of precipitation in every hour
    @staticmethod
    def rainfall_sum(rainfall_hour):
        rainfall_day = 0
        current_record = rainfall_hour[0]
        out_list = []
        for record in rainfall_hour:
            if record['DATE'] == current_record['DATE']:
                rainfall_day = round(rainfall_day + record['Suma opadu'], 1)
            else:
                out_list.append(OrderedDict([(u'DATE', current_record['DATE']), (u'Rainfall sum', rainfall_day)]))
                current_record = record
                rainfall_day = record['Suma opadu']
        out_list.append(OrderedDict([(u'DATE', record['DATE']), (u'Rainfall sum', rainfall_day)]))
        return out_list


    class RainfallTests(unittest.TestCase):
        def setUp(self):
            self.sample_list = [OrderedDict([(u'DATE', datetime.date(2016, 4, 12)), (u'TIME', u'21:00:00'), (u'Suma opadu', 0.1)]),
                            OrderedDict([(u'DATE', datetime.date(2016, 4, 12)), (u'TIME', u'22:00:00'), (u'Suma opadu', 0.2)]),
                            OrderedDict([(u'DATE', datetime.date(2016, 4, 12)), (u'TIME', u'23:00:00'), (u'Suma opadu', 0.3)]),
                            OrderedDict([(u'DATE', datetime.date(2016, 4, 13)), (u'TIME', u'00:00:00'), (u'Suma opadu', 0.4)]),
                            OrderedDict([(u'DATE', datetime.date(2016, 4, 13)), (u'TIME', u'01:00:00'), (u'Suma opadu', 0.5)])]

            self.out_list = [OrderedDict([(u'DATE', datetime.date(2016, 4, 12)), (u'Rainfall sum', 0.6)]),
                            OrderedDict([(u'DATE', datetime.date(2016, 4, 13)), (u'Rainfall sum', 0.9)])]

        def test_first_normal_case(self):
            self.assertEqual(rainfall_sum(self.sample_list), self.out_list)

        def test_end_case_and_new_day(self):
            sample_list_2 = self.sample_list[:-1]
            out_list_2 = [OrderedDict([(u'DATE', datetime.date(2016, 4, 12)), (u'Rainfall sum', 0.6)]),
                            OrderedDict([(u'DATE', datetime.date(2016, 4, 13)), (u'Rainfall sum', 0.4)])]
            self.assertEqual(rainfall_sum(sample_list_2), out_list_2)

        def test_end_of_day(self):
            sample_list_3 = self.sample_list[:-2]
            out_list_3 = [OrderedDict([(u'DATE', datetime.date(2016, 4, 12)), (u'Rainfall sum', 0.6)])]
            self.assertEqual(rainfall_sum(sample_list_3), out_list_3)


    # Function loading DBF files and merge it if possible
    @staticmethod
    def merge_dbf(file1, file2):

        table1 = DBF(file1)
        records1 = list(table1)

        table2 = DBF(file2)
        records2 = list(table2)

        # Delete unnecessary fields from lists
        for records in [records1, records2]:

            for record in records:
                del record['INTERRUPT']
                if record['Suma opadu'] < 0:
                    record['Suma opadu'] = 0.0

        # Check is it possible to  connect lists
        # Find variable last record, change add one hour
        # Make variable next record
        # Measurements are made every hour
        last_record = records1[-1]
        next_hour = unicode(int(last_record['TIME'][:2]) + 1)
        new_day = last_record['DATE']
        if len(next_hour) == 1:
            next_hour = '0' + next_hour

        # Check is it new day
        elif next_hour == '24':
            next_hour = unicode('00')
            new_day = last_record['DATE'] + datetime.timedelta(days=1)
        else:
            pass

        # Specify search date and search day
        search_date = new_day
        search_time = next_hour + last_record['TIME'][2:]

        # Search date and time to connect values
        for index, record in enumerate(records2):
            if (record['DATE'] == search_date and record['TIME'] == search_time):
                print("Possible to connect")
                # TODO Check this case
                records2 = records2[index:]
                merged_list = records1 + records2
                break

        return merged_list

    class MergeDBFTests(unittest.TestCase):

        def setUp(self):
            self.file1 = 'Miedzybrodzie_2016_10_26_no00.dbf'
            self.file2 = 'Miedzybrodzie_2017_05_24_no00.dbf'

        def test_merged_normal_list(self):
            list_out = merge_dbf(self.file1, self.file2)
            print list_out


    # Function which writes list to f.txt file
    @staticmethod
    def write_file(nlist):
        # Creating list to save as txt
        out_list_txt = ["date, rainfall_sum"]
        for record in nlist:
            out_list_txt.append(str(record['DATE']) + ", " + str(record['Rainfall sum']))

        # Saving output as txt file
        # Open a file
        f = open("f.txt", "w+")

        # Write sequence of lines at the end of the file.
        f.write('\n'.join(out_list_txt))

        # Close opened file
        f.close()
