# Dictionaries used to convert CAT values to slider values

reverse_eq1_frequency_cat_values = {'00': '00', '01': '100', '02': '200', '03': '300',
                            '04': '400', '05': '500', '06': '600', '07': '700'}

reverse_eq_level_cat_values = {'-20': '-20', '-19': '-19', '-18': '-18', '-17': '-17', '-16': '-16', '-15': '-15',
                       '-14': '-14', '-13': '-13', '-12': '-12', '-11': '-11', '-10': '-10', '-09': '-9',
                       '-08': '-8', '-07': '-7', '-06': '-6', '-05': '-5', '-04': '-4', '-03': '-3',
                       '-02': '-2', '-01': '-1', '+00': '0', '+01': '1', '+02': '2', '+03': '3', '+04': '4',
                       '+05': '5', '+06': '6', '+07': '7', '+08': '8', '+09': '9', '+10': '10'}

reverse_eq2_frequency_cat_values = {'00': '00', '01': '700', '02': '800', '03': '900', '04': '1000',
                            '05': '11', '06': '1200', '07': '1300', '08': '1400', '09': '1500'}

reverse_eq3_frequency_cat_values = {'00': '00', '01': '1500', '02': '1600', '03': '1700', '04': '1800',
                            '05': '1900', '06': '2000', '07': '2100', '08': '2200', '09': '2300',
                            '10': '2400', '11': '2500', '12': '2600', '13': '2700', '14': '2800',
                            '15': '2900', '16': '3000', '17': '3100', '18': '3200'}

# setup the dictionaries for the values that we will need to pass to the CAT control.  We only need a dictionary
# for the frequency and level because they are not contiguous values.  The bandwidth runs continuous from 01 to 10
# so we can just use the slider value straight from the output.

# because of the differences in the frequencies we need a dictionary for each EQ.  The level is the same across each EQ
# so we only need one dictionary


eq1_frequency_cat_values = {'00': '00', '100': '01', '200': '02', '300': '03',
                     '400': '04', '500': '05', '600': '06', '700': '07'}

eq2_frequency_cat_values = {'00': '00', '700': '01', '800': '02', '900': '03', '1000': '04',
                     '1100': '05', '1200': '06', '1300': '07', '1400': '08', '1500': '09'}

eq3_frequency_cat_values = {'00': '00', '1500': '01', '1600': '02', '1700': '03', '1800': '04',
                     '1900': '05', '2000': '06', '2100': '07', '2200': '08', '2300': '09',
                     '2400': '10', '2500': '11', '2600': '12', '2700': '13', '2800': '14',
                     '2900': '15', '3000': '16', '3100': '17', '3200': '18'}

# For the level values, I can probably replace the dictionary below with an if statement.
# The only reason I am using the dictionary
# is because the 00 has to be either -00 or +00 and I can't get that from the slider.  Look in to something like
# if value is 00 make it +00 else use the slider value.  I'm tired right now and don't want to try it

eq_level_cat_values = {'-20': '-20', '-19': '-19', '-18': '-18', '-17': '-17', '-16': '-16', '-15': '-15',
                '-14': '-14', '-13': '-13', '-12': '-12', '-11': '-11', '-10': '-10', '-9': '-09',
                '-8': '-08', '-7': '-07', '-6': '-06', '-5': '-05', '-4': '-04', '-3': '-03',
                '-2': '-02', '-1': '-01', '00': '+00', '01': '+01', '02': '+02', '03': '+03', '04': '+04',
                '05': '+05', '06': '+06', '07': '+07', '08': '+08', '09': '+09', '10': '+10'}