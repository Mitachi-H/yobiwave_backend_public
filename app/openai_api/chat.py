import openai
from pydantic import BaseModel, Json
import json, re, asyncio
from typing import List
from ..env import OPENAI_API_KEY
from ..schemas import eco as eco_schema

# Load your API key from an environment variable or secret management service
openai.api_key = OPENAI_API_KEY

async def get_LCIs(product_name: str) -> List[eco_schema.LCIs]:
    groups = await get_group_fromchat(product_name)
    subgroups = await get_subgroup_fromchat(product_name, groups)
    names = await get_name_fromchat(product_name, subgroups)
    final_names = await get_final_name_fromchat(product_name, names)
    # name["amount"]が intではなく　"30.6 gram" の場合は　数値の身を抽出する
    for name in final_names:
        if type(name["amount"]) == str:
            name["amount"] = float(re.search(r'(\d+\.?\d*)', name["amount"]).group())
    return [eco_schema.LCIs(LCIName = name["LCIName"], amount = name["amount"]) for name in final_names]

async def get_group_fromchat(product_name: str) -> List[str]:
    reply = await chat(prompt_for_group(product_name))
    return get_data_from_reply(reply)

async def get_subgroup_fromchat(product_name: str, groups: List[str]) -> List[str]:
    prompts = prompts_for_subgroup(product_name, groups) 
    replies = await asyncio.gather(*[chat(prompt) for prompt in prompts])
    return sum([get_data_from_reply(reply) for reply in replies], [])

async def get_name_fromchat(produc_name: str, subgroups: List[str]) -> List[str]:
    prompts = prompts_for_name(produc_name, subgroups)
    replies = await asyncio.gather(*[chat(prompt) for prompt in prompts])
    return sum([get_data_from_reply(reply) for reply in replies], [])

async def get_final_name_fromchat(product_name: str, names: List[str]) -> str:
    replies = await chat(prompt_for_final_name(product_name, names))
    return get_data_from_reply(replies)

# 文字列を正規化する関数
def normalize_string(s: str) -> str:
    return s.lower().replace(" ", "").replace(",", "")

# 文字列が十分に類似しているかどうかを判断する関数（簡易版）
def is_similar(a: str, b: str) -> bool:
    return normalize_string(a) == normalize_string(b)

# jsonファイルからサブグループを取得する関数
def get_subgroups_fromdata(groups: List[str]) -> List[List[str]]:
    with open("app/openai_api/json/en-group_subgroup.json", "r") as f:
        json_obj = json.load(f)

        result = []
        for group in groups:
            # JSON オブジェクトのキーを正規化
            normalized_keys = {normalize_string(k): k for k in json_obj.keys()}
            
            # 入力された group を正規化
            normalized_group = normalize_string(group)
            
            # 類似しているキーを探す
            original_key = normalized_keys.get(normalized_group)
            
            if original_key:
                result.append(json_obj[original_key])

        return result

def get_names_fromdata(subgroups: List[str]) -> List[List[str]]:
    with open("app/openai_api/json/en-subgroup_name.json", "r") as f:
        json_obj = json.load(f)

        result = []
        for subgroup in subgroups:
            # JSON オブジェクトのキーを正規化
            normalized_keys = {normalize_string(k): k for k in json_obj.keys()}
            
            # 入力された group を正規化
            normalized_group = normalize_string(subgroup)
            
            # 類似しているキーを探す
            original_key = normalized_keys.get(normalized_group)
            
            if original_key:
                result.append(json_obj[original_key])

        return result

# Groupを見つけるプロンプトを生成する関数
def prompt_for_group(product_name: str) -> str:
    return f"""# Instruction
Please select all relevant "Material Categories" for "{product_name}". List the selected categories according to the specified output format.

## List of Material Categories
 - "milk and dairy products"
 - "cooking aids and miscellaneous ingredients"
 - "meats, eggs, fish"
 - "fruits, vegetables, legumes and oilseeds"
 - "cereal products"
 - "beverages"
 - "fats"
 - "infant foods"
 - "ice creams and sorbets"
 - "appetizers and composed dishes"
 - "sugary products"

## Output Format
```
[
  "Selected Category 1",
  "Selected Category 2",
  ...
]
```"""

# Subgroupを見つけるプロンプトを生成する関数、複数
def prompts_for_subgroup(product_name: str, groups: List[str]) -> List[str]:
    return [prompt_for_subgroup(product_name, group, subgroups) for group, subgroups in zip(groups, get_subgroups_fromdata(groups))]

# Subgroupを見つけるプロンプトを生成する関数
def prompt_for_subgroup(product_name: str, group: str, subgroups: List[str]) -> str:
    formatted_subgroups = "\n - ".join(subgroups)
    return f"""# Instruction
Please select the material category or categories relevant to "{product_name}" from the list below. These selected categories must be sub-categories of "{group}". If no categories are applicable, provide an empty list.

## Target Material Categories{formatted_subgroups}

## Output Format
```
[
  "Selected Category 1",
  "Selected Category 2",
  ...
]
```"""

def prompts_for_name(product_name: str, subgroups: List[str]) -> List[str]:
    return [prompt_for_name(product_name, subgroup, names) for subgroup, names in zip(subgroups, get_names_fromdata(subgroups))]

def prompt_for_name(product_name: str, subgroup: str, names: List[str]) -> str:
    formatted_names = "\n - ".join(names)
    return f"""# Instruction
Please choose the relevant LCI Name associated with '{product_name}' from the list below, making sure it falls under the sub-category '{subgroup}'. If no LCI Name is applicable, return an empty list. Avoid selecting duplicate or similar LCI Names; if the choice is ambiguous, narrow it down to the most generally accepted option.

## Target Material Categories{names}

## Output Format
```
[
  "Selected LCI Name 1",
  "Selected LCI Name 2",
  ...
]
```"""

def prompt_for_final_name(product_name: str, names: List[str]) -> str:
    formatted_names = "\n - ".join(names)
    return f"""
# Imperative Sentence
I want to measure the environmental impact of the product "{product_name}". Below are the general candidates for its ingredients. From the LCI Name List below, please select the main ingredients of "{product_name}" and indicate their quantity per product. Please follow the output format for your results. The purpose is to estimate the environmental impact, so if you do not know the specific numbers, please base it on the most commonly sold "{product_name}" in the market. Also, if the same ingredient is listed under multiple LCI Names, please avoid duplication.

# LCI Name List
{formatted_names}

## Output Format
```
[
{{"LCIName": "Selected LCI Name 1", "amount": "float amount in grams"}},
{{"LCIName": "Selected LCI Name 2", "amount": "float amount in grams"}}
...
]
```
"""

# 文字列からJSONを抽出する関数
def get_data_from_reply(reply: str) -> List[str]:
    print("---reply---")
    print(reply)
    print("---*---")
    # 文字列の中に潜むjsonを抽出する正規表現
    match = re.search(r'(\[[\s\S]*?\])', reply, re.DOTALL)


    if match:
        json_string = match.group()

        print("---json_string---")
        print(json_string)
        print("---*---")

        json_data = json.loads(json_string)
        return json_data
    else:
        return []

# チャットを行う関数
async def chat(prompt: str) -> str:
    return  (await openai.ChatCompletion.acreate(
    model="gpt-4",
    temperature=0,
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )).choices[0].message.content