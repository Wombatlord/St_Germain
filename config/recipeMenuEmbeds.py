# Colours
kindaGold = 16565763
green = 0x20e845
blue = 0x0b29d6

# icons
titleIcon = ":pencil:"
ingredientIcon = ":sweet_potato:"
timeIcon = ":stopwatch:"
methodIcon = ":magic_wand:"
servesIcon = ":shopping_bags:"
exitIcon = ":white_check_mark:"


mainRecipeMenu = {
    "title": "St. Germain's Kitchen",
    "description": "Choose an option to construct a recipe entry.",
    "color": kindaGold,
    "fields": [
        {
            "name": "Options",
            "value": f"`1` {titleIcon} Title\n"
                     f"`2` {ingredientIcon} Ingredients\n"
                     f"`3` {timeIcon} Cook Time\n"
                     f"`4` {methodIcon} Method\n"
                     f"`5` {servesIcon} Serves\n"
                     f"`6` {exitIcon} Exit\n",
            "inline": True
        },
        {
            "name": "\u200B",
            "value": "[Cash Me Outside Howbow Dah.](https://www.youtube.com/watch?v=ZrtSOTGNqA8)",
            "inline": False
        },
    ],
}

recipeTitlePrompt = {
    "title": "Title your dish!",
    "description": "Type in a name for your recipe.",
    "color": green,

}

ingredientsPrompt = {
    "title": "Ingredients!",
    "description": "Type in an ingredient.",
    "color": blue,

}

cookTimePrompt = {
    "title": "Cook time?",
    "description": "How long should this recipe be cooked for?",
    "color": blue,

}

methodPrompt = {
    "title": "Method",
    "description": "How do?",
    "color": blue,

}

servesPrompt = {
    "title": "Serves?",
    "description": "How many people does this recipe serve?",
    "color": blue,

}
