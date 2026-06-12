.. _installation:

============
Installation
============

Requirements
------------

eRMSF requires:

* Python >= 3.9
* MDAnalysis >= 2.0.0
* NumPy

Installation from PyPI
----------------------

The easiest way to install eRMSF is using ``pip``:

.. code-block:: bash

   pip install ermsfkit

Installation from conda-forge
-----------------------------

eRMSF can also be installed using ``conda`` (when available):

.. code-block:: bash

   conda install -c conda-forge ermsfkit

Installation from Source
------------------------

To install the latest development version from GitHub:

.. code-block:: bash

   git clone https://github.com/pablo-arantes/ermsfkit.git
   cd ermsfkit
   pip install -e .

This installs the package in editable mode, which is useful for development.

Development Installation
------------------------

If you want to contribute to the project, install the development dependencies
as well:

.. code-block:: bash

   git clone https://github.com/pablo-arantes/ermsfkit.git
   cd ermsfkit
   pip install -e ".[test,doc]"

This will install:

* **Testing dependencies**: ``pytest``, ``pytest-xdist``, ``pytest-cov``
* **Documentation dependencies**: ``sphinx``, ``sphinx_rtd_theme``

Verifying Installation
----------------------

After installation, you can verify that eRMSF was installed correctly:

.. code-block:: python

   import eRMSF
   print(eRMSF.__version__)

Running Tests
-------------

To run the test suite:

.. code-block:: bash

   pytest eRMSF/tests/

Or with coverage:

.. code-block:: bash

   pytest --cov=eRMSF eRMSF/tests/
