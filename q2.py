# rankine_cycle.py
# Simulation of an Ideal Rankine Cycle for a Steam Power Plant

import numpy as np
import matplotlib.pyplot as plt

mass_flowrate = 48  # kg/s
P_low = 50  # kPa (condenser pressure)
P_high_list = [3000, 4000, 5000]  # kPa (boiler pressures)
T_high = 400 + 273.15  # °C -> K


h_fg_100 = 2257  # kJ/kg (approx latent heat at 100°C)
cp_liquid = 4.18  # kJ/kg·K
gamma = 1.33  # assumed for steam expansion
R = 0.4615  # kJ/kg·K

def approximate_rankine(P_high_kPa):
    # 1 -> 2: Pump (liquid water compressed)
    h1 = 340  # kJ/kg (approx saturated liquid at 50 kPa)
    v1 = 0.001  # m3/kg
    pump_work = v1 * (P_high_kPa - P_low)  # kJ/kg
    h2 = h1 + pump_work

    # 2 -> 3: Boiler (liquid to superheated vapor)
    h_g = 2800 + 0.1 * (P_high_kPa - 3000) / 1000 * 100  # rough trend
    h3 = h_g + cp_liquid * (T_high - 473.15) / 1000 * 100  # superheat correction

    # 3 -> 4: Turbine (isentropic expansion)
    h4 = h3 - 0.25 * (h3 - h1)  # crude isentropic drop fraction

    # Efficiency and work
    turbine_work = h3 - h4
    pump_work = h2 - h1
    net_work = turbine_work - pump_work
    heat_added = h3 - h2
    efficiency = net_work / heat_added

    # Net power (kW)
    net_power = net_work * mass_flowrate  # kJ/kg * kg/s = kJ/s = kW

    return efficiency, net_power, (h1, h2, h3, h4)

efficiencies = []
powers = []

for P_high in P_high_list:
    eff, power, states = approximate_rankine(P_high)
    efficiencies.append(eff)
    powers.append(power)
    print(f"\nFor Boiler Pressure = {P_high/1000:.1f} MPa:")
    print(f"  Thermal Efficiency = {eff*100:.2f}%")
    print(f"  Net Power Output = {power/1000:.2f} MW")

# --- Plot results ---
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.plot(np.array(P_high_list)/1000, np.array(efficiencies)*100, 'o-b', lw=2)
plt.xlabel("Boiler Pressure (MPa)")
plt.ylabel("Thermal Efficiency (%)")
plt.title("Rankine Cycle Efficiency vs Boiler Pressure")
plt.grid(True)

plt.subplot(1,2,2)
plt.plot(np.array(P_high_list)/1000, np.array(powers)/1000, 's-r', lw=2)
plt.xlabel("Boiler Pressure (MPa)")
plt.ylabel("Net Power Output (MW)")
plt.title("Net Power Output vs Boiler Pressure")
plt.grid(True)

plt.tight_layout()
plt.show()
