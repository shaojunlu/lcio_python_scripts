Examples for generating root histograms using LCIO from python
==============================================================
It distributed under the [LGPLv3 License](http://www.gnu.org/licenses/lgpl-3.0.en.html)

## basic setup
```
source /cvmfs/ilc.desy.de/sw/x86_64_gcc49_sl6/v02-00-02/init_ilcsoft.sh

export PYTHONPATH=/<your_path>/lcio_python_scripts/examples:$PYTHONPATH

alias pylcio='python ${LCIO}/src/python/pylcio.py'

pylcio <steeringFile.xml>
```

## examples of usage
```
mkdir output

cd output

cp -fr /<your_path>/lcio_python_scripts/examples/exampleSteering .

pylcio exampleSteering/TracksPlots.xml
```

## output root file to be checked
```
root EffTrk2D.root
```

---
This is just a backup old scripts.
They (all or parts) may not be maintained in time. 
Please update as you wish.
