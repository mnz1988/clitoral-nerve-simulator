"""Exact reference solutions used to verify the field solver (checklist step 3.1).

Units: SI (m, S/m, A, V). Geometry as in geometry.py: surface z = 0, tissue z <= 0,
depth d = -z >= 0. All sources sit on the surface and inject current into the tissue.

Formulas (derivations are standard; written here from first principles, not copied):
- Point source I on the surface of a homogeneous half-space of conductivity sigma:
  V = I / (2 pi sigma r).
- Uniform-flux disc of radius a (current density I / (pi a^2)), on its axis at depth d:
  V = I / (pi a^2 sigma) * (sqrt(d^2 + a^2) - d), from integrating the point source over the
  disc.
- Two-layer half-space, top layer thickness h and conductivity s1 over a half-space s2,
  point source I at the surface origin, reflection coefficient k = (s1 - s2) / (s1 + s2)
  (method of images, as in two-layer resistivity sounding; the standard form is in Telford,
  Geldart and Sheriff, Applied Geophysics, 2nd ed., Cambridge University Press, 1990,
  resistivity chapter. Source not opened by us: unverified. The series below was written
  from first principles and is checked against the independent Hankel-transform solution
  in this module, see two_layer_point_hankel):
  top layer (0 <= d <= h):
    V = I / (2 pi s1) * [1 / rho(d) + sum_{n>=1} k^n (1 / rho(2nh - d) + 1 / rho(2nh + d))]
  lower layer (d >= h):
    V = I / (2 pi s1) * (1 + k) * sum_{n>=0} k^n / rho(d + 2nh)
  with rho(D) = sqrt(r^2 + D^2). Continuity of V at d = h follows term by term; far from the
  source V -> I / (2 pi s2 r).
  A uniform-flux disc is the integral of this point solution over the disc; on the axis each
  image term integrates in closed form: mean over the disc of 1 / rho(D) is
  2 (sqrt(a^2 + D^2) - |D|) / a^2.
- Two-layer half-space by Hankel transform (independent of the image series; derivation by
  the step 3.1 verifier, re-derived here): with K = I / (2 pi s1),
    top layer:   V = K int_0^inf [e^(-l d) + B (e^(-l d) + e^(l d))] J0(l r) dl
    lower layer: V = K int_0^inf C e^(-l d) J0(l r) dl
  Continuity of V and of s dV/dd at d = h gives B = k e^(-2lh) / (1 - k e^(-2lh)) and
  C = 1 + B (1 + e^(2lh)). The e^(-l d) term integrates to 1 / rho(d) and is added in closed
  form; the rest decays like e^(-l h) or faster and is integrated numerically. For a
  uniform-flux disc of radius a the source spectrum 1 becomes 2 J1(l a) / (l a).
"""

from __future__ import annotations

import numpy as np
from scipy import integrate, special


def halfspace_point(current: float, sigma: float, r: np.ndarray) -> np.ndarray:
    """Point source on a homogeneous half-space; `r` is the distance to the source (m)."""
    return current / (2 * np.pi * sigma * np.asarray(r, dtype=float))


def halfspace_disc_axis(current: float, radius: float, sigma: float, depth) -> np.ndarray:
    """Uniform-flux disc on a homogeneous half-space, on the disc axis at `depth` (m)."""
    d = np.asarray(depth, dtype=float)
    return current / (np.pi * radius**2 * sigma) * (np.sqrt(d**2 + radius**2) - d)


def _image_weights(sigma1: float, sigma2: float, h: float, tol: float = 1e-13):
    """Image depths offsets and weights for the two-layer point source (see module doc)."""
    k = (sigma1 - sigma2) / (sigma1 + sigma2)
    if k == 0:
        n_max = 1
    else:
        n_max = int(np.ceil(np.log(tol) / np.log(abs(k)))) + 1
    n = np.arange(1, n_max + 1)
    return k, n, k**n


def two_layer_point_kernel(sigma1, sigma2, h, r, depth):
    """Potential per ampere (V/A) of a surface point source on a two-layer half-space.

    `r` is the horizontal distance and `depth` the depth (arrays of equal shape, m).
    """
    r = np.asarray(r, dtype=float)
    d = np.asarray(depth, dtype=float)
    k, n, kn = _image_weights(sigma1, sigma2, h)
    out = np.empty(np.broadcast(r, d).shape)
    rr, dd = np.broadcast_arrays(r, d)
    top = dd <= h
    # top layer
    rt, dt = rr[top][..., None], dd[top][..., None]
    up = 1 / np.sqrt(rt**2 + (2 * n * h - dt) ** 2)
    down = 1 / np.sqrt(rt**2 + (2 * n * h + dt) ** 2)
    s = 1 / np.sqrt(rt[..., 0] ** 2 + dt[..., 0] ** 2) + np.sum(kn * (up + down), axis=-1)
    out[top] = s / (2 * np.pi * sigma1)
    # lower layer
    rb, db = rr[~top][..., None], dd[~top][..., None]
    n0 = np.concatenate([[0], n])
    k0 = np.concatenate([[1.0], kn])
    s = np.sum(k0 / np.sqrt(rb**2 + (db + 2 * n0 * h) ** 2), axis=-1)
    out[~top] = (1 + k) * s / (2 * np.pi * sigma1)
    return out


def two_layer_disc_axis(current, radius, sigma1, sigma2, h, depth) -> np.ndarray:
    """Uniform-flux disc on a two-layer half-space, on the disc axis at `depth` (m)."""
    d = np.atleast_1d(np.asarray(depth, dtype=float))
    a = radius
    k, n, kn = _image_weights(sigma1, sigma2, h)

    def mean_inv(D):  # mean over the disc of 1 / sqrt(rho^2 + D^2)
        D = np.abs(D)
        return 2 * (np.sqrt(a**2 + D**2) - D) / a**2

    out = np.empty_like(d)
    for i, di in enumerate(d):
        if di <= h:
            s = mean_inv(di) + np.sum(kn * (mean_inv(2 * n * h - di) + mean_inv(2 * n * h + di)))
            out[i] = s / (2 * np.pi * sigma1)
        else:
            n0 = np.concatenate([[0], n])
            k0 = np.concatenate([[1.0], kn])
            out[i] = (1 + k) * np.sum(k0 * mean_inv(di + 2 * n0 * h)) / (2 * np.pi * sigma1)
    return current * out


def two_layer_point_hankel(sigma1, sigma2, h, r, depth, disc_radius=None) -> float:
    """Potential per ampere (V/A) of the two-layer problem by Hankel transform (see module doc).

    Point source at the surface origin, or with `disc_radius` a uniform-flux disc centred on
    the origin (then only on the axis, r = 0). Scalar r and depth (m). Slow (adaptive
    quadrature); for checking the image series, not for production use.
    """
    k = (sigma1 - sigma2) / (sigma2 + sigma1)  # same k as above, written apart from it
    r, d = float(r), float(depth)
    if disc_radius is not None and r != 0:
        raise ValueError("the disc form is implemented on the axis only (r = 0)")

    def source(lam):
        if disc_radius is None:
            return 1.0
        x = lam * disc_radius
        return 1.0 if x == 0 else 2 * special.j1(x) / x

    def extra(lam):
        q = k * np.exp(-2 * lam * h)
        if d <= h:  # B (e^(-l d) + e^(l d)), written without growing exponentials
            e = k * (np.exp(-lam * (2 * h + d)) + np.exp(-lam * (2 * h - d)))
        else:  # (C - 1) e^(-l d) = B (1 + e^(2lh)) e^(-l d)
            e = k * (np.exp(-lam * (2 * h + d)) + np.exp(-lam * d))
        return source(lam) * e / (1 - q) * special.j0(lam * r)

    decay = 2 * h - d if d <= h else d  # slowest exponential in `extra`
    lam_max = 40.0 / decay  # e^-40 is below double precision
    val, _ = integrate.quad(extra, 0, lam_max, limit=4000, epsabs=0, epsrel=1e-11)
    if disc_radius is None:
        base = 1 / np.hypot(r, d)
    else:
        base = 2 * (np.sqrt(disc_radius**2 + d**2) - d) / disc_radius**2
    return (base + val) / (2 * np.pi * sigma1)


def disc_quadrature(radius: float, centre=(0.0, 0.0), n_radial: int = 48, n_angle: int = 96):
    """Quadrature points (x, y) and weights (summing to 1) for the mean over a disc.

    Gauss-Legendre in the radius, trapezoid (spectral for periodic integrands) in the angle.
    Accurate when the evaluation point is not close to the disc itself.
    """
    xg, wg = np.polynomial.legendre.leggauss(n_radial)
    s = 0.5 * radius * (xg + 1)
    ws = 0.5 * radius * wg * s
    phi = 2 * np.pi * np.arange(n_angle) / n_angle
    S, P = np.meshgrid(s, phi, indexing="ij")
    W = np.repeat(ws[:, None], n_angle, axis=1) * (2 * np.pi / n_angle)
    W = W / (np.pi * radius**2)
    x = centre[0] + S * np.cos(P)
    y = centre[1] + S * np.sin(P)
    return x.ravel(), y.ravel(), W.ravel()


def disc_potential(points, current, radius, kernel, centre=(0.0, 0.0), **quad) -> np.ndarray:
    """Potential of a uniform-flux disc at `points` (N x 3, m), by quadrature of a point kernel.

    `kernel(r, depth)` is the potential per ampere of a unit surface point source at
    horizontal distance r and depth.
    """
    pts = np.atleast_2d(points)
    qx, qy, qw = disc_quadrature(radius, centre, **quad)
    r = np.hypot(pts[:, 0:1] - qx[None, :], pts[:, 1:2] - qy[None, :])
    depth = np.broadcast_to(-pts[:, 2:3], r.shape)
    return current * np.sum(kernel(r, depth) * qw[None, :], axis=1)


def halfspace_kernel(sigma: float):
    """Point kernel (V/A) for a homogeneous half-space, for use with disc_potential."""
    return lambda r, depth: 1 / (2 * np.pi * sigma * np.sqrt(r**2 + depth**2))


def two_layer_kernel(sigma1: float, sigma2: float, h: float):
    """Point kernel (V/A) for a two-layer half-space, for use with disc_potential."""
    return lambda r, depth: two_layer_point_kernel(sigma1, sigma2, h, r, depth)
