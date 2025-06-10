#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import hydralit_components as hc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Set page layout to centered and responsive
# st.set_page_config(layout="wide")
st.set_page_config(layout='wide',initial_sidebar_state='collapsed')


# specify the primary menu definition
menu_data = [
    {'icon': "far fa-copy", 'label':"Model & Parameters"},
    {'icon': "far fa-chart-bar", 'label':"Simulation"},#no tooltip message
    #{'icon': "fas fa-chart-line", 'label':"Genetic Drift"},
    {'icon': "fas fa-tachometer-alt", 'label':"Settings"},
    #{'icon': "fas fa-download", 'label':"Download report"},
]

over_theme = {'txc_inactive': '#FFFFFF', 'menu_background':'#85929E'}
st.markdown("# Nemo")
main_tab= hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Introduction',
    #login_name='Logout',
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)


# Define default parameter values
st.session_state.setdefault("a_freq", 0.1)
st.session_state.setdefault("init_infest", 40)
st.session_state.setdefault("s", 0.25)
st.session_state.setdefault("m", 0.35)
st.session_state.setdefault("h", 0.17)
st.session_state.setdefault("mu", 0.10)
st.session_state.setdefault("c", 0.4)
st.session_state.setdefault("e", 300)
st.session_state.setdefault("detection_threshold", 1)
st.session_state.setdefault("num_years", 10)
st.session_state.setdefault("bc_vector", [])
st.session_state.setdefault("all_bc", 0.0)
st.session_state.setdefault("all_types", 1)
st.session_state.setdefault("plant_type_vector", [])
step = 0.01
                            

# Define parameter values for reset
st.session_state.setdefault("reset_a_freq", 0.1)
st.session_state.setdefault("reset_init_infest", 30)
st.session_state.setdefault("reset_s", 0.25)
st.session_state.setdefault("reset_m", 0.35)
st.session_state.setdefault("reset_h", 0.17)
st.session_state.setdefault("reset_mu", 0.10)
st.session_state.setdefault("reset_c", 0.4)
st.session_state.setdefault("reset_e", 300)
st.session_state.setdefault("reset_detection_threshold", 1)
st.session_state.setdefault("reset_num_years", 10)
st.session_state.setdefault("reset_all_bc", 0.0)

# Set Streamlit app title
#st.title("Nemo")
def dec2(x):
    d = round(x * 100) / 100
    return d
# def ratio(u,r):
    # r_attrib = []
    # for val in u:
        # if val == 0:
            # r_attrib.append(r)
        # else:
            # r_attrib.append(1)
    # return r_attrib

# def attrib_constants(u,r):
    # M_A = [st.session_state.s * r_attributed for r_attributed in ratio(u,r)]
    # M_a = [st.session_state.s * r] * len(u)
    # F_A = [(st.session_state.s * (1 - r_attributed)) for r_attributed in ratio(u,r)]
    # F_a = [st.session_state.s * (1 - r)] * len(u)
    # return M_A, M_a, F_A, F_a

# def generate_deployment_vector(input_string):
    # temp = ""
    # n_count = 0

    # for char in input_string:
        # if char == "N":
            # n_count += 1
        # else:
            # if n_count > 0:
                # temp += str(n_count)
                # n_count = 0

            # if temp and (temp[-1] == char or (temp[-1] == "S" and char == "R") or (temp[-1] == "R" and char == "S")):
                # temp += "0"
            # temp += char

    # if n_count > 0:
        # temp += str(n_count)

    # deployment = ""
    # jn = []

    # num_buffer = ""
    # for char in temp:
        # if char.isdigit():
            # num_buffer += char
        # else:
            # if num_buffer:
                # jn.append(int(num_buffer))
                # num_buffer = ""
            # deployment += char

    # if num_buffer:
        # jn.append(int(num_buffer))

    # jn_vector = [int(num) for num in jn]  # Convert jn to int vector
    # deployment_vector = [1 if char == 'R' else 0 for char in deployment]
    # if len(jn_vector)==len(deployment_vector):
        # jn_vector = jn_vector[:-1] # To discard deployment ended by Non-Host
    # return deployment_vector, jn_vector
def round1d(number):
    return round(number, 1)      
def generate_main_plot(tot,f_A, f_a, Y, Z):
    fig, ax = plt.subplots(figsize=(14, 10), dpi=100)
    nb_gen = len(tot)
    ax.plot(np.arange(0, nb_gen), tot, '-r', linewidth=3)
    th = st.session_state.detection_threshold
    ax.plot([0, nb_gen-1], [th, th], 'k--', label='Acceptance threshold')
    ax.set_xlabel("Year", fontsize=30)
    ax.set_ylabel("PCNs/g of soil", fontsize=30)
    ax.set_xlim([0, nb_gen-1])
    #ax.set_ylim([10**(-6), st.session_state.K])
    #ax.set_yscale('log')
    tick_locations = list(range(20,np.ceil(max(tot)).astype('int'),20))
    tick_locations.append(th)
    tick_labels = [str(val) for val in [0] + tick_locations[1:]]
    ax.set_yticks(tick_locations, tick_labels)
    ax.tick_params(axis='both', which='major', labelsize=30)
    ax.legend(fontsize=15)
    # Create two columns with widths in the ratio 2:1
    col1, col2 = st.columns([2, 1])
    with col1:
        # Display the plot in Streamlit
        st.pyplot(fig)
    with col2:
        # Upper plot
        with st.expander("Frequency of avirulence allele A"):
            # Create a new figure and axes
            fig_upper, ax_upper = plt.subplots(figsize=(8, 5), dpi=100)

            # Plot the upper plot data
            ax_upper.plot(np.arange(0, nb_gen), f_A, linewidth=3)
            ax_upper.set_xlabel("Year", fontsize=30)
            #ax_upper.set_ylabel("Frequency of allele A")
            #ax_upper.set_title("Frequency of allele avirulence A", fontsize=40)
            ax_upper.tick_params(axis='both', which='major', labelsize=30)

            # Display the upper plot using Streamlit's pyplot function
            st.pyplot(fig_upper)

        # Lower plot
        with st.expander("Frequency of virulence allele a"):
            # Create a new figure and axes
            fig_lower, ax_lower = plt.subplots(figsize=(8, 5), dpi=100)

            # Plot the lower plot data
            ax_lower.plot(np.arange(0, nb_gen), f_a, linewidth=3)
            ax_lower.set_xlabel("Year", fontsize=30)
            #ax_lower.set_ylabel("Frequency of allele a")
            #ax_lower.set_title("Frequency of allele virulence a", fontsize=40)
            ax_lower.tick_params(axis='both', which='major', labelsize=30)
            # Display the lower plot using Streamlit's pyplot function
            st.pyplot(fig_lower)



# Main tab
#with st.sidebar:
#    main_tab = st.radio("Navigation", ["Introduction", "Model & Parameters", "Simulation", "Settings"])

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
    # Define the paths to your logo images
    logo_paths = ["figs/logo_agro.png", "figs/logo_igepp.png", "figs/logo_inrae.png", "figs/logo_inov3pt.png"]
        # Display the logos side by side with the same size and centered
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
    #st.markdown("In this table as in the simulation, the **efficacy of biocontrol** is modulable and we can analyze its effect on the PCN reproduction number and suppression. Other modulable parameters for simulation are the **initial frequency of virulence allele** and the **initial soil infestation**.")
    #st.markdown("The detection threshold defines the PCN level below which the field is considered clean")
    st.markdown("The simulation allows to choose the plant cultivar which is deployed per season. The other parameters, very little variable and estimated on literature data, are in the Settings menu.")
    # Create a checkbox to toggle the hidden content
    #checkbox = st.checkbox("See the general model")
    # if checkbox:
        # st.markdown("- More generally, under arbitrary deployment of susceptible and resistant plants, the model reads:")
        # st.latex(r'''
        # \begin{equation*}
            # \left\{\begin{aligned}
            # X_{k+1} &= \frac{G_{j_k} M}{M + (X_k+Y_k+Z_k)} \displaystyle\frac{M_A(k)F_A(k)\big(X_k + \frac{1}{2}Y_k\big)^2}{M_A(k)(X_k+Y_k) + M_a(k)Z_k}, \\
        # \\
        # Y_{k+1} &=  \frac{G_{j_k} M}{M + (X_k+Y_k+Z_k)}  \displaystyle\frac{M_A(k)\big(F_a(k)Z_k + \frac{1}{2}F_A(k)Y_k \big)\big(X_k + \frac{1}{2}Y_k \big) + F_A(k)\big(X_k + \frac{1}{2}Y_k \big)\big(M_a(k)Z_k + \frac{1}{2}M_A(k)Y_k \big) }{M_A(k)(X_k+Y_k) + M_a(k)Z_k},\\
        # \\
        # Z_{k+1} &= \frac{G_{j_k} M}{M + (X_k+Y_k+Z_k)} \displaystyle\frac{\big(F_a(k)Z_k + \frac{1}{2}F_A(k)Y_k\big)\big(M_a(k)Z_k + \frac{1}{2}M_A(k)Y_k\big)}{M_A(k)(X_k+Y_k) + M_a(k)Z_k},
        # \end{aligned}\right.
    # \end{equation*}
        # ''')
        # st.markdown("Where $F_A$ (resp. $F_a$) is the proportion larvae that becomes avirulent (resp. virulent) female adults, $G_{j_k}$ is the generation $k$'s growth factor ($G_{j_k} = e[w(1-h_a)(1-b)]^{j_k+1}$ ) provided there is are $j_k$-year rotations after generation $k$, and $M$ is a limiting factor.")
    # # Add a link to expand/collapse the hidden content
    # #st.markdown("[Expand / Collapse](javascript:void(0);)")
    
    
elif main_tab == "Simulation":
    st.markdown("# Simulation")
    # Other parameters
    col1, col2, col3 = st.columns([6, 6, 10])
    with col1:
        if st.button("Reset initial values"):
            st.session_state.a_freq = st.session_state.reset_a_freq
            st.session_state.init_infest = st.session_state.reset_init_infest
        st.markdown("### Initial values")
        subcol1, subcol2 = st.columns([1,1])
        with subcol1:
            st.session_state.a_freq = st.slider("Initial frequency of the virulence allele (%):", min_value=0.0, max_value=99.9, value=st.session_state.a_freq*100, step=0.1)/100
        with subcol2:
            st.session_state.init_infest = st.slider("Initial infestation (eggs/g of soil):", min_value=0, max_value=80, value=st.session_state.init_infest, step=1)
        
    with col2:
        if st.button("Reset set up"):
            st.session_state.num_years = st.session_state.reset_num_years
            st.session_state.detection_threshold = st.session_state.reset_detection_threshold
        st.markdown("### Simulation set up")
        subcol1, subcol2 = st.columns([1,1])
        with subcol1:
            st.session_state.num_years = st.number_input("Numb. Years:", min_value=1, max_value=100, value=st.session_state.num_years, step=1)
        with subcol2:
            st.session_state.detection_threshold = st.slider(f"Acceptance threshold (eggs/g of soil):", min_value=1, max_value=3, value=st.session_state.detection_threshold, step=1)    
    with col3:
        st.markdown("### Configure the deployment")
        
        # Define plant type mappings
        type_mapping = {'Susceptible': 1, 'M. Resistant': 2, 'Rotation': 0}
        reverse_mapping = {v: k for k, v in type_mapping.items()}
        
        # Initialize/update DataFrame in session state
        if 'config_df' not in st.session_state or len(st.session_state.config_df) != st.session_state.num_years:
            types = [reverse_mapping[st.session_state.all_types]] * st.session_state.num_years
            bc_values = [st.session_state.all_bc * 100] * st.session_state.num_years  # Store as percentages
            st.session_state.config_df = pd.DataFrame({
                'Year': range(1, st.session_state.num_years + 1),
                'Type': types,
                'Biocontrol (%)': bc_values
            })
        
        # Global configuration controls
        subcol1, subcol2 = st.columns([1, 1])
        with subcol1:
            st.session_state.all_bc = st.slider(
                "Biocontrol efficacy all at once (%):", 
                0.0, 100.0, st.session_state.all_bc * 100, 1.0
            ) / 100  # Convert back to fraction
        with subcol2:
            selected_global_type = st.selectbox(
                "Plant cultivar to deploy each year:", 
                options=list(type_mapping.keys())
            )
            st.session_state.all_types = type_mapping[selected_global_type]
        
        # Apply global settings to all years
        if st.button("Apply to all years", use_container_width=True):
            st.session_state.config_df['Type'] = selected_global_type
            st.session_state.config_df['Biocontrol (%)'] = st.session_state.all_bc * 100
    colu1, colu2 = st.columns([3,8])  
    with colu1:
        # Data Editor for per-year configuration
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
        
        # Update session state with edited values
        st.session_state.config_df = edited_df
        
        # Convert to vectors for model input
        plant_type_vector = [type_mapping[t] for t in edited_df['Type']]
        bc_vector = [x / 100 for x in edited_df['Biocontrol (%)']]  # Convert to fractions
    with colu2:
        st.session_state.plant_type_vector = plant_type_vector
        st.session_state.bc_vector = bc_vector
        X = np.zeros(st.session_state.num_years+1)
        Y = np.zeros(st.session_state.num_years+1)
        Z = np.zeros(st.session_state.num_years+1)
        init_juveniles = st.session_state.init_infest
        J_AA_0 = init_juveniles * (1-st.session_state.a_freq)**2
        J_Aa_0 = init_juveniles * 2 * st.session_state.a_freq*(1-st.session_state.a_freq)
        J_aa_0 = init_juveniles * (st.session_state.a_freq)**2
        X[0] = J_AA_0
        Y[0] = J_Aa_0
        Z[0] = J_aa_0
        k=0
        for plant_type in st.session_state.plant_type_vector:
            #st.markdown(str(X[k]))
            #st.markdown(str(Y[k]))
            #st.markdown(str(Z[k]))
            R = (1-st.session_state.m)*st.session_state.e*st.session_state.s*((1-st.session_state.mu)*(1-st.session_state.h)*(1-st.session_state.bc_vector[k]))  
            M = 1/st.session_state.c  # as K = (R-1)/c and M = K/(R-1)
            if plant_type == 1:
                X[k+1] = round1d(R*M*(X[k]+0.5*Y[k])**2/((M+X[k]+Y[k]+Z[k])*(X[k]+Y[k]+Z[k])))
                Y[k+1] = round1d(2*R*M*(X[k]+0.5*Y[k])*(Z[k]+0.5*Y[k])/((M+X[k]+Y[k]+Z[k])*(X[k]+Y[k]+Z[k])))
                Z[k+1] = round1d(R*M*(Z[k]+0.5*Y[k])**2/((M+X[k]+Y[k]+Z[k])*(X[k]+Y[k]+Z[k])))
            if plant_type == 2:
                X[k+1] = 0
                Y[k+1] = round1d(R*M*Z[k]*(X[k]+0.5*Y[k])/((M+X[k]+Y[k]+Z[k])*(X[k]+Y[k]+st.session_state.m*Z[k])))
                Z[k+1] = round1d(R*M*Z[k]*(st.session_state.m*Z[k]+0.5*Y[k])/((M+X[k]+Y[k]+Z[k])*(X[k]+Y[k]+st.session_state.m*Z[k])))   
            if plant_type == 0:
                X[k+1] = round1d(((1-st.session_state.mu)*(1-st.session_state.h)*(1-st.session_state.bc_vector[k]))*X[k])
                Y[k+1] = round1d(((1-st.session_state.mu)*(1-st.session_state.h)*(1-st.session_state.bc_vector[k]))*Y[k])
                Z[k+1] = round1d(((1-st.session_state.mu)*(1-st.session_state.h)*(1-st.session_state.bc_vector[k]))*Z[k])
            k+=1
        tot = X + Y + Z
        f_AA = np.zeros(st.session_state.num_years+1)
        f_Aa = np.zeros(st.session_state.num_years+1)
        f_aa = np.zeros(st.session_state.num_years+1)
        f_A = np.zeros(st.session_state.num_years+1)
        f_a = np.zeros(st.session_state.num_years+1)

        for n in range(st.session_state.num_years+1):
            if tot[n] == 0:
                f_AA[n] = 0
                f_Aa[n] = 0
                f_aa[n] = 0
            else:
                f_AA[n] = X[n] / tot[n]
                f_Aa[n] = Y[n] / tot[n]
                f_aa[n] = Z[n] / tot[n]
            
            f_A[n] = f_AA[n] + f_Aa[n] / 2
            f_a[n] = f_aa[n] + f_Aa[n] / 2          
        generate_main_plot(tot,f_A, f_a, Y, Z)
    
elif main_tab == "Settings":
    st.markdown("# Settings")
    st.markdown("These parameters describe the basic biology of the nematode. They are retrieved from intensive literature review and cautious estimations.")
    st.session_state.s = st.slider("Survival fraction of larvae (%):", min_value=0.0, max_value=100.0, value=st.session_state.s*100, step=0.1)/100
    st.session_state.m = st.slider("Average male fraction in the progeny (%):", min_value=0.0, max_value=40.0, value=st.session_state.m*100, step=0.1)/100
    st.session_state.mu = st.slider("Yearly egg mortality fraction (%):", min_value=0, max_value=20, value=int(st.session_state.mu*100), step=1)/100
    st.session_state.h = st.slider("Yearly accidental hatching fraction (%):", min_value=0, max_value=35, value=int(st.session_state.h*100), step=1)/100
    st.session_state.e = st.slider("Average eggs per cyst:", min_value=200, max_value=500, value=st.session_state.e, step=1)
    st.session_state.c = st.slider("Intraspecific competition parameter:", min_value=0.1, max_value=0.9, value=st.session_state.c, step=0.1)
