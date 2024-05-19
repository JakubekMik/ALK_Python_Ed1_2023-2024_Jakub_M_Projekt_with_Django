from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CountryList, ProcessTaxonomy, ProcessValue

@receiver(post_save, sender=CountryList)
def create_or_update_process_values_cl(sender, instance, created, **kwargs):
    if created:
        create_process_values(instance)
    else:
        update_process_values(instance)

@receiver(post_save, sender=ProcessTaxonomy)
def create_process_values_pt(sender, instance, created, **kwargs):
    if created:
        countries = CountryList.objects.all()
        for country in countries:
            if instance.standard_local == 'Standard':
                value = 'No'
            elif instance.standard_local == 'Local':
                value = 'N/A'
            else:
                value = ''

            ProcessValue.objects.create(process_taxonomy=instance, country=country, value=value)


def create_process_values(country):
    process_taxonomies = ProcessTaxonomy.objects.all()

    for process_taxonomy in process_taxonomies:
        if process_taxonomy.standard_local == 'Standard':
            value = 'No'
        elif process_taxonomy.standard_local == 'Local':
            value = 'N/A'
        else:
            value = ''

        existing_process_value = ProcessValue.objects.filter(process_taxonomy=process_taxonomy, country=country).first()
        if not existing_process_value:
            ProcessValue.objects.create(process_taxonomy=process_taxonomy, country=country, value=value)

def update_process_values(country):
    process_taxonomies = ProcessTaxonomy.objects.all()
    for process_taxonomy in process_taxonomies:
        try:
            process_value = ProcessValue.objects.get(process_taxonomy=process_taxonomy, country=country)
            if process_taxonomy.standard_local == 'Standard':
                if  len(process_value.value)>0:
                    pass
                else:
                    process_value.value = 'No'
            elif process_taxonomy.standard_local == 'Local':
                if  len(process_value.value)>0:
                    pass
                else:
                    process_value.value = 'N/A'
            else:
                process_value.value = ''
            process_value.save()
        except ProcessValue.DoesNotExist:
            create_process_values(country)
