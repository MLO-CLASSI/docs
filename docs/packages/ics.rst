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

The ``[backends]`` section of ``config.ini`` selects ``mock`` or ``alpaca``
implementations for ``tcs`` and ``stage``. The Alpaca clients communicate with
the :doc:`ace-bridge` on the telescope-control-system (TCS) computer; the ICS
host therefore does not install the vendor ACE Connector package or store its
credentials. ``[alpaca]`` configures the bridge host, port, protocol, and
device-number mapping.

The guide-camera backend remains ``mock`` in the current ICS. The bridge now
advertises the guide/acquisition camera as Alpaca Camera 0, but the corresponding
ICS client is not yet implemented.

.. warning::

   The current bridge advertises one Focuser (the telescope focus mechanism) and
   does not yet advertise the X/Y guide stage. The ICS ``alpaca`` stage backend
   expects X, Y, and optionally focus/Z Focuser device numbers. Do not enable it
   until the bridge device mapping and installed hardware have been verified.

The factory layer builds the concrete backend objects from these settings,
which keeps the rest of the application independent of the vendor interface.

Web application
---------------

The Flask application exposes acquisition/status endpoints and the observer UI.
Completed science FITS files can be served to the UI for direct JS9 display.
The current loader explicitly requests the full detector dimensions with no
JS9 display binning, preventing the browser from cropping or resampling the
preview. This keeps the preview faithful to the detector data and permits
normal FITS inspection tools in the browser.

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
``[indi]``, ``[backends]``, and ``[alpaca]`` sections. It is the authoritative
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
