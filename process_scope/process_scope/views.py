from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import ProcessTaxonomy, ProcessValue, CountryList
import matplotlib.pyplot as plt
import urllib, base64, io, json
import pandas as pd

def index(request):
    process_values = ProcessValue.objects.all()
    return render(request, 'index.html', {'process_values': process_values})

def proces_page(request):
    process_tax_values = ProcessTaxonomy.objects.all()
    return render(request, 'proces_page.html', {'process_tax_values': process_tax_values})

def region_page(request):
    region_values = CountryList.objects.all()
    return render(request, 'region_page.html', {
        'region_values': region_values
    })

def procesvalue_page(request):
    process_values = ProcessValue.objects.all()
    return render(request, 'procesvalue_page.html', {'process_values': process_values})

def edit_process_value(request, id):
    process_value = get_object_or_404(ProcessValue, id=id)
    if process_value.process_taxonomy.standard_local == 'Standard':
        value_choices = dict(ProcessValue.VALUE_CHOICES_STANDARD)
    elif process_value.process_taxonomy.standard_local == 'Local':
        value_choices = dict(ProcessValue.VALUE_CHOICES_LOCAL)
    else:
        value_choices = {}

    return render(request, 'edit_process_value.html', {
        'process_value': process_value,
        'value_choices': value_choices,
    })

def update_process_value(request):
    if request.method == 'POST':
        process_value_id = request.POST.get('process_value_id')
        new_value = request.POST.get('new_value')
        process_value = get_object_or_404(ProcessValue, id=process_value_id)
        process_value.value = new_value
        process_value.save()
        return redirect('procesvalue_page')
def edit_region(request, id):
    region = get_object_or_404(CountryList, id=id)
    return render(request, 'edit_region.html', {
        'region': region
    })

def add_region(request):
    return render(request, 'add_region.html')

def create_region(request):
    if request.method == 'POST':
        region = request.POST.get('region')
        cluster = request.POST.get('cluster')
        country = request.POST.get('country')
        CountryList.objects.create(region=region, cluster=cluster, country_description=country)
        return redirect('region_page')
def update_region(request):
    if request.method == 'POST':
        region_id = request.POST.get('region_id')
        new_region = request.POST.get('new_region')
        new_cluster = request.POST.get('new_cluster')
        new_country = request.POST.get('new_country')
        region = get_object_or_404(CountryList, id=region_id)
        region.region = new_region
        region.cluster = new_cluster
        region.country_description = new_country
        region.save()
        return redirect('region_page')

def edit_process(request, id):
    process_tax = get_object_or_404(ProcessTaxonomy, id=id)
    return render(request, 'edit_process.html', {
        'process_tax': process_tax
    })
def update_process(request):
    if request.method == 'POST':
        process_id = request.POST.get('process_id')
        category_level1 = request.POST.get('category_level1')
        process_group_level2 = request.POST.get('process_group_level2')
        process_level3 = request.POST.get('process_level3')
        subprocess_level4 = request.POST.get('subprocess_level4')
        activity_level5 = request.POST.get('activity_level5')
        task_level6 = request.POST.get('task_level6')
        standard_local = request.POST.get('standard_local')
        process_tax = get_object_or_404(ProcessTaxonomy, id=process_id)
        process_tax.category_level1 = category_level1
        process_tax.process_group_level2 = process_group_level2
        process_tax.process_level3 = process_level3
        process_tax.subprocess_level4 = subprocess_level4
        process_tax.activity_level5 = activity_level5
        process_tax.task_level6 = task_level6
        process_tax.standard_local = standard_local
        process_tax.save()
        return redirect('proces_page')

def add_process(request):
    return render(request, 'add_process.html')

def create_process(request):
    if request.method == 'POST':
        category_level1 = request.POST.get('category_level1')
        process_group_level2 = request.POST.get('process_group_level2')
        process_level3 = request.POST.get('process_level3')
        subprocess_level4 = request.POST.get('subprocess_level4')
        activity_level5 = request.POST.get('activity_level5')
        task_level6 = request.POST.get('task_level6')
        standard_local = request.POST.get('standard_local')
        ProcessTaxonomy.objects.create(
            category_level1=category_level1, process_group_level2=process_group_level2,
            process_level3=process_level3, subprocess_level4=subprocess_level4,
            activity_level5=activity_level5, task_level6=task_level6, standard_local=standard_local)
        return redirect('proces_page')

def bar_chart_with_colors(x, y, selected_country=None, selected_cluster=None, selected_region=None):
    plt.figure(figsize=(10, 6))
    colors = ["#05647e"] * len(x)

    for i, country in enumerate(x):
        if selected_country and country == selected_country:
            colors[i] = "#ff5733"  # Highlight selected country in red
        elif selected_cluster and CountryList.objects.filter(country_description=country,
                                                             cluster=selected_cluster).exists():
            colors[i] = "#FFA500"  # Highlight selected cluster in orange
        elif selected_region and CountryList.objects.filter(country_description=country,
                                                            region=selected_region).exists():
            colors[i] = "#008000"  # Highlight selected region in green

    plt.bar(x, y, color=colors)
    plt.xlabel('Country')
    plt.ylabel('Process Level 3 Percentage')
    plt.title('Process Completion Percentage per Country')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()

    image_base64 = base64.b64encode(image_png).decode('utf-8')
    return image_base64

def process_comp_per_country(request):
    countries = CountryList.objects.all()
    process_comp_data = []
    for country in countries:
        process_comp_percentage = ProcessValue.process_comp(country)
        process_comp_data.append({
            'country': country.country_description,
            'process_comp_percentage': process_comp_percentage
        })

    context = {
        'process_comp_data': process_comp_data,
    }

    return render(request, 'process_comp_per_country.html', context)

    selected_country = request.GET.get('country')
    highlight_index = None
    if selected_country:
        for idx, data in enumerate(process_comp_data):
            if data['country'] == selected_country:
                highlight_index = idx
                break

    # Generate the bar chart
    x = [data['country'] for data in process_comp_data]
    y = [data['process_comp_percentage'] for data in process_comp_data]
    chart_base64 = bar_chart_with_colors(x, y, TextX='Country', TextY='Process Comp Percentage',
                                         Title='Process Comp Percentage per Country', highlight_index=highlight_index)

    context = {
        'process_comp_data': process_comp_data,
        'chart_base64': chart_base64,
        'countries': countries,
        'selected_country': selected_country
    }

    return render(request, 'process_comp_per_country.html', context)

def calculate_harmonization_per_country(request):
    countries = CountryList.objects.all()
    regions = CountryList.objects.values_list('region', flat=True).distinct()
    clusters = CountryList.objects.values_list('cluster', flat=True).distinct()

    selected_country = request.GET.get('country')
    selected_region = request.GET.get('region')
    selected_cluster = request.GET.get('cluster')

    calculate_harmonization_data = []
    for country in countries:
        harmonization_percentage = ProcessValue.calculate_harmonization(country=country.country_description)
        calculate_harmonization_data.append({
            'country': country.country_description,
            'region': country.region,
            'cluster': country.cluster,
            'calculate_harmonization_percentage': harmonization_percentage
        })

    x = [data['country'] for data in calculate_harmonization_data]
    y = [data['calculate_harmonization_percentage'] for data in calculate_harmonization_data]
    chart_base64 = bar_chart_with_colors(
        x, y,
        selected_country=selected_country,
        selected_cluster=selected_cluster,
        selected_region=selected_region
    )

    context = {
        'calculate_harmonization_data': calculate_harmonization_data,
        'chart_base64': chart_base64,
        'countries': countries,
        'regions': regions,
        'clusters': clusters,
        'selected_country': selected_country,
        'selected_region': selected_region,
        'selected_cluster': selected_cluster
    }

    return render(request, 'calculate_harmonization_per_country.html', context)
def process_level3_percentage(request):
    countries = CountryList.objects.all()
    regions = CountryList.objects.values_list('region', flat=True).distinct()
    clusters = CountryList.objects.values_list('cluster', flat=True).distinct()

    selected_region = request.GET.get('region')
    selected_cluster = request.GET.get('cluster')
    selected_country = request.GET.get('country')
    process_data = []
    for country in countries:
        percentage = ProcessValue.calculate_process_level3_percentage(
            region=None, cluster=None, country=country.country_description
        )
        process_data.append({
            'country': country.country_description,
            'region': country.region,
            'cluster': country.cluster,
            'percentage': percentage
        })

    x = [data['country'] for data in process_data]
    y = [data['percentage'] for data in process_data]
    chart_base64 = bar_chart_with_colors(
        x, y,
        selected_country=selected_country,
        selected_cluster=selected_cluster,
        selected_region=selected_region
    )

    context = {
        'process_data': process_data,
        'chart_base64': chart_base64,
        'countries': list(countries.values('country_description', 'region', 'cluster')),
        'regions': regions,
        'clusters': clusters,
        'selected_country': selected_country,
        'selected_region': selected_region,
        'selected_cluster': selected_cluster
    }

    return render(request, 'process_level3_percentage.html', context)