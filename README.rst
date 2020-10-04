===========
Photonomist
===========
Photonomist aims at helping photo-lovers (or simply photo-owners :D) with tidying their photos.
Given a path that contains photos, photonomist will extract the dates of your photos, 
create directories and group photos according to their dates.

Photonomist took its name from the words:

- Photo..  --> Photography (art of captruring the light)                (Greek root: (Φως) Φωτογραφία)
- ..nomist --> Taxonomist  (person who groups entities into categories) (Greek root: Ταξινομία ή Ταξινόμηση)

Motivation
===========
As both a photo-owner and a photo-lover, I found myself struggling with grouping my photos in a sustainable way.

I kept creating different directories, with different name patterns to store my photos in a meaningfull way.
Each time I was sure that after 3 months I would remember when, where and with whom I had captured each banch of photos.


Except for that, I was always failing with the groupping them depending on different criteria. 
I know that proffs and semi-proffs tend to group photos according to their rating (1 star.. 5 stars), 
but in my case the time aspect proved to be the most meaningful.

It was impossible, though, to check the date of each photo and create a different directory for each date and
then manually move the photos to the corresponding directory. 
Especially, when I was supposed to "tidy" photos of 2 years time-span!!!!

That's why I decided to build this cool app, which does the dirty work for me (but not only)!!

Features
==========
Photonomist just took its first breath. It is in version 0.1.0.

What makes it standing out, except for **taking care of your photos for you** is that:

- It ascertains the **validity** of user's input
- It verifies that the **provided input path contains** *.jpg* or *.nef* (*Nikon* raw) photos
- It checks if you have *enough disk space* **ONLY** in case that the **input** and the **export** path point to different disks. I.e. if you move your photos from a cellphone to a hard drive!
- It automatically **extracts** your photos' metadata, **creates and names** directories using the extracted dates and **moves** the photos to the corresponding directory
- It **writes** in the *not_transerred.txt* all the photos' that was not possible to be moved

Minimum Requirements
====================
- Python 3.8+
- Download `Anaconda`_

.. _Anaconda: https://www.anaconda.com/products/individual

|

Basic Setup
===========
Create **Photonomist** Virtual Environmet
-----------------------------------------
1. Start *Anaconda Powershell Prompt*
2. Change Directory to Photonomist root dir (*cd C:\\repos\\photonomist*)
3. Create the environment from the environment.yml file

.. code-block:: console

    $ conda env create -f environment.yml

4. Activate your new venv

.. code-block:: console

    $ conda activate photonomist

5. Congratulations!! You have your new env with all dependencies in there!

| 

Install for the current user:
-------------------------------

.. code-block:: console

    $ python -m pip install . --user

| 

Run the application:
--------------------

.. code-block:: console

    $ python -m photonomist

| 

Developer Edition
==================

Optional Requirements
---------------------

.. _pytest: http://pytest.org
.. _Sphinx: http://sphinx-doc.org

- `pytest`_ (for running the test suite)
- `Sphinx`_ (for generating documentation)

| 

Did you touch the code?
-----------------------

.. code-block:: console

    $ python -m pip install . --user

| 

Run the test suite:
-------------------

**Change Directory to photonomist root dir** (*cd C:\\repos\\photonomist*)

.. code-block:: console
   
    $ pytest test/

|

Build documentation:
----------------------
**Change Directory to photonomist doc dir** (*cd C:\\repos\\photonomist\\doc*)

.. code-block:: console

    $ make html

|

Usage
======

1. Double click the .exe file

|       **OR**

2. - Start *Anaconda Powershell Prompt*
   - Activate the *Photonomist* env ( $ conda activate photonomist)
   - Run: $ python -m photonomist

|       **OR**

3. - Open your favorite `IDE`_
   - Do your magic and activate the *Photonomist* env
   - Open the *__main__* file
   - Run it

.. _IDE: https://en.wikipedia.org/wiki/Integrated_development_environment