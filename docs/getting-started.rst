Getting started
===============

Choose a path
-------------

Most users do not need to begin with the software repositories.

* **Observers and operators:** start with the
  :doc:`instrument overview <user-guide/overview>`, then continue through
  :doc:`planning <user-guide/planning>`,
  :doc:`observing <user-guide/observing>`, and
  :doc:`reduction <user-guide/reduction>`.
* **Instrument scientists:** read the :doc:`hardware overview <hardware/index>`,
  :doc:`system architecture <user-guide/architecture>`, and
  :doc:`reference conventions <reference/conventions>` before using the
  component and package reference pages.
* **Software developers:** use the repository map below and the
  :doc:`development guide <development>`.

The operational procedures in this manual should be checked against the current
observatory configuration and commissioning status. Repository documentation is
useful implementation reference, but it is not a substitute for the observing
workflow.

Software layout
---------------

The software stack is organized as several repositories with distinct
responsibilities. Keeping these concerns separate makes the scientific
packages usable without requiring observatory-control dependencies and keeps
shared calibration/reference files from being copied into every repository.

.. list-table:: Main repositories
   :header-rows: 1
   :widths: 20 80

   * - Repository / distribution / import
     - Role
   * - ``etc`` / ``classi-etc`` / ``etc``
     - Predict source and sky counts and signal-to-noise for a supplied spectrum,
       instrument configuration, exposure time, and optional photometric scaling.
   * - ``sim`` / ``classi-sim`` / ``simulator``
     - Forward-model spectra through the optical geometry and detector to produce
       realistic synthetic data products.
   * - ``pipeline`` / ``classi-pipeline`` / ``pipeline``
     - Reduce detector frames and extract one-dimensional spectra from the fiber
       traces, carrying masks and uncertainties through the reduction.
   * - ``shared-data`` / ``classi-shared-data`` / ``shared_data``
     - Installable package containing common CSV calibration/reference curves and
       reference spectra.
   * - ``ics`` / ``classi-ics`` / ``ics``
     - Operate and monitor the science camera, camera-lens focus, telescope-side
       guide hardware, and related observatory interfaces.

Environment strategy
--------------------

For development, clone the repositories side-by-side and use editable installs.
A typical checkout can look like this:

.. code-block:: text

   spectrograph/
   ├── etc/
   ├── sim/
   ├── pipeline/
   ├── shared-data/
   ├── ics/
   └── docs/

Create a virtual environment and install the packages you need. Package metadata
should declare ``classi-shared-data`` as a dependency rather than asking
users to copy its files manually. Repository, distribution, and import names
are not always identical; the table above lists them in that order.

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   python -m pip install -U pip
   python -m pip install -e ./shared-data
   python -m pip install -e ./etc
   python -m pip install -e ./sim
   python -m pip install -e ./pipeline
   python -m pip install -e ./ics

The ICS requires Python 3.11 or newer. Once installed, launch it with
``classi-ics``; its Python modules are imported under ``ics`` (for
example, ``ics.web``). The ETC and pipeline likewise provide the
``classi-etc`` and ``classi-pipeline`` commands.

The ICS can be kept in a separate environment because hardware-control stacks can
have tighter platform and version constraints than the analysis software.

Which package do I need?
------------------------

Use the ETC when you are deciding whether an observation is practical or how
long to expose. Use the simulator when you need a detector-level prediction,
want to exercise the pipeline without real data, or want to study how geometry
changes the recorded traces. Use the pipeline for real or simulated FITS data.
Use the ICS only when controlling the instrument or developing against its mock
backends.

Continue with :doc:`user-guide/index` for the instrument user manual.
