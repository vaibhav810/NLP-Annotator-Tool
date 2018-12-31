# NER Tool

NER Tool is an open source text annotation tool for human. It provides annotation features for text classification, sequence labeling and sequence to sequence. So, you can create labeled data for sentiment analysis, named entity recognition, text summarization and so on. Just create project, upload data and start annotation. You can build dataset in hours.

## Demo

## Features

* Collaborative annotation
* Language independent
* (future) Auto labeling

## Requirements

* Python 3.6+
* django 2.0.5+
* Google Chrome(highly recommended)

## Installation

To install NER Tool, simply run:

```bash
$ git clone https://github.com/vaibhav810/NLP-Annotator-Tool.git
$ cd nlp_tool
$ pip install -r requirements.txt
$ cd app
```

First we’ll need to create a user who can login to the admin site. Run the following command:


```bash
$ python manage.py createsuperuser
```

Enter your desired username and press enter.

```bash
Username: admin
```

You will then be prompted for your desired email address:

```bash
Email address: admin@example.com
```

The final step is to enter your password. You will be asked to enter your password twice, the second time as a confirmation of the first.

```bash
Password: **********
Password (again): *********
Superuser created successfully.
```

## Usage

### Start the development server

Let’s start the development server and explore it.

If the server is not running start it like so:

```bash
$ python manage.py runserver
```

Now, open a Web browser and go to <http://127.0.0.1:8080/login/>. You should see the login screen:

<img src="./docs/login_form.png" alt="Login Form" width=400>

### Create a project

Now, try logging in with the superuser account you created in the previous step. You should see the NER Tool project list page:

<img src="./docs/projects.png" alt="projects" width=600>

You should see there is no project.

To create your project, make sure you’re in the project list page and select `Create Project` button. You should see the following screen:

<img src="./docs/create_project.png" alt="Project Creation" width=400>

In project creation, you can select three project types: text classificatioin, sequence labeling and sequence to sequence. You should select a type with your purpose.

### Import text items

Now that we’ve created a project. Now you’re at the “dataset” page for the project. This page displays all the documents in the project. You can see there is no documents.

To import text items, select `Import Data` button in the navigation bar. You should see the following screen:

<img src="./docs/upload.png" alt="Upload project" width=600>

The text items should be provided in txt format. As of now, it must contain only texts. Each line must contain a text:

```python
EU rejects German call to boycott British lamb.
President Obama is speaking at the White House.
He lives in Newark, Ohio.
...
```

Once you select a csv file on your computer, select `Upload` button.

### Define labels

Now we’ll define your labels. To define your labels, select `Labels` menu. You should see the label editor page:

<img src="./docs/label_editor.png" alt="Edit label" width=600>

In label editor page, we can create labels by specifying label text, shortcut key, background color and text color.

### Annotation

Now, we are ready to annotate the texts. Back to the project list page and select the project. You can start annotation!

<img src="./docs/annotation.png" alt="Edit label" width=600>

