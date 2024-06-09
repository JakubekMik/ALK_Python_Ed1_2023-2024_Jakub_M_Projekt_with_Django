# Jakub Mikołajczyk - Django Process Harmonization Project

## Introduction to Process Harmonization Program

The Process Harmonization Program is a data analysis tool built using Django, which enables the processing and analysis of information related to business processes. Below you will find a description of the tasks performed by this program:

### Illustration of Major Factors

This program illustrates two major factors:

- **Process Centralization (Process Scope)**: This factor illustrates the transition of processes from local operations to a central hub. It indicates whether specific business processes have been moved to a central location for standardized execution.
- **Process Harmonization**: This factor demonstrates if the processes performed at the central hub follow a standard procedure. It also highlights any extra tasks or tasks that have not been transitioned to the central hub.

### Models

The program uses three main data models:

- **ProcessTaxonomy**:
  - `category_level1`
  - `process_group_level2`
  - `process_level3`
  - `subprocess_level4`
  - `activity_level5`
  - `task_level6`
  - `standard_local`

- **CountryList**:
  - `country_description`
  - `cluster`
  - `region`

- **ProcessValue**:
  - `process_taxonomy` (ForeignKey to `ProcessTaxonomy`)
  - `country` (ForeignKey to `CountryList`)
  - `value` (choices: 'Yes', 'No' for standard, 'A', 'B', 'C', 'N/A' for local)

### Signals

The application uses Django signals to automate the creation and updating of `ProcessValue` records whenever new `CountryList` or `ProcessTaxonomy` records are added or updated. This ensures that all relevant combinations of processes and countries are tracked.

### Calculations

- **Calculation of Process Scope Completion:**

The program calculates whether for a given process level (level 4) there is a task performed at level 6 (value "Yes"). The process is considered adopted if such a task exists. Otherwise, if such a task is missing, the process is considered unadopted, with the possibility of "Local Exception" being skipped.

- **Calculation of Process Harmonization:**

The program calculates the process harmonization index, which is the ratio of the number of Standard Tasks performed (value Yes) to the total number of Standard Tasks in the process, taking into account any Local Exceptions. This index helps understand the degree of standardization and consistency in the processes being performed.

### Graphical Presentation of Results

The program presents the analysis results graphically, making them easier to understand and interpret. Users have the option to limit the results to a specific region or process, enabling a more detailed analysis.

### Running Instructions

To run the Django project, follow these steps:

- ** Clone the repository:**

```python
git clone https://github.com/JakubekMik/your-django-repo.git
cd your-django-repo
```

- ** Install the required Python packages:**
```python
pip install -r requirements.txt
```
- **Apply migrations:**

```python
python manage.py migrate
```
- ** Create a superuser:**

```python
python manage.py createsuperuser
```
- ** Run the development server:**

```python
python manage.py runserver
```

- ** Access the application:**
Open your web browser and navigate to http://127.0.0.1:8000/.

### Future Development

In future versions of the Process Harmonization Program, we aim to include the following features:

- ** Enhanced Search Functionality:** 

Implement a robust search feature that allows users to quickly and easily find specific process or country values. This will improve the usability and efficiency of the program, especially when dealing with large datasets.

- ** Logging Functionality:** 

Add the ability for users to log in to the system to update and add values. This feature will enhance the security and integrity of the data by ensuring that only authorized users can make changes.

These enhancements will further streamline the process of analyzing and harmonizing business processes, making the program even more valuable to users.