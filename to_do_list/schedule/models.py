from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from multiselectfield import MultiSelectField

MY_PRIORITIES = (
('lenient', 'lenient'),
('intermediate', 'intermediate'),
('urgent', 'urgent')
)

MY_DAYS = (
 ('Monday', 'Monday'),
 ('Tuesday', 'Tuesday'),
 ('Wednesday', 'Wednesday'),
 ('Thursday', 'Thursday'),
 ('Friday', 'Friday'),
 ('Saturday', 'Saturday'),
 ('Sunday', 'Sunday')
)

MY_HOURS = (
 (1, '1'),
 (2, '2'),
 (3, '3'),
 (4, '4'),
 (5, '5'),
 (6, '6'),
 (7, '7'),
 (8, '8'),
 (9, '9'),
 (10, '10'),
 (11, '11'),
 (0, '12'),
 
)

MY_MIN = (
 (0, '00'),
 (10, '10'),
 (15, '15'),
 (20, '20'),
 (25, '25'),
 (30, '30'),
 (35, '35'),
 (40, '40'),
 (45, '45'),
 (50, '50'),
 (55, '55'),
)

MY_MODES = (
 ('a.m.', 'a.m.'),
 ('p.m.', 'p.m.')
)

MY_TYPES = (
 ('static', 'static'),
 ('fluid', 'fluid')
)

class Task(models.Model):
 task_type = models.CharField(max_length=20, choices=MY_TYPES, default='static')
 title = models.CharField(max_length=100)
 content = models.TextField()
 priority_level = models.CharField(max_length=20, choices= MY_PRIORITIES, default='intermediate')
 day_of_week = models.CharField(max_length=20, choices= MY_DAYS, default='Monday')
 date_posted = models.DateTimeField(default=timezone.now)
 author = models.ForeignKey(User, on_delete=models.CASCADE)
 start_time_hour = models.IntegerField(choices=MY_HOURS, default=1)
 end_time_hour = models.IntegerField(choices=MY_HOURS, default=1)
 start_time_min = models.IntegerField(choices=MY_MIN, default=10)
 end_time_min = models.IntegerField(choices=MY_MIN, default=10)
 start_time_mode = models.CharField(max_length=10, choices=MY_MODES, default='a.m.')
 end_time_mode = models.CharField(max_length=10, choices=MY_MODES, default='a.m.')

  #----Fluid Task Attributes----
 duration_of_task = models.IntegerField(choices=MY_HOURS, default=1)
 divided_into_parts = models.FloatField(default=0.0)
 between = models.IntegerField(choices=MY_HOURS, default=1)
 and_end_time = models.IntegerField(choices=MY_HOURS,default=1)
 start_mode = models.CharField(max_length=10, choices=MY_MODES, default='a.m.')
 end_mode = models.CharField(max_length=10, choices=MY_MODES, default='a.m.')




 def __str__(self):
  return self.title
  
 
 def get_absolute_url(self):
  return reverse('schedule-detail', kwargs={'pk' : self.pk})

