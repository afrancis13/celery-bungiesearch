===================
celery-bungiesearch
===================
.. image:: https://travis-ci.org/afrancis13/celery-bungiesearch.svg?branch=master
    :target: https://travis-ci.org/afrancis13/celery-bungiesearch

A repository that wraps the provided Bungiesearch signal processing class
in your own celery tasks.

This Django app allows you to utilize Celery for automatically updating and deleting
objects in a Bungiesearch search index.

Compatible with most recent version of Bungiesearch, which is similar to Haystack,
but interacts directly with elasticsearch-dsl and therefore allows for more custom
ranking functions.

Install
-------
.. code-block:: python

    pip install celery-bungiesearch

Requirements
------------
* Django 1.4.3+
* Bungiesearch_ 1.2.1+
* Celery_ 3.1.18+

Usage
-----
\1. Add ``'celery_bungiesearch'`` to ``INSTALLED_APPS`` in settings

.. code-block:: python

 INSTALLED_APPS = [
     # ..
     'celery_bungiesearch',
 ]

\2. Add ``CelerySignalProcessor`` to ``settings.BUNGIESEARCH['SIGNAL_CLASS']`` in settings. This will ensure that any model that's managed by a ``BungiesearchManager`` acquire ``CelerySignalProcessor`` as the signal processor.

.. code-block:: python

 from celery_bungiesearch import CelerySignalProcessor

 BUNGIESEARCH = {
    # ..
    'SIGNALS': {
        'SIGNAL_CLASS': 'celery_bungiesearch.signals.CelerySignalProcessor',
        'BUFFER_SIZE' : 100
    }
 }

\3. Add celery-bungisearch configuration variables to your settings file. The task below is the default version, but you may include your own custom classes if you desire (note that none of these environment variable are required, and can be entirely excluded from the settings file):

.. code-block:: python

 CELERY_BUNGIESEARCH_QUEUE = None
 CELERY_BUNGIESEARCH_TASK = 'Your custom index task path'
 CELERY_BUNGIESEARCH_CUSTOM_TASK = 'Your custom celery task path'

\4. Ensure your Celery instance is running.

Testing
-------
You can run tests locally for celery-bungiesearch by simply running the command ``tox`` or ``tox test``. You must have an instance of elasticsearch running locally. You can also run tests using continuous integration with Travis CI (build status at the top of this README).

Thanks
------
This application borrows liberally from Jannis Leidel's `celery-haystack`_ and from Christopher Rabotin's Bungiesearch_, which itself was the inspiration for this project.

Issues
------
Please submit a pull request or use the `Github issue tracker`_ for any bug fixes, bug reports, or feature requests.

.. _`celery-haystack`: https://celery-haystack.readthedocs.org/en/latest/
.. _Bungiesearch: https://github.com/Sparrho/bungiesearch
.. _Celery: http://celeryproject.org/
.. _`Github issue tracker`: https://github.com/afrancis13/celery-bungiesearch/issues
