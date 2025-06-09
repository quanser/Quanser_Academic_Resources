import numpy as np
from scipy.special import logit, expit
from scipy import ndimage
from abc import ABC,abstractmethod

'''
Finds slices that correspond to over lapping cells of a and b
i,j are the location in a's index-space where b[0,0] is located
i and j must be integers. There are no other restrictions on the values of i and j
'''
def find_overlap(a,b,i,j):
    ma,na = a.shape
    mb,nb = b.shape

    ia = np.int_(np.array([np.clip(i,0,ma),np.clip(i+mb,0,ma)]))
    ja = np.int_(np.array([np.clip(j,0,na),np.clip(j+nb,0,na)]))
    ib = np.int_(ia - i)
    jb = np.int_(ja - j)

    aSlice = (slice(ia[0],ia[1]),slice(ja[0],ja[1]))
    bSlice = (slice(ib[0],ib[1]),slice(jb[0],jb[1]))

    return aSlice,bSlice


def wrap_to_2pi(th):
    return np.mod(np.mod(th,2*np.pi)+2*np.pi,2*np.pi)


"""
Map Coordinates: || Grid Coordinates:
=====================================
^ y              || .----> j
|                || |
| <.             || |
|   \ theta      || v i
|    |           ||
.---------> x    ||
"""
class OccupancyGrid:
    def __init__(self,
        xLength=0,
        yLength=0,
        cellWidth=0,
        sensor=None,
        pPrior=0.5,
        pSatLimit = 0.001,
        useGPU=False
    ):
        self.pPrior = pPrior
        self.pSatLimit = pSatLimit

        if sensor is None:
            self.sensor = OGRPLidarModel(cellWidth,filter=True)
        elif isinstance(sensor,OGSensorModel):
            self.sensor = sensor
        else:
            raise TypeError("Sensor must be an instance of an OGSensorModel derived class")
        self.create_grid(xLength,yLength,cellWidth)

    #region Properties
    # Read-only Properties
    @property
    def m(self):
        return self._m
    @property
    def n(self):
        return self._n
    @property
    def cellWidth(self):
        return self._cellWidth
    @property
    def xLength(self):
        return self._xLength
    @property
    def yLength(self):
        return self._yLength

    # Only update pMap if we need to
    @property
    def pMap(self):
        if self._pMapOutOfDate:
            self._pMap = expit(self.lMap)
            self._pMapOutOfDate = False
        return self._pMap

    # Auto-compute l limits after updating pSatLimit
    @property
    def pSatLimit(self):
        return self._pSatLimit
    @pSatLimit.setter
    def pSatLimit(self,value):
        self._pSatLimit = value
        self._lMin= logit(value)

        self._lMax= logit(1-value)
    @property
    def pPrior(self):
        return self._pPrior
    @pPrior.setter
    def pPrior(self,value):
        self._pPrior = value
        self._lPrior = logit(value)
    @property
    def lPrior(self):
        return self._lPrior
    #endregion

    def create_grid (self,xLength,yLength,cellWidth):
        if xLength<=0 or yLength<=0 or cellWidth<=0:
            raise ValueError("All parameters must be >0")

        self._xLength = xLength
        self._yLength = yLength
        self._cellWidth = cellWidth
        self._m = np.int_(np.ceil(self._yLength/self._cellWidth)+1)
        self._n = np.int_(np.ceil(self._xLength/self._cellWidth)+1)
        self._xOffset = (self._n)*self._cellWidth/2
        self._yOffset = (self._m)*self._cellWidth/2

        self.lMap = np.full(
            shape = (self._m, self._n),
            fill_value = self._lPrior,
            dtype = np.float32)
        self._pMapOutOfDate = True

    def reset(self):
        self.lMap = self.lMap*self._lPrior #XXX incorrect if lPrior not zero

    def update(self, x, y, th, *args,**kwargs):
        if self.sensor is None: return

        # calculate Location of cells to update position offsets
        iy,jx = self.xy_to_ij_rounded(x,y)

        xGrid,yGrid = self.xy_to_grid(x,y)
        xOffset = x-xGrid
        yOffset = y-yGrid

        mPatch,nPatch = self.sensor.patch.shape
        iTop = np.int_(iy - np.round((mPatch-1)/2 + yOffset/self.cellWidth))
        jLeft = np.int_(jx - np.round((nPatch-1)/2 - xOffset/self.cellWidth))

        self.sensor.update_patch(xOffset,yOffset,th,*args,**kwargs)
        lSlice,patchSlice = find_overlap(self.lMap,self.sensor.patch,iTop,jLeft)
        self.lMap[lSlice] = np.clip((self.lMap[lSlice]+self.sensor.patch[patchSlice]),self._lMin,self._lMax)
        #self.lMap[iy,jx] = self._lMax
        #self.lMap[iTop,jLeft] = self._lMax
        self._pMapOutOfDate = True

    #region Coordinate system conversion functions:
    def xy_to_ij(self,x,y):
        i = (self._yOffset-y)/self._cellWidth
        j = (x+self._xOffset)/self._cellWidth
        return i,j

    def xy_to_ij_rounded(self,x,y):
        # Return error if outside grid?
        i,j = self.xy_to_ij(x,y)
        iRounded = np.int_(np.round(i))
        jRounded = np.int_(np.round(j))
        return iRounded,jRounded

    def ij_to_xy(self,i,j):
        x = j*self._cellWidth - self._xOffset
        y = self._yOffset - i*self._cellWidth
        return x,y

    def xy_to_grid(self,x,y):
        i,j = self.xy_to_ij_rounded(x,y)
        return self.ij_to_xy(i,j)
    #endregion
    pass


class RollingOccupancyGrid(OccupancyGrid):
    def __init__(self,
        radius=0,
        cellWidth=0,
        sensor=None,
        pPrior=0.5,
        pSatLimit = 0.001,
        useGPU=False,
    ):
        super().__init__(
            radius*2,
            radius*2,
            cellWidth,
            sensor,
            pPrior,
            pSatLimit,
            useGPU
        )

    def update(self,dx,dy,th,*args,**kwargs):
        i0,j0 = self.xy_to_ij(0,0)
        i1,j1 = self.xy_to_ij(-dx,-dy)
        dj = -dx /self._cellWidth
        di = dy /self._cellWidth

        self.lMap = ndimage.shift(self.lMap,(di,dj),cval=self._lPrior)

        super().update(0,0,th,*args,**kwargs)


'''
Abstract class that OG sensor models are derived from
'''
class OGSensorModel(ABC):
    def __init__(self):
        self.patch = None

    @abstractmethod
    def update_patch(self):
        pass

'''
This is useful for testing and demos, but thats about it
'''
class OGExternalModel(OGSensorModel):
    def __init__(self,m,n):
        super().__init__()

        self.m = m
        self.n = n

        self.patch = np.full(
            shape = (self.m, self.n),
            fill_value=v,
            dtype = np.float32)

    def update_patch(self,patch):
        self.patch = patch


'''
General Lidar sensor model
'''
class OGLidarModel(OGSensorModel):
    def __init__(self,fov,rMax,phiRes,rRes,cellWidth,filter=True):
        super().__init__()

        # Patches and Related Stuff
        self._nPatch = 0

        self._polarPatch = None
        self._mPolarPatch = 0
        self._nPolarPatch = 0

        # Probabilities
        self.pOcc = 0.8
        self.pFree = 0.2
        self.pPrior = 0.5
        self.pSatLimit = 0.001

        self.create_patches(fov,rMax,phiRes,rRes,cellWidth)
        self._precompute_patch_accessories()

    #region Read only Properties
    @property
    def fov(self):
        return self._fov
    @property
    def rMax(self):
        return self._rMax
    @property
    def phiRes(self):
        return self._phiRes
    @property
    def rRes(self):
        return self._rRes
    @property
    def nPatch(self):
        return self._nPatch

    # Probabilities and Related
    @property
    def pPrior(self):
        return self._pPrior
    @pPrior.setter
    def pPrior(self,value):
        self._pPrior = value
        self._lPrior = logit(value)
    @property
    def lPrior(self):
        return self._lPrior
    @property
    def pOcc(self):
        return self._pOcc
    @pOcc.setter
    def pOcc(self,value):
        self._pOcc = value
        self._lOcc = logit(value)
    @property
    def pFree(self):
        return self._pFree
    @pFree.setter
    def pFree(self,value):
        self._pFree = value
        self._lFree = logit(value)
    #endregion

    def create_patches(self,fov,rMax,phiRes,rRes,cellWidth):
        if fov<=0 or rMax<=0 or phiRes<=0 or rRes<=0 or cellWidth<=0:
            raise ValueError("All parameters must be >0")

        self._fov = fov
        self._rMax = rMax
        self._phiRes = phiRes
        self._rRes = rRes
        self._cellWidth = cellWidth

        self._mPolarPatch = np.int_(np.ceil(self._fov/self._phiRes))
        self._nPolarPatch = np.int_(np.ceil(self._rMax/self._rRes))
        self._polarPatch = np.zeros(
            shape = (self._mPolarPatch, self._nPolarPatch),
            dtype = np.float32)
        self._phi = np.linspace(0,self._fov,self._mPolarPatch)

        self._nPatch = np.int_(np.ceil(2*self._rMax/self._cellWidth)+1)
        self.patch = np.zeros(
            shape = (self._nPatch, self._nPatch),
            dtype = np.float32)

    def _precompute_patch_accessories(self):
        cx = (self._nPatch*self._cellWidth)/2
        cy = cx

        x = np.linspace(-cx,cx,self._nPatch)
        y = np.linspace(-cy,cy,self._nPatch)
        self._xv,self._yv = np.meshgrid(x,y)

    def _update_polarPatch(self,r):
        if len(r) != self._mPolarPatch: return
        r = np.int_(np.round(r/self._rRes))

        w = 1
        # XXX This can be parallelized
        for i in range(self._mPolarPatch):
            self._polarPatch[i,:r[i]] = self._lFree
            self._polarPatch[i,r[i]:r[i]+w] = self._lOcc
            self._polarPatch[i,r[i]+w:] = self._lPrior

    def update_patch(self,dx,dy,th,angles,distances):
        xv = self._xv
        yv = self._yv
        self._rPatch = (np.sqrt(np.square(xv)+np.square(yv)))/self._rRes
        self._phiPatch = wrap_to_2pi(np.arctan2(yv,xv)+th)/self._phiRes

        self._update_polarPatch(distances)
        self.patch = ndimage.map_coordinates(self._polarPatch,[self._phiPatch,self._rPatch])


'''
OGLidarModel tuned for the specifics of the RPLidar
this is what will be used for QCar by default
'''
class OGRPLidarModel(OGLidarModel):

    def __init__(self,patchCellWidth,filter=True):
        super().__init__(
            fov=2*np.pi,
            rMax=6,
            phiRes= 1*np.pi/180,
            rRes=0.02,
            cellWidth=patchCellWidth
        )
        self.filter = filter

    def update_patch(self, dx, dy, th, angles, distances):
        if self.filter:
            angles,distances = self.filter_rplidar_data(angles,distances)
        if angles.size == 0: return
        super().update_patch(dx, dy, th, angles, distances)

    def filter_rplidar_data(self,angles,distances):
        # Delete invalid reads
        ids = (distances==0)
        phiMeas = np.delete(angles,ids)
        rMeas = np.delete(distances,ids)
        if phiMeas.size == 0: return phiMeas,rMeas

        # Flip angle direction from CW to CCW and add 90 deg offset
        #phiMeas = wrap_to_2pi(2.5*np.pi-phiMeas)

        # Eliminate duplicate reads and sort
        phiMeas, ids = np.unique(phiMeas,return_index=True)
        rMeas = rMeas[ids]

        # Interpolate distances to regularly spaced angles
        rFiltered = np.interp(
            self._phi,
            phiMeas,
            rMeas,
            period=2*np.pi
        )

        # Find gaps where measurements were missed
        ids = np.diff(phiMeas) > 1.1*self._phiRes
        ids_lb = np.append(ids,False)
        ids_ub = np.append(False,ids)

        # Fill gaps with zeros
        lb = np.int_(np.ceil(phiMeas[ids_lb]/self._phiRes))
        ub = np.int_(np.floor(phiMeas[ids_ub]/self._phiRes))
        for i in range(lb.size):
            rFiltered[lb[i]:ub[i]] = 0

        phiMeasMin = np.int_(np.round(phiMeas[0]/self._phiRes))
        phiMeasMax = np.int_(np.round(phiMeas[-1]/self._phiRes))
        rFiltered[0:phiMeasMin] = 0
        rFiltered[phiMeasMax+1:] = 0

        return self._phi, rFiltered