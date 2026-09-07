Instrument-control system
=========================

Purpose
-------

The ICS is the web-based control and monitoring layer for the spectrograph. It
keeps acquisition logic separate from the scientific reduction packages and
provides interchangeable hardware backends for development and deployment.

Installation and launch
-----------------------

The distribution is named ``classi-ics``, requires Python 3.11 or newer,
and installs the ``ics`` Python package. From a sibling checkout, install and
launch it with:

.. code-block:: bash

   python -m pip install -e ./ics
   classi-ics

Application modules therefore use imports such as ``ics.web`` and
``ics.devices``; ``src`` is the source directory, not the import namespace.

Backend selection
-----------------

Environment configuration selects the implementations used for each hardware
family.

``ICS_BACKEND_MODE``
   Selects the instrument-side camera/focus implementation. ``mock`` is used for
   development; ``indi`` connects to the INDI server used by the science-camera
   and focus devices.

``ICS_TCS_BACKEND``
   Selects the telescope-control backend.

``ICS_GUIDE_CAMERA_BACKEND``
   Selects the guide-camera backend.

``ICS_STAGE_BACKEND``
   Selects guide-stage motion. ACE-backed stage axes can be configured
   individually so an optional focus/Z axis does not need to exist.

The factory layer builds the concrete backend objects from this configuration,
which keeps the rest of the application independent of the vendor interface.

Web application
---------------

The Flask application exposes acquisition/status endpoints and the observer UI.
Completed science FITS files can be served to the UI for direct JS9 display.
This keeps the preview faithful to the detector data and permits normal FITS
inspection tools in the browser.

Configuration
-------------

Keep deployment-specific device names and ACE/INDI addresses in the environment
rather than source code. A typical environment file defines the local INDI host
and devices plus the ACE node/instrument names for the telescope, guide camera,
and guide-stage axes.

Never commit production credentials or secret keys.
