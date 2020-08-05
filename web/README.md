# Protein-prediction-web

## Install

### 1. Install python
using Python 2.7.16

### 2. Install package


```bash
pip install -r requirement.txt
```

### 3. Run

```bash
python manage.py runserver
```

## Add Project

If you want to add another project to this website, you have to follow the steps below.

### 1. Create template

In the path(```/Protein/templates/psldoc3```), you should duplicate this folder like ```/Protein/templates/example```.
You can create your own ```project.html```, set the input you needed.
You can create your own ```result.html```, display the output you needed.
You should upload ```tutorial.pdf``` for your project.

The file name about ```*.html``` and ```tutorial.pdf``` can not be changed.

### 2. Write your own function

In the path(```/Protein/views.py```), you can find out all the code about the website.
You should write your own function in ``` def result(request)```, and specify for your own project(just like add statement ``` project == "psldoc3"```)
  
