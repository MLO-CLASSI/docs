shared-data
===========

Purpose
-------

``classi-shared-data`` is an installable Python distribution containing common
spectrograph reference files. It exists so that each scientific repository can
declare a dependency on one authoritative data package instead of carrying a
private copy of the same curves.

Package layout
--------------

The current distribution contains two top-level data directories:

.. code-block:: text

   shared-data/
   ├── __init__.py
   ├── csv_files/
   │   └── *.csv
   ├── reference_spectra/
   │   └── ...
   └── pyproject.toml

The repository is named ``shared-data``, the distribution installed by pip is
``classi-shared-data``, and the import package is
``shared_data``.

The packaging metadata includes ``csv_files/*.csv`` and all files immediately
under ``reference_spectra`` as package data.

Accessing packaged files
------------------------

The package exposes dictionaries of traversable resources keyed by filename
stem. Use these as the primary interface rather than constructing paths from
``__file__``:

.. code-block:: python

   from shared_data import CSV_FILES, REFERENCE_SPECTRA

   qe_file = CSV_FILES["kaf8300c_qe"]
   template_file = REFERENCE_SPECTRA["SNIa_max_z0p05"]

   with qe_file.open("rb") as handle:
       payload = handle.read()

The values support methods such as ``open()`` and can be passed directly to
many readers. For libraries that require a real filesystem path, wrap a value
with ``importlib.resources.as_file`` so it remains compatible with different
package loaders.

The authoritative list of available spectra and their metadata is maintained
in the shared-data repository's `reference-spectrum inventory`_.

.. _reference-spectrum inventory:
   https://github.com/MLO-CLASSI/shared-data/blob/main/reference_spectra/README.md

What belongs here?
------------------

Put data here when multiple spectrograph packages need the same authoritative
file: detector QE curves, grating-efficiency curves, fiber attenuation,
atmospheric extinction, and common reference spectra are typical examples.

Do not put generated observation products or user-specific calibration data in
this package.
