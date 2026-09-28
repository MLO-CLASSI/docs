ACE Alpaca bridge
=================

Purpose
-------

The ACE Alpaca bridge is the compatibility service between the observatory's
ACE telescope-control system and network clients such as the CLASSI ICS. It runs
on the TCS-side computer, where the vendor ACE Connector Python modules are
available, and exposes a fixed set of devices through the standard ASCOM Alpaca
HTTP/JSON protocol.

The ICS uses Alpyca clients and does not import ACE Connector directly. ACE node
names, credentials, and vendor-specific configuration remain on the TCS
computer.

Device mapping
--------------

The bridge advertises:

* Telescope 0 for J2000 position, target, asynchronous slews, and an ``Offset``
  custom action;
* Focuser 0 for the telescope focus mechanism, including position, motion,
  halt, and a ``Home`` custom action; and
* Camera 0 for the CLASSI guide/acquisition camera.

Camera exposures run in a worker thread. The bridge watches the configured ACE
archive directory for the resulting FITS file and returns its pixels through
Alpaca ``ImageArray``. Subframes are not implemented, and the camera-specific
limits and installed sensor geometry still require on-telescope verification.

The ACE ``XYStage`` interface is not advertised because its motion and position
API has not been verified. The ICS therefore implements only the mock stage
backend and rejects ``stage = alpaca``. That setting should remain ``mock``
until a network interface for the native stage is implemented and verified on
both sides.

Installation and configuration
------------------------------

Install the Python requirements in an environment that can import the
vendor-supplied ``ace`` modules, then run ``device/app.py`` on the TCS computer.
The service listens on TCP port 5555 by default and supports standard Alpaca UDP
discovery.

The repository's
`README <https://github.com/MLO-CLASSI/ace-alpaca-bridge/blob/master/README.md>`_
and
`device/config.toml <https://github.com/MLO-CLASSI/ace-alpaca-bridge/blob/master/device/config.toml>`_
are the authoritative setup and configuration references. The repository is
private and these links require MLO-CLASSI access. Installation-specific values
can be placed in ``/alpyca/config.toml`` so credentials and local overrides do
not need to be committed.

Security and protocol boundary
------------------------------

The bridge is intentionally not a generic RPC server. It translates a fixed set
of Alpaca operations into fixed ACE calls; requests cannot provide a Python
expression or arbitrary ACE attribute or method name.

The default deployment uses ordinary HTTP. Restrict it to the observatory or
another trusted private network, and use protected transport if traffic must
cross an untrusted network. Validate the bridge with ASCOM ConformU and verify
real hardware limits before unattended operation.
