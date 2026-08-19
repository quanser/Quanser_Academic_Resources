/*
 * CheckInvDiffKin_sf.c
 *
 * Sponsored Third Party Support License -- for use only to support
 * products interfaced to MathWorks software under terms specified in your
 * company's restricted use license agreement.
 *
 * Code generation for model "CheckInvDiffKin_sf".
 *
 * Model version              : 5.4
 * Simulink Coder version : 9.3 (R2020a) 18-Nov-2019
 * C source code generated on : Fri Feb  4 12:47:30 2022
 *
 * Target selection: rtwsfcn.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: Intel->x86-64 (Windows64)
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */

#include <math.h>
#include "CheckInvDiffKin_sf.h"
#include "CheckInvDiffKin_sf_private.h"
#include "simstruc.h"
#include "fixedpoint.h"
#if defined(RT_MALLOC) || defined(MATLAB_MEX_FILE)

extern void *CheckInvDiffKin_malloc(SimStruct *S);

#endif

#ifndef __RTW_UTFREE__
#if defined (MATLAB_MEX_FILE)

extern void * utMalloc(size_t);
extern void utFree(void *);

#endif
#endif                                 /* #ifndef __RTW_UTFREE__ */

/* Forward declaration for local functions */
static void CheckInvDiffKin_rt_invd4x4_snf(const real_T u[16], real_T y[16]);

#if defined(MATLAB_MEX_FILE)
#include "rt_nonfinite.c"
#endif

static const char_T *RT_MEMORY_ALLOCATION_ERROR =
  "memory allocation error in generated S-Function";
static void CheckInvDiffKin_rt_invd4x4_snf(const real_T u[16], real_T y[16])
{
  int8_T p[4];
  real_T A[16];
  int8_T ipiv[4];
  int32_T pipk;
  int32_T jj;
  int32_T jp1j;
  int32_T jBcol;
  int32_T c;
  int32_T ix;
  real_T smax;
  real_T s;
  int32_T iy;
  int32_T jA;
  int32_T ijA;
  for (iy = 0; iy < 16; iy++) {
    y[iy] = 0.0;
    A[iy] = u[iy];
  }

  ipiv[0] = 1;
  ipiv[1] = 2;
  ipiv[2] = 3;
  for (pipk = 0; pipk < 3; pipk++) {
    jBcol = pipk * 5 + 2;
    jj = pipk * 5;
    c = 4 - pipk;
    iy = 1;
    ix = jBcol - 2;
    smax = fabs(A[jj]);
    for (jA = 2; jA <= c; jA++) {
      ix++;
      s = fabs(A[ix]);
      if (s > smax) {
        iy = jA;
        smax = s;
      }
    }

    if (A[(jBcol + iy) - 3] != 0.0) {
      if (iy - 1 != 0) {
        ix = pipk + iy;
        ipiv[pipk] = (int8_T)ix;
        iy = ix - 1;
        smax = A[pipk];
        A[pipk] = A[iy];
        A[iy] = smax;
        ix = pipk + 4;
        iy += 4;
        smax = A[ix];
        A[ix] = A[iy];
        A[iy] = smax;
        ix += 4;
        iy += 4;
        smax = A[ix];
        A[ix] = A[iy];
        A[iy] = smax;
        ix += 4;
        iy += 4;
        smax = A[ix];
        A[ix] = A[iy];
        A[iy] = smax;
      }

      iy = jBcol - pipk;
      for (ix = jBcol; ix <= iy + 2; ix++) {
        A[ix - 1] /= A[jj];
      }
    }

    c = 2 - pipk;
    jA = jj;
    jj += 4;
    for (jp1j = 0; jp1j <= c; jp1j++) {
      if (A[jj] != 0.0) {
        smax = -A[jj];
        ix = jBcol - 1;
        iy = jA - pipk;
        for (ijA = jA + 6; ijA <= iy + 8; ijA++) {
          A[ijA - 1] += A[ix] * smax;
          ix++;
        }
      }

      jj += 4;
      jA += 4;
    }
  }

  p[0] = 1;
  p[1] = 2;
  p[2] = 3;
  p[3] = 4;
  if (ipiv[0] > 1) {
    jBcol = ipiv[0] - 1;
    pipk = p[jBcol];
    p[jBcol] = 1;
    p[0] = (int8_T)pipk;
  }

  if (ipiv[1] > 2) {
    jBcol = ipiv[1] - 1;
    pipk = p[jBcol];
    p[jBcol] = p[1];
    p[1] = (int8_T)pipk;
  }

  if (ipiv[2] > 3) {
    jBcol = ipiv[2] - 1;
    pipk = p[jBcol];
    p[jBcol] = p[2];
    p[2] = (int8_T)pipk;
  }

  jBcol = p[0] - 1;
  y[jBcol << 2] = 1.0;
  for (pipk = 1; pipk < 5; pipk++) {
    iy = jBcol << 2;
    c = (iy + pipk) - 1;
    if (y[c] != 0.0) {
      for (ix = pipk + 1; ix < 5; ix++) {
        jj = (iy + ix) - 1;
        y[jj] -= A[(((pipk - 1) << 2) + ix) - 1] * y[c];
      }
    }
  }

  jBcol = p[1] - 1;
  y[((p[1] - 1) << 2) + 1] = 1.0;
  for (pipk = 2; pipk < 5; pipk++) {
    iy = jBcol << 2;
    c = (iy + pipk) - 1;
    if (y[c] != 0.0) {
      for (ix = pipk + 1; ix < 5; ix++) {
        jj = (iy + ix) - 1;
        y[jj] -= A[(((pipk - 1) << 2) + ix) - 1] * y[c];
      }
    }
  }

  jBcol = p[2] - 1;
  y[((p[2] - 1) << 2) + 2] = 1.0;
  for (pipk = 3; pipk < 5; pipk++) {
    if (y[((jBcol << 2) + pipk) - 1] != 0.0) {
      for (ix = pipk + 1; ix < 5; ix++) {
        jj = jBcol << 2;
        iy = jj + 3;
        y[iy] -= y[(jj + pipk) - 1] * A[((pipk - 1) << 2) + 3];
      }
    }
  }

  y[((p[3] - 1) << 2) + 3] = 1.0;
  for (pipk = 0; pipk < 4; pipk++) {
    jBcol = pipk << 2;
    smax = y[jBcol + 3];
    if (smax != 0.0) {
      y[jBcol + 3] = smax / A[15];
      for (ix = 0; ix < 3; ix++) {
        jj = ix + jBcol;
        y[jj] -= y[jBcol + 3] * A[ix + 12];
      }
    }

    smax = y[jBcol + 2];
    if (smax != 0.0) {
      y[jBcol + 2] = smax / A[10];
      for (ix = 0; ix < 2; ix++) {
        jj = ix + jBcol;
        y[jj] -= y[jBcol + 2] * A[ix + 8];
      }
    }

    smax = y[jBcol + 1];
    if (smax != 0.0) {
      y[jBcol + 1] = smax / A[5];
      for (ix = 0; ix < 1; ix++) {
        y[jBcol] -= y[jBcol + 1] * A[4];
      }
    }

    if (y[jBcol] != 0.0) {
      y[jBcol] /= A[0];
    }
  }
}

/* System initialize for root system: '<Root>' */
#define MDL_INITIALIZE_CONDITIONS

static void mdlInitializeConditions(SimStruct *S)
{
  if (ssIsFirstInitCond(S)) {
    X_CheckInvDiffKin_T *_rtX;
    _rtX = ((X_CheckInvDiffKin_T *) ssGetContStates(S));

    /* InitializeConditions for Integrator: '<S1>/Integrator' */
    if (ssIsFirstInitCond(S)) {
      _rtX->Integrator_CSTATE[0] = 0.0;
      _rtX->Integrator_CSTATE[1] = 0.0;
      _rtX->Integrator_CSTATE[2] = 0.0;
      _rtX->Integrator_CSTATE[3] = 0.0;
    }

    ((int_T *)ssGetDWork(S, 1))[0] = 1;

    /* End of InitializeConditions for Integrator: '<S1>/Integrator' */
  } else {
    X_CheckInvDiffKin_T *_rtX;
    _rtX = ((X_CheckInvDiffKin_T *) ssGetContStates(S));

    /* InitializeConditions for Integrator: '<S1>/Integrator' */
    if (ssIsFirstInitCond(S)) {
      _rtX->Integrator_CSTATE[0] = 0.0;
      _rtX->Integrator_CSTATE[1] = 0.0;
      _rtX->Integrator_CSTATE[2] = 0.0;
      _rtX->Integrator_CSTATE[3] = 0.0;
    }

    ((int_T *)ssGetDWork(S, 1))[0] = 1;

    /* End of InitializeConditions for Integrator: '<S1>/Integrator' */
  }
}

/* Start for root system: '<Root>' */
#define MDL_START

static void mdlStart(SimStruct *S)
{
  /* instance underlying S-Function data */
#if defined(RT_MALLOC) || defined(MATLAB_MEX_FILE)
#  if defined(MATLAB_MEX_FILE)

  /* non-finites */
  rt_InitInfAndNaN(sizeof(real_T));

  /* Check for invalid switching between solver types */
  if (ssIsVariableStepSolver(S)) {
    ssSetErrorStatus(S, "This Simulink Coder generated "
                     "S-Function cannot be used in a simulation with "
                     "a solver type of variable-step "
                     "because this S-Function was created from a model with "
                     "solver type of fixed-step and it has continuous time blocks. "
                     "See the Solver page of the simulation parameters dialog.");
    return;
  }

  if (fabs(ssGetFixedStepSize(S) - 0.002) > mxGetEps()*100*0.002) {
    ssSetErrorStatus(S, "This Simulink Coder generated "
                     "S-Function cannot be used in a simulation with "
                     "the current fixed step size "
                     "because this S-Function was created from a model with "
                     "a fixed step size of 0.002 and had both "
                     "continuous blocks and discrete blocks running at this rate. "
                     "See the Solver page of the simulation parameters dialog.");
    return;
  }

#  endif

  CheckInvDiffKin_malloc(S);
  if (ssGetErrorStatus(S) != (NULL) ) {
    return;
  }

#endif

  {
  }
}

/* Outputs for root system: '<Root>' */
static void mdlOutputs(SimStruct *S, int_T tid)
{
  real_T rtb_J[16];
  real_T rtb_p4_tmp;
  real_T rtb_p4_tmp_0;
  real_T rtb_p4_tmp_1;
  int8_T rtb_p4_tmp_2[4];
  int8_T rtb_p4_tmp_3[4];
  int8_T rtb_p4_tmp_4[16];
  int8_T rtb_p4_tmp_5[16];
  int8_T rtb_p4_tmp_6[16];
  real_T rtb_p4_tmp_7[16];
  real_T rtb_p4_tmp_8[16];
  real_T rtb_p4_tmp_9[16];
  real_T rtb_p4_tmp_a[16];
  real_T rtb_p4_tmp_b[16];
  real_T rtb_p4_tmp_c[16];
  real_T tmp[16];
  real_T tmp_0[16];
  real_T tmp_1[16];
  int32_T i;
  int32_T i_0;
  int32_T rtb_p4_tmp_tmp;
  int32_T rtb_p4_tmp_tmp_tmp;
  int32_T rtb_p4_tmp_tmp_0;
  real_T rtb_p4_tmp_tmp_1;
  real_T rtb_p4_tmp_tmp_2;
  real_T rtb_p4_tmp_tmp_3;
  int32_T tmp_2;
  int32_T tmp_3;
  real_T rtb_p4_tmp_tmp_4;
  real_T rtb_p4_tmp_tmp_5;
  static const int8_T T_T_z[16] = { 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    1 };

  static const real_T c_T_T_z[16] = { 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.14, 1.0 };

  static const real_T b_T_T_x[16] = { 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0, 0.35355339059327373, 0.0, 0.0, 1.0 };

  static const real_T b_T_R_x[16] = { 1.0, 0.0, 0.0, 0.0, 0.0,
    6.123233995736766E-17, -1.0, 0.0, 0.0, 1.0, 6.123233995736766E-17, 0.0, 0.0,
    0.0, 0.0, 1.0 };

  static const real_T b_T_T_z[16] = { 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.4, 1.0 };

  static const int8_T b[4] = { 0, 0, 1, 0 };

  static const int8_T c[4] = { 0, 0, 0, 1 };

  B_CheckInvDiffKin_T *_rtB;
  X_CheckInvDiffKin_T *_rtX;
  _rtX = ((X_CheckInvDiffKin_T *) ssGetContStates(S));
  _rtB = ((B_CheckInvDiffKin_T *) ssGetLocalBlockIO(S));
  if (ssIsContinuousTask(S, tid)) {
    /* Integrator: '<S1>/Integrator' */
    if (((int_T *)ssGetDWork(S, 1))[0] != 0) {
      _rtX->Integrator_CSTATE[0] = *((const real_T **)ssGetInputPortSignalPtrs(S,
        0))[0];
      _rtX->Integrator_CSTATE[1] = *((const real_T **)ssGetInputPortSignalPtrs(S,
        0))[1];
      _rtX->Integrator_CSTATE[2] = *((const real_T **)ssGetInputPortSignalPtrs(S,
        0))[2];
      _rtX->Integrator_CSTATE[3] = *((const real_T **)ssGetInputPortSignalPtrs(S,
        0))[3];
    }

    /* MATLAB Function: '<S1>/forward kinematics1' incorporates:
     *  Integrator: '<S1>/Integrator'
     */
    rtb_p4_tmp = sin(_rtX->Integrator_CSTATE[0]);
    rtb_p4_tmp_0 = cos(_rtX->Integrator_CSTATE[0]);
    rtb_p4_tmp_1 = sin((_rtX->Integrator_CSTATE[1] + 0.14189705460416394) -
                       1.5707963267948966);
    rtb_p4_tmp_tmp_1 = cos((_rtX->Integrator_CSTATE[1] + 0.14189705460416394) -
      1.5707963267948966);

    /* Outport: '<Root>/Phi (rad) [4]' incorporates:
     *  Integrator: '<S1>/Integrator'
     */
    ((real_T *)ssGetOutputPortSignal(S, 0))[0] = _rtX->Integrator_CSTATE[0];

    /* MATLAB Function: '<S1>/forward kinematics1' */
    rtb_p4_tmp_2[0] = 0;
    rtb_p4_tmp_3[0] = 0;

    /* Outport: '<Root>/Phi (rad) [4]' incorporates:
     *  Integrator: '<S1>/Integrator'
     */
    ((real_T *)ssGetOutputPortSignal(S, 0))[1] = _rtX->Integrator_CSTATE[1];

    /* MATLAB Function: '<S1>/forward kinematics1' */
    rtb_p4_tmp_2[1] = 0;
    rtb_p4_tmp_3[1] = 0;

    /* Outport: '<Root>/Phi (rad) [4]' incorporates:
     *  Integrator: '<S1>/Integrator'
     */
    ((real_T *)ssGetOutputPortSignal(S, 0))[2] = _rtX->Integrator_CSTATE[2];

    /* MATLAB Function: '<S1>/forward kinematics1' */
    rtb_p4_tmp_2[2] = 1;
    rtb_p4_tmp_3[2] = 0;

    /* Outport: '<Root>/Phi (rad) [4]' incorporates:
     *  Integrator: '<S1>/Integrator'
     */
    ((real_T *)ssGetOutputPortSignal(S, 0))[3] = _rtX->Integrator_CSTATE[3];

    /* MATLAB Function: '<S1>/forward kinematics1' incorporates:
     *  Integrator: '<S1>/Integrator'
     */
    rtb_p4_tmp_2[3] = 0;
    rtb_p4_tmp_3[3] = 1;
    rtb_p4_tmp_tmp_3 = sin(_rtX->Integrator_CSTATE[2] - 0.14189705460416394);
    rtb_p4_tmp_tmp_2 = cos(_rtX->Integrator_CSTATE[2] - 0.14189705460416394);
    rtb_p4_tmp_tmp_5 = sin(_rtX->Integrator_CSTATE[3]);
    rtb_p4_tmp_tmp_4 = cos(_rtX->Integrator_CSTATE[3]);
    for (i = 0; i < 16; i++) {
      rtb_p4_tmp_4[i] = T_T_z[i];
      rtb_p4_tmp_5[i] = T_T_z[i];
      rtb_p4_tmp_6[i] = T_T_z[i];
    }

    rtb_p4_tmp_7[0] = rtb_p4_tmp_0;
    rtb_p4_tmp_7[4] = -rtb_p4_tmp;
    rtb_p4_tmp_7[8] = 0.0;
    rtb_p4_tmp_7[12] = 0.0;
    rtb_p4_tmp_7[1] = rtb_p4_tmp;
    rtb_p4_tmp_7[5] = rtb_p4_tmp_0;
    rtb_p4_tmp_7[9] = 0.0;
    rtb_p4_tmp_7[13] = 0.0;
    rtb_p4_tmp_7[2] = 0.0;
    rtb_p4_tmp_7[3] = 0.0;
    rtb_p4_tmp_7[6] = 0.0;
    rtb_p4_tmp_7[7] = 0.0;
    rtb_p4_tmp_7[10] = 1.0;
    rtb_p4_tmp_7[11] = 0.0;
    rtb_p4_tmp_7[14] = 0.0;
    rtb_p4_tmp_7[15] = 1.0;
    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += c_T_T_z[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_7[i];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += c_T_T_z[rtb_p4_tmp_tmp_tmp + 1] *
          rtb_p4_tmp_7[i + 4];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += c_T_T_z[rtb_p4_tmp_tmp_tmp + 2] *
          rtb_p4_tmp_7[i + 8];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += c_T_T_z[rtb_p4_tmp_tmp_tmp + 3] *
          rtb_p4_tmp_7[i + 12];
      }

      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_5[rtb_p4_tmp_tmp_tmp]
          * rtb_p4_tmp_8[i];
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_5[rtb_p4_tmp_tmp_tmp
          + 1] * rtb_p4_tmp_8[i + 4];
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_5[rtb_p4_tmp_tmp_tmp
          + 2] * rtb_p4_tmp_8[i + 8];
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_5[rtb_p4_tmp_tmp_tmp
          + 3] * rtb_p4_tmp_8[i + 12];
      }
    }

    rtb_p4_tmp_7[0] = rtb_p4_tmp_tmp_1;
    rtb_p4_tmp_7[4] = -rtb_p4_tmp_1;
    rtb_p4_tmp_7[8] = 0.0;
    rtb_p4_tmp_7[12] = 0.0;
    rtb_p4_tmp_7[1] = rtb_p4_tmp_1;
    rtb_p4_tmp_7[5] = rtb_p4_tmp_tmp_1;
    rtb_p4_tmp_7[9] = 0.0;
    rtb_p4_tmp_7[13] = 0.0;
    rtb_p4_tmp_7[2] = 0.0;
    rtb_p4_tmp_7[3] = 0.0;
    rtb_p4_tmp_7[6] = 0.0;
    rtb_p4_tmp_7[7] = 0.0;
    rtb_p4_tmp_7[10] = 1.0;
    rtb_p4_tmp_7[11] = 0.0;
    rtb_p4_tmp_7[14] = 0.0;
    rtb_p4_tmp_7[15] = 1.0;
    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp]
          * rtb_p4_tmp_7[i];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp
          + 1] * rtb_p4_tmp_7[i + 4];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp
          + 2] * rtb_p4_tmp_7[i + 8];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp
          + 3] * rtb_p4_tmp_7[i + 12];
      }

      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += b_T_T_x[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_8[i];
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += b_T_T_x[rtb_p4_tmp_tmp_tmp + 1] *
          rtb_p4_tmp_8[i + 4];
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += b_T_T_x[rtb_p4_tmp_tmp_tmp + 2] *
          rtb_p4_tmp_8[i + 8];
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += b_T_T_x[rtb_p4_tmp_tmp_tmp + 3] *
          rtb_p4_tmp_8[i + 12];
      }
    }

    rtb_p4_tmp_b[0] = rtb_p4_tmp_tmp_2;
    rtb_p4_tmp_b[4] = -rtb_p4_tmp_tmp_3;
    rtb_p4_tmp_b[8] = 0.0;
    rtb_p4_tmp_b[12] = 0.0;
    rtb_p4_tmp_b[1] = rtb_p4_tmp_tmp_3;
    rtb_p4_tmp_b[5] = rtb_p4_tmp_tmp_2;
    rtb_p4_tmp_b[9] = 0.0;
    rtb_p4_tmp_b[13] = 0.0;
    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_9[i];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_6[rtb_p4_tmp_tmp_tmp]
          * rtb_p4_tmp_a[i];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 1;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_9[i + 4];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_6[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_a[i + 4];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 2;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_9[i + 8];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_6[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_a[i + 8];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 3;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_9[i + 12];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_6[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_a[i + 12];
      }

      rtb_p4_tmp_tmp = i << 2;
      rtb_p4_tmp_b[rtb_p4_tmp_tmp + 2] = rtb_p4_tmp_2[i];
      rtb_p4_tmp_b[rtb_p4_tmp_tmp + 3] = rtb_p4_tmp_3[i];
    }

    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp]
          * rtb_p4_tmp_b[i];
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp
          + 1] * rtb_p4_tmp_b[i + 4];
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp
          + 2] * rtb_p4_tmp_b[i + 8];
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp
          + 3] * rtb_p4_tmp_b[i + 12];
      }

      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp]
          * rtb_p4_tmp_9[i];
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp
          + 1] * rtb_p4_tmp_9[i + 4];
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp
          + 2] * rtb_p4_tmp_9[i + 8];
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_4[rtb_p4_tmp_tmp_tmp
          + 3] * rtb_p4_tmp_9[i + 12];
      }
    }

    rtb_p4_tmp_c[0] = rtb_p4_tmp_tmp_4;
    rtb_p4_tmp_c[4] = -rtb_p4_tmp_tmp_5;
    rtb_p4_tmp_c[8] = 0.0;
    rtb_p4_tmp_c[12] = 0.0;
    rtb_p4_tmp_c[1] = rtb_p4_tmp_tmp_5;
    rtb_p4_tmp_c[5] = rtb_p4_tmp_tmp_4;
    rtb_p4_tmp_c[9] = 0.0;
    rtb_p4_tmp_c[13] = 0.0;
    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += rtb_p4_tmp_8[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_7[i];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_a[i];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 1;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += rtb_p4_tmp_8[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_7[i + 4];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_a[i + 4];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 2;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += rtb_p4_tmp_8[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_7[i + 8];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_a[i + 8];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 3;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += rtb_p4_tmp_8[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_7[i + 12];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_a[i + 12];
      }

      rtb_p4_tmp_tmp = i << 2;
      rtb_p4_tmp_c[rtb_p4_tmp_tmp + 2] = rtb_p4_tmp_2[i];
      rtb_p4_tmp_c[rtb_p4_tmp_tmp + 3] = rtb_p4_tmp_3[i];
    }

    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += b_T_T_z[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_c[i];
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += b_T_T_z[rtb_p4_tmp_tmp_tmp + 1] *
          rtb_p4_tmp_c[i + 4];
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += b_T_T_z[rtb_p4_tmp_tmp_tmp + 2] *
          rtb_p4_tmp_c[i + 8];
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += b_T_T_z[rtb_p4_tmp_tmp_tmp + 3] *
          rtb_p4_tmp_c[i + 12];
      }

      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_5[rtb_p4_tmp_tmp_tmp]
          * rtb_p4_tmp_7[i];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_5[rtb_p4_tmp_tmp_tmp
          + 1] * rtb_p4_tmp_7[i + 4];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_5[rtb_p4_tmp_tmp_tmp
          + 2] * rtb_p4_tmp_7[i + 8];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_5[rtb_p4_tmp_tmp_tmp
          + 3] * rtb_p4_tmp_7[i + 12];
      }
    }

    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i << 2;
        rtb_p4_tmp_tmp = i_0 + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += rtb_p4_tmp_b[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_9[i_0];
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_6[rtb_p4_tmp_tmp_tmp]
          * rtb_p4_tmp_8[i_0];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 1;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += rtb_p4_tmp_b[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_9[i_0 + 4];
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_6[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_8[i_0 + 4];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 2;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += rtb_p4_tmp_b[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_9[i_0 + 8];
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_6[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_8[i_0 + 8];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 3;
        rtb_p4_tmp_7[rtb_p4_tmp_tmp] += rtb_p4_tmp_b[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_9[i_0 + 12];
        rtb_p4_tmp_a[rtb_p4_tmp_tmp] += (real_T)rtb_p4_tmp_6[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_8[i_0 + 12];
      }
    }

    rtb_p4_tmp = cos(_rtX->Integrator_CSTATE[0]);
    rtb_p4_tmp_9[0] = rtb_p4_tmp;
    rtb_p4_tmp_0 = sin(_rtX->Integrator_CSTATE[0]);
    rtb_p4_tmp_9[4] = -rtb_p4_tmp_0;
    rtb_p4_tmp_9[8] = 0.0;
    rtb_p4_tmp_9[12] = 0.0;
    rtb_p4_tmp_9[1] = rtb_p4_tmp_0;
    rtb_p4_tmp_9[5] = rtb_p4_tmp;
    rtb_p4_tmp_9[9] = 0.0;
    rtb_p4_tmp_9[13] = 0.0;
    rtb_p4_tmp_9[2] = 0.0;
    rtb_p4_tmp_9[3] = 0.0;
    rtb_p4_tmp_9[6] = 0.0;
    rtb_p4_tmp_9[7] = 0.0;
    rtb_p4_tmp_9[10] = 1.0;
    rtb_p4_tmp_9[11] = 0.0;
    rtb_p4_tmp_9[14] = 0.0;
    rtb_p4_tmp_9[15] = 1.0;
    tmp[0] = rtb_p4_tmp_tmp_1;
    rtb_p4_tmp = sin((_rtX->Integrator_CSTATE[1] + 0.14189705460416394) -
                     1.5707963267948966);
    tmp[4] = -rtb_p4_tmp;
    tmp[8] = 0.0;
    tmp[12] = 0.0;
    tmp[1] = rtb_p4_tmp;
    tmp[5] = rtb_p4_tmp_tmp_1;
    tmp[9] = 0.0;
    tmp[13] = 0.0;
    tmp[2] = 0.0;
    tmp[3] = 0.0;
    tmp[6] = 0.0;
    tmp[7] = 0.0;
    tmp[10] = 1.0;
    tmp[11] = 0.0;
    tmp[14] = 0.0;
    tmp[15] = 1.0;
    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i << 2;
        rtb_p4_tmp_tmp = i_0 + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += rtb_p4_tmp_a[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_7[i_0];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += rtb_p4_tmp_a[rtb_p4_tmp_tmp_tmp + 1] *
          rtb_p4_tmp_7[i_0 + 4];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += rtb_p4_tmp_a[rtb_p4_tmp_tmp_tmp + 2] *
          rtb_p4_tmp_7[i_0 + 8];
        rtb_p4_tmp_8[rtb_p4_tmp_tmp] += rtb_p4_tmp_a[rtb_p4_tmp_tmp_tmp + 3] *
          rtb_p4_tmp_7[i_0 + 12];
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += c_T_T_z[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_9[i];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += c_T_T_z[rtb_p4_tmp_tmp_tmp + 1] *
          rtb_p4_tmp_9[i + 4];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += c_T_T_z[rtb_p4_tmp_tmp_tmp + 2] *
          rtb_p4_tmp_9[i + 8];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += c_T_T_z[rtb_p4_tmp_tmp_tmp + 3] *
          rtb_p4_tmp_9[i + 12];
      }

      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_b[i];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 1;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_b[i + 4];
        tmp_2 = rtb_p4_tmp_tmp_tmp + 2;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += (real_T)T_T_z[tmp_2] * rtb_p4_tmp_b[i +
          8];
        tmp_3 = rtb_p4_tmp_tmp_tmp + 3;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += (real_T)T_T_z[tmp_3] * rtb_p4_tmp_b[i +
          12];
        tmp_0[rtb_p4_tmp_tmp] = 0.0;
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp] * tmp[i];
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_0] * tmp[i + 4];
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[tmp_2] * tmp[i + 8];
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[tmp_3] * tmp[i + 12];
      }

      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        tmp_1[rtb_p4_tmp_tmp] = 0.0;
        tmp_1[rtb_p4_tmp_tmp] += b_T_T_x[rtb_p4_tmp_tmp_tmp] * tmp_0[i];
        tmp_1[rtb_p4_tmp_tmp] += b_T_T_x[rtb_p4_tmp_tmp_tmp + 1] * tmp_0[i + 4];
        tmp_1[rtb_p4_tmp_tmp] += b_T_T_x[rtb_p4_tmp_tmp_tmp + 2] * tmp_0[i + 8];
        tmp_1[rtb_p4_tmp_tmp] += b_T_T_x[rtb_p4_tmp_tmp_tmp + 3] * tmp_0[i + 12];
      }
    }

    tmp[0] = rtb_p4_tmp_tmp_2;
    tmp[4] = -sin(_rtX->Integrator_CSTATE[2] - 0.14189705460416394);
    tmp[8] = 0.0;
    tmp[12] = 0.0;
    tmp[1] = rtb_p4_tmp_tmp_3;
    tmp[5] = rtb_p4_tmp_tmp_2;
    tmp[9] = 0.0;
    tmp[13] = 0.0;
    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_c[i];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp] *
          tmp_1[i];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 1;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_c[i + 4];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_0] *
          tmp_1[i + 4];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 2;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_c[i + 8];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_0] *
          tmp_1[i + 8];
        rtb_p4_tmp_tmp_tmp += 3;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_c[i + 12];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp] *
          tmp_1[i + 12];
      }

      i_0 = i << 2;
      tmp[i_0 + 2] = b[i];
      tmp[i_0 + 3] = c[i];
    }

    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp] *
          tmp[i];
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp + 1] *
          tmp[i + 4];
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp + 2] *
          tmp[i + 8];
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp + 3] *
          tmp[i + 12];
      }

      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        tmp_0[rtb_p4_tmp_tmp] = 0.0;
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_c[i];
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp + 1] *
          rtb_p4_tmp_c[i + 4];
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp + 2] *
          rtb_p4_tmp_c[i + 8];
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp + 3] *
          rtb_p4_tmp_c[i + 12];
      }
    }

    tmp_1[0] = rtb_p4_tmp_tmp_4;
    tmp_1[4] = -sin(_rtX->Integrator_CSTATE[3]);
    tmp_1[8] = 0.0;
    tmp_1[12] = 0.0;
    tmp_1[1] = rtb_p4_tmp_tmp_5;
    tmp_1[5] = rtb_p4_tmp_tmp_4;
    tmp_1[9] = 0.0;
    tmp_1[13] = 0.0;
    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] = 0.0;
        tmp[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += rtb_p4_tmp_b[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_9[i];
        tmp[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_tmp] * tmp_0[i];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 1;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += rtb_p4_tmp_b[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_9[i + 4];
        tmp[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_0] * tmp_0[i + 4];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 2;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += rtb_p4_tmp_b[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_9[i + 8];
        tmp[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_0] * tmp_0[i + 8];
        rtb_p4_tmp_tmp_tmp += 3;
        rtb_p4_tmp_c[rtb_p4_tmp_tmp] += rtb_p4_tmp_b[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_9[i + 12];
        tmp[rtb_p4_tmp_tmp] += b_T_R_x[rtb_p4_tmp_tmp_tmp] * tmp_0[i + 12];
      }

      i_0 = i << 2;
      tmp_1[i_0 + 2] = b[i];
      tmp_1[i_0 + 3] = c[i];
    }

    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += b_T_T_z[rtb_p4_tmp_tmp_tmp] * tmp_1[i];
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += b_T_T_z[rtb_p4_tmp_tmp_tmp + 1] *
          tmp_1[i + 4];
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += b_T_T_z[rtb_p4_tmp_tmp_tmp + 2] *
          tmp_1[i + 8];
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += b_T_T_z[rtb_p4_tmp_tmp_tmp + 3] *
          tmp_1[i + 12];
      }

      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i_0 << 2;
        rtb_p4_tmp_tmp = i + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_9[i];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp + 1] *
          rtb_p4_tmp_9[i + 4];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp + 2] *
          rtb_p4_tmp_9[i + 8];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp + 3] *
          rtb_p4_tmp_9[i + 12];
      }
    }

    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i << 2;
        rtb_p4_tmp_tmp = i_0 + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] = 0.0;
        tmp_0[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += tmp[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_c[i_0];
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_b[i_0];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 1;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += tmp[rtb_p4_tmp_tmp_0] * rtb_p4_tmp_c[i_0
          + 4];
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_b[i_0 + 4];
        rtb_p4_tmp_tmp_0 = rtb_p4_tmp_tmp_tmp + 2;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += tmp[rtb_p4_tmp_tmp_0] * rtb_p4_tmp_c[i_0
          + 8];
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_0] *
          rtb_p4_tmp_b[i_0 + 8];
        rtb_p4_tmp_tmp_tmp += 3;
        rtb_p4_tmp_9[rtb_p4_tmp_tmp] += tmp[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_c[i_0 + 12];
        tmp_0[rtb_p4_tmp_tmp] += (real_T)T_T_z[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_b[i_0 + 12];
      }
    }

    for (i = 0; i < 4; i++) {
      for (i_0 = 0; i_0 < 4; i_0++) {
        rtb_p4_tmp_tmp_tmp = i << 2;
        rtb_p4_tmp_tmp = i_0 + rtb_p4_tmp_tmp_tmp;
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] = 0.0;
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += tmp_0[rtb_p4_tmp_tmp_tmp] *
          rtb_p4_tmp_9[i_0];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += tmp_0[rtb_p4_tmp_tmp_tmp + 1] *
          rtb_p4_tmp_9[i_0 + 4];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += tmp_0[rtb_p4_tmp_tmp_tmp + 2] *
          rtb_p4_tmp_9[i_0 + 8];
        rtb_p4_tmp_b[rtb_p4_tmp_tmp] += tmp_0[rtb_p4_tmp_tmp_tmp + 3] *
          rtb_p4_tmp_9[i_0 + 12];
      }
    }

    /* MATLAB Function: '<S1>/differential kinematics' */
    rtb_p4_tmp = sin(*((const real_T **)ssGetInputPortSignalPtrs(S, 0))[0]);
    rtb_p4_tmp_0 = cos((*((const real_T **)ssGetInputPortSignalPtrs(S, 0))[1] +
                        0.14189705460416394) - 1.5707963267948966);
    rtb_p4_tmp_tmp_1 = ((*((const real_T **)ssGetInputPortSignalPtrs(S, 0))[1] +
                         0.14189705460416394) - 1.5707963267948966) + (*((const
      real_T **)ssGetInputPortSignalPtrs(S, 0))[2] - 0.14189705460416394);
    rtb_p4_tmp_1 = sin(rtb_p4_tmp_tmp_1);
    rtb_J[0] = -0.35355339059327373 * rtb_p4_tmp * rtb_p4_tmp_0 + 0.4 *
      rtb_p4_tmp * rtb_p4_tmp_1;
    rtb_p4_tmp_tmp_3 = cos(*((const real_T **)ssGetInputPortSignalPtrs(S, 0))[0]);
    rtb_p4_tmp_tmp_1 = cos(rtb_p4_tmp_tmp_1);
    rtb_p4_tmp_tmp_2 = sin((*((const real_T **)ssGetInputPortSignalPtrs(S, 0))[1]
      + 0.14189705460416394) - 1.5707963267948966);
    rtb_J[4] = -0.35355339059327373 * rtb_p4_tmp_tmp_3 * rtb_p4_tmp_tmp_2 - 0.4 *
      rtb_p4_tmp_tmp_3 * rtb_p4_tmp_tmp_1;
    rtb_J[8] = -0.4 * rtb_p4_tmp_tmp_3 * rtb_p4_tmp_tmp_1;
    rtb_J[12] = 0.0;
    rtb_J[1] = 0.35355339059327373 * rtb_p4_tmp_tmp_3 * rtb_p4_tmp_0 - 0.4 * cos
      (*((const real_T **)ssGetInputPortSignalPtrs(S, 0))[0]) * rtb_p4_tmp_1;
    rtb_J[5] = -0.35355339059327373 * sin(*((const real_T **)
      ssGetInputPortSignalPtrs(S, 0))[0]) * rtb_p4_tmp_tmp_2 - 0.4 * sin(*((
      const real_T **)ssGetInputPortSignalPtrs(S, 0))[0]) * rtb_p4_tmp_tmp_1;
    rtb_J[9] = -0.4 * rtb_p4_tmp * rtb_p4_tmp_tmp_1;
    rtb_J[13] = 0.0;
    rtb_J[2] = 0.0;
    rtb_J[6] = -0.35355339059327373 * rtb_p4_tmp_0 + 0.4 * rtb_p4_tmp_1;
    rtb_J[10] = sin(((*((const real_T **)ssGetInputPortSignalPtrs(S, 0))[1] +
                      0.14189705460416394) - 1.5707963267948966) + (*((const
      real_T **)ssGetInputPortSignalPtrs(S, 0))[2] - 0.14189705460416394)) * 0.4;
    rtb_J[14] = 0.0;
    rtb_J[3] = 0.0;
    rtb_J[7] = 0.0;
    rtb_J[11] = 0.0;
    rtb_J[15] = 1.0;

    /* Product: '<S1>/MatrixMultiply' */
    CheckInvDiffKin_rt_invd4x4_snf(rtb_J, rtb_p4_tmp_9);

    /* Outport: '<Root>/Motor Enable' incorporates:
     *  Constant: '<S2>/Constant'
     *  Constant: '<S3>/Constant'
     *  Constant: '<S4>/Constant'
     *  DotProduct: '<S10>/Dot Product'
     *  DotProduct: '<S9>/Dot Product'
     *  Logic: '<S1>/OR2'
     *  MATLAB Function: '<S1>/forward kinematics1'
     *  RelationalOperator: '<S2>/Compare'
     *  RelationalOperator: '<S3>/Compare'
     *  RelationalOperator: '<S4>/Compare'
     *  Sqrt: '<S5>/Sqrt'
     *  Sqrt: '<S6>/Sqrt'
     */
    ((boolean_T *)ssGetOutputPortSignal(S, 1))[0] = ((rtb_p4_tmp_b[14] < 0.02) ||
      (sqrt((rtb_p4_tmp_8[12] * rtb_p4_tmp_8[12] + rtb_p4_tmp_8[13] *
             rtb_p4_tmp_8[13]) + rtb_p4_tmp_8[14] * rtb_p4_tmp_8[14]) >= 0.7) ||
      (sqrt(((real_T)(*((const real_T **)ssGetInputPortSignalPtrs(S, 1))[0] *
                      *((const real_T **)ssGetInputPortSignalPtrs(S, 1))[0]) +
             *((const real_T **)ssGetInputPortSignalPtrs(S, 1))[1] * *((const
      real_T **)ssGetInputPortSignalPtrs(S, 1))[1]) + *((const real_T **)
      ssGetInputPortSignalPtrs(S, 1))[2] * *((const real_T **)
      ssGetInputPortSignalPtrs(S, 1))[2]) != 0.0));

    /* Product: '<S1>/MatrixMultiply1' incorporates:
     *  SignalConversion generated from: '<S1>/MatrixMultiply1'
     */
    for (i = 0; i < 4; i++) {
      _rtB->MatrixMultiply1[i] = 0.0;
      _rtB->MatrixMultiply1[i] += rtb_p4_tmp_9[i] * *((const real_T **)
        ssGetInputPortSignalPtrs(S, 1))[0];
      _rtB->MatrixMultiply1[i] += rtb_p4_tmp_9[i + 4] * *((const real_T **)
        ssGetInputPortSignalPtrs(S, 1))[1];
      _rtB->MatrixMultiply1[i] += rtb_p4_tmp_9[i + 8] * *((const real_T **)
        ssGetInputPortSignalPtrs(S, 1))[2];
      _rtB->MatrixMultiply1[i] += rtb_p4_tmp_9[i + 12] * 0.0;
    }

    /* End of Product: '<S1>/MatrixMultiply1' */
  }

  UNUSED_PARAMETER(tid);
}

/* Update for root system: '<Root>' */
#define MDL_UPDATE

static void mdlUpdate(SimStruct *S, int_T tid)
{
  if (ssIsContinuousTask(S, tid)) {
    /* Update for Integrator: '<S1>/Integrator' */
    ((int_T *)ssGetDWork(S, 1))[0] = 0;
  }

  UNUSED_PARAMETER(tid);
}

/* Derivatives for root system: '<Root>' */
#define MDL_DERIVATIVES

static void mdlDerivatives(SimStruct *S)
{
  B_CheckInvDiffKin_T *_rtB;
  XDot_CheckInvDiffKin_T *_rtXdot;
  _rtXdot = ((XDot_CheckInvDiffKin_T *) ssGetdX(S));
  _rtB = ((B_CheckInvDiffKin_T *) ssGetLocalBlockIO(S));

  /* Derivatives for Integrator: '<S1>/Integrator' */
  _rtXdot->Integrator_CSTATE[0] = _rtB->MatrixMultiply1[0];
  _rtXdot->Integrator_CSTATE[1] = _rtB->MatrixMultiply1[1];
  _rtXdot->Integrator_CSTATE[2] = _rtB->MatrixMultiply1[2];
  _rtXdot->Integrator_CSTATE[3] = _rtB->MatrixMultiply1[3];
}

/* Termination for root system: '<Root>' */
static void mdlTerminate(SimStruct *S)
{

#if defined(RT_MALLOC) || defined(MATLAB_MEX_FILE)

  if (ssGetUserData(S) != (NULL) ) {
    rt_FREE(ssGetLocalBlockIO(S));
  }

  rt_FREE(ssGetUserData(S));

#endif

}

#if defined(RT_MALLOC) || defined(MATLAB_MEX_FILE)
#  include "CheckInvDiffKin_mid.h"
#endif

/* Function to initialize sizes. */
static void mdlInitializeSizes(SimStruct *S)
{
  ssSetNumSampleTimes(S, 2);           /* Number of sample times */
  ssSetNumContStates(S, 4);            /* Number of continuous states */
  ssSetNumPeriodicContStates(S, 0);   /* Number of periodic continuous states */
  ssSetNumNonsampledZCs(S, 0);         /* Number of nonsampled ZCs */

  /* Number of output ports */
  if (!ssSetNumOutputPorts(S, 2))
    return;

  /* outport number: 0 */
  if (!ssSetOutputPortVectorDimension(S, 0, 4))
    return;
  if (ssGetSimMode(S) != SS_SIMMODE_SIZES_CALL_ONLY) {
    ssSetOutputPortDataType(S, 0, SS_DOUBLE);
  }

  ssSetOutputPortSampleTime(S, 0, 0.0);
  ssSetOutputPortOffsetTime(S, 0, 0.0);
  ssSetOutputPortOptimOpts(S, 0, SS_REUSABLE_AND_LOCAL);

  /* outport number: 1 */
  if (!ssSetOutputPortVectorDimension(S, 1, 1))
    return;
  if (ssGetSimMode(S) != SS_SIMMODE_SIZES_CALL_ONLY) {
    ssSetOutputPortDataType(S, 1, SS_BOOLEAN);
  }

  ssSetOutputPortSampleTime(S, 1, 0.0);
  ssSetOutputPortOffsetTime(S, 1, 0.0);
  ssSetOutputPortOptimOpts(S, 1, SS_REUSABLE_AND_LOCAL);

  /* Number of input ports */
  if (!ssSetNumInputPorts(S, 2))
    return;

  /* inport number: 0 */
  {
    if (!ssSetInputPortVectorDimension(S, 0, 4))
      return;
    if (ssGetSimMode(S) != SS_SIMMODE_SIZES_CALL_ONLY) {
      ssSetInputPortDataType(S, 0, SS_DOUBLE);
    }

    ssSetInputPortDirectFeedThrough(S, 0, 1);
    ssSetInputPortSampleTime(S, 0, 0.0);
    ssSetInputPortOffsetTime(S, 0, 0.0);
    ssSetInputPortOverWritable(S, 0, 0);
    ssSetInputPortOptimOpts(S, 0, SS_NOT_REUSABLE_AND_GLOBAL);
  }

  /* inport number: 1 */
  {
    if (!ssSetInputPortVectorDimension(S, 1, 3))
      return;
    if (ssGetSimMode(S) != SS_SIMMODE_SIZES_CALL_ONLY) {
      ssSetInputPortDataType(S, 1, SS_DOUBLE);
    }

    ssSetInputPortDirectFeedThrough(S, 1, 1);
    ssSetInputPortSampleTime(S, 1, 0.0);
    ssSetInputPortOffsetTime(S, 1, 0.0);
    ssSetInputPortOverWritable(S, 1, 0);
    ssSetInputPortOptimOpts(S, 1, SS_NOT_REUSABLE_AND_GLOBAL);
  }

  ssSetRTWGeneratedSFcn(S, 1);         /* Generated S-function */

  /* DWork */
  if (!ssSetNumDWork(S, 5)) {
    return;
  }

  /* '<S1>/MatrixMultiply': DWORK4 */
  ssSetDWorkName(S, 0, "DWORK0");
  ssSetDWorkWidth(S, 0, 16);

  /* '<S1>/Integrator': IWORK */
  ssSetDWorkName(S, 1, "DWORK1");
  ssSetDWorkWidth(S, 1, 1);
  ssSetDWorkDataType(S, 1, SS_INTEGER);

  /* '<S1>/MatrixMultiply': DWORK1 */
  ssSetDWorkName(S, 2, "DWORK2");
  ssSetDWorkWidth(S, 2, 16);

  /* '<S1>/MatrixMultiply': DWORK3 */
  ssSetDWorkName(S, 3, "DWORK3");
  ssSetDWorkWidth(S, 3, 16);

  /* '<S1>/MatrixMultiply': DWORK2 */
  ssSetDWorkName(S, 4, "DWORK4");
  ssSetDWorkWidth(S, 4, 4);
  ssSetDWorkDataType(S, 4, SS_INT32);

  /* Tunable Parameters */
  ssSetNumSFcnParams(S, 0);

  /* Number of expected parameters */
#if defined(MATLAB_MEX_FILE)

  if (ssGetNumSFcnParams(S) == ssGetSFcnParamsCount(S)) {

#if defined(MDL_CHECK_PARAMETERS)

    mdlCheckParameters(S);

#endif                                 /* MDL_CHECK_PARAMETERS */

    if (ssGetErrorStatus(S) != (NULL) ) {
      return;
    }
  } else {
    return;                /* Parameter mismatch will be reported by Simulink */
  }

#endif                                 /* MATLAB_MEX_FILE */

  /* Options */
  ssSetOptions(S, (SS_OPTION_RUNTIME_EXCEPTION_FREE_CODE |
                   SS_OPTION_PORT_SAMPLE_TIMES_ASSIGNED ));

#if SS_SFCN_FOR_SIM

  {
    ssSupportsMultipleExecInstances(S, true);
    ssHasStateInsideForEachSS(S, false);
  }

#endif

}

/* Function to initialize sample times. */
static void mdlInitializeSampleTimes(SimStruct *S)
{
  /* task periods */
  ssSetSampleTime(S, 0, 0.0);
  ssSetSampleTime(S, 1, 0.002);

  /* task offsets */
  ssSetOffsetTime(S, 0, 0.0);
  ssSetOffsetTime(S, 1, 0.0);
}

#if defined(MATLAB_MEX_FILE)
# include "fixedpoint.c"
# include "simulink.c"
#else
# undef S_FUNCTION_NAME
# define S_FUNCTION_NAME               CheckInvDiffKin_sf
# include "cg_sfun.h"
#endif                                 /* defined(MATLAB_MEX_FILE) */
