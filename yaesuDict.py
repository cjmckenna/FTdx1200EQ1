# Dictionaries used to convert CAT values to slider values

reverse_eq1_frequency_cat_values = {'00': '00', '01': '1', '02': '2', '03': '3',
                            '04': '4', '05': '5', '06': '6', '07': '7'}

reverse_eq_level_cat_values = {'-20': '-20', '-19': '-19', '-18': '-18', '-17': '-17', '-16': '-16', '-15': '-15',
                       '-14': '-14', '-13': '-13', '-12': '-12', '-11': '-11', '-10': '-10', '-09': '-9',
                       '-08': '-8', '-07': '-7', '-06': '-6', '-05': '-5', '-04': '-4', '-03': '-3',
                       '-02': '-2', '-01': '-1', '+00': '0', '+01': '1', '+02': '2', '+03': '3', '+04': '4',
                       '+05': '5', '+06': '6', '+07': '7', '+08': '8', '+09': '9', '+10': '10'}

reverse_eq2_frequency_cat_values = {00: 00, 1: 7, 2: 8, 3: 9, 4: 10,
                            5: 11, 6: 12, 7: 13, 8: 14, 9: 15}

reverse_eq3_frequency_cat_values = {00: 00, 1: 15, 2: 16, 3: 17, 4: 18,
                            5: 19, 6: 20, 7: 21, 8: 22, 9: 23,
                            10: 24, 11: 25, 12: 26, 13: 27, 14: 28,
                            15: 29, 16: 30, 17: 31, 18: 32}

# setup the dictionaries for the values that we will need to pass to the CAT control.  We only need a dictionary
# for the frequency and level because they are not contiguous values.  The bandwidth runs continuous from 01 to 10
# so we can just use the slider value straight from the output.

# because of the differences in the frequencies we need a dictionary for each EQ.  The level is the same across each EQ
# so we only need one dictionary


eq1_frequency_cat_values = {'00': '00', 1: '01', 2: '02', 3: '03',
                     4: '04', 5: '05', 6: '06', 7: '07'}

eq2_frequency_cat_values = {'00': '00', 7: '01', 8: '02', 9: '03', 10: '04',
                     11: '05', 12: '06', 13: '07', 14: '08', 15: '09'}

eq3_frequency_cat_values = {'00': '00', 15: '01', 16: '02', 17: '03', 18: '04',
                     19: '05', 20: '06', 21: '07', 22: '08', 23: '09',
                     24: '10', 25: '11', 26: '12', 27: '13', 28: '14',
                     29: '15', 30: '16', 31: '17', 32: '18'}

# For the level values, I can probably replace the dictionary below with an if statement.
# The only reason I am using the dictionary
# is because the 00 has to be either -00 or +00 and I can't get that from the slider.  Look in to something like
# if value is 00 make it +00 else use the slider value.  I'm tired right now and don't want to try it

eq_level_cat_values = {'-20': '-20', '-19': '-19', '-18': '-18', '-17': '-17', '-16': '-16', '-15': '-15',
                '-14': '-14', '-13': '-13', '-12': '-12', '-11': '-11', '-10': '-10', '-9': '-09',
                '-8': '-08', '-7': '-07', '-6': '-06', '-5': '-05', '-4': '-04', '-3': '-03',
                '-2': '-02', '-1': '-01', '0': '+00', '1': '+01', '2': '+02', '3': '+03', '4': '+04',
                '5': '+05', '6': '+06', '7': '+07', '8': '+08', '9': '+09', '10': '+10'}