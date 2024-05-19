from django.db import models

class ProcessTaxonomy(models.Model):
    category_level1 = models.CharField(max_length=100)
    process_group_level2 = models.CharField(max_length=100)
    process_level3 = models.CharField(max_length=100)
    subprocess_level4 = models.CharField(max_length=100)
    activity_level5 = models.CharField(max_length=100)
    task_level6 = models.CharField(max_length=100)
    standard_local = models.CharField(max_length=100,choices=(('Standard', 'Standard'), ('Local', 'Local')) )
class CountryList(models.Model):
    country_description = models.CharField(max_length=100)
    cluster = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
class ProcessValue(models.Model):
    VALUE_CHOICES_STANDARD = [('Yes', 'Yes'),('No', 'No')]
    VALUE_CHOICES_LOCAL = [('A', 'A'),('B', 'B'),('C', 'C'),('N/A', 'N/A')]
    process_taxonomy = models.ForeignKey(ProcessTaxonomy, on_delete=models.CASCADE)
    country = models.ForeignKey(CountryList, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    def calculate_harmonization(self):
        total_rows = ProcessValue.objects.filter(process_taxonomy=self.process_taxonomy, country=self.country).exclude(
            value="N/A").count()
        count_different_values = ProcessValue.objects.filter(process_taxonomy=self.process_taxonomy,
                                                             country=self.country).exclude(
            value__in=["No", "N/A"]).count()


        # Calculate harmonization percentage
        #if total_rows > 0:
            #percentage = round((count_different_values / total_rows) * 100, 2)
        #    percentage = ProcessValue.objects.filter(process_taxonomy__standard_local='Standard', value='Yes').values('process_taxonomy__process_level3').distinct().count()

        #else:
        #    percentage = 0

        percentage = ProcessValue.objects.filter(value='Yes').values('process_taxonomy__task_level6').distinct().count()

        return percentage

    def process_comp(self):
        total_process_level3 = ProcessValue.objects.filter(process_taxonomy__standard_local='Standard').values('process_taxonomy__process_level3').distinct().count()
        count_process_level3_with_yes = ProcessValue.objects.filter(process_taxonomy__standard_local='Standard', value='Yes').values('process_taxonomy__process_level3').distinct().count()

        if total_process_level3 > 0:
            percentage = round((count_process_level3_with_yes / total_process_level3) * 100, 2)
        else:
            percentage = 0

        return percentage

    def save(self, *args, **kwargs):
        if self.process_taxonomy.standard_local == 'Standard':
            if self.value not in dict(self.VALUE_CHOICES_STANDARD).keys():
                raise ValueError("For Standard, value must be either 'Yes' or 'No'")
        elif self.process_taxonomy.standard_local == 'Local':
            if self.value not in dict(self.VALUE_CHOICES_LOCAL).keys():
                raise ValueError("For Local, value must be 'A', 'B', 'C', or 'N/A'")
        super(ProcessValue, self).save(*args, **kwargs)
