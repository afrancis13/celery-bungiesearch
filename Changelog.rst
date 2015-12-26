Changelog
=========
1.2.3
------------------
* Provide a simple mechanism for tests to run with refresh behavior.

1.2.2
------------------
* Bug fixes, do not force refresh the index when running tasks.

1.2.0
------------------
* Fixing bulk delete task and removing dependency on djcelery_transactions.

1.1.4
------------------
* Fixes bug in the setup.py file from 1.1.0 release

1.1.0
------------------
Updates ``celery-bungiesearch`` to be compatible with the most up to date version of bungiesearch (1.2.1 as of 8/13/2015).

* The setup and teardown methods in the signal processor reflect the mechanism by which bungiesearch performs signal processing
* Defaults index task to ``CeleryIndexTask`` (no longer required to provide this in settings)
* Bulk delete acts upon primary keys, and not entire instances
* Clean up and increased error handling

1.0.0
------------------
Initial release.
