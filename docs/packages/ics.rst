Instrument control system
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
   cp ics/config.ini.example config.ini
   classi-ics

Application modules therefore use imports such as ``ics.web`` and
``ics.devices``; ``src`` is the source directory, not the import namespace.

Backend selection
-----------------

The science camera and camera-lens controller use INDI. The default INDI device
names are ``FLI Aurora`` and ``Pinefeat CEF``; the observer interface can select
different devices discovered on the configured INDI server without restarting
the ICS.

The ``[backends]`` section of ``config.ini`` selects ``mock`` or ``ace``
implementations independently for ``tcs``, ``guide_camera``, and ``stage``.
When the stage backend is ``ace``, the configured X, Y, and optional focus/Z
axis names determine which axes are exposed.

The factory layer builds the concrete backend objects from these settings,
which keeps the rest of the application independent of the vendor interface.

Web application
---------------

The Flask application exposes acquisition/status endpoints and the observer UI.
Completed science FITS files can be served to the UI for direct JS9 display.
This keeps the preview faithful to the detector data and permits normal FITS
inspection tools in the browser.

Configuration
-------------

Copy the repository's
`config.ini.example <https://github.com/MLO-CLASSI/ics/blob/main/config.ini.example>`_
to ``config.ini`` and adjust it for the deployment. ``classi-ics`` reads
``config.ini`` from the current working directory by default;
``create_app(config_path)`` accepts an alternate path for embedded or test
deployments. Relative ``data_root`` paths are resolved relative to the
configuration file rather than the process working directory.

The file groups settings into ``[server]``, ``[instrument]``, ``[js9]``,
``[indi]``, ``[backends]``, and ``[ace]`` sections. It is the authoritative
inventory of supported options and defaults. Instrument geometry and component
names configured there are written into acquired FITS headers, so they must
match the hardware actually in use.

Never commit production credentials or secret keys.

FITS metadata
-------------

The exposure form records the observer, target, image type, exposure request,
binning, and optional comment. After acquisition, the ICS preserves the
camera-reported exposure time and supplements the raw header with provenance,
instrument configuration, detector state, target and telescope coordinates,
guide/stage state, timing, and file metadata. See
:doc:`../reference/products` for the keyword conventions, including the
distinction between requested and actual exposure time.
