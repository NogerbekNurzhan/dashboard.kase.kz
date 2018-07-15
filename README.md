# Description 

**dashboard.kase.kz** is a corporate project of the kazakhstan stock exchange (KASE) for the administration of the main website of the organization. In other words, it is an administrative panel, which can be used only by employees of the KASE.

# Implementation detail

Django web framework (version 1.11.5) and Python programming language (version 2.7) were used to create the current project. Oracle 11g had been used as a DBMS. In production project deployed in stack: ```NGINX + gunicorn + supervisor```.

The project uses several third-party packages which you can install to your virtual environment by command:

```pip install -r requirements.txt```

All user queries are written to ```debug.log``` file. With the help of the ```django-split-settings``` application the django settings are divided into production and development versions of the sites.

The project consists of several large applications (modules):
* slider
* static_pages
* documents
* events
* faq
* indicators
* video
* users

Create, Read, Update, Delete (CRUD) are basic operations we perform in all above modules. I вуused AJAX to create asynchronous requests to manipulate models. AJAX allows us to perform CRUD operations without reboot the page.

# Modules

We display a list of all slides in the main page of ```"Slider"``` module. Informativeness increased by displaying values from 4 fields of the Slide model in each record.These fields are: header, optional header, the location of the slide, the status of the slide. Thus, the moderator can easily find the information he is looking for. Each record has buttons to edit, delete and view the change history.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/1.png)

If the administrator or moderator of the system decided to delete the slide, he will need to click on the delete button, then he will see a modal. Thus, you will not be able to delete a record by accident.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/3.png)

In the screenshot below you can see the page with the history of changes. ```django-reversion``` application was used to implement such mechanism. The moderator of the system can see who made the change, how much the change was made and the status of the change. Also if it necessary, he can roll back to a certain version of the record.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/4.png)

```django-modeltranslation``` application was used to create language tabs in edit and create forms.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/2.png)

We display a list of all users of the system in the main page of ```"Users"``` module.  Informativeness increased by displaying the login, email and user status. Search the user by login or email is implemented through JavaScript. The search is case-insensitive. Thus, the probability of finding the desired record by the administrator is increased.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/8.png)

To create a new user in the system we use the following form:

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/10.png)

We can use the following form to edit user information:

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/11.png)

The system administrator can see all the information about the user in edit form. Django store user password in encrypted form in the database by default. Therefore, a separate form is used to set a new password, which verifies the complexity of the created password. The administrator specifies the user status in the edit form. User status: moderator, administrator or simple user. The system administrator has all access rights. The moderator has only those rights that were set in the field "user permissions". That field is implemented by ```django-select2``` application. When you activate the checkbox "display wysiwyg editor" for a specific user, that user in the form of editing static pages can see wysiwyg widget. With the help of that widget he can work with html code pages comfortably.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/9.png)

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/21.png)

In fact, many of the mechanisms in ```"Static Pages"``` module respond to those that I described earlier for the "Slider" module.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/5.png)

I would like to focus only on the editing form of static page. The form has a "page body" field, which is available in two modes. In the first mode, it is a simple text field, which can be expanded to the entire screen by clicking the icon in the upper right corner. In the second mode it is wysiwyg widget for more convenient work with html. The [summernote](https://summernote.org/) plugin was used in the second mode.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/6.png)

```"Corporate Documents"``` module is used in 10 pages of the project. The screenshots below are an example of just a few of these pages.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/17.png)

In this module we use ```"Closure Table"``` method to store hierarchical data in database. We use ```Nestable2``` plugin in frontend to display data in tree order. When you drag documents between branches occurs an AJAX request, which saves the new tree structure.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/18.png)

The first 10 top level documents with all descendants are displayed initially. When user scrolling down, 10 more documents are loaded by AJAX. Thus, we reduce the active load to databaseand accelerate the response of the page to user requests. A filter by different characteristics and search for a document by name is implemented for quick search of a document. They are also used for AJAX requests.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/19.png)

In ```"Events"``` module will be displayed a different list of events depending on the selected characteristics in the filter panel.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/14.png)

The ```"bootstrap 3 datepicker"``` plugin was used in "event date" field of editing form. You can also select one or more files when uploading images.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/12.png)

Then, if necessary, in the future, in the form of editing, you can mark the images you need and delete them. AJAX was used to implement this mechanism. It updates the block with images when we delete selected images and does not close the form.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/13.png)

```"Indicators"``` (reference book of indicators) module should be perceived only as a reference. Therefore, there is only the ability to edit records. This module displays a list of categories. Each category has a list of indexes. Depending on the status of the indicator, the record has different colors. Indicators can also be sorted and dragged between categories. The categories themselves can also be sorted for convenience by changing the order.

![](https://github.com/NogerbekNurzhan/dashboard.kase.kz/blob/master/screenshots/16.png)

The ```"Video"``` and ```"FAQ"``` modules perform similar operations and similar implementation mechanisms, which were described earlier in other modules.
