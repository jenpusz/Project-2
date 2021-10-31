from requests import Session
import os
import pandas as pd

names = [name for name in os.listdir("Data/main-csvs") if "csv" in name if "Water-by-sector.csv" not in name]
names = sorted(names)
datasets = [pd.read_csv(f"Data/main-csvs/{name}",header=0,index_col=False) for name in names]

varids = [4100, 4103, 4104, 4105, 4106, 4111, 4537, 4112, 4458, 4113, 4548, 4473, 4474, 4114, 4403, 4150, 4541, 4542, 4543, 4159, 4171, 4177, 4178, 4192, 4157, 4158, 4185, 4187, 4196, 4182, 4188, 
4190, 4317, 4313, 4555, 4557, 4273, 4250, 4260, 4475, 4251, 4252, 4253, 4261, 4262, 4263, 4264, 4265, 4269, 4493, 4491, 4270, 4510, 4517, 4512, 4549, 4550, 4551, 4552, 4553, 4554, 4400, 4401, 4345,
4346, 4347, 4348, 4349, 4350, 4351, 4352, 4353, 4354, 4355, 4356, 4357, 4358, 4359, 4360, 4361, 4362, 4363, 4364, 4365, 4366, 4367, 4368, 4369, 4370, 4371, 4372, 4373, 4374, 4375, 4376, 4377, 4378]
varinfo = dict.fromkeys(varids)
infourls = [f"https://www.fao.org/aquastat/statistics/popups/itemDefn.html?id={varid}" for varid in varids]

res = []
with Session() as s:
    for url in infourls:
        r = s.get(url)
        res.append(r.text)

for i in range(len(varids)):
    split0 = res[i].split('<h1 style="color: #484848;">')
    rep1 = split0[1].replace('</h1><h2 style="color: #484848;">Metadata</h2><br/><strong>Definition</strong><br/>',': ')
    rep2 = rep1.replace('<br/><br/><strong>','\n')
    rep3 = rep2.replace('</strong><br/>',': ')
    rep4 = rep3.replace('<br>','')
    rep5 = rep4.replace('<i>','\n')
    rep6 = rep5.replace('</i>',' ')
    rep7 = rep6.replace('</sup>','')
    rep8 = rep7.replace('<sup>','^')
    rep9 = rep8.replace('_x000D_','')
    rep10 = rep9.replace('Harvested irrigated temporary crop area: ', 'Temporary - ')
    rep11 = rep10.replace('Harvested irrigated permanent crop area: ', 'Permanent - ')
    split1 = rep11.split('<br/><div id="moreinfo">')
    final = split1[0]
    varinfo[varids[i]] = final

varinfotxt = open("Docs/variable-info.txt","w")
for key, value in varinfo.items():
    varinfotxt.write(f"\nVarId: {key}\n"+value+"\n\n")
varinfotxt.close()

VI = "Variable Id"

variables = [[*zip(sets["Variable Name"].drop_duplicates().values,sets[VI].drop_duplicates().values)] for sets in datasets]
all_variables = sorted([tups for group in variables for tups in group],key=lambda x: x[1])
variabletxt = [f"{vars[1]}: {vars[0]}\n" for vars in all_variables]

varfile = open("./Docs/variables.txt", "w")
for var in variabletxt:
    varfile.write(var)
varfile.close()