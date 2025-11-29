
import numpy as np
import matplotlib.pyplot as plt

upper_temp_lim = 2400.0 

# Constants for air
R_air = 287.0
gamma = 1.4
Cv = R_air / (gamma - 1)
Cp = Cv * gamma

def otto_cycle(T1=300.0, P1=101325.0, r=6.0, T3=upper_temp_lim, gamma=1.4):
    R = R_air
    Cv = R / (gamma - 1)
    Cp = Cv * gamma

    # 1 -> 2 (isentropic compression)
    T2 = T1 * r ** (gamma - 1)
    P2 = P1 * r ** gamma

    # 2 -> 3 (constant-volume heat addition)
    P3 = P2 * (T3 / T2)

    # 3 -> 4 (isentropic expansion)
    T4 = T3 * r ** (1 - gamma)
    P4 = P3 * (T4 / T3)

    # Work & heat terms per kg
    q_in = Cv * (T3 - T2)
    q_out = Cv * (T4 - T1)
    w_net = q_in - q_out

    # Efficiency and MEP
    eta = 1 - q_out / q_in
    eta_theory = 1 - 1 / (r ** (gamma - 1))
    v1 = R * T1 / P1
    v2 = v1 / r
    mep = w_net / (v1 - v2)

    states = dict(T1=T1, P1=P1, T2=T2, P2=P2, T3=T3, P3=P3, T4=T4, P4=P4)
    return dict(states=states, q_in=q_in, q_out=q_out, w_net=w_net,
                eta=eta, eta_theory=eta_theory, mep=mep)

# --- Main evaluation for r = 6 ---
r_main = 6
otto = otto_cycle(r=r_main, T3=upper_temp_lim)

print("\n=== IDEAL OTTO CYCLE RESULTS ===")
print(f"Compression ratio (r): {r_main}")
print(f"T1 = {otto['states']['T1']:.2f} K,  P1 = {otto['states']['P1']/1e5:.3f} bar")
print(f"T2 = {otto['states']['T2']:.2f} K,  P2 = {otto['states']['P2']/1e5:.3f} bar")
print(f"T3 = {otto['states']['T3']:.2f} K,  P3 = {otto['states']['P3']/1e5:.3f} bar")
print(f"T4 = {otto['states']['T4']:.2f} K,  P4 = {otto['states']['P4']/1e5:.3f} bar")
print(f"Heat added (q_in): {otto['q_in']:.1f} J/kg")
print(f"Heat rejected (q_out): {otto['q_out']:.1f} J/kg")
print(f"Net work (w_net): {otto['w_net']:.1f} J/kg")
print(f"Thermal efficiency (energy): {otto['eta']*100:.2f} %")
print(f"Theoretical efficiency: {otto['eta_theory']*100:.2f} %")
print(f"Mean effective pressure (MEP): {otto['mep']/1e5:.3f} bar")

# --- Plots for r = 6, 8, 10 ---
r_values = [6, 8, 10]
colors = ['C0', 'C1', 'C2']
labels = ['1', '2', '3', '4', '1']

plt.figure(figsize=(12, 5))

# Temperature plot
plt.subplot(2, 2, 1)
for i, r in enumerate(r_values):
    res = otto_cycle(r=r, T3=upper_temp_lim)
    T = [res['states'][f'T{i}'] for i in [1, 2, 3, 4]] + [res['states']['T1']]
    plt.plot(range(1, 6), T, 'o-', label=f"r={r}", color=colors[i])
plt.xticks(range(1, 6), labels)
plt.ylabel("Temperature (K)")
plt.xlabel("State Point")
plt.title("Temperature at each state")
plt.legend()

# Pressure plot
plt.subplot(2, 2, 2)
for i, r in enumerate(r_values):
    res = otto_cycle(r=r, T3=upper_temp_lim)
    P = [res['states'][f'P{i}'] / 1e5 for i in [1, 2, 3, 4]] + [res['states']['P1'] / 1e5]
    plt.plot(range(1, 6), P, 'o-', label=f"r={r}", color=colors[i])

plt.xticks(range(1, 6), labels)
plt.ylabel("Pressure (bar)")
plt.xlabel("State Point")
plt.title("Pressure at each state")
plt.legend()

plt.tight_layout()


r_range = np.linspace(3, 12, 100)
etas = [otto_cycle(r=r)['eta'] * 100 for r in r_range]
meps = [otto_cycle(r=r)['mep'] / 1e5 for r in r_range]

plt.subplot(2, 2, 3)
plt.plot(r_range, etas, color='tab:blue')
plt.xlabel("Compression Ratio (r)")
plt.ylabel("Thermal Efficiency (%)")
plt.title("Efficiency vs Compression Ratio")

plt.subplot(2, 2, 4)
plt.plot(r_range, meps, color='tab:red')
plt.xlabel("Compression Ratio (r)")
plt.ylabel("MEP (bar)")
plt.title("MEP vs Compression Ratio")

plt.tight_layout()
plt.show()