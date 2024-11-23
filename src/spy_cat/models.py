from django.db import models
from config import VALID_BREEDS

from django.core.exceptions import ValidationError

class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
    

class Mission(models.Model):
    cat = models.OneToOneField(
        SpyCat, 
        null=True, blank=True, 
        on_delete=models.SET_NULL,
        related_name="current_mission"
    )
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.targets.exists() and all(target.is_completed for target in self.targets.all()):
            self.is_completed = True
        else:
            raise ValidationError("All targets must be completed before marking the mission as completed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Mission ({'Completed' if self.is_completed else 'In Progress'})"


class Target(models.Model):
    mission = models.ForeignKey(
        Mission, 
        on_delete=models.CASCADE, 
        related_name="targets"
    )
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk and self.is_completed:
            original = Target.objects.get(pk=self.pk)
            if original.notes != self.notes:
                raise ValidationError("Cannot update notes for a completed target.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Target {self.name} ({'Completed' if self.is_completed else 'In Progress'})"