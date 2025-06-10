#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import hydralit_components as hc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set page layout to centered and responsive
st.set_page_config(layout='wide', initial_sidebar_state='collapsed')

# Define reset callback functions
def reset_initial_values():
    st.session_state.a_freq = st.session_state.reset_a_freq
    st.session_state.init_infest = st.session_state.reset_init_infest

def reset_setup():
    st.session_state.num_years = st.session_state.reset_num_years
    st.session_state.detection_threshold = st.session_state.reset_detection_threshold

# specify the primary menu definition
menu_data = [
    {'icon': "far fa-copy", 'label': "Model & Parameters"},
    {'icon': "far fa-chart-bar", 'label': "Simulation"},
    {'icon': "fas fa-tachometer-alt", 'label': "Settings"},
]

over_theme = {'txc_inactive': '#FFFFFF', 'menu_background': '#85929E'}
st.markdown("# Nemo")
main_tab = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Introduction',
    hide_streamlit_markers=False,
    sticky_nav=True,
    sticky_mode='pinned',
)

# Initialize session state with default values
default_params = {
    "a_freq": 0.1,
    "init_infest": 40,
    "s": 0.25,
    "m": 0.35,
    "h": 0.17,
    "mu": 0.10,
    "c": 0.4,
    "e": 300,
    "detection_threshold": 1,
    "num_years": 10,
    "bc_vector": [],
    "all_bc": 0.0,
    "all_types": 1,
    "plant_type_vector": [],
    "reset_a_freq": 0.1,
    "reset_init_infest": 30,
    "reset_s": 0.25,
    "reset_m": 0.35,
    "reset_h": 0.17,
    "reset_mu": 0.10,
    "reset_c": 0.4,
    "reset_e": 300,
    "reset_detection_threshold": 1,
    "reset_num_years": 10,
    "reset_all_bc": 0.0
}

for key, value in default_params.items():
    st.session_state.setdefault(key, value)

# Helper functions
def round1d(number):
    return round(number, 1)

def update_deployment_vectors():
    """Update deployment vectors from configuration DataFrame"""
    if 'config_df' in st.session_state:
        config_df = st.session_state.config_df
        plant_type_vector = [type_mapping[t] for t in config_df['Type']]
        bc_vector = [x / 100 for x in config_df['Biocontrol (%)']]
        return plant_type_vector, bc_vector
    return [], []

def run_simulation():
    """Run the simulation with current parameters"""
    num_years = st.session_state.num_years
    plant_type_vector, bc_vector = update_deployment_vectors()
    
    # Ensure we have enough configuration data
    if len(plant_type_vector) < num_years:
        st.error("Configuration error: Not enough years configured. Please check deployment settings.")
        return None, None, None, None, None, None
    
    X = np.zeros(num_years + 1)
    Y = np.zeros(num_years + 1)
    Z = np.zeros(num_years + 1)
    
    init_juveniles = st.session_state.init_infest
    a_freq = st.session_state.a_freq
    J_AA_0 = init_juveniles * (1 - a_freq) ** 2
    J_Aa_0 = init_juveniles * 2 * a_freq * (1 - a_freq)
    J_aa_0 = init_juveniles * (a_freq) ** 2
    
    X[0] = J_AA_0
    Y[0] = J_Aa_0
    Z[0] = J_aa_0
    
    for k in range(num_years):
        plant_type = plant_type_vector[k]
        R = (1 - st.session_state.m) * st.session_state.e * st.session_state.s * (
            (1 - st.session_state.mu) * (1 - st.session_state.h) * (1 - bc_vector[k]))
        M = 1 / st.session_state.c
        
        if plant_type == 1:  # Susceptible
            total = X[k] + Y[k] + Z[k]
            X[k + 1] = round1d(R * M * (X[k] + 0.5 * Y[k]) ** 2 / ((M + total) * total))
            Y[k + 1] = round1d(2 * R * M * (X[k] + 0.5 * Y[k]) * (Z[k] + 0.5 * Y[k]) / ((M + total) * total))
            Z[k + 1] = round1d(R * M * (Z[k] + 0.5 * Y[k]) ** 2 / ((M + total) * total))
        elif plant_type == 2:  # Resistant
            total = X[k] + Y[k] + Z[k]
            X[k + 1] = 0
            denom = (M + total) * (X[k] + Y[k] + st.session_state.m * Z[k])
            Y[k + 1] = round1d(R * M * Z[k] * (X[k] + 0.5 * Y[k]) / denom)
            Z[k + 1] = round1d(R * M * Z[k] * (st.session_state.m * Z[k] + 0.5 * Y[k]) / denom)
        elif plant_type == 0:  # Rotation
            survival_factor = (1 - st.session_state.mu) * (1 - st.session_state.h) * (1 - bc_vector[k])
            X[k + 1] = round1d(survival_factor * X[k])
            Y[k + 1] = round1d(survival_factor * Y[k])
            Z[k + 1] = round1d(survival_factor * Z[k])
    
    tot = X + Y + Z
    f_A = np.zeros(num_years + 1)
    f_a = np.zeros(num_years + 1)
    
    for n in range(num_years + 1):
        total_n = tot[n]
        if total_n == 0:
            f_AA = 0
            f_Aa = 0
            f_aa = 0
        else:
            f_AA = X[n] / total_n
            f_Aa = Y[n] / total_n
            f_aa = Z[n] / total_n
        f_A[n] = f_AA + f_Aa / 2
        f_a[n] = f_aa + f_Aa / 2
    
    return tot, f_A, f_a, X, Y, Z

def generate_main_plot(tot, f_A, f_a):
    """Generate the main plot with simulation results"""
    if tot is None:
        return
        
    fig, ax = plt.subplots(figsize=(14, 10), dpi=100)
    nb_gen = len(tot)
    th = st.session_state.detection_threshold
    
    ax.plot(np.arange(0, nb_gen), tot, '-r', linewidth=3)
    ax.plot([0, nb_gen - 1], [th, th], 'k--', label='Acceptance threshold')
    
    ax.set_xlabel("Year", fontsize=30)
    ax.set_ylabel("PCNs/g of soil", fontsize=30)
    ax.set_xlim([0, nb_gen - 1])
    
    max_val = max(max(tot), th)
    tick_locations = [0] + list(range(20, int(max_val) + 20, 20))
    if th not in tick_locations:
        tick_locations.append(th)
    tick_locations.sort()
    tick_labels = [str(int(val)) for val in tick_locations]
    
    ax.set_yticks(tick_locations)
    ax.set_yticklabels(tick_labels)
    ax.tick_params(axis='both', which='major', labelsize=30)
    ax.legend(fontsize=15)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.pyplot(fig)
    
    with col2:
        with st.expander("Frequency of avirulence allele A"):
            fig_upper, ax_upper = plt.subplots(figsize=(8, 5), dpi=100)
            ax_upper.plot(np.arange(0, nb_gen), f_A, linewidth=3)
            ax_upper.set_xlabel("Year", fontsize=30)
            ax_upper.tick_params(axis='both', which='major', labelsize=30)
            st.pyplot(fig_upper)
        
        with st.expander("Frequency of virulence allele a"):
            fig_lower, ax_lower = plt.subplots(figsize=(8, 5), dpi=100)
            ax_lower.plot(np.arange(0, nb_gen), f_a, linewidth=3)
            ax_lower.set_xlabel("Year", fontsize=30)
            ax_lower.tick_params(axis='both', which='major', labelsize=30)
            st.pyplot(fig_lower)

# Define plant type mappings globally
type_mapping = {'Susceptible': 1, 'M. Resistant': 2, 'Rotation': 0}
reverse_mapping = {v: k for k, v in type_mapping.items()}

# Main tab logic
if main_tab == "Introduction":
    st.markdown("# Introduction")
    st.markdown("- Globodera pallida, or Pale Cyst Nematode (PCN), is a serious quarantine pest that threatens potato crops worldwide.")
    st.markdown("- The use of resistant potato cultivars is a popular sustainable pest control measure, but the evolution of PCN populations towards virulence can reduce the long-term effectiveness of resistance-based control.")
    st.markdown("- Masculinizing resistance prevents avirulent nematodes from producing females, which could ultimately eliminate avirulent PCNs from the population.")
    st.markdown("- However, [Shouten's model](https://link.springer.com/article/10.1007/BF03041409) tracing genotypic frequencies in real conditions shows that the long-term fixation of the virulence allele does not necessarily occur despite the selection pressure.")
    st.markdown("- Avirulent nematodes, which are exclusively male, survive as heterozygotes by mating with virulent females, weakening the PCN's reproduction number.")
    st.markdown("- Biocontrol efficiency required for PCN long-term suppression under resistant plants is lower than under susceptible plants.")
    st.markdown("- But the efficiency required even under resistant plant can be very high, thus unachievable")
    st.markdown("- Rotations are proven to be an efficient and sustainable lever of PCN control, but required long periods of cultivating non-host crops or leaving a bare soil")
    st.markdown("- Combining resistant cultivars with biocontrol methods and rotations appears to be an effective solution for speeding up the suppression of PCN populations.")
    st.markdown("- The model presented for this simulation tracks at the same time the PCN genetics and dynamics to describe selection for virulence and biocontrol+rotation size needs under resistance.")
    st.markdown("- The user is able to enter the type of crop for each season - S for Susceptible, R for Resistant, N for Non-host (corresponding to a rotation) - and the app will draw the PCN population trajectories as well as the corresponding allele frequencies.")
    
    logo_paths = ["figs/logo_agro.png", "figs/logo_igepp.png", "figs/logo_inrae.png", "figs/logo_inov3pt.png"]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image(logo_paths[0], width=200, use_column_width=False)
    with col2:
        st.image(logo_paths[1], width=200, use_column_width=False)
    with col3:
        st.image(logo_paths[2], width=200, use_column_width=False)
    with col4:
        st.image(logo_paths[3], width=200, use_column_width=False)

elif main_tab == "Model & Parameters":
    st.markdown("# Model & parameters")
    image1_path = "figs/diagram.png"
    st.image(image1_path)
    
    checkbox = st.checkbox("See the simple models")
    if checkbox:
        st.markdown("$X_n \longrightarrow AA$ PCNs, $\qquad Y_n \longrightarrow Aa$ PCNs, $\qquad Z_n \longrightarrow aa$ PCNs")
        st.markdown("- When susceptible plants are deployed in every generation, the overall PCN population $N_k$ at generation $k$ is given by the law:")
        st.latex(r'''
        \begin{equation*}
             N_{k+1} = (1-m)R \displaystyle\frac{ N_k}{1 + c N_k}
        \end{equation*}
        ''')
        st.markdown("Where $R$ is the PCN reproduction number and $c>0$ is an interspecific competition parameter. The term $(1-m)R$ is the basic reproduction number of the parasite.")
        st.markdown("If $(1-m)R>1$, the parasite population grows until it reaches carrying capacity")
        st.latex(r'''
            \begin{equation}
            K(R,m,c)=\frac{(1-m)R-1}{c}\,.
            \end{equation}
        ''')
        st.markdown("- When resistance plants are deployed in every generation, the overall PCN population $N_k$ at generation $k$ is given by the law:")
        st.latex(r'''
        \begin{equation*}
            \left\{\begin{aligned}
                N_{k+1} &= N_{k+1} = (1-m)R \displaystyle\frac{ N_k}{1 + c N_k}v_k\\
                v_{k+1} &= \displaystyle\frac{m v_k + \frac{1}{2}(1-v_k)}{m v_k + (1-v_k)}
        \end{aligned}\right.
        \end{equation*}
        ''')
        st.markdown("Where $N_k$ tracks the population dynamics while $v_k$ tracks the frequency of virulent nematodes (aa) and $m$ represents the relative proportion of juveniles that develop into virulent males to those that develop into avirulent males")
    
    st.markdown("### Basic reproduction number")
    checkbox = st.checkbox("Read the text")
    if checkbox:
        st.markdown("Several factors compose \textit{G. pallida}'s reproduction number $R$, which is the number of secondary infections generated by a single female, in a susceptible host population, at low nematode density, and in the absence of control.")
        st.markdown("The first one is the number of eggs, $e$, produced by a single female during her reproductive lifespan. The others are the viability of eggs inside the cyst, $1-\mu$, the fraction of eggs which survive accidental hatching in-between seasons, $1-h$, and the survival fraction of larvae in the soil, $s$:")
        st.latex(r'''
            \begin{equation}
                R = e(1-\mu)(1-h)s
            \end{equation}
        ''')
        st.markdown("Multiplying the reproduction number, $R$, by the proportion of female, $(1-m)$, yields the \textit{basic} reproduction number $R(1-m)$, that is the average number of daughters generated by a single mother, in a susceptible host population, and at low nematode density.")
        st.markdown("We model rotations as regular potato cultivation breaks of $r$ years, meaning that the potato is grown once every $r+1$ years. We consider that alternative crops to potato (or the absence of crop) have the same effect on nematodes (no trap-crop is used). We will refer to the $r$ as the ``rotation number''.")
        st.markdown("We model the biocontrol efficacy as the percentage of nematodes that do not survive biocontrol application, $b$ and we consider that biocontrol is applied every year, regardless of whether potato is grown or not.")
        st.markdown("Under these control methods, the reproduction number becomes")
        st.latex(r'''
        \begin{equation*} R' = e\big[(1-\mu)(1-h)(1-b)\big]^{r+1}s\,.
        \end{equation*}
        ''')
        
        markdown_text = r'''
        Blocking resistances quickly become obsolete as the resistance gene is fixed by natural selection. Thus, as with susceptible plants, the long-term suppression of PCNs must be ensured by a biocontrol that brings the nematode reprodution number $R'$ below 1/(1-m).

        On the other hand, masculinizing resistances keep a partial resistance indefinitely. This is conditioned by the male allocation rate $m$. When $m < \frac{1}{2}$, which is the case in real setups, it suffices to ensure the long-term suppression of PCNs
        that control efforts bring the reproduction number $R'$ below $2$. The partial resistance is ensured by the survival
        of susceptible phenotype through the pairing of avirulent males with virulent females.
        '''
        st.markdown(markdown_text)
    
    image2_path = "figs/scenario_diagram.png"
    st.image(image2_path, width=1000)
    
    st.markdown("### Parameters")
    table_md = r'''
    | Parameter | Description | Value | Range |
    | --- | --- | --- | --- |
    | $s$ | Survival fraction of larvae | $25\%$ | [0,100\%] |
    | $m$ | Male fraction in the progeny | $35\%$ | (0, 35\%] |
    | $e$ | Average number of eggs per cyst | 300 | [200, 500] |
    | $\mu$ | Yearly egg mortality | $10\%$ | [0.01, 20\%] |
    | $h$ | Yearly accidental hatching fraction | 17% | [0, 35\%] |
    | $b$ | Biocontrol efficacy fraction | variable | [0, 99.9\%] |
    | $c$ | Intraspecific competition parameter | 0.4 g | [0.1, 0.9] |
    | $\tau$ | Acceptance threshold | 1 egg/g of soil | [1, 3] eggs/g of soil |
    '''
    st.markdown(table_md)

elif main_tab == "Simulation":
    st.markdown("# Simulation")
    
    # Update configuration if needed
    if 'config_df' not in st.session_state or len(st.session_state.config_df) != st.session_state.num_years:
        types = [reverse_mapping[st.session_state.all_types]] * st.session_state.num_years
        bc_values = [st.session_state.all_bc * 100] * st.session_state.num_years
        st.session_state.config_df = pd.DataFrame({
            'Year': range(1, st.session_state.num_years + 1),
            'Type': types,
            'Biocontrol (%)': bc_values
        })
    
    col1, col2, col3 = st.columns([6, 6, 10])
    
    with col1:
        st.button("Reset initial values", on_click=reset_initial_values)
        st.markdown("### Initial values")
        subcol1, subcol2 = st.columns([1, 1])
        with subcol1:
            st.session_state.a_freq = st.slider(
                "Initial frequency of the virulence allele (%):", 
                min_value=0.0, max_value=99.9, 
                value=st.session_state.a_freq * 100, 
                step=0.1
            ) / 100
        with subcol2:
            st.session_state.init_infest = st.slider(
                "Initial infestation (eggs/g of soil):", 
                min_value=0, max_value=80, 
                value=st.session_state.init_infest, 
                step=1
            )
    
    with col2:
        st.button("Reset set up", on_click=reset_setup)
        st.markdown("### Simulation set up")
        subcol1, subcol2 = st.columns([1, 1])
        with subcol1:
            new_num_years = st.number_input(
                "Numb. Years:", 
                min_value=1, max_value=100, 
                value=st.session_state.num_years, 
                step=1,
                key='num_years_input'
            )
            # Update session state if changed
            if new_num_years != st.session_state.num_years:
                st.session_state.num_years = new_num_years
                st.rerun()
                
        with subcol2:
            st.session_state.detection_threshold = st.slider(
                "Acceptance threshold (eggs/g of soil):", 
                min_value=1, max_value=3, 
                value=st.session_state.detection_threshold, 
                step=1
            )
    
    with col3:
        st.markdown("### Configure the deployment")
        subcol1, subcol2 = st.columns([1, 1])
        with subcol1:
            st.session_state.all_bc = st.slider(
                "Biocontrol efficacy all at once (%):", 
                0.0, 100.0, 
                st.session_state.all_bc * 100, 
                1.0
            ) / 100
        with subcol2:
            selected_global_type = st.selectbox(
                "Plant cultivar to deploy each year:", 
                options=list(type_mapping.keys())
                )
            st.session_state.all_types = type_mapping[selected_global_type]
        
        if st.button("Apply to all years", use_container_width=True):
            st.session_state.config_df['Type'] = selected_global_type
            st.session_state.config_df['Biocontrol (%)'] = st.session_state.all_bc * 100
            st.rerun()
    
    colu1, colu2 = st.columns([3, 8])
    
    with colu1:
        edited_df = st.data_editor(
            st.session_state.config_df,
            column_config={
                "Year": st.column_config.NumberColumn("Year", disabled=True),
                "Type": st.column_config.SelectboxColumn(
                    "Plant Type", 
                    options=list(type_mapping.keys())
                ),
                "Biocontrol (%)": st.column_config.NumberColumn(
                    "Biocontrol (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=1.0,
                    format="%.0f%%"
                )
            },
            hide_index=True,
            key="config_editor"
        )
        
        # Update session state if changes detected
        if not edited_df.equals(st.session_state.config_df):
            st.session_state.config_df = edited_df
            st.rerun()
    
    with colu2:
        # Run simulation and display results
        tot, f_A, f_a, X, Y, Z = run_simulation()
        if tot is not None:
            generate_main_plot(tot, f_A, f_a)
        else:
            st.warning("Simulation could not run due to configuration issues. Please check your settings.")

elif main_tab == "Settings":
    st.markdown("# Settings")
    st.markdown("These parameters describe the basic biology of the nematode. They are retrieved from intensive literature review and cautious estimations.")
    st.session_state.s = st.slider("Survival fraction of larvae (%):", min_value=0.0, max_value=100.0, value=st.session_state.s*100, step=0.1)/100
    st.session_state.m = st.slider("Average male fraction in the progeny (%):", min_value=0.0, max_value=40.0, value=st.session_state.m*100, step=0.1)/100
    st.session_state.mu = st.slider("Yearly egg mortality fraction (%):", min_value=0, max_value=20, value=int(st.session_state.mu*100), step=1)/100
    st.session_state.h = st.slider("Yearly accidental hatching fraction (%):", min_value=0, max_value=35, value=int(st.session_state.h*100), step=1)/100
    st.session_state.e = st.slider("Average eggs per cyst:", min_value=200, max_value=500, value=st.session_state.e, step=1)
    st.session_state.c = st.slider("Intraspecific competition parameter:", min_value=0.1, max_value=0.9, value=st.session_state.c, step=0.1)