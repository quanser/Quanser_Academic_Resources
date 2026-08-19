/*
 * CheckInvDiffKin_sid.h
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
 *
 * SOURCES: CheckInvDiffKin_sf.c
 */

/* statically allocated instance data for model: CheckInvDiffKin */
{
  {
    /* Local SimStruct for the generated S-Function */
    static LocalS slS;
    LocalS *lS = &slS;
    ssSetUserData(rts, lS);

    /* block I/O */
    {
      static B_CheckInvDiffKin_T sfcnB;
      void *b = (real_T *) &sfcnB;
      ssSetLocalBlockIO(rts, b);
      (void) memset(b, 0,
                    sizeof(B_CheckInvDiffKin_T));
    }

    /* model checksums */
    ssSetChecksumVal(rts, 0, 3223851012U);
    ssSetChecksumVal(rts, 1, 1427526093U);
    ssSetChecksumVal(rts, 2, 2809483908U);
    ssSetChecksumVal(rts, 3, 637710602U);
  }
}
