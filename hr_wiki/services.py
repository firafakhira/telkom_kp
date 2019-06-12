from django.db.models import Q
from .models import Log

#INI UNTUK NGERUBAH TIMESTAMP JADI DATETIME
from datetime import datetime
import pytz

def find_log(username, incident_id):
    return Log.objects.filter(Q(username = username) & Q(incident_id = incident_id))

def update_log_incident(column, table, username, incident_id):
    findLog = find_log(username, incident_id)
    if findLog: #KALO ADA LOG DENGAN USERNAME DAN INCIDENT ID TERSEBUT
        if column == 'like' or column == 'dislike':
            likeDisIsThere = findLog.filter(Q(like = True) | Q(dislike = True))
            hitsIsThere = []
        elif column == 'hits':
            hitsIsThere = findLog.filter(hits=True)
            likeDisIsThere = []

        if likeDisIsThere or hitsIsThere: #KALO ADA LIKE ATAU DISLIKE DI LOG
            pass
        else: #KALO GAADA
            saveLog = findLog.first()
            if column == 'like':
                saveLog.like = True
                table.like += 1
            elif column == 'dislike':
                saveLog.dislike = True
                table.dislike += 1
            elif column == 'hits':
                saveLog.hits = True
                table.hits += 1

            saveLog.save()
            table.save()
    else: #KALO GAADA LOG DENGAN USERNAME DAN INCIDENT ID TERSEBUT
        if column == 'like':
            logs = Log(username=username, like=True)
            table.like += 1
        elif column == 'dislike':
            logs = Log(username=username, dilike=True)
            table.dislike += 1
        elif column == 'hits':
            logs = Log(username=username, hits=True)
            table.hits += 1
            
        
        logs.incident_id = incident_id
        logs.save()

        table.save()

def count_stars(content):
    if (int(content.like) + int(content.dislike)) != 0:
        pLike = (int(content.like) // (int(content.like) + int(content.dislike))) * 5
    else:
        pLike = 0

    stars = []
    for i in range(pLike):
        stars.append('<span class="fa fa-star checked"></span>')
    if pLike != 5:
        for i in range(5-pLike):
            stars.append('<span class="fa fa-star"></span>')
    
    return stars

def get_highlight(string, max=20):
    hilite = string.split()
    return f"{' '.join(hilite[:max])}..."

def get_expired(timestamp):
    local_tz = pytz.timezone("Asia/Jakarta")
    utc_dt = datetime.utcfromtimestamp(timestamp).replace(tzinfo=pytz.utc)
    local_dt = local_tz.normalize(utc_dt.astimezone(local_tz))

    return (local_dt.replace(tzinfo=None) - datetime.now()).total_seconds()