#include <finufft.h>

#include <complex>
#include <iomanip>
#include <iostream>
#include <vector>
using namespace std;

int main(int argc, char *argv[]) {
  /* 2D demo of computing the *adjoint* of the planned transform, needing the
     guru interface.
     We plan a type 2, and then perform its adjoint (which is a type 1 with the
     opposite isign).
     We call the FINUFFT library from C++,
     using STL double complex vectors, with a math test.
     Computes an identical transform to guru2d1 except using the execute_adjoint
     feature. Barbone and Barnett, June 2025.
     To compile, see README.  Usage: ./guru2d1_adjoint
  */
  int M      = 1e6;  // number of nonuniform points
  int N      = 1e6;  // approximate total number of modes (N1*N2)
  double tol = 1e-6; // desired accuracy
  finufft_opts opts;
  finufft_default_opts(&opts);
  opts.upsampfac = 1.25;
  complex<double> I(0.0, 1.0); // the imaginary unit

  // generate random non-uniform points on (x,y) and complex strengths (c):
  vector<double> x(M), y(M);
  vector<complex<double>> c(M);

  for (int i = 0; i < M; i++) {
    x[i] = M_PI * (2 * (double)rand() / RAND_MAX - 1); // uniform random in [-pi, pi)
    y[i] = M_PI * (2 * (double)rand() / RAND_MAX - 1); // uniform random in [-pi, pi)
    // each component uniform random in [-1,1]
    c[i] =
        2 * ((double)rand() / RAND_MAX - 1) + I * (2 * ((double)rand() / RAND_MAX) - 1);
  }

  // choose numbers of output Fourier coefficients in each dimension
  int N1 = round(2.0 * sqrt(N));
  int N2 = round(N / N1);

  // output array for the Fourier modes
  vector<complex<double>> F(N1 * N2);

  int type = 2, dim = 2, ntrans = 1; // you could also do ntrans>1
  int64_t Ns[] = {N1, N2};           // N1,N2 as 64-bit int array

  // step 1: make a plan... note we choose isign=-1 for this type 2 plan
  finufft_plan plan;
  int ier = finufft_makeplan(type, dim, Ns, -1, ntrans, tol, &plan, NULL);
  // step 2: send in M nonuniform points (just x, y in this case)...
  finufft_setpts(plan, M, &x[0], &y[0], NULL, 0, NULL, NULL, NULL);
  // step 3: do the adjoint of the planned transform. This maps
  // c strength data, to F output, and is identical to the type 1 with isign=+1.
  finufft_execute_adjoint(plan, &c[0], &F[0]);
  // ... you could now send in new points, and/or do transforms or their adjoints.
  // ...
  // step 4: free the memory used by the plan...
  finufft_destroy(plan);

  int k1 = round(0.45 * N1); // check the answer for mode frequency (k1,k2)
  int k2 = round(-0.35 * N2);

  complex<double> Ftest(0, 0);
  for (int j = 0; j < M; j++)
    Ftest += c[j] * exp(I * ((double)k1 * x[j] + (double)k2 * y[j]));

  // compute inf norm of F
  double Fmax = 0.0;
  for (int m = 0; m < N1 * N2; m++) {
    double aF = abs(F[m]);
    if (aF > Fmax) Fmax = aF;
  }

  // indices in output array for this frequency pair (k1,k2)
  int k1out    = k1 + (int)N1 / 2;
  int k2out    = k2 + (int)N2 / 2;
  int indexOut = k1out + k2out * (N1);

  // compute relative error
  double err = abs(F[indexOut] - Ftest) / Fmax;
  cout << "2D adjoint-of-type-2 NUFFT done. ier=" << ier << ", err in F[" << indexOut
       << "] rel to max(F) is " << setprecision(2) << err << endl;
  return ier;
}
