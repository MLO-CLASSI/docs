MLO CLASSI Spectrograph
=======================

This site is the unified user and developer documentation for the software
supporting the MLO CLASSI (Claud Low-resolution Array-fed Small Scale Integral
field) spectrograph. The software is split into focused repositories, but users
should approach the instrument as one system rather than learning each
repository in isolation.

The normal path through the software is:

.. code-block:: text

   target or template spectrum
            |
            v
       Exposure-time calculator
            |
            v
      observing plan / SNR target
            |
       +----+-------------------+
       |                        |
       v                        v
   Simulator               Instrument control
       |                        |
       v                        v
   synthetic FITS          acquired FITS frames
       \                        /
        +----------+-----------+
                   |
                   v
             Reduction pipeline
                   |
                   v
            extracted spectra

Reference throughput curves, detector-response data, atmospheric-extinction
data, and template spectra are shared across packages through the
``classi-shared-data`` distribution where practical.

.. note::

   The majority of the content on this site was machine-generated using GPT-5.6
   based on the contents of the various software repositories.

Start here
----------

* :doc:`getting-started` -- install the software and understand the repository split.
* :doc:`user-guide/index` -- end-to-end guide from planning through extracted spectra.
* :doc:`hardware/index` -- instrument optics, camera, and controllers.
* :doc:`packages/index` -- package-by-package documentation.
* :doc:`reference/conventions` -- units, coordinate, detector, and spectrum conventions.
* :doc:`development` -- how the repositories fit together and how to update these docs.

.. toctree::
   :maxdepth: 2
   :hidden:

   getting-started
   user-guide/index
   hardware/index
   packages/index
   reference/index
   development
