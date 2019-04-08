
import numpy as np
import scipy as sp
import scipy.stats
import warnings

__version__ = '0.3'

def ctransform(x):

    xi = np.argsort(np.atleast_2d(x))
    xr = np.argsort(xi)
    cx = (xr+1).astype(np.float) / (xr.shape[-1]+1)
    return cx
 

def copnorm(x):

    cx = sp.stats.norm.ppf(ctransform(x))
    return cx


def ent_g(x, biascorrect=True):

    x = np.atleast_2d(x)
    if x.ndim > 2:
        raise ValueError("x must be at most 2d")
    Ntrl = x.shape[1]
    Nvarx = x.shape[0]

    # demean data
    x = x - x.mean(axis=1)[:,np.newaxis]
    # covariance
    C = np.dot(x,x.T) / float(Ntrl - 1)
    chC = np.linalg.cholesky(C)

    # entropy in nats
    HX = np.sum(np.log(np.diagonal(chC))) + 0.5*Nvarx*(np.log(2*np.pi)+1.0)

    ln2 = np.log(2)
    if biascorrect:
        psiterms = sp.special.psi((Ntrl - np.arange(1,Nvarx+1).astype(np.float))/2.0) / 2.0
        dterm = (ln2 - np.log(Ntrl-1.0)) / 2.0
        HX = HX - Nvarx*dterm - psiterms.sum()

    # convert to bits
    return HX / ln2


def mi_gg(x, y, biascorrect=True, demeaned=False):

    x = np.atleast_2d(x)
    y = np.atleast_2d(y)
    if x.ndim > 2 or y.ndim > 2:
        raise ValueError("x and y must be at most 2d")
    Ntrl = x.shape[1]
    Nvarx = x.shape[0]
    Nvary = y.shape[0]
    Nvarxy = Nvarx+Nvary

    if y.shape[1] != Ntrl:
        raise ValueError("number of trials do not match")

    # joint variable
    xy = np.vstack((x,y))
    if not demeaned:
        xy = xy - xy.mean(axis=1)[:,np.newaxis]
    Cxy = np.dot(xy,xy.T) / float(Ntrl - 1)
    # submatrices of joint covariance
    Cx = Cxy[:Nvarx,:Nvarx]
    Cy = Cxy[Nvarx:,Nvarx:]

    chCxy = np.linalg.cholesky(Cxy)
    chCx = np.linalg.cholesky(Cx)
    chCy = np.linalg.cholesky(Cy)

    # entropies in nats
    # normalizations cancel for mutual information
    HX = np.sum(np.log(np.diagonal(chCx))) # + 0.5*Nvarx*(np.log(2*np.pi)+1.0)
    HY = np.sum(np.log(np.diagonal(chCy))) # + 0.5*Nvary*(np.log(2*np.pi)+1.0)
    HXY = np.sum(np.log(np.diagonal(chCxy))) # + 0.5*Nvarxy*(np.log(2*np.pi)+1.0)

    ln2 = np.log(2)
    if biascorrect:
        psiterms = sp.special.psi((Ntrl - np.arange(1,Nvarxy+1)).astype(np.float)/2.0) / 2.0
        dterm = (ln2 - np.log(Ntrl-1.0)) / 2.0
        HX = HX - Nvarx*dterm - psiterms[:Nvarx].sum()
        HY = HY - Nvary*dterm - psiterms[:Nvary].sum()
        HXY = HXY - Nvarxy*dterm - psiterms[:Nvarxy].sum()

    # MI in bits
    I = (HX + HY - HXY) / ln2
    return I


def gcmi_cc(x,y):

    x = np.atleast_2d(x)
    y = np.atleast_2d(y)
    if x.ndim > 2 or y.ndim > 2:
        raise ValueError("x and y must be at most 2d")
    Ntrl = x.shape[1]
    Nvarx = x.shape[0]
    Nvary = y.shape[0]

    if y.shape[1] != Ntrl:
        raise ValueError("number of trials do not match")

    # check for repeated values
    for xi in range(Nvarx):
        if (np.unique(x[xi,:]).size / float(Ntrl)) < 0.9:
            warnings.warn("Input x has more than 10% repeated values")
            break
    for yi in range(Nvary):
        if (np.unique(y[yi,:]).size / float(Ntrl)) < 0.9:
            warnings.warn("Input y has more than 10% repeated values")
            break

    # copula normalization
    cx = copnorm(x)
    cy = copnorm(y)
    # parametric Gaussian MI
    I = mi_gg(cx,cy,True,True)
    return I


def mi_model_gd(x, y, Ym, biascorrect=True, demeaned=False):

    x = np.atleast_2d(x)
    y = np.squeeze(y)
    if x.ndim > 2:
        raise ValueError("x must be at most 2d")
    if y.ndim > 1:
        raise ValueError("only univariate discrete variables supported")
    if not np.issubdtype(y.dtype, np.integer):
        raise ValueError("y should be an integer array")
    if not isinstance(Ym, int):
        raise ValueError("Ym should be an integer")

    Ntrl = x.shape[1]
    Nvarx = x.shape[0]

    if y.size != Ntrl:
        raise ValueError("number of trials do not match")

    if not demeaned:
        x = x - x.mean(axis=1)[:,np.newaxis]

    # class-conditional entropies
    Ntrl_y = np.zeros(Ym)
    Hcond = np.zeros(Ym)
    c = 0.5*(np.log(2.0*np.pi)+1)
    for yi in range(Ym):
        idx = y==yi
        xm = x[:,idx]
        Ntrl_y[yi] = xm.shape[1]
        xm = xm - xm.mean(axis=1)[:,np.newaxis]
        Cm = np.dot(xm,xm.T) / float(Ntrl_y[yi]-1)
        chCm = np.linalg.cholesky(Cm)
        Hcond[yi] = np.sum(np.log(np.diagonal(chCm))) # + c*Nvarx

    # class weights
    w = Ntrl_y / float(Ntrl)

    # unconditional entropy from unconditional Gaussian fit
    Cx = np.dot(x,x.T) / float(Ntrl-1)
    chC = np.linalg.cholesky(Cx)
    Hunc = np.sum(np.log(np.diagonal(chC))) # + c*Nvarx

    ln2 = np.log(2)
    if biascorrect:
        vars = np.arange(1,Nvarx+1)

        psiterms = sp.special.psi((Ntrl - vars).astype(np.float)/2.0) / 2.0
        dterm = (ln2 - np.log(float(Ntrl-1))) / 2.0
        Hunc = Hunc - Nvarx*dterm - psiterms.sum()

        dterm = (ln2 - np.log((Ntrl_y-1).astype(np.float))) / 2.0
        psiterms = np.zeros(Ym)
        for vi in vars:
            idx = Ntrl_y-vi
            psiterms = psiterms + sp.special.psi(idx.astype(np.float)/2.0)
        Hcond = Hcond - Nvarx*dterm - (psiterms/2.0)

    # MI in bits
    I = (Hunc - np.sum(w*Hcond)) / ln2
    return I


def gcmi_model_cd(x,y,Ym):


    x = np.atleast_2d(x)
    y = np.squeeze(y)
    if x.ndim > 2:
        raise ValueError("x must be at most 2d")
    if y.ndim > 1:
        raise ValueError("only univariate discrete variables supported")
    if not np.issubdtype(y.dtype, np.integer):
        raise ValueError("y should be an integer array")
    if not isinstance(Ym, int):
        raise ValueError("Ym should be an integer")

    Ntrl = x.shape[1]
    Nvarx = x.shape[0]

    if y.size != Ntrl:
        raise ValueError("number of trials do not match")

    # check for repeated values
    for xi in range(Nvarx):
        if (np.unique(x[xi,:]).size / float(Ntrl)) < 0.9:
            warnings.warn("Input x has more than 10% repeated values")
            break

    # check values of discrete variable
    if y.min()!=0 or y.max()!=(Ym-1):
        raise ValueError("values of discrete variable y are out of bounds")

    # copula normalization
    cx = copnorm(x)
    # parametric Gaussian MI
    I = mi_model_gd(cx,y,Ym,True,True)
    return I


def mi_mixture_gd(x, y, Ym):

    x = np.atleast_2d(x)
    y = np.squeeze(y)
    if x.ndim > 2:
        raise ValueError("x must be at most 2d")
    if y.ndim > 1:
        raise ValueError("only univariate discrete variables supported")
    if not np.issubdtype(y.dtype, np.integer):
        raise ValueError("y should be an integer array")
    if not isinstance(Ym, int):
        raise ValueError("Ym should be an integer")

    Ntrl = x.shape[1]
    Nvarx = x.shape[0]

    if y.size != Ntrl:
        raise ValueError("number of trials do not match")

    # class-conditional entropies
    Ntrl_y = np.zeros(Ym)
    Hcond = np.zeros(Ym)
    m = np.zeros((Ym,Nvarx))
    w = np.zeros(Ym)
    cc = 0.5*(np.log(2.0*np.pi)+1)
    C = np.zeros((Ym,Nvarx,Nvarx))
    chC = np.zeros((Ym,Nvarx,Nvarx))
    for yi in range(Ym):
        # class conditional data
        idx = y==yi
        xm = x[:,idx]
        # class mean
        m[yi,:] = xm.mean(axis=1)
        Ntrl_y[yi] = xm.shape[1]

        xm = xm - m[yi,:][:,np.newaxis]
        C[yi,:,:] = np.dot(xm,xm.T) / float(Ntrl_y[yi]-1)
        chC[yi,:,:] = np.linalg.cholesky(C[yi,:,:])
        Hcond[yi] = np.sum(np.log(np.diagonal(chC[yi,:,:]))) + cc*Nvarx

    # class weights
    w = Ntrl_y / float(Ntrl)

    D = Nvarx
    Ds = np.sqrt(Nvarx)
    Hmix = 0.0
    for yi in range(Ym):
        Ps = Ds * chC[yi,:,:].T
        thsm = m[yi,:,np.newaxis]
        # unscented points for this class
        usc = np.hstack([thsm + Ps, thsm - Ps])

        # class log-likelihoods at unscented points
        log_lik = np.zeros((Ym,2*Nvarx))
        for mi in range(Ym):
            # demean points
            dx = usc -  m[mi,:,np.newaxis]
            # gaussian likelihood
            log_lik[mi,:] = _norm_innerv(dx, chC[mi,:,:]) - Hcond[mi] + 0.5*Nvarx

        # log mixture likelihood for these unscented points
        # sum over classes, axis=0
        logmixlik = sp.misc.logsumexp(log_lik,axis=0,b=w[:,np.newaxis])

        # add to entropy estimate (sum over unscented points for this class)
        Hmix = Hmix + w[yi]*logmixlik.sum()

    Hmix = -Hmix / (2*D)

    # no bias correct
    I = (Hmix - np.sum(w*Hcond)) / np.log(2.0)
    return I

def _norm_innerv(x, chC):
    """ normalised innervations """
    m = np.linalg.solve(chC,x)
    w = -0.5 * (m * m).sum(axis=0)
    return w


def gcmi_mixture_cd(x,y,Ym):

    x = np.atleast_2d(x)
    y = np.squeeze(y)
    if x.ndim > 2:
        raise ValueError("x must be at most 2d")
    if y.ndim > 1:
        raise ValueError("only univariate discrete variables supported")
    if not np.issubdtype(y.dtype, np.integer):
        raise ValueError("y should be an integer array")
    if not isinstance(Ym, int):
        raise ValueError("Ym should be an integer")

    Ntrl = x.shape[1]
    Nvarx = x.shape[0]

    if y.size != Ntrl:
        raise ValueError("number of trials do not match")

    # check for repeated values
    for xi in range(Nvarx):
        if (np.unique(x[xi,:]).size / float(Ntrl)) < 0.9:
            warnings.warn("Input x has more than 10% repeated values")
            break

    # check values of discrete variable
    if y.min()!=0 or y.max()!=(Ym-1):
        raise ValueError("values of discrete variable y are out of bounds")

    # copula normalise each class
    # shift and rescale to match loc and scale of raw data
    # this provides a robust way to fit the gaussian mixture
    classdat = []
    ydat = []
    for yi in range(Ym):
        # class conditional data
        idx = y==yi
        xm = x[:,idx]
        cxm = copnorm(xm)

        xmmed = np.median(xm,axis=1)[:,np.newaxis]
        # robust measure of s.d. under Gaussian assumption from median absolute deviation
        xmmad = np.median(np.abs(xm - xmmed),axis=1)[:,np.newaxis]
        cxmscaled = cxm * (1.482602218505602*xmmad)
        # robust measure of loc from median
        cxmscaled = cxmscaled + xmmed
        classdat.append(cxmscaled)
        ydat.append(yi*np.ones(xm.shape[1],dtype=np.int))

    cx = np.concatenate(classdat,axis=1) 
    newy = np.concatenate(ydat)
    I = mi_mixture_gd(cx,newy,Ym)
    return I


def cmi_ggg(x, y, z, biascorrect=True, demeaned=False):

    x = np.atleast_2d(x)
    y = np.atleast_2d(y)
    z = np.atleast_2d(z)
    if x.ndim > 2 or y.ndim > 2 or z.ndim > 2:
        raise ValueError("x, y and z must be at most 2d")
    Ntrl = x.shape[1]
    Nvarx = x.shape[0]
    Nvary = y.shape[0]
    Nvarz = z.shape[0]
    Nvaryz = Nvary + Nvarz
    Nvarxy = Nvarx + Nvary
    Nvarxz = Nvarx + Nvarz
    Nvarxyz = Nvarx + Nvaryz

    if y.shape[1] != Ntrl or z.shape[1] != Ntrl:
        raise ValueError("number of trials do not match")

    # joint variable
    xyz = np.vstack((x,y,z))
    if not demeaned:
        xyz = xyz - xyz.mean(axis=1)[:,np.newaxis]
    Cxyz = np.dot(xyz,xyz.T) / float(Ntrl - 1)
    # submatrices of joint covariance
    Cz = Cxyz[Nvarxy:,Nvarxy:]
    Cyz = Cxyz[Nvarx:,Nvarx:]
    Cxz = np.zeros((Nvarxz,Nvarxz))
    Cxz[:Nvarx,:Nvarx] = Cxyz[:Nvarx,:Nvarx]
    Cxz[:Nvarx,Nvarx:] = Cxyz[:Nvarx,Nvarxy:]
    Cxz[Nvarx:,:Nvarx] = Cxyz[Nvarxy:,:Nvarx]
    Cxz[Nvarx:,Nvarx:] = Cxyz[Nvarxy:,Nvarxy:]

    chCz = np.linalg.cholesky(Cz)
    chCxz = np.linalg.cholesky(Cxz)
    chCyz = np.linalg.cholesky(Cyz)
    chCxyz = np.linalg.cholesky(Cxyz)

    # entropies in nats
    # normalizations cancel for cmi
    HZ = np.sum(np.log(np.diagonal(chCz))) # + 0.5*Nvarz*(np.log(2*np.pi)+1.0)
    HXZ = np.sum(np.log(np.diagonal(chCxz))) # + 0.5*Nvarxz*(np.log(2*np.pi)+1.0)
    HYZ = np.sum(np.log(np.diagonal(chCyz))) # + 0.5*Nvaryz*(np.log(2*np.pi)+1.0)
    HXYZ = np.sum(np.log(np.diagonal(chCxyz))) # + 0.5*Nvarxyz*(np.log(2*np.pi)+1.0)

    ln2 = np.log(2)
    if biascorrect:
        psiterms = sp.special.psi((Ntrl - np.arange(1,Nvarxyz+1)).astype(np.float)/2.0) / 2.0
        dterm = (ln2 - np.log(Ntrl-1.0)) / 2.0
        HZ = HZ - Nvarz*dterm - psiterms[:Nvarz].sum()
        HXZ = HXZ - Nvarxz*dterm - psiterms[:Nvarxz].sum()
        HYZ = HYZ - Nvaryz*dterm - psiterms[:Nvaryz].sum()
        HXYZ = HXYZ - Nvarxyz*dterm - psiterms[:Nvarxyz].sum()

    # MI in bits
    I = (HXZ + HYZ - HXYZ - HZ) / ln2
    return I


def gccmi_ccc(x,y,z):

    x = np.atleast_2d(x)
    y = np.atleast_2d(y)
    z = np.atleast_2d(z)
    if x.ndim > 2 or y.ndim > 2 or z.ndim > 2:
        raise ValueError("x, y and z must be at most 2d")

    Ntrl = x.shape[1]
    Nvarx = x.shape[0]
    Nvary = y.shape[0]
    Nvarz = z.shape[0]

    if y.shape[1] != Ntrl or z.shape[1] != Ntrl:
        raise ValueError("number of trials do not match")

    # check for repeated values
    for xi in range(Nvarx):
        if (np.unique(x[xi,:]).size / float(Ntrl)) < 0.9:
            warnings.warn("Input x has more than 10% repeated values")
            break
    for yi in range(Nvary):
        if (np.unique(y[yi,:]).size / float(Ntrl)) < 0.9:
            warnings.warn("Input y has more than 10% repeated values")
            break
    for zi in range(Nvarz):
        if (np.unique(z[zi,:]).size / float(Ntrl)) < 0.9:
            warnings.warn("Input y has more than 10% repeated values")
            break

    # copula normalization
    cx = copnorm(x)
    cy = copnorm(y)
    cz = copnorm(z)
    # parametric Gaussian CMI
    I = cmi_ggg(cx,cy,cz,True,True)
    return I


def gccmi_ccd(x,y,z,Zm):

    x = np.atleast_2d(x)
    y = np.atleast_2d(y)
    if x.ndim > 2 or y.ndim > 2:
        raise ValueError("x and y must be at most 2d")
    if z.ndim > 1:
        raise ValueError("only univariate discrete variables supported")
    if not np.issubdtype(z.dtype, np.integer):
        raise ValueError("z should be an integer array")
    if not isinstance(Zm, int):
        raise ValueError("Zm should be an integer")

    Ntrl = x.shape[1]
    Nvarx = x.shape[0]
    Nvary = y.shape[0]

    if y.shape[1] != Ntrl or z.size != Ntrl:
        raise ValueError("number of trials do not match")

    # check for repeated values
    for xi in range(Nvarx):
        if (np.unique(x[xi,:]).size / float(Ntrl)) < 0.9:
            warnings.warn("Input x has more than 10% repeated values")
            break
    for yi in range(Nvary):
        if (np.unique(y[yi,:]).size / float(Ntrl)) < 0.9:
            warnings.warn("Input y has more than 10% repeated values")
            break

    # check values of discrete variable
    if z.min()!=0 or z.max()!=(Zm-1):
        raise ValueError("values of discrete variable z are out of bounds")

    # calculate gcmi for each z value
    Icond = np.zeros(Zm)
    Pz = np.zeros(Zm)
    cx = []
    cy = []
    for zi in range(Zm):
        idx = z==zi
        thsx = copnorm(x[:,idx])
        thsy = copnorm(y[:,idx])
        Pz[zi] = x.shape[1]
        cx.append(thsx)
        cy.append(thsy)
        Icond[zi] = mi_gg(thsx,thsy,True,True)

    Pz = Pz / float(Ntrl)

    # conditional mutual information
    CMI = np.sum(Pz*Icond)
    I = mi_gg(np.hstack(cx),np.hstack(cy),True,False)
    return (CMI,I)
