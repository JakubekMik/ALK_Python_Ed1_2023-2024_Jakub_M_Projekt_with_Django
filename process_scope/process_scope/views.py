from django.shortcuts import render
from django.http import HttpResponse
from .models import ProcessTaxonomy,ProcessValue,CountryList
import matplotlib.pyplot as plt
import urllib, base64, io, json
def index(request):
    process_values = ProcessValue.objects.all()

    return render(request, 'index.html', {'process_values': process_values})

def proces_page(request):
    process_tax_values = ProcessTaxonomy.objects.all()

    return render(request, 'proces_page.html', {'process_tax_values': process_tax_values})

def region_page(request):
    region_values = CountryList.objects.all()

    return render(request, 'region_page.html', {'region_values': region_values})

def procesvalue_page(request):
    process_values = ProcessValue.objects.all()

    return render(request, 'procesvalue_page.html', {'process_values': process_values})



def test(request):
    countries = CountryList.objects.all()
    calculate_harmonization_data = []

    for country in countries:
        process_values = ProcessValue.objects.filter(country=country)
        if process_values.exists():
            calculate_harmonization_percentage = process_values.first().calculate_harmonization()
            calculate_harmonization_data.append({
                'country': country.country_description,
                'calculate_harmonization_percentage': calculate_harmonization_percentage
            })

    context = {
        'calculate_harmonization_data': calculate_harmonization_data,
        'countries': countries,
    }

    return render(request, 'calculate_harmonization_per_country.html', context)


def bar_chart_with_colors(x, y, TextX=None, TextY=None, Title=None, highlight_index=None):
    plt.figure(figsize=(10, 6))
    colors = ["#05647e"] * len(x)
    if highlight_index is not None:
        colors[highlight_index] = "#ff5733"
    plt.bar(x, y, color=colors)
    plt.xlabel(TextX)
    plt.ylabel(TextY)
    plt.title(Title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()
    image_base64 = base64.b64encode(image_png)
    image_base64 = image_base64.decode('utf-8')

    return image_base64


def process_comp_per_country_old(request):
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

def process_comp_per_country(request):
    countries = CountryList.objects.all()
    regions = CountryList.objects.values_list('region', flat=True).distinct()
    clusters = CountryList.objects.values_list('cluster', flat=True).distinct()

    selected_region = request.GET.get('region')
    selected_cluster = request.GET.get('cluster')
    selected_country = request.GET.get('country')

    process_comp_data = []
    region_results = []
    cluster_results = []

    # Filter and calculate process_comp_percentage per country
    for country in countries:
        process_values = ProcessValue.objects.filter(country=country)
        if process_values.exists():
            process_comp_percentage = process_values.first().calculate_harmonization(
                region=selected_region, cluster=selected_cluster
            )
            process_comp_data.append({
                'country': country.country_description,
                'region': country.region,
                'cluster': country.cluster,
                'process_comp_percentage': process_comp_percentage
            })

    # Calculate process_comp_percentage per region
    for region in regions:
        region_percentage = ProcessValue().calculate_harmonization(region=region)
        region_results.append({'region': region, 'percentage': region_percentage})

    # Calculate process_comp_percentage per cluster
    for cluster in clusters:
        cluster_percentage = ProcessValue().calculate_harmonization(cluster=cluster)
        cluster_results.append({'cluster': cluster, 'region': CountryList.objects.filter(cluster=cluster).first().region, 'percentage': cluster_percentage})

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
        'regions': regions,
        'clusters': clusters,
        'selected_country': selected_country,
        'selected_region': selected_region,
        'selected_cluster': selected_cluster,
        'region_results': region_results,
        'cluster_results': cluster_results
    }

    return render(request, 'process_comp_per_country.html', context)


def calculate_harmonization_per_country(request):
    countries = CountryList.objects.all()
    calculate_harmonization_data = []

    regions = CountryList.objects.values_list('region', flat=True).distinct()
    clusters = CountryList.objects.values_list('cluster', flat=True).distinct()

    region_results = []
    for region in regions:
        if region:  # Avoid processing empty regions
            region_percentage = ProcessValue().calculate_harmonization(region=region)
            region_results.append({'region': region, 'percentage': region_percentage})

    cluster_results = []
    for cluster in clusters:
        if cluster:  # Avoid processing empty clusters
            cluster_percentage = ProcessValue().calculate_harmonization(cluster=cluster)
            region = CountryList.objects.filter(cluster=cluster).values_list('region', flat=True).distinct().first()
            cluster_results.append({'cluster': cluster, 'region': region, 'percentage': cluster_percentage})

    for country in countries:
        process_values = ProcessValue.objects.filter(country=country)
        if process_values.exists():
            calculate_harmonization_percentage = ProcessValue().calculate_harmonization(region=country.region, cluster=country.cluster)
            calculate_harmonization_data.append({
                'country': country.country_description,
                'region': country.region,
                'cluster': country.cluster,
                'calculate_harmonization_percentage': calculate_harmonization_percentage
            })

    selected_country = request.GET.get('country')
    selected_region = request.GET.get('region')
    selected_cluster = request.GET.get('cluster')
    highlight_index = None
    if selected_country:
        for idx, data in enumerate(calculate_harmonization_data):
            if data['country'] == selected_country:
                highlight_index = idx
                break

    # Generate the bar chart
    x = [data['country'] for data in calculate_harmonization_data]
    y = [data['calculate_harmonization_percentage'] for data in calculate_harmonization_data]
    chart_base64 = bar_chart_with_colors(x, y, TextX='Country', TextY='calculate_harmonization Percentage',
                                         Title='calculate_harmonization Percentage per Country', highlight_index=highlight_index)

    context = {
        'calculate_harmonization_data': calculate_harmonization_data,
        'chart_base64': chart_base64,
        'countries': countries,
        'regions': regions,
        'clusters': clusters,
        'selected_country': selected_country,
        'selected_region': selected_region,
        'selected_cluster': selected_cluster,
        'region_results': region_results,
        'cluster_results': cluster_results
    }

    return render(request, 'calculate_harmonization_per_country.html', context)

def process_level3_percentage(request):
    countries = CountryList.objects.all()
    regions = CountryList.objects.values_list('region', flat=True).distinct()
    clusters = CountryList.objects.values_list('cluster', flat=True).distinct()

    selected_region = request.GET.get('region')
    selected_cluster = request.GET.get('cluster')
    selected_country = request.GET.get('country')

    # Filter countries based on selected filters
    if selected_region:
        countries = countries.filter(region=selected_region)
    if selected_cluster:
        countries = countries.filter(cluster=selected_cluster)
    if selected_country:
        countries = countries.filter(country_description=selected_country)

    process_data = []

    for country in countries:
        percentage = ProcessValue.calculate_process_level3_percentage(
            region=selected_region, cluster=selected_cluster, country=country.country_description
        )
        process_data.append({
            'country': country.country_description,
            'region': country.region,
            'cluster': country.cluster,
            'percentage': percentage
        })

    context = {
        'process_data': process_data,
        'regions': regions,
        'clusters': clusters,
        'selected_country': selected_country,
        'selected_region': selected_region,
        'selected_cluster': selected_cluster
    }

    return render(request, 'process_level3_percentage.html', context)