MLO CLASSI Spectrograph
=======================

This site is the documentation home for the MLO CLASSI (Claud Low-resolution
Array-fed Small Scale Integral field) spectrograph. It describes the instrument
as an integrated observing system: its optical and detector hardware, observing
and calibration workflows, data products, control system, exposure-time tools,
simulator, and reduction pipeline.

The :doc:`user-guide/index` is the primary manual for observers and operators.
Hardware and software pages provide deeper reference material, but repository
boundaries do not define the observing workflow.

The normal path through the instrument is:

.. code-block:: text

   target and observing requirements
            |
            v
       Exposure-time calculator
            |
            v
      observing plan / SNR target
            |
            telescope
               |
               v
        fiber input assembly
               |
               v
    collimator -> filter -> grating
               |
               v
       camera lens -> detector
               |
               v
        acquired FITS frames
               |
               v
         reduction pipeline
               |
               v
        calibrated spectra

Reference throughput curves, detector-response data, atmospheric-extinction
data, and template spectra are shared across packages through the
``classi-shared-data`` distribution where practical.

.. note::

   The majority of the content on this site was machine-generated using GPT-5.6
   based on the contents of the various software repositories.

Start here
----------

* :doc:`user-guide/index` -- instrument manual from system overview through data reduction.
* :doc:`user-guide/overview` -- what CLASSI is and how its subsystems fit together.
* :doc:`hardware/index` -- optics, detector, mechanisms, and controllers.
* :doc:`getting-started` -- choose the documentation path for your role and install software if needed.
* :doc:`packages/index` -- package-by-package software reference.
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
