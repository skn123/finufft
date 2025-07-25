#include <algorithm>
#include <finufft/fft.h>

using namespace std;

#ifdef FINUFFT_USE_DUCC0
#include "ducc0/fft/fftnd_impl.h"
#endif

template<typename TF> std::vector<int> gridsize_for_fft(const FINUFFT_PLAN_T<TF> &p) {
  // local helper func returns a new int array of length dim, extracted from
  // the finufft plan, that fftw_plan_many_dft needs as its 2nd argument.
  if (p.dim == 1) return {(int)p.nfdim[0]};
  if (p.dim == 2) return {(int)p.nfdim[1], (int)p.nfdim[0]};
  // if (p.dim == 3)
  return {(int)p.nfdim[2], (int)p.nfdim[1], (int)p.nfdim[0]};
}
template std::vector<int> gridsize_for_fft<float>(const FINUFFT_PLAN_T<float> &p);
template std::vector<int> gridsize_for_fft<double>(const FINUFFT_PLAN_T<double> &p);

template<typename TF>
void do_fft(const FINUFFT_PLAN_T<TF> &p, std::complex<TF> *fwBatch, int ntrans_actual,
            bool adjoint) {
#ifdef FINUFFT_USE_DUCC0
  size_t nthreads = min<size_t>(MY_OMP_GET_MAX_THREADS(), p.opts.nthreads);
  const auto ns   = gridsize_for_fft(p);
  vector<size_t> arrdims, axes;
  // ntrans_actual may be smaller than batchSize, which we can use
  // to our advantage with ducc FFT.
  arrdims.push_back(size_t(ntrans_actual));
  arrdims.push_back(size_t(ns[0]));
  axes.push_back(1);
  if (p.dim >= 2) {
    arrdims.push_back(size_t(ns[1]));
    axes.push_back(2);
  }
  if (p.dim >= 3) {
    arrdims.push_back(size_t(ns[2]));
    axes.push_back(3);
  }
  // in DUCC0, "forward=true/false" corresponds to an FFT exponent sign of -/+.
  // Analogous to FFTW, transforms are not normalized in either direction.
  bool forward   = (p.fftSign < 0) != adjoint;
  bool spreading = (p.type == 1) != adjoint;
  ducc0::vfmav<std::complex<TF>> data(fwBatch, arrdims);
#ifdef FINUFFT_NO_DUCC0_TWEAKS
  ducc0::c2c(data, data, axes, forward, TF(1), nthreads);
#else
  /* When spreading, only the low-frequency parts of the output fine grid are
     going to be used, and when interpolating, the high frequency parts of the
     input fine grid are zero by definition. This can be used to reduce the
     total FFT work for 2D and 3D NUFFTs. One of the FFT axes always has to be
     transformed fully (that's why there is no savings for 1D NUFFTs), for the
     second axis we need to do (roughly) a fraction of 1/oversampling_factor
     of all 1D FFTs, and for the last remaining axis the factor is
     1/oversampling_factor^2. */
  if (p.dim == 1)        // 1D: no chance for FFT shortcuts
    ducc0::c2c(data, data, axes, forward, TF(1), nthreads);
  else if (p.dim == 2) { // 2D: do partial FFTs
    if (p.mstu[0] < 2)   // something is weird, do standard FFT
      ducc0::c2c(data, data, axes, forward, TF(1), nthreads);
    else {
      size_t y_lo = size_t((p.mstu[0] + 1) / 2);
      size_t y_hi = size_t(ns[1] - p.mstu[0] / 2);
      // the next line is analogous to the Python statement "sub1 = data[:, :, :y_lo]"
      auto sub1 = ducc0::subarray(data, {{}, {}, {0, y_lo}});
      // the next line is analogous to the Python statement "sub2 = data[:, :, y_hi:]"
      auto sub2 = ducc0::subarray(data, {{}, {}, {y_hi, ducc0::MAXIDX}});
      if (spreading) // spreading, not all parts of the output array are needed
        // do axis 2 in full
        ducc0::c2c(data, data, {2}, forward, TF(1), nthreads);
      // do only parts of axis 1
      ducc0::c2c(sub1, sub1, {1}, forward, TF(1), nthreads);
      ducc0::c2c(sub2, sub2, {1}, forward, TF(1), nthreads);
      if (!spreading) // interpolation, parts of the input array are zero
        // do axis 2 in full
        ducc0::c2c(data, data, {2}, forward, TF(1), nthreads);
    }
  } else {                                  // 3D
    if ((p.mstu[0] < 2) || (p.mstu[1] < 2)) // something is weird, do standard FFT
      ducc0::c2c(data, data, axes, forward, TF(1), nthreads);
    else {
      size_t z_lo = size_t((p.mstu[0] + 1) / 2);
      size_t z_hi = size_t(ns[2] - p.mstu[0] / 2);
      size_t y_lo = size_t((p.mstu[1] + 1) / 2);
      size_t y_hi = size_t(ns[1] - p.mstu[1] / 2);
      auto sub1   = ducc0::subarray(data, {{}, {}, {}, {0, z_lo}});
      auto sub2   = ducc0::subarray(data, {{}, {}, {}, {z_hi, ducc0::MAXIDX}});
      auto sub3   = ducc0::subarray(sub1, {{}, {}, {0, y_lo}, {}});
      auto sub4   = ducc0::subarray(sub1, {{}, {}, {y_hi, ducc0::MAXIDX}, {}});
      auto sub5   = ducc0::subarray(sub2, {{}, {}, {0, y_lo}, {}});
      auto sub6   = ducc0::subarray(sub2, {{}, {}, {y_hi, ducc0::MAXIDX}, {}});
      if (spreading) { // spreading, not all parts of the output array are needed
        // do axis 3 in full
        ducc0::c2c(data, data, {3}, forward, TF(1), nthreads);
        // do only parts of axis 2
        ducc0::c2c(sub1, sub1, {2}, forward, TF(1), nthreads);
        ducc0::c2c(sub2, sub2, {2}, forward, TF(1), nthreads);
      }
      // do even smaller parts of axis 1
      ducc0::c2c(sub3, sub3, {1}, forward, TF(1), nthreads);
      ducc0::c2c(sub4, sub4, {1}, forward, TF(1), nthreads);
      ducc0::c2c(sub5, sub5, {1}, forward, TF(1), nthreads);
      ducc0::c2c(sub6, sub6, {1}, forward, TF(1), nthreads);
      if (!spreading) { // interpolation, parts of the input array are zero
        // do only parts of axis 2
        ducc0::c2c(sub1, sub1, {2}, forward, TF(1), nthreads);
        ducc0::c2c(sub2, sub2, {2}, forward, TF(1), nthreads);
        // do axis 3 in full
        ducc0::c2c(data, data, {3}, forward, TF(1), nthreads);
      }
    }
  }
#endif
#else
  // if thisBatchSize<batchSize it wastes some flops
  if (adjoint)
    p.fftPlan->execute_adjoint(fwBatch);
  else
    p.fftPlan->execute(fwBatch);
#endif
}
template void do_fft<float>(const FINUFFT_PLAN_T<float> &p, std::complex<float> *fwBatch,
                            int ntrans_actual, bool adjoint);
template void do_fft<double>(const FINUFFT_PLAN_T<double> &p,
                             std::complex<double> *fwBatch, int ntrans_actual,
                             bool adjoint);
