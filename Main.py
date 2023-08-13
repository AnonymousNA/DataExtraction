import csv
import re
import logging
import sys

# Opens the raw copy/paste from the website
with open("/Users/willowleahy/PycharmProjects/DoctorFormat/PortlandGPsRaw.txt", "r") as File:
    RawData = File.read()    # Read the <File> (file object) into <RawData> (string object)


def data_format(data):  # Takes the raw format of the data and strips all necessary characters and outputs a list where each element is a single doctor's details.
    try:
        split_criteria = re.compile('([0-9]{3}-[0-9]{3}-[0-9]{4})')    # RegEx patten that matches a phone number embedded in a string. Below is the expression broken down.
        #                                                   (                          ): Capture characters that includes the matched string in the list (see re.split)
        #                                                    [0-9]     [0-9]     [0-9]    : Matches a character with the number value 0-9
        #                                                         {3}       {3}       {4} : Formats so that 3, 3, and 4 characters are needed for a match respectively
        #                                                            \-        \-         : Matches only a single dash
        sub_criteria = re.compile('Data\sSourced\sBy\sAnthem\sBlueCross[\n]BlueShield[\n]Printed\son\s[0-9]{2}/[0-9]{2}/[0-9]{4}\s[0-9]{2}:[0-9]{2}\s[a-zA-Z]{2}\s[a-zA-Z]{3}\s[|]\sPage\s\d+\sof\s\d+[\n]')
        # TODO: the RegEx substitution seems to be implemented but on inspection none of the footers was substituted. Revise <sbu_criteria> and ensure it is a good RegEx
        data = re.sub(sub_criteria, '', data)
        data = re.split(split_criteria, data)    # Splits <data> based on <split_criteria> into <data> (list object). Below is a sample of the format of <data>
        #                                          ['str between <split_criteria>', '<split_criteria>', 'str between <split_criteria>', '<split_criteria>']

        counter = 0    # Counts the element of <data>. So that counter(int obj)
        temp = str()   # Temporary buffer (str obj)
        data_formatted = list()    # Creates a list for appending the partially formatted data.
        for i in data:
            if i != data[counter]:    # Validates that the counter is in sync with the for loop
                raise ValueError("Loop counter broken")
            if len(i) > 12:    # Catches all elements of <data> that are longer than a typical phone number
                temp = i.strip().replace('\n', ' ').replace(',', '')    # Adds <i> to the buffer list and removes all the new lines, commas, and leading/trailing whitespaces
            elif len(i) == 12:  # Catches only strings with the length of 12 (the only ones that short should be phone numbers
                # TODO: Add validation logic that ensures the string caught was a phone number (will be a latter feature for more formats)
                temp = temp + ' ' + i    # Should append the phone number to the end of the string
                data_formatted.append(temp)
            else:
                pass
            counter += 1
        return data_formatted

    except ValueError:
        logging.error("Function: data_format \n Message: Loop counter broken")   # Logs an error message
        sys.exit(1)     # Exits with non-0 status to indicate the function has failed


# Parses the <data_format> to a comma separated value (.csv) format TODO: Combine with <data_format> and have a new function for taking nested lists into a .csv
def parse_csv(data, fields=None):
    # <data> should be a list were each element is details of a single doctor (the output of data_format)
    data_return = [['Name', 'In-Network', 'Gender', 'Specialty', 'Location', 'Telephone', '']]
    data_return_format = data_return[0]
    data_format_regex = [re.compile('In\-Network'), re.compile('Gender'), re.compile('Specialty'), re.compile('Location'), re.compile('Telephone'), '', '']
    counter = 0   # Keep tracks of the element of split_criteria that is being accessed
    subject = data[0]   # The specific doctor being parsed (will be integrated with a for loop)
    out = []
    while counter <= len(data_format_regex):
        temp = re.split(data_format_regex[counter], subject)
        out.append(temp[0].strip())
        # print('Before:', subject)
        subject = subject.replace(temp[0].strip(), '').strip()
        subject = subject.replace(data_return_format[counter + 1], '')
        print(out)
        # print('After:', subject)
        # if out[counter] == '':
        #     out.insert(1, 'In-Network')
        counter += 1

    # for i in range(len(data)):  # Iterates over a range that represents an elements of <data>. where each iteration <i> is the element position.
    #     out.append(data[i].split())    # Appends a list of <data[i]> split by spaces. Each nested list is the details of 1 doc. For easy assigning of fields (list obj with nested list obj)




    # for i in out:   # Iterates over the entire out list (should be the same amount of loops as for i in data)
    #     # <i> is a nested list of out
    #
    #     temp_str = str()    # Used to catch all parts of <i> before 'In-Network' (str obj)
    #     counter = 1    # Used to increment <data_return[0]> with the loop (int obj)
    #     for j in i:   # Loops over all nested lists of <out>
    #         if i.index(j) == data_fields[counter]:  # Finds the index of 'In-Network' and exits when <i> is that element
    #             counter += 1
    #             # data_return[i].append(temp_str)
    #             temp_str = str()
    #             print('___', data_return[0][counter], '___', sep='')
    #         elif i.index(j) != i.index('In-Network'):   # Appends <j> the temp_str for output to <data_return>
    #             temp_str += ' '+j
    #             temp_str = temp_str.strip()
    #             # print(temp_str)
    #             # print(data_return)
    #             # TODO: Replace 'In-Network' with the elements of data_return[1] so that this loop will iterate across
    #             #       the entirety of i.
    #             # TODO: <out_str> needs to be appended to the appropriate element of <data_return>. Remember the format
    #             #       of a .csv is: (new line at end of each list)
    #             #            xxx,yyy,zzz
    #             #            x1x1x1,y1y1y1,z1z1z1
    #             #            x2x2x2,y2y2y2,z2z2z2
    #             #            x3x3x3,y3y3y3,z3z3z3
    #         else:
    #             pass
    #             # Add error logging here

    return data_return


parse_csv(data_format(RawData))
