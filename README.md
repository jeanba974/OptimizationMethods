# OptimizationMethods
In this project, we share the algorithms related to the research paper "Energy efficiency in O-RAN through sleep modes", accepted at the ICC conference 2025.


We developed in Python a set of algorithms to address the following optimization problem:

$$
&(\mathbb P): \quad \min_{\bm x} \sum_{i=1}^{n} TP_ax_iy_i + TP_s (1-x_i)(1-y_i)+\notag\\
    &T_{\text{off}}P_{\text{off}}(1-x_i)y_i + (T-T_{\text{off}})P_s(1-x_i)y_i+\notag\\
    &T_{\text{on}}P_{\text{on}}(1-y_i)x_i + (T-T_{\text{on}})P_a(1-y_i)x_i\label{eq:obj}\\
    \text{s.t.} &\quad x_i=\{0,1\},\quad\forall i\in\{1,\ldots,n\}\\
    &\quad y_i=\{0,1\},\quad\forall i\in\{1,\ldots,n\}\\
    &\sum_{i=1}^{n} TC_ix_iy_i + (T-T_{\text{on}})C_i(1-y_i)x_i \geq L,\quad \label{eq:load}
$$
