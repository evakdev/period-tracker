def find_cycle(day, cycles):
    for cycle in cycles:
        if cycle.first_day <= day:
            return cycle



def cycle_calibrator(log):
    if log != "blood":
        return
    cycles = Cycle.objects.all().order_by("-first_day")
    blood_logs = Record.objects.filter(log="blood").order_by("log_date")
    first_after = blood_logs.filter(date__gt=log.day).first()
    last_before = blood_logs.filter(date_lte=log.day).last()
    
    def checking_befores(log):
        #checking befores
        if (log.date-last_before.date)<=5:
            my_cycle = find_cycle(last_before.date)
            cycle_calibrator(first_after)
        else:
            checking_afters(log)

    def checking_afters(log):
        #checking afters
        if (first_after.date-log.date)<=5:
            my_cycle = find_cycle(first_after.date)
            my_cycle.first_date = log.date
            cycle_calibrator(first_after)
        else: 
            Cycle.objects.create(first_date = log.date)


cycles = Cycle.objects.all().order_by("-first_day")
blood_logs = Record.objects.filter(log="blood").order_by("log_date").values_list('log_date',flat=True)
cycle_dates = []
cycle_dates.append(blood_logs[0])
for log in blood_logs[1:]:
    if log-cycle_dates[-1]>5:
        cycle_dates.append(log)
