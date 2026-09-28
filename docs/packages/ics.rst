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
   cp ics/config.example.ini config.ini
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
implementations for ``tcs`` and ``guide_camera``. The Alpaca clients communicate
with the :doc:`ace-bridge` on the telescope-control-system (TCS) computer; the
ICS host therefore does not install the vendor ACE Connector package or store
its credentials. ``[alpaca]`` configures the bridge host and port, telescope and
camera device numbers, and guide-camera exposure timeout. The connection uses
ordinary HTTP; there is no configurable ``protocol`` option.

The Alpaca acquisition-camera backend starts an exposure, polls ``ImageReady``,
retrieves ``ImageArray``, converts the Alpaca X-major array to NumPy/FITS
``(y, x)`` order, and writes
``previews/latest_guide_preview.fits`` beneath the configured data root.

.. warning::

   The current bridge advertises one Focuser (the telescope focus mechanism) and
   does not advertise the native X/Y guide stage. The ICS currently supports
   only ``stage = mock`` and rejects ``stage = alpaca`` during backend creation.
   The stage should remain on the mock backend until a verified network mapping
   is implemented on both sides.

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
`config.example.ini <https://github.com/MLO-CLASSI/ics/blob/main/config.example.ini>`_
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

Production credentials and secret keys should not be committed.

FITS metadata
-------------

The exposure form records the observer, target, image type, exposure request,
binning, and optional comment. After acquisition, the ICS preserves the
camera-reported exposure time and supplements the raw header with provenance,
instrument configuration, detector state, target and telescope coordinates,
guide/stage state, timing, and file metadata. See
:doc:`../reference/products` for the keyword conventions, including the
distinction between requested and actual exposure time.
