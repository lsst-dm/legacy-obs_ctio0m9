import os.path
from lsst.utils import getPackageDir

config.load(os.path.join(getPackageDir("obs_lsst"), "config", "auxTel", "auxTel.py"))

# Configuration for processStarTask

# we currently have no calibration products for this camera, so disable most isr
config.isr.doBias = False
config.isr.doLinearize = False
config.isr.doDark = False
config.isr.doFlat = False
config.isr.doDefect = False
config.isr.doCrosstalk = False
config.isr.doSaturationInterpolation = False

# For all current data the dispersion direction was set to the x direction
config.dispersionDirection = 'x'
