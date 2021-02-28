import boto3
import time
import csv



def get_day():
    localtime = time.localtime(time.time())

    day = localtime[6]

    # 0 is Monday, ... , 6 is Sunday
    return int(day)+4


def get_time():
    localtime = time.localtime(time.time())
    return localtime[3], localtime[4]


ec2 = boto3.resource('ec2')
#instance = ec2.Instance('i-0077a14907f60c54f')



with open('ec2.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')

    for row in csv_reader:

        time.sleep(15)
        
        day_to_work = False  
        should_be_online = False
        actual_online = False

        instance = ec2.Instance(row[0])
        workduration = int(row[1])
        start_hour = int(row[2])
        start_minute = int(row[3])

        if (int(row[get_day()]) == 1):
            day_to_work = True

        if (day_to_work): 

            actual_hour, actual_minute = get_time()
            # check for time to be actual_online
            if (start_hour < actual_hour or (actual_hour == start_hour and actual_minute > start_minute)):
                # Working start was there
                end_hour = start_hour + workduration
                if (end_hour > actual_hour or (actual_hour == end_hour and actual_minute < start_minute)):
                    # Time to work
                    should_be_online = True
                else:
                    # Enjoy your Freetime
                    should_be_online = False
            else:
                # To early to work now
                    should_be_online = False



        if (day_to_work):
            # Instance Code 16 -> running 80 -> stopped andere sind irgendwo da zwischen
            temp_status = int(instance.state['Code'])

            if (temp_status == 16):
                actual_online = True

            else:
                actual_online = False

        # Check for start or stop of the instances

        # print (actual_online)
        # print (should_be_online)

        if (actual_online != should_be_online):
            # action required

            if (should_be_online):
                # Start of the Instance
                instance.start()
            else:
                # Stop of the instance
                instance.stop()

