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
st.session_state.setdefault("init_infest", 80)
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
st.session_state.setdefault("reset_init_infest", 80)
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
            st.session_state.init_infest = st.slider("Initial infestation (eggs/g of soil):", min_value=0, max_value=170, value=st.session_state.init_infest, step=1)
        
    with col2:
        if st.button("Reset set up"):
            st.session_state.num_years = st.session_state.reset_num_years
            st.session_state.detection_threshold = st.session_state.reset_detection_threshold
        st.markdown("### Simulation set up")
        subcol1, subcol2 = st.columns([1,1])
        with subcol1:
            st.session_state.num_years = st.number_input("Enter the number of years of simulation:", min_value=1, max_value=100, value=st.session_state.num_years, step=1)
        with subcol2:
            st.session_state.detection_threshold = st.slider(f"Acceptance threshold (eggs/g of soil):", min_value=1, max_value=3, value=st.session_state.detection_threshold, step=1)    
    with col3:
        st.markdown("## Configure the deployment")
        subcol1, subcol2 = st.columns([1,1])
        with subcol1:
            st.session_state.all_bc = st.slider("Biocontrol efficacy all at at once (%):", 0.0, 100.0, st.session_state.all_bc*100, 1.0)/100
        with subcol2:
            option_dic = {'Susceptible': 1, 'M. Resistant': 2, 'Rotation': 0}
            selected_all_types = st.selectbox("Plant cultivar to deploy each year:", options=list(option_dic.keys()))
            st.session_state.all_types = option_dic[selected_all_types]  # Store the selected value in session state
        subsubcol1, subsubcol2, subsubcol3 = st.columns([2,2,3])
        with subsubcol1:
            # Create a scrolling menu to select the year
            selected_year = st.selectbox("Select the year to reconfigure:", range(1, st.session_state.num_years + 1))
            if 'bc_dic' not in st.session_state:
                st.session_state.bc_dic = {}
            for k in range(1, st.session_state.num_years + 1):
                st.session_state.bc_dic[k] = st.session_state.all_bc
        with subsubcol2:
            # Initialize session state to store slider values of the biocontrol
            if 'bc_dic' not in st.session_state:
                st.session_state.bc_dic = {}
            # Initialize session state to store plant type values
            if 'plant_type_dic' not in st.session_state:
                st.session_state.plant_type_dic = {}
            # Create plant type input for each year and show/hide based on the selected year
            for k in range(1, st.session_state.num_years + 1):
                year_name = f"Year {k}"
                if k == selected_year:
                    # Use the stored value if available, otherwise initialize to all_types
                    option_dic = {'Susceptible': 1, 'M. Resistant': 2, 'Rotation': 0}
                    selected_plant_type = st.selectbox(f"Cultivar deployed at {year_name}:", options=list(option_dic.keys()))
                    st.session_state.plant_type_dic[k] = option_dic[selected_plant_type]  # Store the selected value in session state
                else:
                    # If it's not the selected season, show the stored value without the slider
                    selected_plant_type = st.session_state.plant_type_dic.get(k, st.session_state.all_types) 
        with subsubcol3:
            # Create biocontrol sliders for each year and show/hide based on the selected year
            for k in range(1, st.session_state.num_years + 1):
                year_name = f"Year {k}"
                if k == selected_year:
                    # Use the stored value if available, otherwise initialize to 0.0
                    biocontrol = st.slider(f"Biocontrol efficacy at {year_name} (%):", 0.0, 100.0, st.session_state.bc_dic.get(k, 0.0)*100, 1.0, key=f"slider_{k}")/100
                    st.session_state.bc_dic[k] = biocontrol  # Store the slider value in session state
                else:
                    # If it's not the selected season, show the stored value without the slider
                    biocontrol = st.session_state.bc_dic.get(k, 0.0)
                
        # Create a vector from the dictionnaries
        st.session_state.plant_type_vector = [st.session_state.plant_type_dic.get(k, st.session_state.all_types) for k in range(1, st.session_state.num_years + 1)]
        st.session_state.bc_vector = [st.session_state.bc_dic.get(k, 0.0) for k in range(1, st.session_state.num_years + 1)]
        
    # Create a DataFrame for display
    data = {
        'Year': ['Year'] + list(range(1, st.session_state.num_years + 1)),
        'Type': ['Type'] + ['X' if x == 0 else 'S' if x == 1 else 'R' for x in st.session_state.plant_type_vector],
        'Biocontrol': ['Biocontrol'] + [x for x in st.session_state.bc_vector],
    }
    df = pd.DataFrame(data)
    # Transpose the DataFrame and display the table without indexes
    transposed_df = df.transpose()
    transposed_df = transposed_df.rename_axis('Year')
    st.data_editor(transposed_df.iloc[1:, 1:],num_rows="dynamic",use_container_width=True)
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
    ############################
# if main_tab == "Genetic Drift":
    # def generate_drift_plot(tot_matrix,f_A_matrix,f_a_matrix):
        # fig_drift, ax = plt.subplots(figsize=(14, 10), dpi=100)
        # simu, nb_gen = tot_matrix.shape
        # #st.markdown(str(f_a_matrix))
        # for si in range(simu):
            # ax.plot(np.arange(0, nb_gen), tot_matrix[si,:], '-r', linewidth=1)
        # th = st.session_state.detection_threshold
        # ax.plot([0, nb_gen-1], [th, th], 'k--', label='Healthiness threshold')
        # ax.set_xlabel("Year", fontsize=30)
        # ax.set_ylabel("PCNs/g of soil (50 simulations)", fontsize=25)
        # ax.set_xlim([0, nb_gen-1])
        # ax.set_ylim([10**(-6), st.session_state.K])
        # tick_locations = list(range(0,st.session_state.K,20))
        # tick_locations.append(th)
        # tick_labels = [str(val) for val in [0] + tick_locations[1:]]
        # ax.set_yticks(tick_locations, tick_labels)
        # ax.tick_params(axis='both', which='major', labelsize=30)
        # ax.legend(fontsize=15)
        # # Create two columns with widths in the ratio 2:1
        # col1, col2 = st.columns([2, 1])
        # with col1:
            # # Display the plot in Streamlit
            # st.pyplot(fig_drift)
        # with col2:
            # # Upper plot
            # with st.expander("Frequency of avirulence allele A"):
                # # Create a new figure and axes
                # fig_drift_upper, ax_upper = plt.subplots(figsize=(8, 5), dpi=100)

                # # Plot the upper plot data
                # for si in range(simu):
                    # ax_upper.plot(np.arange(0, nb_gen), f_A_matrix[si,:], '-b', linewidth=1)
                # ax_upper.set_xlabel("Year", fontsize=30)
                # #ax_upper.set_ylabel("Frequency of allele A")
                # #ax_upper.set_title("Frequency of allele avirulence A", fontsize=40)
                # ax_upper.tick_params(axis='both', which='major', labelsize=30)

                # # Display the upper plot using Streamlit's pyplot function
                # st.pyplot(fig_drift_upper)

            # # Lower plot
            # with st.expander("Frequency of virulence allele a"):
                # # Create a new figure and axes
                # fig_drift_lower, ax_lower = plt.subplots(figsize=(8, 5), dpi=100)

                # # Plot the lower plot data
                # for si in range(simu):
                    # ax_lower.plot(np.arange(0, nb_gen), f_a_matrix[si,:], '-b', linewidth=1)
                # ax_lower.set_xlabel("Year", fontsize=30)
                # #ax_lower.set_ylabel("Frequency of allele a")
                # #ax_lower.set_title("Frequency of allele virulence a", fontsize=40)
                # ax_lower.tick_params(axis='both', which='major', labelsize=30)
                # # Display the lower plot using Streamlit's pyplot function
                # st.pyplot(fig_drift_lower)
                
    # ##############################################
    # X = np.zeros(st.session_state.num_years+1)
    # Y = np.zeros(st.session_state.num_years+1)
    # Z = np.zeros(st.session_state.num_years+1)
    # init_juveniles = st.session_state.init_infest
    # J_AA_0 = init_juveniles * (1-st.session_state.a_freq)**2
    # J_Aa_0 = init_juveniles * 2 * st.session_state.a_freq*(1-st.session_state.a_freq)
    # J_aa_0 = init_juveniles * (st.session_state.a_freq)**2
    # X[0] = J_AA_0
    # Y[0] = J_Aa_0
    # Z[0] = J_aa_0
    # n_simulations = 50
    # tot_matrix = np.zeros((n_simulations,st.session_state.num_years+1))
    # f_A_matrix = np.zeros((n_simulations,st.session_state.num_years+1))
    # f_a_matrix = np.zeros((n_simulations,st.session_state.num_years+1))
    # for simulate in range(n_simulations):
        # k=0
        # for plant_type in st.session_state.plant_type_vector:
            # R = (1-st.session_state.m)*st.session_state.e*st.session_state.s*((1-st.session_state.mu)*(1-st.session_state.h)*(1-st.session_state.bc_vector[k]))
            # M = st.session_state.K/(R-1)
            # #############
            # if X[k] + Y[k] + Z[k] == 0:
                # X[k+1] = 0
                # Y[k+1] = 0
                # Z[k+1] = 0
            # else:
                # if plant_type == 1:    
                    # Pf = (1-st.session_state.m) * (X[k] + Y[k] / 2) / ((1-st.session_state.m)* (X[k] + Y[k]) + (1-st.session_state.m) * Z[k])
                    # Qf = 1 - Pf
                    # Pm = st.session_state.m * (X[k] + Y[k] / 2) / (st.session_state.m * (X[k] + Y[k]) + st.session_state.m * Z[k])
                    # Qm = 1 - Pm
                    # offspring = (R/((1-st.session_state.m)*st.session_state.e)) * M*((1-st.session_state.m)* (X[k] + Y[k]) + (1-st.session_state.m) * Z[k]) * np.random.multinomial(st.session_state.e, [Pf * Pm, Pf * Qm + Pm * Qf, Qf * Qm]) / (M + X[k] + Y[k] + Z[k])
                # if plant_type == 2:    
                    # Pf = 0
                    # Qf = 1
                    # Pm = (X[k] + Y[k] / 2) / ((X[k] + Y[k]) + st.session_state.m * Z[k])
                    # Qm = 1 - Pm
                    # offspring = (R/((1-st.session_state.m)*st.session_state.e)) * M * (1-st.session_state.m) * Z[k] * np.random.multinomial(st.session_state.e, [Pf * Pm, Pf * Qm + Pm * Qf, Qf * Qm]) / (M + X[k] + Y[k] + Z[k])
                # if plant_type == 0:
                    # offspring = ((1-st.session_state.mu)*(1-st.session_state.h)*(1-st.session_state.bc_vector[k]))*np.array([X[k], Y[k], Z[k]])
                    
                # X[k+1] = round1d(offspring[0])
                # Y[k+1] = round1d(offspring[1])
                # Z[k+1] = round1d(offspring[2]) 
            # k=k+1
        # tot = X + Y + Z
        # f_AA = np.zeros(st.session_state.num_years+1)
        # f_Aa = np.zeros(st.session_state.num_years+1)
        # f_aa = np.zeros(st.session_state.num_years+1)
        # f_A = np.zeros(st.session_state.num_years+1)
        # f_a = np.zeros(st.session_state.num_years+1)

        # for n in range(st.session_state.num_years+1):
            # if tot[n] == 0:
                # f_AA[n] = 0
                # f_Aa[n] = 0
                # f_aa[n] = 0
            # else:
                # f_AA[n] = X[n] / tot[n]
                # f_Aa[n] = Y[n] / tot[n]
                # f_aa[n] = Z[n] / tot[n]
            
            # f_A[n] = f_AA[n] + f_Aa[n] / 2
            # f_a[n] = f_aa[n] + f_Aa[n] / 2  
        # tot_matrix[simulate,:] = tot
        # f_A_matrix[simulate,:] = f_A
        # f_a_matrix[simulate,:] = f_a
    # generate_drift_plot(tot_matrix,f_A_matrix, f_a_matrix)
    
elif main_tab == "Settings":
    st.markdown("# Settings")
    st.markdown("These parameters describe the basic biology of the nematode. They are retrieved from intensive literature review and cautious estimations.")
    st.session_state.s = st.slider("Survival fraction of larvae (%):", min_value=0.0, max_value=100.0, value=st.session_state.s*100, step=0.1)/100
    st.session_state.m = st.slider("Average male fraction in the progeny (%):", min_value=0.0, max_value=40.0, value=st.session_state.m*100, step=0.1)/100
    st.session_state.mu = st.slider("Yearly egg mortality fraction (%):", min_value=0, max_value=20, value=int(st.session_state.mu*100), step=1)/100
    st.session_state.h = st.slider("Yearly accidental hatching fraction (%):", min_value=0, max_value=35, value=int(st.session_state.h*100), step=1)/100
    st.session_state.e = st.slider("Average eggs per cyst:", min_value=200, max_value=500, value=st.session_state.e, step=1)
    st.session_state.c = st.slider("Intraspecific competition parameter:", min_value=0.1, max_value=0.9, value=st.session_state.c, step=0.1)
