import os
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go

Z0='#ffffff'; Z1='#333333'; Z2='#666666'; Z3='#999999';Z4='#cccccc'
R0='#D62728'; R1='#EE3A43'; R2='#f37279'; R3='#f9b9bc'
O0='#FF7F0E';O1='#ffad66'; O2='#ffd6b3'
B0='#1F77B4'; B1='#51a5e1'; B2='#a8d2f0'
G0='#2CA02C'; G1='#5fd35f'; G2='#9be49b'; G3='#d7f4d7'
Y0='#fecb01'; Y1='#fedb4d'; Y2='#feea9a'
V0='#ace600'; V1='#d2ff4d'; V2='#ecffb3'
p1='#FDE725';p2='#9FDA3A';p3='#4AC16D';p4='#1FA187';p5='#277F8E';p6='#365C8D';p7='#46337E';p8='#440154';

## **NOTE**: following trick to **save file in `eps` format**
def save_plot(fig, plot_name):
    py.plot(fig, show_link=False, image='svg', auto_open=True)

# #call the following in a different cell or after sleep
def move_plot(plot_name,from_dir,to_dir):
     os.environ['plot_name']=plot_name
     os.environ['from_dir']=from_dir
     os.environ['to_dir']=to_dir
     os.system("mv ${from_dir}/plot_image.svg ${to_dir}/${plot_name}.svg")

def convert_plot(plot_name,to_dir):
    # this generates a warning on MacOS
     os.environ['plot_name']=plot_name
     os.environ['to_dir']=to_dir
     # os.system('/Applications/Inkscape.app/Contents/Resources/script -z -d 300 "${to_dir}/${plot_name}.svg" --export-png="${PWD}/img/${plot_name}.png"')  # for png
     os.system('inkscape "${to_dir}/${plot_name}.svg" -E "${to_dir}/${plot_name}.eps" --export-ignore-filters --export-ps-level=3')  # for png

def move_convert_plot(plot_name,from_dir,to_dir):
    move_plot(plot_name,from_dir,to_dir)
    convert_plot(plot_name,to_dir)
    os.system('rm ${from_dir}/Unknown*.txt')
    os.system('rm ${to_dir}/${plot_name}.svg')

def arrange_data(plot_input):
    arranged_data={}
    num_cols=len(plot_input['columns'])
    visibility=['' for i in range(num_cols)]
    colors=['' for i in range(num_cols)]
    opacity=[1 for i in range(num_cols)]
    xplacement=[i+1 for i in range(len(plot_input['data'][:,1]))]
    
    if 'xvals' in plot_input:
        if type(plot_input['xvals']) is list:
                xplacement=plot_input['xvals'] 

    if 'visibility' in plot_input:
        if type(plot_input['visibility']) is dict:
            if type(plot_input['visibility']['attribute'])is list:
                j=0
                for i in plot_input['visibility']['index']:
                    visibility[i]=plot_input['visibility']['attribute'][j]
                    j=j+1
            else:
                for i in plot_input['visibility']['index']:
                    visibility[i]=plot_input['visibility']['attribute']

    if 'colors' in plot_input:
        if type(plot_input['colors']) is dict:
            if type(plot_input['colors']['attribute'])is list:
                j=0
                for i in plot_input['colors']['index']:
                    colors[i]=plot_input['colors']['attribute'][j]
                    j=j+1
            else:
                for i in plot_input['colors']['index']:
                    colors[i]=plot_input['colors']['attribute']
    
    arranged_data={
            'columns':plot_input['columns'],
            'xvals': xplacement,
            'names':plot_input['names'],
            'colors':colors,
            'opacity':opacity,
            'visibility':visibility
            }
    return arranged_data


def get_data(plot_input):
    trace=[];
    y=[];
    arranged_data=arrange_data(plot_input)

    for i in plot_input['columns'][0:len(plot_input['columns'])]:
        y.append(plot_input['data'][:,i])
    for i in range(len(y)):
        trace.append({
            'x':arranged_data['xvals'],
            'y':y[i],
            'name':arranged_data['names'][i],
            'marker':dict(
                        color=arranged_data['colors'][i],
                    ),
            'type':'bar',
            'width':0.35,
            'opacity':arranged_data['opacity'][i],
            'visible': arranged_data['visibility'][i]
        })
    data=[t for t in trace]
    return data

def get_layout(layout_input):
    if layout_input['margin']=='default':
        layout_input['margin']=[80,80,80,80,0]
    if layout_input['xtickvals']=='default':
        mytickvals=[i+1 for i in range(len(layout_input['xlabel'])+1)]
    else:
        mytickvals=layout_input['xtickvals']

    myxaxis = go.XAxis(
        title=layout_input['xtitle'],
        titlefont=dict(
                    size=16,
                ),
        showticklabels=True,
        ticktext=layout_input['xlabel'],
        # tickvals=tickvals,
        tickvals=mytickvals,
        showline=True,
        mirror="ticks",
        ticks="inside",
        tickfont=dict(
            size=16,
            ),
        linewidth=2,
        tickwidth=2,
    )
    myyaxis = go.YAxis(
        title=layout_input['ytitle'],
        titlefont=dict(
                    size=16,
                ),
        showline=True,
        tickprefix="  ",
        mirror="ticks",
        ticks="inside",
        tickfont=dict(
            size=16,
            ),
        linewidth=2,
        tickwidth=2,

    )
    layout = go.Layout(
        title=layout_input['title'],
        margin=dict(
            t=layout_input['margin'][0],
            r=layout_input['margin'][1],
            b=layout_input['margin'][2],
            l=layout_input['margin'][3],
            pad=layout_input['margin'][4],
            ),
        barmode='stack',
        xaxis=myxaxis,
        yaxis=myyaxis,
        shapes=layout_input['shapes'],
        legend=dict(
            x=layout_input['legend'][0], 
            y=layout_input['legend'][1],
            bordercolor = Z2,
            borderwidth = 2,
            )

    )
    return layout
