from app import *
from freq_words import *
import itertools
def app(uni_name):
    st.write("Current and Past Students of ", uni_name)
    df = pd.read_csv("students.csv")
    #st.write(df[df['name'] == uni_name])
    data = df.loc[df['name'] == uni_name, ['current', 'past']]
    
    #df.loc[:,'current':'past']]
    
    data = data.loc[:, :].values.tolist()
    data = list(itertools.chain(*data))
    print(data)
    # assign data of lists.  
    df2 = {'Type': ['Current Students', 'Past Students'], 'Total': data}

    # Create DataFrame  
    df2 = pd.DataFrame(df2)
    print(df2)
    fig, ax = plt.subplots(figsize=(8,8))
        #d = data.sort_values(by='count')
    st.bar_chart(df2, x='Type', y='Total',width=100, height=400, use_container_width=True)
        
#app("Stanford University")