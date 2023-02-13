from django.db import models

# Create your models here.


class Participant(models.Model):
    conditions_option = [(1, 1), (2, 2)]
    id = models.AutoField(auto_created=True, primary_key=True)
    condition = models.CharField(max_length=7, choices=conditions_option, default=1)
    order = models.CharField(max_length=7, choices=conditions_option, default=1)
    aid = models.CharField(max_length=50)
    start_time = models.TimeField(auto_now_add=True)
    end_time = models.TimeField(auto_now=True)
    total_time = models.FloatField(null=True)
    user_agent = models.CharField(max_length=1000)
    is_pc = models.BooleanField()
    is_mobile = models.BooleanField()
    is_tablet = models.BooleanField()
    is_bot = models.BooleanField()
    ip = models.CharField(max_length=10)
    finish = models.BooleanField()

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Participants"

    def __str__(self):
        return f'ID = {self.id}, Condition = {self.condition}, AID={self.aid}'


class Events(models.Model):
    classification_options = [('Blue', 'Blue'), ('Orange', 'Orange'), ('None', 'None')]

    id_block_trial = models.CharField(max_length=130, primary_key=True)
    user_id = models.CharField(max_length=4)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    block = models.CharField(max_length=1)
    trial = models.CharField(max_length=3)
    stimulus_h = models.FloatField(null=True)
    stimulus_s = models.FloatField(null=True)
    p_h = models.CharField(max_length=10)
    p_s = models.CharField(max_length=10)
    pd = models.BooleanField()
    time = models.TimeField(auto_now_add=True)
    score = models.CharField(max_length=10)

    event = models.CharField(max_length=7, choices=classification_options, default='None')
    output = models.CharField(max_length=7, choices=classification_options, default='None')
    classification = models.CharField(max_length=7, choices=classification_options, default='None')

    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return f'user: {self.user_id}, block: {self.block}, trial: {self.trial}, classification: {self.classification},' \
               f'pd: {self.pd}, time: {self.time}'


class Nasa(models.Model):

    unique_id = models.AutoField(auto_created=True, primary_key=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=4)
    system = models.BooleanField()
    mental_demand = models.CharField(max_length=4)
    physical_demand = models.CharField(max_length=4)
    performance = models.CharField(max_length=4)
    effort = models.CharField(max_length=4)
    frustration = models.CharField(max_length=4)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Nasa"

    def __str__(self):
        return f'id: {self.user_id}, system: {self.system},\
               mental: {self.mental_demand}, physical: {self.physical_demand}, \
               performance: {self.performance}, effort: {self.effort}, frustration: {self.frustration}'


class Trust(models.Model):

    unique_id = models.AutoField(auto_created=True, primary_key=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=4)
    trust_1 = models.CharField(max_length=4)
    trust_2 = models.CharField(max_length=4)

    class Meta:
        # Gives the proper plural name for admin
        verbose_name_plural = "Trust"

    def __str__(self):
        return 'user_id: {}'.format(self.id)
