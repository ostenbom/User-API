from __future__ import unicode_literals

from django.db import models


class Constituency(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "constituencies"


class Station(models.Model):
    # Station Location
    name = models.CharField(max_length=100)
    addr_line_1 = models.CharField(max_length=100)
    addr_line_2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=8)

    # Station Constituency
    constituency = models.ForeignKey(
        Constituency,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Voter(models.Model):
    # Voter Name
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)

    # Voter Location
    addr_line_1 = models.CharField(max_length=100)
    addr_line_2 = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=8)

    # Voter Details
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=14)

    # Which station voter registered to
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE
    )

    # If the users vote has been used
    used_vote = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Party(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    # Candidate Name
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)

    constituency = models.ForeignKey(
        Constituency,
        #TODO worry about delete
        on_delete=models.CASCADE
    )

    party = models.ForeignKey(
        Party,
        #TODO worry about delete
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.first_name + ' ' + self.last_name
