# -*- coding: utf-8 -*-

from json import tool
from pyexpat import features
from tkinter import W
from tkinter.tix import PopupMenu
import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import pydeck as pdk
import folium
from folium.features import CustomIcon


# df1 = pd.DataFrame([
#     [35.739451, 139.556461],
#     [35.736178, 139.555526],
#     [35.734234, 139.549479],
#     [35.733213, 139.542760]], columns=['lat', 'lon'])
# df2 = pd.DataFrame([
#     [35.737909, 139.540239],
#     [35.728404, 139.531738],
#     [35.731405, 139.558090],
#     [35.731585, 139.563387]], columns=['lat', 'lon'])

df = pd.read_csv('df.csv', encoding="shift-jis")

icons= {
    'トマト':'tomato.png',
    '枝豆'  :'edamame.png'
}

def makeicon(icon_image):
    icon = CustomIcon(
        icon_image=icon_image,
        icon_size=(30,30),
        icon_anchor=(30,30),
        shadow_image='',
        shadow_size=(5,5),
        shadow_anchor=(4,4),
        popup_anchor=(-3,-3),
        )
    return icon

def markUp(row):
    mrk=folium.Marker(
        location=[row['lat'],row['lon']],
        popup=row['information'],
        tooltip=row['name'],
        icon= makeicon(icons[row['name']])
    )
    return mrk

        
def createMapFromFoliun(li):

    latMean,lonMean = df.mean()

    # create map obj
    plot_map = folium.Map(location=[latMean, lonMean], zoom_start=15)
    
    group1 = folium.FeatureGroup(name='トマト').add_to(plot_map)
    group2 = folium.FeatureGroup(name='枝豆').add_to(plot_map)
    
    for index,row in df[df['name']=='トマト'].iterrows():
        group1.add_child(markUp(row))
    for index,row in df[df['name']=='枝豆'].iterrows():
        group2.add_child(markUp(row))
    
    folium.LayerControl().add_to(plot_map)

    st.components.v1.html(folium.Figure().add_child(plot_map).render(), height=600, width=800)


# def createMapFromPydeck(li):

#     layers = []
#     if li[4]:
#         layers.append(
#             pdk.Layer(
#                 'HexagonLayer',
#                 data=df1,
#                 get_position='[lon, lat]',
#                 radius=100,
#                 elevation_scale=4,
#                 elevation_range=[0, 1000],
#                 pickable=True,
#                 extruded=True,
#             )
#         )
#     if li[7]:
#         layers.append(
#             pdk.Layer(
#                 'ScatterplotLayer',
#                 data=df2,
#                 get_position='[lon, lat]',
#                 get_color='[200, 30, 0, 160]',
#                 get_radius=100,
#             ),
#         )
    
#     st.pydeck_chart(pdk.Deck(
#         map_style='mapbox://styles/mapbox/light-v9',
#         initial_view_state=pdk.ViewState(
#             latitude=35.74,
#             longitude=139.55,
#             zoom=13,
#             pitch=0,
#         ),
#         layers=layers
#     ))

def sideber():
    st.sidebar.text('＋西東京市')
    tanemaki    = st.sidebar.checkbox('　種まき（9）')
    tutidukuri  = st.sidebar.checkbox('　土づくり（12）')
    uetuke      = st.sidebar.checkbox('　植え付け（6）')
    kanrisagyou = st.sidebar.checkbox('　＋管理作業（29）')
    mizuyari    = st.sidebar.checkbox('　　　　水やり（4）')
    josou       = st.sidebar.checkbox('　　　　除草（25）')
    syuukaku    = st.sidebar.checkbox('　＋収穫（15）')
    tomato      = st.sidebar.checkbox('　　　　トマト（5）')
    edamame     = st.sidebar.checkbox('　　　　枝豆（10）')

    li = [tanemaki,tutidukuri,uetuke,kanrisagyou,mizuyari,josou,syuukaku,tomato,edamame]
    # if mizuyari & tomato:
    #     st.map(df1.append(df2))
    # if mizuyari:
    #     st.map(df1)
    # if tomato:
    #     st.map(df2)
    createMapFromFoliun(li)

def main():
    sideber()
    

if __name__=="__main__":
    main()