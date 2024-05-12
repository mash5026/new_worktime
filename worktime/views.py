from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .models import WorkRecord, Holiday
from .utils import calculate_deduction_evening, calculate_deduction_morning, calculate_night_work, calculate_overtime_morning, calculate_night_work1, calculate_normal_working_hours, calculate_overtime_evening
from datetime import datetime
import jdatetime
from django. contrib import messages
from worktime.models import WorkRecordFinally as work
from django.db.models import F, Case, When, Value, IntegerField, Sum, DecimalField
import holidays

 # Adjust the import path according to your project structure

result_set = WorkRecord.objects.values('date', 'person').annotate(
    night_work=Sum('night_work'),
    overtime_morning=Sum('overtime_morning'),
    normal_working_hours=Sum('normal_working_hours'),
    overtime_evening=Sum('overtime_evening'),
    work_nights=Sum('work_nights'),
    work_deduction_evening=Sum('work_deduction_evening'),
    work_deduction_morning=Sum('work_deduction_morning')
).annotate(
    status=Case(
        When(normal_working_hours__lt=5, then=Value(1)),
        default=Value(0),
        output_field=IntegerField()
    )
).annotate(
    total_night=F('night_work') + F('work_nights'),
    over_time=F('overtime_morning') + F('overtime_evening'),
    work_deduction=F('work_deduction_evening') + F('work_deduction_morning'),
    absent_overtime=Case(
        When(status=1, then=F('normal_working_hours')+F('overtime_evening')),
        default=Value(0),
        output_field=DecimalField()
    )
).values('date', 'person', 'total_night', 'over_time', 'work_deduction', 'normal_working_hours', 'status', 'absent_overtime')

def create_work_record_finally(result_set):
    for item in result_set:
        record = work(
            person=item['person'],
            date=item['date'],
            normal_working_hours=item['normal_working_hours'],
            over_time=item['over_time'],
            work_night=item['total_night'],  # assuming total_night from previous steps
            work_deduction=item['work_deduction'],
            absent_overtime=item['absent_overtime'],
            status=str(item['status'])  # assuming status is a string field
        )
        record.save()

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        df = pd.read_excel(fs.path(filename))

        for index, row in df.iterrows():
            # Assuming 'date' is in Persian calendar and in 'YYYY/MM/DD' format
            persian_date_parts = str(row['date']).split('/')
            if len(persian_date_parts) == 3:
                persian_year, persian_month, persian_day = map(int, persian_date_parts)
                gregorian_date = jdatetime.date(persian_year, persian_month, persian_day).togregorian()
            else:
                # Handle error or set a default date
                continue  # Skip this row or set gregorian_date to a default value

            # Convert time strings to time objects
            try:
                arrived_time = datetime.strptime(str(row['arrivedtime']), '%H:%M:%S').time()
                departure_time = datetime.strptime(str(row['departuretime']), '%H:%M:%S').time()
            except ValueError as e:
                # Handle the error, log it, or set a default time
                continue  # Skip this row or set default times

            # Create and save the WorkRecord instance
            record = WorkRecord(
                person=row['person'],
                date=gregorian_date,
                arrived_time=arrived_time,
                departure_time=departure_time,
                night_work=calculate_night_work(arrived_time, departure_time),
                overtime_morning=calculate_overtime_morning(arrived_time, departure_time),
                normal_working_hours=calculate_normal_working_hours(arrived_time, departure_time, gregorian_date),
                overtime_evening=calculate_overtime_evening(arrived_time, departure_time, gregorian_date),
                work_nights=calculate_night_work1(arrived_time, departure_time),
                work_deduction_morning=calculate_deduction_morning(arrived_time, departure_time),
                work_deduction_evening=calculate_deduction_evening(arrived_time, departure_time, gregorian_date),
            )
            record.save()

        # Redirect or render a template to show success and provide the link to the uploaded file
        return render(request, 'result.html', {'uploaded_file_url': uploaded_file_url})

    # Render the upload form template if method is not POST or no file was provided
    return render(request, 'upload.html')

def insert_records(request):
    if request.method=='POST':
        create_work_record_finally(result_set)
        messages.success(request, 'Data inserted succefully.')
    return render(request, 'insert.html')

def show_holiday(request):
    holidays_iran = holidays.Iran(years=[2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]).items()
    for date, event in holidays_iran:
        holiday = Holiday(date_holiday=date, event=event)
        holiday.save()
        #print(date.year, '/' ,date.month,  '/' ,date.day,  '>>>>>' ,event)
    return render(request, 'holiday.html', {'holidays_iran':holidays_iran})


# def upload_file(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         df = pd.read_excel(fs.path(filename))

#         # Perform calculations and store the results in the database
#         for index, row in df.iterrows():
#             # Perform your calculations here
#             # For example:
#             record = WorkRecord(
#                 arrived_time = datetime.strptime(str(row['arrivedtime']), '%H:%M:%S').time(),
#                 departure_time = datetime.strptime(str(row['departuretime']), '%H:%M:%S').time(),
#                 person=row['person'],
#                 date = row['date'],
#                 night_work = calculate_night_work(row['arrivedtime'], row['departuretime']),
#                 overtime_morning = calculate_overtime_morning(row['arrivedtime'], row['departuretime']),
#                 work_nights = calculate_night_work1(row['arrivedtime'], row['departuretime']),
#                 normal_working_hours = calculate_normal_working_hours(row['arrivedtime'], row['departuretime']),
#                 overtime_evening = calculate_overtime_evening(row['arrivedtime'], row['departuretime']),
#                 work_deduction_morning = calculate_deduction_morning(row['arrivedtime'], row['departuretime']),
#                 work_deduction_evening = calculate_deduction_evening(row['arrivedtime'], row['departuretime'])
#             )
#             record.save()

#         return render(request, 'result.html', {})
#     return render(request, 'upload.html', {})


# def upload_file(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         df = pd.read_excel(fs.path(filename))

#         # Perform calculations and store the results in the database
#         for person, group in df.groupby(['person', 'date']):
#             arrived_times = group['arrivedtime'].apply(lambda x: datetime.strptime(str(x), '%H:%M:%S').time()).tolist()
#             departure_times = group['departuretime'].apply(lambda x: datetime.strptime(str(x), '%H:%M:%S').time()).tolist()
#             night_work_hours = calculate_night_work(arrived_times, departure_times)
#             overtime_morning = calculate_overtime_morning(arrived_times, departure_times)
#             work_nights = calculate_night_work1(arrived_times, departure_times)
#             normal_working_hours = calculate_normal_working_hours(arrived_times, departure_times)
#             overtime_evening = calculate_overtime_evening(arrived_times, departure_times)
#             work_deduction_morning = calculate_deduction_morning(arrived_times, departure_times)
#             work_deduction_evening = calculate_deduction_evening(arrived_times, departure_times)
#             # Calculate other metrics similarly based on your functions
#             print('arrived_times>>>>>>>', arrived_times)

#             # Save the results to the database
#             record = WorkRecord(
#                 arrived_time = datetime.strptime(str(arrived_times[0]), '%H:%M:%S').time(),
#                 departure_time = datetime.strptime(str(departure_times[0]), '%H:%M:%S').time(),
#                 person=person[0],
#                 date=group['date'].iloc[0],
#                 night_work=night_work_hours,
#                 overtime_morning = overtime_morning,
#                 work_nights = work_nights,
#                 normal_working_hours = normal_working_hours,
#                 overtime_evening = overtime_evening,
#                 work_deduction_morning = work_deduction_morning,
#                 work_deduction_evening = work_deduction_evening
#                 # Other fields...
#             )
#             record.save()

#         return render(request, 'result.html', {})
#     return render(request, 'upload.html', {})


# def upload_file(request):
#     if request.method == 'POST' and request.FILES['myfile']:
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         df = pd.read_excel(fs.path(filename))

#         for index, row in df.iterrows():
#             # Ensure that the values are in the expected format before parsing into datetime
#             arrived_time = datetime.strptime(row['arrivedtime'], '%H:%M:%S').time()
#             departure_time = datetime.strptime(row['departuretime'], '%H:%M:%S').time()
#             # Call the calculation function with the parsed datetime values
#             #perform_work_time_calculation(arrived_time, departure_time, row['Person'])

#         return render(request, 'result.html', {})
#     return render(request, 'upload.html', {})
