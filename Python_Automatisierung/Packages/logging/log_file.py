import time

pathForLog = r"C:\\log.csv"

def get_time():
    localtime = time.localtime(time.time())

    timestamp = time.asctime(localtime)

    return timestamp

def log_event(text):

    logfile = open(pathForLog, 'a')
    timestamp = get_time()

    logfile.write(timestamp + ';' + text + '\n')

    logfile.close()


