import plotly.graph_objects as go 

labels= ["Source A ","Source B","Source C","Target X","Target Y","Target Z"]

source = [0,1,0,2,3,3,4]
target = [3,3,4,4,5,5,5]
values = [8,4,2,8,4,2,3]


fig = go.Figure(data=[go.Sankey(node=dict(pad=15,thickness=20,line=dict(color="black",width=0.5),label=labels),link=dict(source=source,target=target,value=values))])

fig.update_layout(title_text="Basic Sanky Diagram",font_size=10)
fig.show()