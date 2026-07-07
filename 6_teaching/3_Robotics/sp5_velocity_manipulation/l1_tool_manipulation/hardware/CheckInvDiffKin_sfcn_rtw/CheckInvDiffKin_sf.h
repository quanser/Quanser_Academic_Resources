/*
 * CheckInvDiffKin_sf.h
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

#ifndef RTW_HEADER_CheckInvDiffKin_sf_h_
#define RTW_HEADER_CheckInvDiffKin_sf_h_
#include <math.h>
#include <string.h>
#include <stddef.h>
#ifndef CheckInvDiffKin_sf_COMMON_INCLUDES_
# define CheckInvDiffKin_sf_COMMON_INCLUDES_
#include <stdlib.h>
#define S_FUNCTION_NAME                CheckInvDiffKin_sf
#define S_FUNCTION_LEVEL               2
#define RTW_GENERATED_S_FUNCTION
#include "rtwtypes.h"
#include "simstruc.h"
#include "fixedpoint.h"
#if !defined(MATLAB_MEX_FILE)
#include "rt_matrx.h"
#endif

#if !defined(RTW_SFUNCTION_DEFINES)
#define RTW_SFUNCTION_DEFINES

typedef struct {
  void *blockIO;
  void *defaultParam;
  void *nonContDerivSig;
} LocalS;

#define ssSetLocalBlockIO(S, io)       ((LocalS *)ssGetUserData(S))->blockIO = ((void *)(io))
#define ssGetLocalBlockIO(S)           ((LocalS *)ssGetUserData(S))->blockIO
#define ssSetLocalDefaultParam(S, paramVector) ((LocalS *)ssGetUserData(S))->defaultParam = (paramVector)
#define ssGetLocalDefaultParam(S)      ((LocalS *)ssGetUserData(S))->defaultParam
#define ssSetLocalNonContDerivSig(S, pSig) ((LocalS *)ssGetUserData(S))->nonContDerivSig = (pSig)
#define ssGetLocalNonContDerivSig(S)   ((LocalS *)ssGetUserData(S))->nonContDerivSig
#endif
#endif                                 /* CheckInvDiffKin_sf_COMMON_INCLUDES_ */

#include "CheckInvDiffKin_sf_types.h"

/* Shared type includes */
#include "multiword_types.h"
#include "rtGetNaN.h"
#include "rt_nonfinite.h"
#include "rt_defines.h"

/* Block signals (default storage) */
typedef struct {
  real_T MatrixMultiply1[4];           /* '<S1>/MatrixMultiply1' */
} B_CheckInvDiffKin_T;

/* Continuous states (default storage) */
typedef struct {
  real_T Integrator_CSTATE[4];         /* '<S1>/Integrator' */
} X_CheckInvDiffKin_T;

/* State derivatives (default storage) */
typedef struct {
  real_T Integrator_CSTATE[4];         /* '<S1>/Integrator' */
} XDot_CheckInvDiffKin_T;

/* State disabled  */
typedef struct {
  boolean_T Integrator_CSTATE[4];      /* '<S1>/Integrator' */
} XDis_CheckInvDiffKin_T;

/* External inputs (root inport signals with default storage) */
typedef struct {
  real_T *InitialJointPositionrad4[4];
                                 /* '<Root>/Initial Joint Position (rad) [4]' */
  real_T *DesiredEESpeedms3[3];       /* '<Root>/Desired EE Speed (m//s) [3]' */
} ExternalUPtrs_CheckInvDiffKin_T;

/* External outputs (root outports fed by signals with default storage) */
typedef struct {
  real_T *Phirad4[4];                  /* '<Root>/Phi (rad) [4]' */
  boolean_T *MotorEnable;              /* '<Root>/Motor Enable' */
} ExtY_CheckInvDiffKin_T;

/*-
 * The generated code includes comments that allow you to trace directly
 * back to the appropriate location in the model.  The basic format
 * is <system>/block_name, where system is the system number (uniquely
 * assigned by Simulink) and block_name is the name of the block.
 *
 * Note that this particular code originates from a subsystem build,
 * and has its own system numbers different from the parent model.
 * Refer to the system hierarchy for this subsystem below, and use the
 * MATLAB hilite_system command to trace the generated code back
 * to the parent model.  For example,
 *
 * hilite_system('checkDiffKinematics/CheckInvDiffKin')    - opens subsystem checkDiffKinematics/CheckInvDiffKin
 * hilite_system('checkDiffKinematics/CheckInvDiffKin/Kp') - opens and selects block Kp
 *
 * Here is the system hierarchy for this model
 *
 * '<Root>' : 'checkDiffKinematics'
 * '<S1>'   : 'checkDiffKinematics/CheckInvDiffKin'
 * '<S2>'   : 'checkDiffKinematics/CheckInvDiffKin/Compare To Constant2'
 * '<S3>'   : 'checkDiffKinematics/CheckInvDiffKin/Compare To Constant3'
 * '<S4>'   : 'checkDiffKinematics/CheckInvDiffKin/Compare To Constant4'
 * '<S5>'   : 'checkDiffKinematics/CheckInvDiffKin/Norm1'
 * '<S6>'   : 'checkDiffKinematics/CheckInvDiffKin/Norm2'
 * '<S7>'   : 'checkDiffKinematics/CheckInvDiffKin/differential kinematics'
 * '<S8>'   : 'checkDiffKinematics/CheckInvDiffKin/forward kinematics1'
 * '<S9>'   : 'checkDiffKinematics/CheckInvDiffKin/Norm1/Norm Squared'
 * '<S10>'  : 'checkDiffKinematics/CheckInvDiffKin/Norm2/Norm Squared'
 */
#endif                                 /* RTW_HEADER_CheckInvDiffKin_sf_h_ */
