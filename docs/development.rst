Development and documentation maintenance
=========================================

Repository boundaries
---------------------

Broadly reusable science logic should remain independent of observatory
hardware. The ETC, simulator, pipeline, and shared-data repositories should
remain usable on a normal scientific Python installation. Hardware-specific
INDI/Alpaca integration belongs in the ICS, while the vendor ACE integration
belongs in the narrowly scoped TCS-side bridge.

Shared data
-----------

When a throughput or reference spectrum is used by more than one package, it
should be moved to ``classi-shared-data`` and the dependent packages updated
together. A scientific discrepancy should not be fixed by editing separate
copies of the same curve in multiple repositories.

Documentation updates
---------------------

Update this site when a change alters any of the following:

* the end-user workflow;
* a public class/function/interface shown in the package pages;
* physical or unit conventions;
* configuration keys used for deployment;
* the meaning or format of a data product; or
* which repository owns a piece of functionality.

Package-internal refactors do not need to be mirrored here unless they affect a
public interface.

Building the docs
-----------------

Run a strict build before merging documentation changes:

.. code-block:: bash

   python -m pip install -r requirements.txt
   make html-strict

GitHub Pages deployment also uses ``-W --keep-going``, so warnings fail CI while
still reporting as many problems as possible in a single run.

Scientific regression tests
---------------------------

The simulator and pipeline repositories provide ``test`` installation extras
and pytest suites. From their common parent directory, a maintainer can install
and run them with:

.. code-block:: bash

   python -m pip install -e "./sim[test]" -e "./pipeline[test]"
   python -m pytest sim/tests
   python -m pytest pipeline/tests

The suites cover physical geometry and rendering, detector noise, WCS
serialization, Level-1 calibration and extraction, FITS output, rebinning, and
the command-line interface. Scientific behavior changes should update or add a
regression fixture rather than relying only on a manual notebook check.

Future API documentation
------------------------

This repository deliberately contains stable, hand-maintained user-facing API
summaries rather than importing all package source trees during every docs
build. Once package public APIs settle, each package can generate detailed
``autodoc``/``autosummary`` reference pages in its own CI and this site can link
to them with Intersphinx.

That approach avoids making the unified documentation deployment depend on
observatory-only drivers, GUI libraries, or every package's complete runtime
environment.
