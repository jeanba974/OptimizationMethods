# OptimizationMethods
In this project, we share the algorithms related to the research paper "Energy efficiency in O-RAN through sleep modes", accepted at the ICC conference 2025.


We developed in Python a set of algorithms to address the following optimization problem:

![Equation](problemOpti.png)

In problem $(\mathbb P)$, the objective to minimize is the energy consumption of the current frame.
We enumerate the variables in our formulation:
\begin{itemize}
    \item $x_i$ represents the decision of the controller concerning the DU $i$: $x_i=1$ means DU $i$ is now active, while $x_i=0$ means DU $i$ is now asleep. The vector $\bm x$ contains the controller's decisions.
    \item $\{y_i\}_{i=1}^n$ stores the controller's decisions taken in the previous frame. This variable is important as the controller must account for the transitions from sleep to active or from active to sleep, when it decides whether to switch on/off the DUs.
    \item $P_a$ is the power consumption per time unit while active.
    \item $P_s$ is the power consumption per time unit while in sleep mode.
    \item $P_{\text{off}}$ is the power consumption per time unit during the transition from active to sleep mode.
    \item $P_{\text{on}}$ is the power consumption per time unit during the transition from sleep to active mode.
    \item $T$ is the total time within one period.
    \item $T_{\text{off}}$ is the transition time from active to sleep mode.
    \item $T_{\text{on}}$ is the transition time from sleep to active mode.
    \item $C_i$ is the capacity of the active DU $i$ for one slot.
    \item $\bm C = [C_1,\ldots,C_n]^\top$.
    \item $L$ is the total workload over one frame.
\end{itemize}
