import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import io
from streamlit_extras.stoggle import stoggle 
from markdownlit import mdlit




st.set_page_config(layout="wide", initial_sidebar_state="expanded") 
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; 
        }
    </style>
    """,
    unsafe_allow_html=True,
)



class Compartment:
    def __init__(self, name:str, value:float):
        self.name = name
        self.value = value


class Parameter:
    def __init__(self, name:str, value:float):
        self.name = name
        self.value = value


class Formula:
    def __init__(self, fromcomp, tocomp, formula):
        self.formula = formula
        self.fromcomp = fromcomp 
        self.tocomp = tocomp 

#empty dict
compdict = []
paramdict = []
formdict = []


if 'compdict' in st.session_state:
        compdict = st.session_state['compdict']
else:
        compdict = []
        st.session_state['compdict'] = compdict


if 'paramdict' in st.session_state:
        paramdict = st.session_state['paramdict']
else:
        paramdict = []

        st.session_state['paramdict'] = paramdict


if 'formdict' in st.session_state:
        formdict = st.session_state['formdict']
else:
        formdict = []
        st.session_state['formdict'] = formdict


def header(url):
     st.markdown(f'<p style="background-color:#FFFFFF;color:#000890;font-size:36px;border-radius:1%;padding:\
                  12px;font-weight:bold;text-align: center;\
                  border:3px dashed #000890">{url}</p>', unsafe_allow_html=True)
                  


def header3(url):
     st.markdown(f'<p style="background-color:#0F7DF1;color:#FFFFFF;font-size:15px;border-radius:1%;padding:\
                  12pxc;text-align: center;\
                  border:3px dashed #FFFFFF">{url}</p>', unsafe_allow_html=True)

def header2(url):
     st.markdown(f'<p style="background-color:#F9F9AD;color:#1E1E1E;font-size:30px;border-radius:1%;padding:\
                  12px;font-weight:bold;text-align: left;\
                  border:3px dashed #1E1E1E">{url}</p>', unsafe_allow_html=True)

def subheader(url):
     st.markdown(f'<p style="background-color:#000890;color:#FFFFFF;font-size:17px;border-radius:1%;\
                 padding:8px;font-weight:bold;text-align: center">{url}</p>', unsafe_allow_html=True)

mdlit("[blue]Welcome![/blue] \
      \n \
      This tool will allow you to [blue]model movement across different compartments[/blue] within a population.\
       \n \
      The flow is determined by the models' [blue]formulas which links each compartment[/blue] and the [blue]parameters which define rate[/blue].")

header("Build Your own Compartmental Models")






with st.sidebar:
 header3("Enter Data for Model")    
 timeframe = st.slider("Choose Amount of Days to Run Model:", max_value=365)


 int(timeframe)

 tab1,tab2,tab3 = st.tabs(["1: Compartments","2: Parameters","3: Formulas"])
 col1, col2, col3= st.columns(3)

 
 paramslides = {}
 st.session_state[paramslides] = paramslides

 comps_download = {}
 st.session_state[comps_download] = comps_download
 
 with tab1:

     subheader("Compartments")
     if 'compbutton' not in st.session_state:
         st.session_state.compbutton = False

     def click_compbutton():
       st.session_state.compbutton = not st.session_state.compbutton
     

     st.markdown("####")
     st.button('Enter Compartments', on_click=click_compbutton)

     if st.session_state.compbutton:
      st.text("click button again to hide form")
      with st.form("Compartment Form"):
        name = st.text_input("Enter Compartment Name:")
        value  = st.number_input("Enter Compartment Value")
        if st.form_submit_button("Create New Compartment"):
              comp = Compartment(name,value)
              st.session_state[comp] = comp
              compdict.append(comp)
              st.session_state[compdict] = compdict
              
     


     if 'compbutton2' not in st.session_state:
         st.session_state.compbutton2 = False

     def click_compbutton2():
        st.session_state.compbutton2 = not st.session_state.compbutton2
      
    
     st.button('Upload Compartments', on_click=click_compbutton2)


     if st.session_state.compbutton2:
        comp_file = st.file_uploader("Upload your Compartment file here...")
        if comp_file is not None:
          comps = pd.read_csv(comp_file, index_col=0)
          for idm,row in comps.iterrows():
                  name = idm
                  value1 = row["value"]
                  e = Compartment(name, value1)
                  compdict.append(e)
                  st.session_state[compdict] = compdict
           

    

    
     compdata1 ={(c.name , c.value)for c in compdict}

     compdata4 = pd.DataFrame(compdata1)
    
     compcsv = compdata4.to_csv().encode('utf-8')
     
     compdown = st.download_button('Download Compartments',data = compcsv, file_name ='Compartments.csv', mime ='text/csv') 
     
  
    
     

     

 with tab2:
      subheader("Parameters")
      if 'parabutton2' not in st.session_state:
         st.session_state.parabutton2 = False

      def click_parabutton2():
         st.session_state.parabutton2 = not st.session_state.parabutton2
      
      st.markdown("####")
      
      st.button('Create Parammeters', on_click=click_parabutton2)

      if st.session_state.parabutton2:
          st.text("click button again to hide form")
          with st.form("Parameter Form"):
           name = st.text_input("Enter Parameter Name:")
           value  = st.number_input("Enter Parameter Value")
           if st.form_submit_button("Create New Parameter"):
              para = Parameter(name,value)
              paramdict.append(para)
              st.session_state[paramdict] = paramdict 

     
      if 'parabutton3' not in st.session_state:
         st.session_state.parabutton3= False

      def click_parabutton3():
         st.session_state.parabutton3 = not st.session_state.parabutton3

  
      st.button('Upload Parameters', on_click=click_parabutton3)

      if st.session_state.parabutton3:
         para_file = st.file_uploader("Upload your Parameter file here...")
         if para_file is not None:
              paras = pd.read_csv(para_file, delimiter=',', index_col=0)
              #paras2 = pd.read_csv(para_file)
              for _,row in paras.iterrows():
                  name = row.name
                  value1 = row["value"]
                  for e in paras:
                   e = Parameter(name, value1)
                   paramdict.append(e)
                   st.session_state[paramdict] = paramdict 
            
      
      paradata1 ={(c.name, c.value) for c in paramdict}
      paradict4 = pd.DataFrame(paradata1)
      
      
    

      paracsv = paradict4.to_csv().encode('utf-8')
      paradown = st.download_button('Download Parameters',data = paracsv, file_name ='Parameters.csv', mime ='text/csv')
             




             
 with tab3:
      subheader("Formulas")
      if 'linkbutton' not in st.session_state:
         st.session_state.linkbutton = False

      def click_linkbutton():
         st.session_state.linkbutton = not st.session_state.linkbutton
         
       
      
      st.markdown("####")
      st.button('Create Formulas', on_click=click_linkbutton)

      if st.session_state.linkbutton:
          st.text("click button again to hide form")
          with st.form("Formula Form"):
           formula = st.text_input("Enter Formula:")
           fromcomp = st.text_input("From Compartment:")
           tocomp =  st.text_input("To Compartment:")
           if st.form_submit_button("Create New Formula"):
              link = Formula(fromcomp,tocomp, formula)
              st.session_state[link] = link
              formdict.append(link)
              st.session_state[formdict] = formdict
            



     
      if 'linkbutton2' not in st.session_state:
         st.session_state.linkbutton2= False

      def click_linkbutton2():
         st.session_state.linkbutton2 = not st.session_state.linkbutton2
      
      
     
    
      st.button('Upload Formulas', on_click=click_linkbutton2)

      @st.cache_data
      def read_file(link_file):
               fomps = pd.read_csv(link_file)
               for row in fomps.itertuples():
                   p = (row.fromcomp,row.tocomp,row.formula)
                   formdict.append(Formula(*p))
         
      if st.session_state.linkbutton2:
         link_file = st.file_uploader("Upload you Formula file here...")
         if link_file is not None:
             read_file(link_file)
     
      
       
     
      linkdata1 = {(c.fromcomp,c.tocomp,c.formula) for c in formdict}
      linkdata4 = pd.DataFrame((linkdata1))
      
      

      
      
      
      
      linkcsv = linkdata4.to_csv().encode('utf-8')
      linkdown = st.download_button('Download Formulas',data = linkcsv, file_name ='Formula.csv', mime ='text/csv')
          
      
 subheader("Customize graph")   

 with st.expander("Expand to Customise"):
  graph_tit = st.text_input("Enter Graph Title")
  st.session_state[graph_tit] = graph_tit
  graph_x = st.text_input("Enter X Axis Title")
  st.session_state[graph_x] = graph_x
  graph_y = st.text_input("Enter Y Axis Title")
  st.session_state[graph_y] = graph_y
  graph_legend = st.text_input("Enter Legends Title")
  st.session_state[graph_legend] = graph_legend
  graph_back = st.color_picker("Pick graph background")
  st.session_state[graph_back] = graph_back
 

         
             
                   
               



###subsititue with initial values
##this code evaluates formula and  adds the formula value calulated to the compartment it is flowing to then updates the subs dict to repeat





subs = {c.name: c.value for c in compdict + paramdict}




datacomps = {c.name: c.value for c in compdict}
#Make the name and value a pair for every compartment entered
results = {n: [v] for n, v in datacomps.items()}
# for every pair create a dictionary which starts with the first value entered into the system
results2 = results
 





stoggle("Click me For Help!",""" Population Size should be entered as a Parameter so when Model is run user can change value. \n
Run Model to see Visualisations
    """)    
      
subheader("")
 


if "run" not in st.session_state:
    st.session_state.run = False
def click_run():
    st.session_state.run = not st.session_state.run



tabledata = 1
st.session_state[tabledata] = tabledata

 
if "run" not in st.session_state:
    st.session_state.run = False

def click_run():
    st.session_state.run = not  st.session_state.run 

paramslide = {c.name: c.value for c in paramdict}
    

paramslides.update(paramslide)
st.session_state[paramslides] = paramslides



     #formslist ={df.formula for df in formdict}

name = st.multiselect("Change Parameter Values:", paramslides)

for f in name:
        
        st.write("Change The value of Parameter:", f)
        max= st.number_input ("Pick Max value", key = f+f)
        min = st.number_input("Pick Min Value", key = f+f+f+f)
        steps = st.number_input("Pick Increment Value", key = f+f+f)
        max = float(max)
        value = st.slider("Slide to Change", key = f, min_value= 0.00, max_value= max, step= steps)
        st.markdown("#")
        subs[f] = value
        st.session_state[subs] = subs



run = st.button("Run Model", on_click = click_run)




if st.session_state.run:
 

 
 

     
     
      
     for a in range(timeframe):
       for d in formdict:
              for w in results2:  #for every formula entered check for every compartment dict 
               formula_Answer = eval(d.formula,subs) #eval and sub formula
               initial_from_comp_val = eval(d.fromcomp,subs)
               initial_to_comp_val = eval(d.tocomp,subs) #val of initial comp formula is linking from
               new_from_comp_val = initial_from_comp_val - formula_Answer
               new_to_comp_val = initial_to_comp_val + formula_Answer #add formula answer to initial from cop to cal next day val
               if w == d.tocomp: #when compartment dict =   compartment formula is linking to
                   results[w].append(new_to_comp_val) #for every initial compartment dict, add the calulated new comp valu
                   subs[w] = new_to_comp_val
                       
     
      
     subheader("Visualise Model")
     tab4,tab5, tab6 = st.tabs(["Animated Graph", "Customisied Graph", "Model Data"])
     with tab4:
      df  = pd.DataFrame.from_dict(results2)
      df2 = df.head(timeframe)
      df2.index.names = [graph_x]
      column_names = list(df.columns.values)
      column_names = list(df.columns.values)

      
      fig1 = px.scatter(df2, x = df2.index,
                     y = df2.columns, title= graph_tit, animation_frame = df2.index,
                     labels={'x': graph_x, 'y': graph_y},
                    range_x =[0, timeframe])
      

   
      
      fig1.update_traces(mode="markers", hovertemplate=None)
      fig1.update_layout(hovermode="x unified", showlegend = True, legend_title = graph_legend)

    
      st.write("Give X axis a Name to animate!")
      st.write(fig1)

     with tab5:
      ax = df2.plot(kind='line', title =graph_tit, legend=True, figsize=(9,4))
      ax.set_xlabel(graph_x, fontsize=10)

      ax.set_ylabel(graph_y)
      ax.set_title(graph_tit)
      ax.legend(title = graph_legend)
      ax.set_facecolor(graph_back)
      fig = ax.figure 
      st.pyplot(fig)
      fig = 'scatter.png'
      img = io.BytesIO()
      plt.savefig(img, format='png')
      btn = st.download_button(
                label="Download Graph as Image",
                data=img,
                file_name=fig,
                mime="image/png"
                )
      csv = df2.to_csv().encode('utf-8')
     with tab6:
      
      
      st.download_button(
      label="Download Data as CSV",
      data=csv,
      file_name='model_data.csv',
      mime='text/csv',
      )
      st.write(df2)


