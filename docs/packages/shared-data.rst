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

The repository contains three top-level data directories:

.. code-block:: text

   shared-data/
   ├── __init__.py
   ├── csv_files/
   │   └── *.csv / *.ecsv
   ├── filters/
   │   └── *.dat
   ├── reference_spectra/
   │   └── ...
   └── pyproject.toml

The repository is named ``shared-data``, the distribution installed by pip is
``classi-shared-data``, and the import package is
``shared_data``.

The installable distribution includes ``csv_files/*.csv``,
``csv_files/*.ecsv``, and all files immediately under ``reference_spectra`` as
package data. The ``filters`` directory is repository-maintained source data and
is not exposed through the installed ``shared_data`` package.

Accessing packaged files
------------------------

The package exposes dictionaries of traversable resources keyed by filename
stem. Use these as the primary interface rather than constructing paths from
``__file__``:

.. code-block:: python

   import pandas as pd
   from shared_data import CSV_FILES, REFERENCE_SPECTRA

   qe_file = CSV_FILES["kaf8300c_qe"]
   collimator_file = CSV_FILES["ac508-180-ab"]
   template_file = REFERENCE_SPECTRA["SNIa_max_z0p05"]

   qe = pd.read_csv(qe_file, header=None, names=["wavelength", "transmission"])

The values support methods such as ``open()`` and can be passed directly to
many readers. For libraries that require a real filesystem path, wrap a value
with ``importlib.resources.as_file`` so it remains compatible with different
package loaders.

The authoritative list of available spectra and their metadata is maintained
in the shared-data repository's `reference-spectrum inventory`_.

.. _reference-spectrum inventory:
   https://github.com/MLO-CLASSI/shared-data/blob/main/reference_spectra/README.md

Atmospheric transmission
------------------------

The `LSST atmosphere profile`_ is an Astropy ECSV table with wavelength in
nanometers and dimensionless throughput. Its embedded metadata identifies
``syseng_throughputs`` version 1.9, upstream commit
``fcc05772f99427e4a45cd1b9da1628dded9a06d5``, nominal airmass 1.0, aerosol
treatment, and the upstream ``atmos_10.dat`` source. The simulator treats that
embedded airmass as the baseline and raises its throughput to the requested
airmass. The repository file and its metadata are authoritative for this model.

.. _LSST atmosphere profile:
   https://github.com/MLO-CLASSI/shared-data/blob/main/csv_files/atm_lsst.ecsv

Photometric bandpasses
----------------------

The repository's `filter-profile directory`_ contains LSST v1.9 total-system
``g``, ``r``, and ``i`` throughput profiles. Each file header records the
upstream ``syseng_throughputs`` version and commit, atmospheric treatment, and
blue/red wavelength cutoffs. These profiles define the AB magnitudes reported
in the reference-spectrum inventory.

Because the filter profiles are not package data, installed-package consumers
cannot access them through ``CSV_FILES`` or ``REFERENCE_SPECTRA``. The
repository directory and the metadata embedded in each profile are the
authoritative sources for their content and provenance.

.. _filter-profile directory:
   https://github.com/MLO-CLASSI/shared-data/tree/main/filters

What belongs here?
------------------

Put data here when multiple spectrograph packages need the same authoritative
file: detector QE curves, grating-efficiency curves, fiber attenuation,
photometric bandpasses, atmospheric extinction, and common reference spectra
are typical examples.

Generated observation products and user-specific calibration data should not be
put in this package.
