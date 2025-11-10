import scipy.interpolate as interpolate
import matplotlib.pyplot as plt
import numpy as np

# data from Fig 3
x_lower_log10 = np.log10([156.2618410776012, 192.72606817802085, 240.26977465653403, 299.0055811910818, 376.7984691084651])
y_lower_log10 = np.log10([0.10009594837806626]*5)
x_upper_log10 = np.log10([404.0839844049945, 507.3929409762994, 635.972999788146, 801.4353837808537, 791.4415231600544])
y_upper_log10 = np.log10([1.9859234818472487, 1.9859234818472487, 1.9859234818472487, 1.9859234818472487, 0.9526735465943842])

# calculate slopes and intercepts
k = (y_upper_log10 - y_lower_log10) / (x_upper_log10 - x_lower_log10)
k_median = np.median(k)
b = y_lower_log10 - k * x_lower_log10

# corresponding alpha values
alpha = [-2, -1, 0, 1, 2]

# create interpolation function
function_balpha = interpolate.interp1d(b, alpha, fill_value="extrapolate")

# reproduce figure 3
plt.figure(figsize=(8,6))
x_range = np.linspace(np.log10(100), np.log10(900), 100)
ax = plt.gca()
for i in range(len(k)):
    alpha_this = function_balpha(b[i])
    y_range = k[i] * x_range + b[i]
    ax.plot(10**x_range, 10**y_range, label=f'{2**alpha_this:.2f} (Msun/Mstar)^{0.5} Myr',  alpha=0.5)
ax.set_xscale('log'); ax.set_yscale('log')
ax.set_ylim(0.1, 2); ax.set_xlim(100, 800)
ax.set_yticks([0.1, 0.5, 2]); ax.set_yticklabels(['0.1', '0.5', '2'])
ax.set_xticks([100, 200, 300, 400, 500, 600, 700, 800])
ax.set_xticklabels(['100','200','300','400','500','600','700','800'])
ax.set_title('Figure 3 Reproduction, Batygin 2012')
ax.set_xlabel('Semi-major axis (AU)')
ax.set_ylabel('M\'cosi\'(1+3e\'/2) (Mstar)')
ax.legend()



# Example calculation for specific input values
mstar = 1.0
x_input = 1200 # AU
M_secondary = 0.5
i_deg = 45 # degrees
e_secondary = 0.5

y_input = M_secondary * np.cos(np.radians(i_deg)) * (1 + 3 * e_secondary**2)
y_input = 0.94
x_input_log10 = np.log10(x_input)
y_input_log10 = np.log10(y_input)
b_input = y_input_log10 - k_median * x_input_log10
alpha_input = function_balpha(b_input)


precession_period_myr = 2**alpha_input * (1/mstar)**0.5
print('Precession period = {:.3f} Myr'.format(precession_period_myr))
