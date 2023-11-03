import json
import asyncio
import pandas as pd

from app.database import async_session
from sqlalchemy.exc import IntegrityError
from app.models.db_models import Base, HazardousSubstance

group_subgroup = None
en_group_subgroup = None
with open("./app/openai_api/json/group_subgroup.json", "r") as f:
    group_subgroup = json.load(f)
with open("./app/openai_api/json/en-group_subgroup.json", "r") as f:
    en_group_subgroup = json.load(f)

def normalize_string(s: str) -> str:
    return s.lower().replace(" ", "").replace(",", "")

async def seed():
    with open('./eco_scoring/data/AGRIBALYSE3.1.1_produits alimentaires.csv', 'r') as f:
        df = pd.read_csv(f, sep=',')

        async with async_session() as session:
            for index, row in df.iterrows():
                async with session.begin():
                    group = row["Groupe d'aliment"]
                    en_group = list(en_group_subgroup.keys())[list(group_subgroup.keys()).index(group)]

                    subgroup = row["Sous-groupe d'aliment"]
                    en_subgroup = en_group_subgroup[en_group][group_subgroup[group].index(subgroup)]

                    name = row["LCI Name"]
                    normalized_name = normalize_string(name)

                    data = {
                        'group': en_group,
                        'subgroup': en_subgroup,
                        'name': name,
                        'normalized_name': normalized_name,
                        'CO2': row["kg CO2 eq/kg de produit"],
                        'CVC11': row["kg CVC11 eq/kg de produit"],
                        'U_235': row["kBq U-235 eq/kg de produit"],
                        'NMVOC': row["kg NMVOC eq/kg de produit"],
                        'disease': row["disease inc./kg de produit"],
                        'CTUh_noncarcinogenic': row["CTUh/kg de produit-non"],
                        'CTUh_carcinogenic': row["CTUh/kg de produit"],  # 注意：元のデータにはCTUhが2回出ていたので適切なカラム名を確認してください
                        'H_plus': row["mol H+ eq/kg de produit"],
                        'Eutrophication_freshwater': row["kg P eq/kg de produit"],
                        'Eutrophication_Marine': row["kg N eq/kg de produit"],
                        'Eutrophication_Land': row["mol N eq/kg de produit"],
                        'CTUe': row["CTUe/kg de produit"],
                        'Pt': row["Pt/kg de produit"],
                        'm3_depriv': row["m3 depriv./kg de produit"],
                        'MJ': row["MJ/kg de produit"],
                        'Sb': row["kg Sb eq/kg de produit"]
                    }

                    adding_data = HazardousSubstance(**data)
                    session.add(adding_data)
                    await session.flush()

    

if __name__ == '__main__':
    BOS = '\033[92m'  # 緑色表示
    EOS = '\033[0m'

    print(f'{BOS}Seeding data...{EOS}')

    # seed()
    # asyncio.run(seed())
   

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(seed())
        loop.close()
        
    except RuntimeError as e:
        pass
    # catchできないね。。
