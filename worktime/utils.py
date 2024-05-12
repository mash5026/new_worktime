from datetime import datetime, timedelta, time, date
import datetime as  dt
from datetime import  time as ti

ABSENT = 'A'
PRESENT = 'P'
LIST_ANSWER = [(ABSENT, 'غایب'), (PRESENT, 'حاضر')]

def calculate_time_overlap(start_time, end_time, period_start, period_end):
    """
    Calculate overlap between two time periods.
    """
    start_dt = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)
    period_start_dt = datetime.combine(datetime.today(), period_start)
    period_end_dt = datetime.combine(datetime.today(), period_end)

    # If the times are in the next day
    if end_time < start_time:
        end_dt += timedelta(days=1)
    if period_end < period_start:
        period_end_dt += timedelta(days=1)

    latest_start = max(start_dt, period_start_dt)
    earliest_end = min(end_dt, period_end_dt)
    delta = (earliest_end - latest_start).total_seconds()
    if delta > 0:
        return max(delta / 3600, 0)
    else:
        return 0

def calculate_night_work(arrived_time, departure_time):
    """
    Calculate work done from 0:00 to 6:00 as night work.
    """
    return calculate_time_overlap(arrived_time, departure_time, time(0, 0), time(6, 0))

def calculate_night_work1(arrived_time, departure_time):
    """
    Calculate work done from 22:00 to 24:00 as evening night work.
    """
    return calculate_time_overlap(arrived_time, departure_time, time(22, 0), time(23, 59, 59))

def calculate_overtime_morning(arrived_time, departure_time):
    """
    Calculate morning overtime work done from 6:00 to 8:00.
    """
    return calculate_time_overlap(arrived_time, departure_time, time(0, 0), time(0, 0))

def calculate_normal_working_hours(arrived_time, departure_time, gregorian_date):
    """
    Calculate normal working hours done from 8:00 to 17:00.
    """
    if gregorian_date.weekday() == 2: # Check if today is Wednesday
        deduction_time = time(16, 0)  # end time at 16:00 on Wednesday
    else:
        deduction_time = time(17, 0)  # end time at 17:00 on rest of the days

    return calculate_time_overlap(arrived_time, departure_time, time(8, 0), deduction_time)

def calculate_overtime_evening(arrived_time, departure_time, gregorian_date):
    """
    Calculate evening overtime work done from 17:00 to 22:00.
    """
    if gregorian_date.weekday() == 2: # Check if today is Wednesday
        deduction_time = time(16, 0)  # Deduction time at 16:00 on Wednesday
    else:
        deduction_time = time(17, 0)  # Deduction time at 17:00 on rest of the days
        
    return calculate_time_overlap(arrived_time, departure_time, deduction_time, time(22, 0))

def calculate_deduction_morning(arrived_time, departure_time):
    """
    Calculate deduction for late arrival between 8:00 to 8:30 if working less than 9 hours.
    """
    total_hours = (datetime.combine(datetime.today(), departure_time) - datetime.combine(datetime.today(), arrived_time)).total_seconds() / 3600
    if (time(8, 0) <= arrived_time <= time(8, 30) and total_hours < 9) or (time(8, 30) <= arrived_time <= time(12, 0)):
        return (datetime.combine(datetime.today(), arrived_time) - datetime.combine(datetime.today(), time(8, 0))).total_seconds() / 3600
    else:
        return 0

def calculate_deduction_evening(arrived_time, departure_time, gregorian_date):
    """
    Calculate deduction for leaving before 17:00.
    """
    
    if gregorian_date.weekday() == 2: # Check if today is Wednesday
        deduction_time = time(16, 0)  # Deduction time at 16:00 on Wednesday
    else:
        deduction_time = time(17, 0)  # Deduction time at 17:00 on rest of the days

    if departure_time < deduction_time:
        return (datetime.combine(datetime.today(), deduction_time) - datetime.combine(datetime.today(), departure_time)).total_seconds() / 3600
    else:
        return 0
    



# def calculate_night_work(arrived_time, departure_time):
#     # Convert string representations of time to Python time objects

#     dummy_date = datetime(2000, 1, 1)
#     arrived_time_obj = datetime.combine(dummy_date, arrived_time)
#     departure_time_obj = datetime.combine(dummy_date, departure_time)

#     start_of_night = datetime.combine(dummy_date, time(0, 0, 0))
#     end_of_night = datetime.combine(dummy_date, time(6, 0, 0))

#     # Calculate night work duration
#     if end_of_night > arrived_time_obj and departure_time_obj > start_of_night:
#         if departure_time_obj < end_of_night:
#             night_work_duration = departure_time_obj - arrived_time_obj
#         else:
#             night_work_duration = end_of_night - arrived_time_obj
#     else:
#         night_work_duration = timedelta(seconds=0)  # No night work

#     # Convert duration to hours (decimal)
#     night_work_hours = night_work_duration.total_seconds() / 3600

#     return night_work_hours

# # def calculate_night_work(arrived_times, departure_times):
# #     night_work_hours = 0
# #     for i in range(len(arrived_times)):
# #         dummy_date = datetime(2000, 1, 1)
# #         arrived_time_obj = datetime.combine(dummy_date, arrived_times[i])
# #         departure_time_obj = datetime.combine(dummy_date, departure_times[i])

# #         start_of_night = datetime.combine(dummy_date, time(0, 0, 0))
# #         end_of_night = datetime.combine(dummy_date, time(6, 0, 0))

# #         if end_of_night > arrived_time_obj and departure_time_obj > start_of_night:
# #             if departure_time_obj < end_of_night:
# #                 night_work_duration = departure_time_obj - arrived_time_obj
# #             else:
# #                 night_work_duration = end_of_night - arrived_time_obj
# #         else:
# #             night_work_duration = timedelta(seconds=0)  # No night work

# #         night_work_hours += night_work_duration.total_seconds() / 3600
# #     return night_work_hours
    
# def calculate_night_work1(arrived_time, departure_time):
#     # Convert string representations of time to Python time objects

#     dummy_date = datetime(2000, 1, 1)
#     arrived_time_obj = datetime.combine(dummy_date, arrived_time)
#     departure_time_obj = datetime.combine(dummy_date, departure_time)

#     start_of_night = datetime.combine(dummy_date, time(22, 0, 0))
#     end_of_night = datetime.combine(dummy_date, time(23, 59, 59))

#     # Calculate night work duration
#     if end_of_night > arrived_time_obj and departure_time_obj > start_of_night:
#         if departure_time_obj < end_of_night:
#             night_work_duration = departure_time_obj - start_of_night
#         else:
#             night_work_duration = end_of_night - start_of_night
#     else:
#         night_work_duration = timedelta(seconds=0)  # No night work

#     # Convert duration to hours (decimal)
#     night_work_hours = night_work_duration.total_seconds() / 3600

#     return night_work_hours

# # def calculate_night_work1(arrived_times, departure_times):
# #     night_work_hours = 0
# #     for i in range(len(arrived_times)):
# #         dummy_date = datetime(2000, 1, 1)
# #         arrived_time_obj = datetime.combine(dummy_date, arrived_times[i])
# #         departure_time_obj = datetime.combine(dummy_date, departure_times[i])

# #         start_of_night = datetime.combine(dummy_date, time(22, 0, 0))
# #         end_of_night = datetime.combine(dummy_date, time(23, 59, 59))

# #         if end_of_night > arrived_time_obj and departure_time_obj > start_of_night:
# #             if departure_time_obj < end_of_night:
# #                 night_work_duration = departure_time_obj - start_of_night
# #             else:
# #                 night_work_duration = end_of_night - start_of_night
# #         else:
# #             night_work_duration = timedelta(seconds=0)  # No night work

# #         night_work_hours += night_work_duration.total_seconds() / 3600
    
# #     return night_work_hours

# def calculate_overtime_morning(arrived_time, departure_time):
#     # Convert string representations of time to datetime objects (with a dummy date)
#     dummy_date = datetime(2000, 1, 1)
#     arrived_datetime = datetime.combine(dummy_date, arrived_time)
#     departure_datetime = datetime.combine(dummy_date, departure_time)

#     # Define the threshold times (6:00:00 AM and 8:00:00 AM)
#     start_of_morning = datetime.combine(dummy_date, time(6, 0, 0))
#     end_of_morning = datetime.combine(dummy_date, time(8, 0, 0))

#     # Calculate overtime in the morning
#     if  arrived_datetime < end_of_morning and departure_datetime > start_of_morning:
#         if departure_datetime < end_of_morning:
#             overtime_morning_duration = end_of_morning - departure_datetime
#         elif arrived_datetime < start_of_morning:
#             overtime_morning_duration = end_of_morning - start_of_morning
#         else:
#             overtime_morning_duration = end_of_morning - arrived_datetime
#     else:
#         overtime_morning_duration = timedelta(seconds=0)  # No overtime in the morning

#     # Convert duration to hours (decimal)
#     overtime_morning_hours = overtime_morning_duration.total_seconds() / 3600

#     return overtime_morning_hours

# # def calculate_overtime_morning(arrived_times, departure_times):
# #     overtime_morning_hours = 0
# #     for i in range(len(arrived_times)):
# #         dummy_date = datetime(2000, 1, 1)
# #         arrived_datetime = datetime.combine(dummy_date, arrived_times[i])
# #         departure_datetime = datetime.combine(dummy_date, departure_times[i])

# #         start_of_morning = datetime.combine(dummy_date, time(6, 0, 0))
# #         end_of_morning = datetime.combine(dummy_date, time(8, 0, 0))

# #         if arrived_datetime < end_of_morning and departure_datetime > start_of_morning:
# #             if departure_datetime < end_of_morning:
# #                 overtime_morning_duration = end_of_morning - departure_datetime
# #             elif arrived_datetime < start_of_morning:
# #                 overtime_morning_duration = end_of_morning - start_of_morning
# #             else:
# #                 overtime_morning_duration = end_of_morning - arrived_datetime
# #         else:
# #             overtime_morning_duration = timedelta(seconds=0)  # No overtime in the morning

# #         overtime_morning_hours += overtime_morning_duration.total_seconds() / 3600

# #     return overtime_morning_hours

# def calculate_normal_working_hours(arrived_time, departure_time):
#     # Similar to the previous function, convert to datetime objects
#     dummy_date = datetime(2000, 1, 1)
#     arrived_datetime = datetime.combine(dummy_date, arrived_time)
#     departure_datetime = datetime.combine(dummy_date, departure_time)

#     # Define the threshold times (8:00:00 AM and 5:00:00 PM)
#     start_of_workday = datetime.combine(dummy_date, time(8, 0, 0))
#     start_of_workday1 = datetime.combine(dummy_date, time(17, 0, 0))
#     end_of_workday = datetime.combine(dummy_date, time(17, 0, 0))
#     end_of_workday1 = datetime.combine(dummy_date, time(8, 30, 0))
#     end_of_mr = datetime.combine(dummy_date, time(11, 59, 59))
    

#     # Calculate normal working hours
#     if start_of_workday1 > arrived_datetime and arrived_datetime < end_of_mr and departure_datetime > start_of_workday:
#         if departure_datetime < end_of_workday: 
#             normal_working_hours_duration = departure_datetime - start_of_workday
#         else:
#             normal_working_hours_duration = end_of_workday - start_of_workday
#     else:
#         normal_working_hours_duration = timedelta(seconds=0)  # No normal working hours

#     # Convert duration to hours (decimal)
#     normal_working_hours = normal_working_hours_duration.total_seconds() / 3600

#     return normal_working_hours

# # def calculate_normal_working_hours(arrived_times, departure_times):
# #     normal_working_hours_total = 0
# #     for i in range(len(arrived_times)):
# #         dummy_date = datetime(2000, 1, 1)
# #         arrived_datetime = datetime.combine(dummy_date, arrived_times[i])
# #         departure_datetime = datetime.combine(dummy_date, departure_times[i])

# #         start_of_workday = datetime.combine(dummy_date, time(8, 0, 0))
# #         start_of_workday1 = datetime.combine(dummy_date, time(17, 0, 0))
# #         end_of_workday = datetime.combine(dummy_date, time(17, 0, 0))
# #         end_of_workday1 = datetime.combine(dummy_date, time(8, 30, 0))
# #         end_of_mr = datetime.combine(dummy_date, time(11, 59, 59))

# #         if start_of_workday1 > arrived_datetime and arrived_datetime < end_of_mr and departure_datetime > start_of_workday:
# #             if departure_datetime < end_of_workday: 
# #                 normal_working_hours_duration = departure_datetime - start_of_workday
# #             else:
# #                 normal_working_hours_duration = end_of_workday - start_of_workday
# #         else:
# #             normal_working_hours_duration = timedelta(seconds=0)  # No normal working hours

# #         normal_working_hours_total += normal_working_hours_duration.total_seconds() / 3600

# #     return normal_working_hours_total

# def calculate_overtime_evening(arrived_time, departure_time):
#     # Convert string representations of time to datetime objects (with a dummy date)
#     dummy_date = datetime(2000, 1, 1)
#     arrived_datetime = datetime.combine(dummy_date, arrived_time)
#     departure_datetime = datetime.combine(dummy_date, departure_time)

#     # Define the threshold times (6:00:00 AM and 8:00:00 AM)
#     start_of_evening = datetime.combine(dummy_date, time(17, 0, 0))
#     end_of_evening = datetime.combine(dummy_date, time(22, 0, 0))

#     start_of_mr = datetime.combine(dummy_date, time(8, 30, 0))
#     end_of_mr = datetime.combine(dummy_date, time(11, 59, 59))

#     # Calculate overtime in the morning
#     if end_of_evening > arrived_datetime and departure_datetime > start_of_evening and start_of_mr<arrived_datetime<end_of_mr:
#         if departure_datetime < end_of_evening:
#             overtime_evening_duration = departure_datetime - start_of_evening
#         else:
#             overtime_evening_duration = end_of_evening - start_of_evening
    
#     elif end_of_evening > arrived_datetime and departure_datetime > start_of_evening:
#         if departure_datetime < end_of_evening:
#             if arrived_datetime > end_of_mr:
#                 overtime_evening_duration = departure_datetime - arrived_datetime
#             else:
#                 overtime_evening_duration = departure_datetime - start_of_evening
#         else:
#             overtime_evening_duration = end_of_evening - arrived_datetime

#     else:
#         overtime_evening_duration = timedelta(seconds=0)  # No overtime in the morning

#     # Convert duration to hours (decimal)
#     overtime_evening_hours = overtime_evening_duration.total_seconds() / 3600

#     return overtime_evening_hours

# # def calculate_overtime_evening(arrived_times, departure_times):
# #     overtime_evening_hours = 0
# #     for i in range(len(arrived_times)):
# #         dummy_date = datetime(2000, 1, 1)
# #         arrived_datetime = datetime.combine(dummy_date, arrived_times[i])
# #         departure_datetime = datetime.combine(dummy_date, departure_times[i])

# #         start_of_evening = datetime.combine(dummy_date, time(17, 0, 0))
# #         end_of_evening = datetime.combine(dummy_date, time(22, 0, 0))
# #         start_of_mr = datetime.combine(dummy_date, time(8, 30, 0))
# #         end_of_mr = datetime.combine(dummy_date, time(11, 59, 59))

# #         if end_of_evening > arrived_datetime and departure_datetime > start_of_evening and start_of_mr < arrived_datetime < end_of_mr:
# #             if departure_datetime < end_of_evening:
# #                 overtime_evening_duration = departure_datetime - start_of_evening
# #             else:
# #                 overtime_evening_duration = end_of_evening - start_of_evening
# #         elif end_of_evening > arrived_datetime and departure_datetime > start_of_evening:
# #             if departure_datetime < end_of_evening:
# #                 if arrived_datetime > end_of_mr:
# #                     overtime_evening_duration = departure_datetime - arrived_datetime
# #                 else:
# #                     overtime_evening_duration = departure_datetime - start_of_evening
# #             else:
# #                 overtime_evening_duration = end_of_evening - arrived_datetime
# #         else:
# #             overtime_evening_duration = timedelta(seconds=0)  # No overtime in the evening

# #         overtime_evening_hours += overtime_evening_duration.total_seconds() / 3600
    
# #     return overtime_evening_hours

# def calculate_deduction_morning(arrived_time, departure_time):
#     # Convert string representations of time to datetime objects (with a dummy date)
#     dummy_date = datetime(2000, 1, 1)
#     arrived_datetime = datetime.combine(dummy_date, arrived_time)
#     departure_datetime = datetime.combine(dummy_date, departure_time)

#     # Define the threshold times (6:00:00 AM and 8:00:00 AM)
#     start_of_mr = datetime.combine(dummy_date, time(8, 30, 0))
#     start_of_mr1 = datetime.combine(dummy_date, time(8, 0, 0))
#     end_of_mr = datetime.combine(dummy_date, time(11, 59, 59))

#     # start_of_ev = datetime.combine(dummy_date, time(17, 0, 0))
#     # end_of_ev = datetime.combine(dummy_date, time(17, 30, 0))

#     # Calculate overtime in the morning
#     if start_of_mr < arrived_datetime < end_of_mr:
#         deduction_morning = arrived_datetime - start_of_mr1
#     elif start_of_mr1 < arrived_datetime < start_of_mr and (departure_datetime - arrived_datetime) < timedelta(hours=9) :
#         deduction_morning = start_of_mr - arrived_datetime
#     elif arrived_datetime > end_of_mr:
#         deduction_morning = timedelta(seconds=32400)
#     # elif departure_datetime < start_of_ev:
#     #     deduction_morning = start_of_ev - departure_datetime
#     else:
#         deduction_morning = timedelta(seconds=0)

#     # Convert duration to hours (decimal)
#     deduction_morning_hours = deduction_morning.total_seconds() / 3600

#     return deduction_morning_hours

# # def calculate_deduction_morning(arrived_times, departure_times):
# #     deduction_hours_total = 0
# #     for i in range(len(arrived_times)):
# #         dummy_date = datetime(2000, 1, 1)
# #         arrived_datetime = datetime.combine(dummy_date, arrived_times[i])
# #         departure_datetime = datetime.combine(dummy_date, departure_times[i])

# #         start_of_mr = datetime.combine(dummy_date, time(8, 30, 0))
# #         start_of_mr1 = datetime.combine(dummy_date, time(8, 0, 0))
# #         end_of_mr = datetime.combine(dummy_date, time(11, 59, 59))

# #         if start_of_mr < arrived_datetime < end_of_mr:
# #             deduction_morning = arrived_datetime - start_of_mr1
# #         elif start_of_mr1 < arrived_datetime < start_of_mr and (departure_datetime - arrived_datetime) < timedelta(hours=9):
# #             deduction_morning = start_of_mr - arrived_datetime
# #         elif arrived_datetime > end_of_mr:
# #             deduction_morning = timedelta(seconds=32400)
# #         else:
# #             deduction_morning = timedelta(seconds=0)

# #         deduction_hours_total += deduction_morning.total_seconds() / 3600

# #     return deduction_hours_total

# def calculate_deduction_evening(arrived_time, departure_time):
#     # Convert string representations of time to datetime objects (with a dummy date)
    
#     dummy_date = datetime(2000, 1, 1)
#     arrived_datetime = datetime.combine(dummy_date, arrived_time)
#     departure_datetime = datetime.combine(dummy_date, departure_time)

#     # Define the threshold times (6:00:00 AM and 8:00:00 AM)
#     start_of_mr = datetime.combine(dummy_date, time(8, 30, 0))
#     start_of_mr1 = datetime.combine(dummy_date, time(8, 0, 0))
#     end_of_mr = datetime.combine(dummy_date, time(11, 59, 59))

#     start_of_ev = datetime.combine(dummy_date, time(17, 0, 0))
#     end_of_ev = datetime.combine(dummy_date, time(17, 30, 0))

#     # Calculate overtime in the morning
#     if departure_datetime < start_of_ev:
#         deduction_evening = start_of_ev - departure_datetime

#     else:
#         deduction_evening = timedelta(seconds=0)

#     # Convert duration to hours (decimal)
#     deduction_evening_hours = deduction_evening.total_seconds() / 3600

#     return deduction_evening_hours

# # def calculate_deduction_evening(arrived_times, departure_times):
# #     # Convert string representations of time to datetime objects (with a dummy date)
# #     deduction_hours_total = 0
# #     for i in range(len(arrived_times)):
# #         dummy_date = datetime(2000, 1, 1)
# #         arrived_datetime = datetime.combine(dummy_date, arrived_times[i])
# #         departure_datetime = datetime.combine(dummy_date, departure_times[i])

# #         # Define the threshold times (6:00:00 AM and 8:00:00 AM)
# #         start_of_mr = datetime.combine(dummy_date, time(8, 30, 0))
# #         start_of_mr1 = datetime.combine(dummy_date, time(8, 0, 0))
# #         end_of_mr = datetime.combine(dummy_date, time(11, 59, 59))

# #         start_of_ev = datetime.combine(dummy_date, time(17, 0, 0))
# #         end_of_ev = datetime.combine(dummy_date, time(17, 30, 0))

# #         # Calculate overtime in the morning
# #         if departure_datetime < start_of_ev:
# #             deduction_evening = start_of_ev - departure_datetime

# #         else:
# #             deduction_evening = timedelta(seconds=0)

# #         # Convert duration to hours (decimal)
# #         deduction_hours_total += deduction_evening.total_seconds() / 3600

# #     return deduction_hours_total
    

# Call the function to insert the records
