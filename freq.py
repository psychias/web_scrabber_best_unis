from freq_words import *
from app import *
import plotly.express as px

def app(uni_name):
    data = extract_data(uni_name)
    m = ["Select", "Detail", "Graph"]
    choice = st.selectbox("", m)
    if choice == "Detail":
        st.write("The most Frequent Words used in the tweets are:: ")
        AgGrid(
        data,
        #fit_columns_on_grid_load=False,
        theme='alpine',  # Add theme color to thse table
        #enable_enterprise_modules=True,
        height=700,
        #width='10%',
        reload_data=True
        )
    elif choice == "Select":
        st.write("")
    
    elif choice == "Graph":
        st.write("The chart for the most Frequent Words used in the tweets is: ")
        fig, ax = plt.subplots(figsize=(8,8))
        #d = data.sort_values(by='count')
        #st.bar_chart(data, x='words', y='count',width=400, height=400, use_container_width=True)
        fig = px.bar(data, y='count', x='words', text_auto='.2s')
        st.plotly_chart(fig, use_container_width=True)
        
    #print(data)
    #ax.hist(d, bins = 20)
    #st.pyplot(fig)
