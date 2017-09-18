#!/usr/bin/env python

import sys
import os
import boto
import datetime
from collections import Counter
from datetime import datetime, timedelta

#D = 3
#date_D_days_ago = datetime.now() - timedelta(days=D)

from boto.ec2 import connect_to_region
ec2_connection = connect_to_region("@region", profile_name="default")
images = ec2_connection.get_all_images(Owners="@OwnerNumber")
print('Get {} Amis'.format(len(images)))

'''
Some Steps to search images per name and values
identifies = ec2_connection.describe_instances( Filters=[{'Name': 'tag-key', 'Values': ['ami-2', 'ami-1']}]).get('Reservations',[])
'''

ami_creation_time = Counter()

for image in images:
	print image.name
	create_time_dt_object = datetime.strptime(image.creationDate, '%Y-%m-%dT%H:%M:%S.%fz')
	epoch_seconds = int(time.mktime(create_time_dt_object.timetuple()))
	ami_creation_time[image.id] = epoch_seconds


mlist = []
for i in sorted(ami_creation_time.items(), key=lambda pair: pair[1]):
	mlist.append(str(i))
print mlist

z = ''.join(mlist)
for k in z:
	k.deregister(dry_run=True, delete_snapshot=False)


#date = datetime.strptime(image.creation_date, "%Y-%m-%dT%H:%M:%S.%fz")
#dateD = date_D_days_ago.strptime('%Y-%m-%dT%H:%M:%S.%fz')
#if date < dateD:

		
