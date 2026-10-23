import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

st.set_page_config(
    page_title="RL Transient Lab | Semester III",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1250px;}
.hero {padding: 1.35rem 1.5rem; border: 1px solid #d6dde8; border-radius: 18px;
       background: linear-gradient(120deg, rgba(50,90,150,.10), rgba(80,150,130,.08));}
.hero h1 {margin: 0; font-size: 2.15rem;}
.smallmuted {color: #64748b; font-size: .92rem;}
.metric-label {font-size:.85rem; color:#64748b;}
div[data-testid="stMetric"] {border:1px solid #dbe2ea; padding: .8rem; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="smallmuted">PHYSICS LAB • INTERACTIVE SIMULATION</div>
  <h1>Series RL Circuit — Transient Response</h1>
  <p>Explore the exponential rise of current, compare measured readings with theory, and design a circuit for a target time constant.</p>
  <p class="smallmuted"><b>Yash Montu Yadav</b> · Semester III · USN 25BSR00210 · 23 October 2026</p>
</div>
""", unsafe_allow_html=True)

# Notebook transcribed values; t=0 was a dash in the source, so only numeric readings are fitted.
time_obs = np.array([30,60,90,120,150,180,210,240,270,300], dtype=float)
current_obs = np.array([185,318,434,527,608,673,727,773,811,843], dtype=float)

def rise(t, i_final, tau):
    return i_final * (1 - np.exp(-t / tau))

popt, _ = curve_fit(rise, time_obs, current_obs, p0=[1000,150], bounds=([0,1],[2000,2000]))
fit_i, fit_tau = popt
fit_vals = rise(time_obs, *popt)
ss_res = np.sum((current_obs-fit_vals)**2)
ss_tot = np.sum((current_obs-current_obs.mean())**2)
r2 = 1 - ss_res/ss_tot

with st.sidebar:
    st.header("Circuit controls")
    voltage = st.number_input("Supply voltage, V (volts)", min_value=0.01, max_value=100.0, value=0.2, step=0.1, format="%.2f")
    resistance = st.number_input("Series resistance, R (ohms)", min_value=0.01, max_value=1000.0, value=0.2, step=0.1, format="%.2f")
    target_tau = st.selectbox("Target time constant", [10, 50, 100, 150], index=1)
    duration = st.slider("Simulation duration (seconds)", min_value=30, max_value=600, value=300, step=30)
    show_measurements = st.checkbox("Show recorded lab measurements", value=True)
    st.caption("The recorded readings are transcribed from the supplied notebook image. Confirm instrument units before interpreting physical parameters.")

i_final_mA = 1000 * voltage / resistance
required_L = resistance * target_tau
t = np.linspace(0, duration, 500)
i_theory = i_final_mA * (1-np.exp(-t/target_tau))
i_target_63 = 0.6321205588 * i_final_mA

st.subheader("At a glance")
c1,c2,c3,c4 = st.columns(4)
c1.metric("Theoretical final current", f"{i_final_mA:.2f} mA")
c2.metric("Selected target τ", f"{target_tau} s")
c3.metric("Required inductance", f"{required_L:.3f} H")
c4.metric("Data-fitted τ", f"{fit_tau:.1f} s")
st.caption("Model: i(t) = (V/R) × [1 − exp(−t/τ)]   |   τ = L/R")

tab1, tab2, tab3 = st.tabs(["Live design simulation", "Recorded-data analysis", "Theory & method"])

with tab1:
    left, right = st.columns([1.65,1])
    with left:
        fig, ax = plt.subplots(figsize=(8.5,4.8))
        ax.plot(t, i_theory, label=f"Designed response (τ = {target_tau} s)", linewidth=2.5)
        ax.axhline(i_final_mA, linestyle="--", label=f"Final current = {i_final_mA:.1f} mA")
        ax.axhline(i_target_63, linestyle=":", label="63.2% of final current")
        ax.set(xlabel="Time (s)", ylabel="Current (mA)", title="Interactive RL step response")
        ax.grid(True, alpha=.25); ax.legend()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with right:
        st.markdown("#### Design interpretation")
        st.write(f"For **R = {resistance:g} Ω** and target **τ = {target_tau} s**:")
        st.latex(r"L=R\\tau")
        st.latex(f"L = {resistance:g} \\times {target_tau} = {required_L:.4g}\\,\\mathrm{{H}}")
        st.write(f"The current reaches **63.2%** of its final value at approximately **{target_tau} s**.")
        st.write(f"After **5τ = {5*target_tau} s**, the ideal response is approximately 99.3% settled.")
    sim_df = pd.DataFrame({"Time_s":t, "Simulated_current_mA":i_theory})
    st.download_button("Download simulated curve (CSV)", sim_df.to_csv(index=False).encode("utf-8"),
                       file_name="rl_design_simulation.csv", mime="text/csv")

with tab2:
    c1,c2,c3 = st.columns(3)
    c1.metric("Fitted final current", f"{fit_i:.1f} mA")
    c2.metric("Fitted time constant", f"{fit_tau:.2f} s")
    c3.metric("R² goodness of fit", f"{r2:.5f}")
    fig, ax = plt.subplots(figsize=(9,4.8))
    if show_measurements:
        ax.scatter(time_obs, current_obs, label="Recorded measurements", zorder=3)
    td = np.linspace(0, max(duration,330), 500)
    ax.plot(td, rise(td, *popt), label=f"Exponential fit (τ={fit_tau:.1f} s)", linewidth=2.5)
    ax.axhline(1000, linestyle="--", label="1000 mA reference (notebook V/R)")
    ax.set(xlabel="Time (s)", ylabel="Current (mA)", title="Measured readings and fitted RL response")
    ax.grid(True, alpha=.25); ax.legend()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    obs_df = pd.DataFrame({"Time_s":time_obs, "Observed_current_mA":current_obs, "Fitted_current_mA":rise(time_obs,*popt)})
    st.dataframe(obs_df.round(2), use_container_width=True, hide_index=True)
    st.download_button("Download observations and fit (CSV)", obs_df.to_csv(index=False).encode("utf-8"),
                       file_name="rl_observations_and_fit.csv", mime="text/csv")
    st.warning("The notebook records a dash at t = 0; the fit excludes t = 0. The fit-derived inductance is only an inference and assumes the stated resistance is the effective total series resistance.")

with tab3:
    st.markdown("#### Governing equation")
    st.latex(r"V=Ri+L\\frac{di}{dt}")
    st.markdown("For a DC step and zero initial current:")
    st.latex(r"i(t)=\\frac{V}{R}\\left(1-e^{-t/\\tau}\\right),\\qquad \\tau=\\frac{L}{R}")
    st.markdown("#### Key physical interpretation")
    st.markdown("""
    - The inductor opposes sudden changes in current.
    - Current rises exponentially toward the steady-state value `V/R`.
    - At one time constant, current reaches about 63.2% of its final value.
    - At five time constants, the ideal response is about 99.3% settled.
    """)
    st.markdown("#### Reproducibility")
    st.write("The measured-data fit and design simulation are computed in Python using NumPy, pandas, SciPy and Matplotlib. The raw readings are embedded in this app and can be downloaded as CSV from the analysis tab.")

st.divider()
st.markdown("**Academic note:** This is a computational simulation based on the transcribed lab readings and ideal RL theory; it is not a claim that a physical circuit was measured by the web app.")
st.markdown("<div class='smallmuted'>Series RL Transient Lab · Semester III · USN 25BSR00210</div>", unsafe_allow_html=True)
