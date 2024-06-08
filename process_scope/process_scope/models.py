from django.db import models

class ProcessTaxonomy(models.Model):
    category_level1 = models.CharField(max_length=100)
    process_group_level2 = models.CharField(max_length=100)
    process_level3 = models.CharField(max_length=100)
    subprocess_level4 = models.CharField(max_length=100)
    activity_level5 = models.CharField(max_length=100)
    task_level6 = models.CharField(max_length=100)
    standard_local = models.CharField(max_length=100, choices=(('Standard', 'Standard'), ('Local', 'Local')))

class CountryList(models.Model):
    country_description = models.CharField(max_length=100)
    cluster = models.CharField(max_length=100)
    region = models.CharField(max_length=100)


class ProcessValue(models.Model):
    VALUE_CHOICES_STANDARD = [('Yes', 'Yes'), ('No', 'No')]
    VALUE_CHOICES_LOCAL = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('N/A', 'N/A')]
    process_taxonomy = models.ForeignKey(ProcessTaxonomy, on_delete=models.CASCADE)
    country = models.ForeignKey(CountryList, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    @classmethod
    def calculate_harmonization(cls, region=None, cluster=None, country=None):
        base_queryset = cls.objects.all()

        if region:
            base_queryset = base_queryset.filter(country__region=region)
        if cluster:
            base_queryset = base_queryset.filter(country__cluster=cluster)
        if country:
            base_queryset = base_queryset.filter(country__country_description=country)

        total_rows = base_queryset.exclude(value="N/A").values('process_taxonomy__task_level6').distinct().count()

        if total_rows > 0:
            yes_count = base_queryset.filter(value='Yes').values('process_taxonomy__task_level6').distinct().count()
            percentage = round((yes_count / total_rows) * 100, 2)
        else:
            percentage = 0

        return percentage

    @classmethod
    def calculate_harmonization_for_countries(cls, countries):
        base_queryset = cls.objects.filter(country__in=countries).exclude(value="N/A")

        total_rows = base_queryset.values('process_taxonomy__task_level6').distinct().count()

        if total_rows > 0:
            yes_count = base_queryset.filter(value='Yes').values('process_taxonomy__task_level6').distinct().count()
            percentage = round((yes_count / total_rows) * 100, 2)
        else:
            percentage = 0

        return percentage
    def process_comp(self, region=None, cluster=None):
        base_queryset = ProcessValue.objects.filter(process_taxonomy__standard_local='Standard')
        if region:
            base_queryset = base_queryset.filter(country__region=region)
        if cluster:
            base_queryset = base_queryset.filter(country__cluster=cluster)

        total_rows = base_queryset.values('process_taxonomy__process_level3').distinct().count()

        if total_rows > 0:
            yes_count = base_queryset.filter(value='Yes').values('process_taxonomy__process_level3').distinct().count()
            percentage = round((yes_count / total_rows) * 100, 2)
        else:
            percentage = 0

        return percentage

    @classmethod
    def calculate_process_level3_percentage(cls, region=None, cluster=None, country=None):
        base_queryset = cls.objects.all()

        if country:
            base_queryset = base_queryset.filter(country__country_description=country)

        total_rows = base_queryset.exclude(value="N/A").values('process_taxonomy__task_level6').distinct().count()

        if total_rows > 0:
            yes_count = base_queryset.filter(value='Yes').values('process_taxonomy__task_level6').distinct().count()
            percentage = round((yes_count / total_rows) * 100, 2)
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

    def process_comp_old(self, region=None, cluster=None):
        total_process_level3 = ProcessValue.objects.filter(process_taxonomy__standard_local='Standard',country=self.country).values('process_taxonomy__process_level3').distinct().count()
        count_process_level3_with_yes = ProcessValue.objects.filter(process_taxonomy__standard_local='Standard', value='Yes',country=self.country).values('process_taxonomy__process_level3').distinct().count()

        if total_process_level3 > 0:
            percentage = round((count_process_level3_with_yes / total_process_level3) * 100, 2)
        else:
            percentage = 0
        return percentage

    @staticmethod
    def calculate_process_level3_percentage(region=None, cluster=None, country=None):
        queryset = ProcessValue.objects.all()

        # Apply filters if provided
        if country:
            queryset = queryset.filter(country__country_description=country)
        if cluster:
            queryset = queryset.filter(country__cluster=cluster)
        if region:
            queryset = queryset.filter(country__region=region)

        # Distinct count of process_level3 where at least one task_level6 has value "Yes"
        yes_count = queryset.filter(value='Yes').values('process_taxonomy__process_level3').distinct().count()

        # Total distinct count of process_level3
        total_count = queryset.values('process_taxonomy__process_level3').distinct().count()

        # Calculate the percentage
        percentage = (yes_count / total_count * 100) if total_count > 0 else 0

        return round(percentage, 2)
