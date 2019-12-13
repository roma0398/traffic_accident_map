import os
from datetime import datetime

from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from folium.plugins import MarkerCluster
import folium
import pandas as pd
import requests
import json
from tqdm import tqdm

app = Flask(__name__)
app.secret_key = 'SHH!'

def map_render(start_date, end_date):
    data = pd.read_csv('../data/new_with_street.csv')
    data = data.dropna()
    data = data.reset_index()
    data.drop(['index'], axis=1, inplace=True)
    mask = (data['date'] >= start_date) & (data['date'] <= end_date)
    df = data.loc[mask]
    f = open('../api_key.txt', 'r')
    api = f.read()
    f.close()
    spb = [59.939095, 30.315868]
    map = folium.Map(location=spb, zoom_start = 10)
    marker_cluster = MarkerCluster().add_to(map)
    for i in tqdm(list(df.index.values)):
        st = df['pavlov'][i]
        if st != '':
            id = df['id'][i]
            addr = f'Санкт-Петербург, {st}'
            try:
                res = requests.get(f'https://geocode-maps.yandex.ru/1.x/?format=json&apikey={api}&geocode={addr}')
                loc = json.loads(res.content.decode('utf8'))['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
                location = [float(loc[1]), float(loc[0])]
            except:
                continue    
            if location is None:
                continue
            if round(location[0], 6) == spb[0] and round(location[1], 6) == spb[1]:
                continue
            folium.Marker(location=[location[0], location[1]], popup = folium.Popup(f'<a href="https://vk.com/spb_today?w=wall-68471405_{id}"target="_blank">link to news in VK</a>'), icon=folium.Icon(color = 'red', icon='info-sign')).add_to(marker_cluster)
    map.save("templates/map.html")

class ExampleForm(FlaskForm):
    dt_from = DateField('DatePicker', format='%Y-%m-%d')
    dt_to = DateField('DatePicker', format='%Y-%m-%d')


@app.route('/', methods=['POST', 'GET'])
def head():
    form = ExampleForm()
    return render_template('date_picker.html', form=form)


@app.route('/date', methods=['POST', 'GET'])
def get_date():
    form = ExampleForm()
    if form.validate_on_submit():
        start = request.form['dt_from']
        end = request.form['dt_to']
        map_render(start, end)
    return render_template('map.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)