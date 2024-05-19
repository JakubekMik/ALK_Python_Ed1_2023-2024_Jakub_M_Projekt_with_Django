from django.shortcuts import render
from django.http import HttpResponse
from .models import ProcessTaxonomy,ProcessValue,CountryList
import matplotlib.pyplot as plt
import io
import urllib, base64
from .define_function import bar_chart_with_colors


def index(request):
    process_values = ProcessValue.objects.all()

    return render(request, 'index.html', {'process_values': process_values})


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
    calculate_harmonization_data = []

    for country in countries:
        process_values = ProcessValue.objects.filter(country=country)
        if process_values.exists():
            calculate_harmonization_percentage = process_values.first().calculate_harmonization()
            calculate_harmonization_data.append({
                'country': country.country_description,
                'calculate_harmonization_percentage': calculate_harmonization_percentage
            })

    selected_country = request.GET.get('country')
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
        'selected_country': selected_country
    }

    return render(request, 'calculate_harmonization_per_country.html', context)
