import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import spoonacular_key

#API Link: https://api.spoonacular.com/recipes/complexSearch

print("HIGH PROTEIN MEAL GENERATOR")

API_Link = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={spoonacular_key.apiKey}&number=1&sort=random&addRecipeInformation=true&addRecipeNutrition=true"

maxCalories = 0
answer = input("Do you have a minimum or maximum amount of calories for the meal. Answer with \"Yes\" or \"No\".\n")
if answer.lower() == "yes":
    answer = input("Type \"Maximum\" to set a Maximum calorie limit and type \"Minimum\" to set a Minimum calorie limit. Type \"Both\" to set a minimum and maximum calorie count.\n")
    if answer.lower() == "maximum":
        answer = input("Type the maximum number of calories for the meal.\n")
        API_Link = API_Link + "&maxCalories=" + answer
        maxCalories = int(answer)
    if answer.lower() == "minimum":
        answer = input("Type the minimum number of calories for the meal.\n")
        API_Link = API_Link + "&minCalories=" + answer
    if answer.lower() == "both":
        answer = input("Type the maximum number of calories for the meal.\n")
        API_Link = API_Link + "&maxCalories=" + answer
        maxCalories = int(answer)
        answer = input("Type the minimum number of calories for the meal.\n")
        API_Link = API_Link + "&minCalories=" + answer

answer = input("Would you like the meal to be high in protein. Answer with \"Yes\" or \"No\".\n")
if answer.lower() == "yes":
    answer = input("Would you like to set the minimum amount of grams of protein. Answer with \"Yes\" or \"No\".\n")
    if answer.lower() == "yes":
        answer = input("Type the minimum grams of protein for the meal.\n")
        API_Link = API_Link + "&minProtein=" + answer
    else:
        if maxCalories > 0:
            protein = maxCalories // 10
            API_Link = API_Link + "&minProtein=" + str(protein)

response = requests.get(API_Link)
recipe_info = response.json()

if response.status_code == 402:
    print("You have used up your daily quota for generating recipes. Try again tomorrow.")
else:
    recipe_URL = recipe_info.get("results")[0].get('sourceUrl')
    calories = recipe_info.get("results")[0].get('nutrition').get('nutrients')[0].get('amount')
    fat = recipe_info.get("results")[0].get('nutrition').get('nutrients')[1].get('amount')
    carbs = recipe_info.get("results")[0].get('nutrition').get('nutrients')[3].get('amount')
    protein = recipe_info.get("results")[0].get('nutrition').get('nutrients')[10].get('amount')
    
    print("\nMeal Macros per serving:\n")
    print(f"{calories} Calories\n{fat} grams of Fat\n{carbs} grams of Carbohydrates\n{protein} grams of Protein")

    #Opens recipe url
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(recipe_URL)
    driver.maximize_window()
