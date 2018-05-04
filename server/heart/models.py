from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=20)
    ip = models.CharField(max_length=12)
    note = models.CharField(max_length=20, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Command(models.Model):
    name = models.CharField(max_length=20, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    command = models.CharField(max_length=20, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Rule(models.Model):
    #  device = models
    status = models.CharField(max_length=100, null=True)
    rpn = models.ForeignKey(Command, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=100, null=True)
    enable = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)

    def _str__(self):
        return self.description


class Status(models.Model):
    rank = models.IntegerField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    command = models.ForeignKey(Command, on_delete=models.CASCADE, null=True)
    flag = models.CharField(default="STAND BY", max_length=50)
    description = models.CharField(max_length=300, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description

class Default(models.Model):
    name = models.CharField(max_length=20, default="物件")
    device = models.ForeignKey(Device, on_delete=models.CASCADE) 
    coommand = models.ForeignKey(Command, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
