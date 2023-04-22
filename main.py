import streamlit as st
import numpy as np
import random
from scipy.integrate import odeint
from matplotlib import pyplot as plt

st.set_page_config(layout="wide")

st.write("""
## Predator-Prey System Simulation
""")

# timestep determines the accuracy of the euler method of integration
timestep = 0.0001
# amplitude of noise term
amp = 0.00
# the time at which the simulation ends
end_time = 50

# creates a time vector from 0 to end_time, separated by a timestep
t = np.arange(0, end_time, timestep)

# initialize rabbits (x) and foxes (y) vectors
x = []
y = []

# noise term to perturb differential equations
def StochasticTerm(amp):
    return (amp * random.uniform(-1,1))

col1, col2 = st.columns(2)

with col1:

    # initial conditions for the rabbit (x) and fox (y) populations at time=0
    initial_rabbit = st.slider('initial conditions for the rabbit', 1, 500, 100, 10)
    initial_fox = st.slider('initial conditions for the fox', 1, 100, 20, 5)
    # factor that describes how many eaten rabbits give birth to a new fox
    d = st.slider('factor that describes how many eaten rabbits give birth to a new fox', 0.0, 0.1, 0.02, 0.005)

x.append(initial_rabbit)
y.append(initial_fox)

with col2:

    # definition of lotka-volterra parameters
    # birth rate of rabbits
    a = st.slider('Birth rate of rabbits', 0.1, 2.0, 1.0, 0.1)
    # death rate of rabbits due to predation
    b = st.slider('death rate of rabbits due to predation', 0.0, 0.5, 0.1, 0.05)
    # natural death rate of foxes
    c = st.slider('natural death rate of foxes', 0.1, 1.0, 0.5, 0.05)

# forward euler method of integration
# a perturbation term is added to the differentials to make the simulation stochastic
for index in range(1,len(t)):
    # make parameters stochastic
    # a = a + StochasticTerm(amp)
    # b = b + StochasticTerm(amp)
    # c = c + StochasticTerm(amp)
    # d = d + StochasticTerm(amp)
    
    # evaluate the current differentials
    xd = x[index-1] * (a - b*y[index-1])
    yd = -y[index-1]*(c - d*x[index-1])
    
    # evaluate the next value of x and y using differentials
    next_x = x[index-1] + xd * timestep
    next_y = y[index-1] + yd * timestep

    # add the next value of x and y 
    x.append(next_x)
    y.append(next_y)

# visualization

with col1:

    fig1, ax1 = plt.subplots(figsize=(10, 6))

    # deterministic populations against time
    ax1.plot(t, x)
    ax1.plot(t, y)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Population Size')
    ax1.legend(('Rabbits', 'Foxes'))
    ax1.set_title('Deterministic Lotka-Volterra')

    # save the plot as a PNG image
    fig1.savefig('deterministic.png')

    # display the image in Streamlit
    st.image('deterministic.png')

with col2:

    fig2, ax2 = plt.subplots(figsize=(10, 6))

    # deterministic phase portrait
    ax2.plot(x,y)
    ax2.set_xlabel('Fox Population')
    ax2.set_ylabel('Rabbit Population')
    ax2.set_title('Phase Portrait of Deterministic Lotka-Volterra')

    # save the plot as a PNG image
    fig2.savefig('phase_portrait.png')

    # display the image in Streamlit
    st.image('phase_portrait.png')