import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

def calculate_R0(beta, gamma, f, rho, S0):
    return beta / (gamma + f * rho) * S0

def model_all_out_const(beta, rho, Pop, par, n):
    ode_flag = 0
    gamma = 0.1429
    f = 1.1013
    I0_1 = par[0] # Python indexing starts from 0

    # Define the differential equations
    def H(t, x):
        return [-beta * x[0] * x[1],
                beta * x[0] * x[1] - (gamma) * x[1] - f * rho * x[1],
                f * rho * x[1]]

    # Solve the differential equations
    sol = solve_ivp(H, [0, n], [Pop - I0_1, I0_1, 0], t_eval=np.arange(n+1))

    # Extract the solution
    S = sol.y[0]
    I = sol.y[1]
    Cases = sol.y[2]

    # Compute the incidence values
    sol_incidence = np.diff(Cases)
    sol_incidence = np.insert(sol_incidence, 0, 0)

    # Check if the solution was successful
    if len(sol.t) == n+1:
        sol = np.vstack((S, I, Cases))
    else:
        ode_flag = 1

    return sol, ode_flag

# Define the parameters
Pop = 4371323.74
n = 72
gamma = 0.1429
f = 1.1013
t_use = np.arange(n+1)
desired_R0 = 1.8861

# Define ranges for beta and rho
beta_range = np.linspace(1e-8, 1e-7, 10000)
rho_range = np.linspace(0.001, 10, 10000)

# Initialize arrays to store valid combinations of beta and rho
valid_combinations = []

# Iterate through beta and rho ranges to find valid combinations
for beta_val in beta_range:
    for rho_val in rho_range:
        # Calculate R0 using the current beta and rho values
        R0 = calculate_R0(beta_val, gamma, f, rho_val, Pop)
        # Check if R0 matches the desired value
        if abs(R0 - desired_R0) < 0.001:
            # Store the valid combination of beta and rho
            valid_combinations.append([beta_val, rho_val])

# Define beta multipliers
beta_multipliers = [1, 1.1, 1.2, 1.3, 1.4, 0.9, 0.8]

# Initialize a list to store output for each scenario
model_output = [[] for _ in range(len(beta_multipliers))]

# Loop through beta multipliers
for j, beta_multiplier in enumerate(beta_multipliers):
    # Loop through each valid combination of beta and rho
    for beta_val, rho_val in valid_combinations:
        beta = beta_val * beta_multiplier
        rho = rho_val
        np.random.seed(0)  # Reset random number generator

        # Define the range for I0
        widths = [235.44, 299.98]
        I0_1_range = np.random.uniform(widths[0], widths[1])

        # Set the parameters for the SIRC model
        par = [I0_1_range]

        # Solve the SIRC model
        sol, ode_flag = model_all_out_const(beta, rho, Pop, par, n)

        # Store the values in the list
        if ode_flag == 0:
            model_output[j].append({'beta': beta, 'rho': rho, 'I': sol[1], 'S': sol[0], 'C': sol[2]})

# Initialize arrays to store peak and cumulative values
peak_infections_values = np.zeros(len(beta_multipliers))
peak_cases_values = np.zeros(len(beta_multipliers))
cumulative_infections_values = np.zeros(len(beta_multipliers))
cumulative_cases_values = np.zeros(len(beta_multipliers))
prop_inf_pop = np.zeros(len(beta_multipliers))

# Loop through each scenario
for j in range(len(beta_multipliers)):
    # Initialize arrays to store values
    hidden_infect_values = np.zeros((len(model_output[j]), n+1))
    cases_values = np.zeros((len(model_output[j]), n+1))
    susc_values = np.zeros((len(model_output[j]), n+1))

    # Loop through all simulations to store values
    for idx, output in enumerate(model_output[j]):
        hidden_infect_values[idx, :] = output['I']
        cases_values[idx, :] = output['C']
        susc_values[idx, :] = output['S']

    # Calculate the mean across all simulations for current scenario
    hidden_infect_mean = np.mean(hidden_infect_values, axis=0)
    cases_mean = np.mean(cases_values, axis=0)
    susc_mean = np.mean(susc_values, axis=0)

    # Find the maximum value and its index in the mean data
    peak_infections_values[j] = np.max(hidden_infect_mean)
    peak_cases_values[j] = np.max(cases_mean)

    # Calculate the cumulative sums
    cumulative_infections_values[j] = np.sum(hidden_infect_mean)
    cumulative_cases_values[j] = np.sum(cases_mean)

    # Finding the end of S to estimate proportion of infected population
    prop_inf_pop[j] = (Pop - susc_mean[-1]) / Pop

# Create DataFrame with results
results = pd.DataFrame(columns=['Scenario', 'Infections_cummulative', 'Infections_peak',
                                'Cases_cummulative', 'Cases_peak', 'Prop_inf_pop'])

# Populate DataFrame with results
for j in range(len(beta_multipliers)):
    results.loc[j] = ['Scenario {}'.format(j+1), cumulative_infections_values[j], peak_infections_values[j],
                      cumulative_cases_values[j], peak_cases_values[j], prop_inf_pop[j]]

# Write DataFrame to CSV file
results.to_csv('results_table.csv', index=False)
