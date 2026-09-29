# CrashPBO: Controller Tuning with Human Feedback (Quanser Qube-Servo 2)

## Overview

`CrashPBO` tunes existing controllers using **human preferences and crash feedback**, rather than a numerical performance score. Users choose the better response and flag unacceptable trials. Each rejected trial is ranked below all accepted trials, giving the optimizer additional information without extra experiments. 

The researchers tested it on **Qube-Servo 2 pendulum swing up**, Crazyflie 2.1 backflips, and Mini Wheelbot driving tasks. The project shares Python optimization code, a browser interface, a PI response demo, and a Qube example for exploring and adapting this tuning approach.  

---

## How the Quanser Community Can Use This

Suggested experiments and extensions:

- **Explore human preferences:** use the [PI response demo][demo] to tune for faster response or less overshoot. Compare the settings produced by different priorities (Control Systems or Robotics).
- **Evaluate crash feedback:** repeat the Qube comparisons against preference only tuning and random search. Track failed swing ups, rejected aggressive motions, and tuning time separately.
- **Study uncertain feedback:** add a "cannot decide" option or test inconsistent choices. Evaluate how feedback quality affects final performance and the number of trials.
- **Start with a digital twin:** build an experiment adapter and test whether virtual comparisons reduce physical tuning trials. Validate transferred settings on hardware; QLabs integration is a proposed extension.
- **Extend to other Quanser plants:** connect the optimizer to Qube-Servo 3 or Aero 2 by supplying the controller, tunable parameters, trial routine, and response plots.

---

## Experimental Setup

- **Platform:** Quanser Qube-Servo 2 rotary pendulum.
- **Software and language:** Quanser SDK, Python, PyTorch, BoTorch, GPyTorch, and Streamlit.
- **Hardware connection:** bundled Qube driver and Quanser HIL SDK; the supplied Docker configuration targets Linux x86-64.

---

## Stack / Tags

`Qube-Servo 2`, `Python`, `Controller Tuning`, `Bayesian Optimization`, `Preference Learning`, `Human Feedback`, `Swing Up`

---

## Links

- **Repository:** [CrashPBO source code and examples][repo].
- **Paper:** [Preferential Bayesian Optimization with Crash Feedback][paper], IEEE Robotics and Automation Letters, 2026. [Open preprint][preprint].
- **Demo video:** Demo video: [Authors' experiment video][video], opening with the Crazyflie 2.1 backflip experiment and then showing the Quanser Qube Servo 2 pendulum experiment.

---

## Authors

Johanna Menn; David Stenger; Sebastian Trimpe.

Institute for Data Science in Mechanical Engineering (DSME), RWTH Aachen University, Germany. David Stenger also lists aiXopt GmbH.

[repo]: https://github.com/Data-Science-in-Mechanical-Engineering/crashpbo
[paper]: https://doi.org/10.1109/LRA.2026.3665446
[preprint]: https://arxiv.org/abs/2604.01776
[demo]: https://github.com/Data-Science-in-Mechanical-Engineering/crashpbo#pbo-demo
[video]: https://www.youtube.com/watch?v=2FTbzqT4wP8
