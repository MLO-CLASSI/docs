Collimator: Thorlabs AC508-180-AB-ML
====================================

The collimating lens is a mounted 2-inch achromatic doublet with a nominal
effective focal length of 180 mm. The ``AB`` antireflection coating is specified
for 400--1100 nm, covering the intended visible and near-infrared spectrograph
band.

.. list-table:: Key catalog properties
   :header-rows: 1
   :widths: 40 60

   * - Property
     - Value
   * - Diameter class
     - 50.8 mm (2 inch)
   * - Effective focal length
     - 180 mm
   * - Lens type
     - Achromatic doublet
   * - Antireflection coating
     - AB, 400--1100 nm
   * - Mechanical format
     - Mounted lens (``-ML``), SM2 thread

Throughput-model limitation
---------------------------

The shared-data `collimator throughput curve`_ includes an estimated 360 nm
point below the manufacturer's 400--1100 nm coating range. Simulator and ETC
predictions below 400 nm should therefore be treated as extrapolations rather
than catalog-validated collimator performance.

.. _collimator throughput curve:
   https://github.com/MLO-CLASSI/shared-data/blob/main/csv_files/ac508-180-ab.csv

Vendor resources
----------------

* `Thorlabs AC508-180-AB-ML product page <https://www.thorlabs.com/item/AC508-180-AB-ML>`_
