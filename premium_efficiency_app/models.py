from django.db import models
from django.utils import timezone
import datetime
from main_app.models import Client


class Premium_Efficiency_Client_Motor(models.Model):
    client = models.ForeignKey(Client)
    motor_name = models.CharField('Motor Name', max_length=160)
    annual_operating_hours = models.FloatField('Annual Operating Hours', default=0)
    energy_cost = models.FloatField('Energy Cost', default=0)
    motor_nameplate_hp = models.FloatField('Motor Nameplate Hp', default=0)
    existing_full_load_eff = models.FloatField('Existing Full Load Efficiency', default=0)
    existing_three_fourth_load_eff = models.FloatField('Existing 3/4 Load Efficiency', default=0)
    existing_half_load_eff = models.FloatField('Existing 1/2 Load Efficiency', default=0)
    existing_motor_purchase_price = models.FloatField('Existing Motor Purchase Price', default=0)
    proposed_full_load_eff = models.FloatField('Proposed Full Load Efficiency', default=0)
    proposed_three_fourth_load_eff = models.FloatField('Proposed 3/4 Load Efficiency', default=0)
    proposed_half_load_eff = models.FloatField('Proposed 1/2 Load Efficiency', default=0)
    proposed_motor_purchase_price = models.FloatField('Proposed Motor Purchase Price', default=0)
    motor_nameplate_rpm = models.FloatField('Motor Nameplate RPMs', default=0)
