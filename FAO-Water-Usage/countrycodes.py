import pandas as pd
import numpy as np
import os
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2, country_alpha2_to_country_name, country_name_to_country_alpha3
from requests import Session
from time import sleep

names = [name for name in os.listdir("Data/main-csvs") if "Water-by-sector" not in name]
names = sorted(names)
datasets = [pd.read_csv(f'Data/main-csvs/{name}',header=0,usecols=["Area","Area Id","Variable Name","Variable Id","Year","Value","Symbol","Md"],index_col=False) for name in names]

countries = dict.fromkeys(names)
for i in range(24):
    countries[names[i]] = list(datasets[i]["Area"].drop_duplicates().values)
all_countries = sorted(list(set(np.concatenate([countries[names[i]] for i in range(24)]))))

codes = dict.fromkeys(all_countries)
badkeys = ['Bolivia (Plurinational State of)',all_countries[45],'Holy See','Iran (Islamic Republic of)','Micronesia (Federated States of)','Republic of Korea','State of Palestine','Timor-Leste','Venezuela (Bolivarian Republic of)']
missed_vals = [{'ISO-alpha2': 'BO', 'Continent': 'SA'}, {'ISO-alpha2': 'CI', 'Continent': 'AF'},{'ISO-alpha2': 'VA', 'Continent': 'EU'},{'ISO-alpha2': 'IR', 'Continent': 'AS'},{'ISO-alpha2': 'FM', 'Continent': 'OC'},{'ISO-alpha2': 'KR', 'Continent': 'AS'},{'ISO-alpha2': 'PS', 'Continent': 'AS'},{'ISO-alpha2': 'TL', 'Continent': 'AS'},{'ISO-alpha2': 'VE', 'Continent': 'SA'}]
exceptions = {badkeys[i]: missed_vals[i] for i in range(len(badkeys))}
for country in all_countries:
    try:
        alpha2 = country_name_to_country_alpha2(country,cn_name_format="upper")
        cont = country_alpha2_to_continent_code(alpha2)
        d = {'ISO-alpha2': alpha2, 'Continent': cont}
        codes[country] = d
    except:
        d = exceptions[country]
        codes[country] = d   

codedf = pd.DataFrame(codes).T
url = lambda x: f"https://nominatim.openstreetmap.org/search.php?country={x}&format=jsonv2"
countrycoord = dict.fromkeys(all_countries)
alpha3 = dict.fromkeys(all_countries)

for alpha in codedf["ISO-alpha2"]:
    country = codedf.loc[codedf["ISO-alpha2"]==alpha].index[0]
    countrycoord[country] = dict.fromkeys(["ISO-alpha3","bbox","lat","lng"])
    name = country_alpha2_to_country_name(alpha)
    countrycoord[country]["ISO-alpha3"] = country_name_to_country_alpha3(name)

res = []
with Session() as s:
    for alpha in codedf["ISO-alpha2"]:
        sleep(.55)
        r = s.get(url(alpha)).json()
        res.append(r)
        sleep(.5)

for r in res:
    idx = res.index(r)
    if idx!=76 and idx!=169:
        countrycoord[all_countries[idx]]["bbox"] = r[0]["boundingbox"]
        countrycoord[all_countries[idx]]["lat"] = r[0]["lat"]
        countrycoord[all_countries[idx]]["lng"] = r[0]["lon"]
    else:
        countrycoord[all_countries[76]]["bbox"] = [12.42931,41.90981,12.47480,41.89781]
        countrycoord[all_countries[76]]["lat"] = 41.90380
        countrycoord[all_countries[76]]["lng"] = 12.45205
        countrycoord[all_countries[169]]["bbox"] = [33.32153,32.57922,36.27686,31.18931]
        countrycoord[all_countries[169]]["lat"] = 31.88693
        countrycoord[all_countries[169]]["lng"] = 34.79752

codekeys = ["ISO-alpha2","Continent"]
coordkeys = ["ISO-alpha3","bbox","lat","lng"]
codecoord = {country: {codekeys[1]: codes[country][codekeys[1]], codekeys[0]: codes[country][codekeys[0]], coordkeys[0]: countrycoord[country][coordkeys[0]], coordkeys[1]: countrycoord[country][coordkeys[1]], coordkeys[2]: countrycoord[country][coordkeys[2]], coordkeys[3]: countrycoord[country][coordkeys[3]]} for country in all_countries}

codecoorddf = pd.DataFrame(codecoord).T
codecoorddf.index.name = "Country"

codecoorddf.to_csv('Docs/FAO-alpha2-3.csv')