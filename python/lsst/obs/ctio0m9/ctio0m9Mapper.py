#
# LSST Data Management System
# Copyright 2016 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
import lsst.afw.image.utils as afwImageUtils
import lsst.afw.geom as afwGeom
#import lsst.afw.image as afwImage
from lsst.obs.base import CameraMapper, MakeRawVisitInfo
import lsst.pex.policy as pexPolicy

from lsst.obs.ctio0m9 import Ctio0m9

__all__ = ["Ctio0m9Mapper"]

class Ctio0m9MakeRawVisitInfo(MakeRawVisitInfo):
    """functor to make a VisitInfo from the FITS header of a raw image
    """

    def setArgDict(self, md, argDict):
        """Fill an argument dict with arguments for makeVisitInfo and pop associated metadata
        """
        super(Ctio0m9MakeRawVisitInfo, self).setArgDict(md, argDict)

    def getDateAvg(self, md, exposureTime):
        """Return date at the middle of the exposure

        @param[in,out] md  metadata, as an lsst.daf.base.PropertyList or PropertySet;
            items that are used are stripped from the metadata
            (except TIMESYS, because it may apply to more than one other keyword).
        @param[in] exposureTime  exposure time (sec)
        """
        dateObs = self.popIsoDate(md, "DATE-OBS")
        return self.offsetDate(dateObs, 0.5*exposureTime)

class Ctio0m9Mapper(CameraMapper):
    packageName = 'obs_ctio0m9'
    MakeRawVisitInfoClass = Ctio0m9MakeRawVisitInfo

    def __init__(self, inputPolicy=None, **kwargs):
        policyFile = pexPolicy.DefaultPolicyFile(self.packageName, "ctio0m9Mapper.paf", "policy")
        policy = pexPolicy.Policy(policyFile)

        CameraMapper.__init__(self, policy, policyFile.getRepositoryPath(), **kwargs)

        afwImageUtils.defineFilter('NONE', 0.0, alias=['no_filter', "OPEN", "clear"])
        afwImageUtils.defineFilter('Ronchi', 0.0, alias=[])

    def _makeCamera(self, policy, repositoryDir):
        """Make a camera (instance of lsst.afw.cameraGeom.Camera) describing the camera geometry
        """
        return Ctio0m9()

    def _extractDetectorName(self, dataId):
        return 'SITE2K'

    def _computeCcdExposureId(self, dataId):
        """Compute the 64-bit (long) identifier for a CCD exposure.

        @param dataId (dict) Data identifier with visit
        """
        visit = dataId['visit']
        return int(visit)