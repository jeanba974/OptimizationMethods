In this project, we share the developed algorithms and solutions of the paper 'Energy efficiency in O-RAN through sleep modes', published in IEEE ICC 2025 conference. The solutions solve the following problem:

The controller takes the decision whether to put the servers/DUs in light/deep sleep mode or not. The goal is to minimize the total energy consumption of the system over one frame, while ensuring that the total workload $L$ over all inter-connected DUs is timely served. The current frame workload $L$ is the traffic generated in the previous frame and queued in the system, hence known from the controller.
$$
\begin{align}
\min_{\mathbf{x}} &\sum_{i=1}^{n} TP_ax_iy_i + TP_s (1-x_i)(1-y_i)+\notag \\
&T_{\text{off}}P_{\text{off}}(1-x_i)y_i + (T-T_{\text{off}})P_s(1-x_i)y_i+\notag\\
&T_{\text{on}}P_{\text{on}}(1-y_i)x_i + (T-T_{\text{on}})P_a(1-y_i)x_i\\
\text{s.t.} &\quad x_i=\{0,1\},\quad\forall i\in\{1,\ldots,n\}\\
    &\quad y_i=\{0,1\},\quad\forall i\in\{1,\ldots,n\}\\
    &\sum_{i=1}^{n} TC_ix_iy_i + (T-T_{\text{on}})C_i(1-y_i)x_i \geq L,
\end{align}
$$


In problem $(\mathbb P)$, the objective to minimize is the energy consumption of the current frame.
We enumerate the variables in our formulation:
- $x_i$ represents the decision of the controller concerning the DU $i$: $x_i=1$ means DU $i$ is now active, while $x_i=0$ means DU $i$ is now asleep. The vector $\mathbf{x}$ contains the controller's decisions.
- $\{y_i\}_{i=1}^n$ stores the controller's decisions taken in the previous frame. This variable is important as the controller must account for the transitions from sleep to active or from active to sleep, when it decides whether to switch on/off the DUs.
- $P_a$ is the power consumption per time unit while active.
- $P_s$ is the power consumption per time unit while in sleep mode.
- $P_{\text{off}}$ is the power consumption per time unit during the transition from active to sleep mode.
- $P_{\text{on}}$ is the power consumption per time unit during the transition from sleep to active mode.
- $T$ is the total time within one period.
- $T_{\text{off}}$ is the transition time from active to sleep mode.
- $T_{\text{on}}$ is the transition time from sleep to active mode.
- $C_i$ is the capacity of the active DU $i$ for one slot.
- $\mathbf{C} = [C_1,\ldots,C_n]^\top$.
- $L$ is the total workload over one frame.
