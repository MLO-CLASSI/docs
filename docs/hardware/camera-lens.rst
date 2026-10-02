Camera lens: Canon EF 100mm f/2 USM
===================================

The camera optic is a Canon ``EF 100mm f/2 USM`` prime lens. Its nominal 100 mm
focal length, together with the :doc:`180 mm collimator <collimator>`, sets the
overall magnification. Focus and aperture are electromechanically controlled by
the :doc:`Pinefeat lens controller <lens-controller>`.

.. list-table:: Key catalog properties
   :header-rows: 1
   :widths: 40 60

   * - Property
     - Value
   * - Focal length
     - 100 mm
   * - Maximum aperture
     - f/2
   * - Optical design
     - 8 elements in 6 groups
   * - Mount
     - Canon EF
   * - Focus drive
     - Ultrasonic motor (USM)

This is a photographic lens rather than a purpose-designed spectrograph camera.
Its best focus, usable aperture, chromatic residuals, field dependence, and
line-spread function still need to be characterized in the assembled instrument.
Stopping down can reduce aberrations but also reduces throughput.

Throughput-model limitation
---------------------------

The simulator represents this lens with the shared-data
`Canon EF 85 mm proxy curve`_, not a measurement of the installed 100 mm f/2
lens. Its blue end includes estimated values extending the curve to 360 nm.
Simulator and ETC results in that region should therefore be treated as an
engineering estimate until the installed lens is measured or a more suitable
source curve is adopted.

.. _Canon EF 85 mm proxy curve:
   https://github.com/MLO-CLASSI/shared-data/blob/main/csv_files/LensTip_CanonEF85mm.csv

Vendor resources
----------------

* `Canon support page <https://www.usa.canon.com/support/p/ef-100mm-f-2-usm>`_
* `User manual (PDF) <https://gdlp01.c-wss.com/gds/0/0300003420/02/ef100f2usm-im3-eng.pdf>`_
* `"Canon Camera Museum" spec page <https://global.canon/en/c-museum/product/ef302.html>`_
