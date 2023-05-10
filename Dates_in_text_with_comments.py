import re # as we will use the regex library we import it here on top

# here we define the main variables that we will need in our code
num_lines = 0 # number of lines in the input
textlines = [] # container to store the lines for processing
# month dictionary is to find the names of months faster
month_dict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}


# This function reads the lines of the file automatically
def get_inputs_from_file(dir):
    global num_lines
    global textlines

    line_number = 0

    file = open(dir, 'r')
    for line in file:
        if line_number == 0:
            num_lines = int(line)

        else:
            if line != "\n":
                temp_line = line.strip("\n")
                textlines.append(temp_line)

        line_number += 1
    file.close()


# This function reads the lines of the input
def get_input():
    global num_lines
    global textlines

    num_lines = int(input())
    for i in range(num_lines):
        line = input().strip("\n")
        if line != "\n": # if line is not the empty line at the end we append the line to the container
            textlines.append(line)



def read_lines():
    global textlines

    # pattern1 searches for DM dates - we get first accurate DM
    pattern1 = re.compile(r"((\s|^)(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.)")

    # pattern2  searches for Months
    pattern2 = re.compile(r"(January|February|March|April|May|June|July|August|September|October|November|December)")

    # pattern3 searches for days
    pattern3 = re.compile(r"(?:\s|^)(3[01]|[12][0-9]|0?[1-9])[.,]?(?!\S)")

    # we go through the textlines one by one
    for i in range(len(textlines)):
        # on each line we do the following:
        dm = pattern1.findall(textlines[i]) # we find the pattern of DD.MM. and save them to a list "dm"
        month = pattern2.findall(textlines[i]) # we find the pattern of DD.MM. and save them to a list "month"
        day = pattern3.findall(textlines[i]) # we find the day D or DD and save them to a list "day"


        if len(dm) == 1: # if there is only ONE DM date on the line, by the task we only need ONE on the line!
            date = dm[0][0].strip(" ") # we delete the possible space on both sides
            date = date.strip(".").split(".") # we delete the second dot -> DD.MM (split) and we separate by strip at middle dot
            # so now date has the format of ['DD', 'MM']

            # print("DATE ", date)
            # print(int(date[0], int(date[1])))

            # we need to check if the date is valid
            if is_valid_dm(date):  # if it is valid we move on with the month
                # now we check if there is a month on the same line
                if len(month) == 0:  # there is NO month on the line
                    # we transform our valid date in order to print it
                    month_name = month_dict[int(date[1])] # we take the month name in a month_dict we created
                    # we give the dictionary a month number and it saves month_name as string
                    # we print what we were asked to print: line number, month, day
                    print(str(i+1)+".", month_name, date[0].strip(" ,."))
                    # print("Line", i + 1, "valid DM date: ", dm[0][0])

            elif not is_valid_dm(date): # if date is not valid we see if there is a valid month and valid day
                # print("Not valid date", date)
                if len(month) == 1: # if there is exactly ONE month on line
                    # print("there is a possible date on line", i+1)
                    if len(day) != 0:  # if there is one or more valid days
                        if len(day) == 1: # if there is exactly ONE valid day on the line
                            print(str(i+1)+".", month[0], day[0].strip(" ,."))  # print the only month, the only day

                        elif len(day) != 1: # if there are MANY valid days we need to choose the closest one
                            left_days = []
                            right_days = []

                            # print("On line ", i, "month: ", month, "possible days: ", day)  # print the month, available days

                            # We need to get the day whose idx is closest to the month from right or left side!!!
                            month_idx = pattern2.finditer(textlines[i])  # we get the start and end idx for the month

                            for m in month_idx: # we iterate over those indexes and try to find the day
                                # print("Month idx:", m.span())
                                # print("Left coor", m.span()[0], ",  Right coor", m.span()[1])

                                day_idx = pattern3.finditer(textlines[i])  # getting the start, end idx for each day

                                for d in day_idx: # we iterate over the day indexes
                                    # print("days idxs: ", d.span())
                                    if d.span()[1] < m.span()[0]:  # we check if the day is to the left of month
                                        left_days.append(d.span())
                                    else:  # the day is to the right of month
                                        right_days.append(d.span())

                                # Now we know which of the days are to the left and which ones are to the right of the month
                                # print("left days", left_days, ", right days", right_days)

                                if len(left_days) != 0 and len(right_days) == 0: # if LEFT ONLY we take the last one in the list
                                    # print("The closest on left", left_days[-1])
                                    corr_day = textlines[i][left_days[-1][0]:left_days[-1][1]]
                                    print(str(i+1)+".", month[0], corr_day.strip(" ,."))

                                elif len(right_days) != 0 and len(left_days) == 0: # if RIGHT only we take the first one in the list
                                    # print("The closest on right", right_days[0])
                                    # print("The correct day is ", textlines[i][right_days[0][0]:right_days[0][1]])
                                    corr_day = textlines[i][right_days[0][0]:right_days[0][1]]
                                    print(str(i+1)+".", month[0], corr_day.strip(" ,."))

                                elif len(left_days) != 0 and len(right_days) != 0: # if both LEFT and RIGHT
                                    # if days are on both sides we need to check which one is the closest

                                    # print("The closest on left", left_days[-1])
                                    # print("The closest on right", right_days[0])

                                    # if the idx of rightmost month coordinate - idx of last day on the left
                                    # is smaller than the idx of first day on the right - idx of leftmost month coordinate
                                    if m.span()[0] - left_days[-1][1] < right_days[0][0] - (m.span()[1] - 1):
                                        # print("We take the left group", left_days[-1])
                                        corr_day = textlines[i][left_days[-1][0]:left_days[-1][1]]
                                        print(str(i+1)+".", month[0], corr_day.strip(" ,."))

                                    # if the idx of rightmost month coordinate - idx of last day on the left
                                    # is bigger than the idx of first day on the right - idx of leftmost month coordinate
                                    elif right_days[0][0] - (m.span()[1] - 1) < m.span()[0] - left_days[-1][1]:
                                        # print("We take the right group", right_days[-1])
                                        # print("The correct day is ", textlines[i][right_days[0][0]:right_days[0][1]])
                                        corr_day = textlines[i][right_days[0][0]:right_days[0][1]]
                                        print(str(i+1)+".", month[0], corr_day.strip(" ,."))

                                    else: # if the distance is same we take the left side one
                                        # print("Distance is same")
                                        # When distance if the same we take the one that appears first - the left one
                                        # print("The correct day is ", textlines[i][left_days[-1][0]:left_days[-1][1]])
                                        corr_day = textlines[i][left_days[-1][0]:left_days[-1][1]]
                                        print(str(i+1)+".", month[0], corr_day.strip(" ,."))


        # underneath the code is the same as starting from line 85 so same comments apply
        elif len(dm) == 0:   # if there is no DM date on the line
            if len(month) == 1: # if there is only ONE month on the line
                if len(day) != 0: # if there is one or more valid days
                    if len(day) == 1:
                        print(str(i+1)+".", month[0], day[0].strip(" ,.")) # print the only month, the only day

                        # !!! CHECK before adding to the dictionary
                        # if month and day are valid for 2021 year calendar

                    elif len(day) != 1:
                        left_days = []
                        right_days = []

                        # print("On line ", i, "month: ", month, "possible days: ", day)  # print the month, available days
                        # We need to get the day whose idx is closest to the month from right or left side!!!

                        month_idx = pattern2.finditer(textlines[i]) # getting the start, end idx for the month

                        for m in month_idx:
                            # print("Month idx:", m.span())
                            # print("Left coor", m.span()[0], ",  Right coor", m.span()[1])

                            day_idx = pattern3.finditer(textlines[i]) # getting the start, end idx for each day

                            for d in day_idx:
                                # print("days idxs: ", d.span())
                                if d.span()[1] < m.span()[0]:  #we check if the day is to the left of month
                                    left_days.append(d.span())
                                else:  #the day is to the right of month
                                    right_days.append(d.span())

                            # print("left days", left_days, ", right days", right_days)

                            if len(left_days) != 0 and len(right_days) == 0:
                                # print("The closest on left", left_days[-1])
                                corr_day = textlines[i][left_days[-1][0]:left_days[-1][1]]
                                print(str(i+1)+".", month[0], corr_day.strip(" ,."))

                            elif len(right_days) != 0 and len(left_days) == 0:
                                # print("The closest on right", right_days[0])
                                # print("The correct day is ", textlines[i][right_days[0][0]:right_days[0][1]])
                                corr_day = textlines[i][right_days[0][0]:right_days[0][1]]
                                print(str(i+1)+".", month[0], corr_day.strip(" ,."))

                            elif len(left_days) != 0 and len(right_days) != 0:
                                # print("The closest on left", left_days[-1])
                                # print("The closest on right", right_days[0])

                                if m.span()[0]-left_days[-1][1] < right_days[0][0]-(m.span()[1]-1):
                                    # print("We take the left group", left_days[-1])
                                    corr_day = textlines[i][left_days[-1][0]:left_days[-1][1]]
                                    print(str(i+1)+".", month[0], corr_day.strip(" ,."))

                                elif right_days[0][0]-(m.span()[1]-1) < m.span()[0]-left_days[-1][1]:
                                    # print("We take the right group", right_days[-1])
                                    # print("The correct day is ", textlines[i][right_days[0][0]:right_days[0][1]])
                                    corr_day = textlines[i][right_days[0][0]:right_days[0][1]]
                                    print(str(i+1)+".", month[0], corr_day.strip(" ,."))

                                else:
                                    # print("Distance is same")
                                    # When distance if the same we take the one that appears first - the left one
                                    # print("The correct day is ", textlines[i][left_days[-1][0]:left_days[-1][1]])
                                    corr_day = textlines[i][left_days[-1][0]:left_days[-1][1]]
                                    print(str(i+1)+".", month[0], corr_day.strip(" ,."))



def is_valid_dm(date):
    # this function checks if the date is valid
    # if the number of days in the month is correct
    # for example we discard such dates as 31.04 or 30.02 as they don´t exist in the calendar
    # this check can be done much better, such as in Optimal Expedition Pairs hw

    if int(date[1]) == 1 or int(date[1]) == 3 or int(date[1]) == 5 or int(date[1]) == 7 or int(date[1]) == 8 or int(date[1]) == 10 or int(date[1]) == 12:
        if int(date[0]) <= 31:
            return True

    elif int(date[1]) == 3 or int(date[1]) == 4 or int(date[1]) == 6 or int(date[1]) == 9 or int(date[1]) == 11:
        if int(date[0]) <= 30:
            return True

    elif int(date[1]) == 2:
        if int(date[0]) <= 28:
            return True



#+++++++++++++++++++++ M A I N +++++++++++++++++++++++++++++++++++++++++++


# print(month_dict)
get_inputs_from_file("./pubdata_datesintext/pub10.in")
# get_input()
read_lines()
