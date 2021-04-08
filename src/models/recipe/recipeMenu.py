import discord
from discord import Message

from config import recipeMenuEmbeds

mainRecipeMenu = discord.Embed.from_dict(recipeMenuEmbeds.mainRecipeMenu)
recipeTitlePrompt = discord.Embed.from_dict(recipeMenuEmbeds.recipeTitlePrompt)
ingredientsPrompt = discord.Embed.from_dict(recipeMenuEmbeds.ingredientsPrompt)
cookTimePrompt = discord.Embed.from_dict(recipeMenuEmbeds.cookTimePrompt)
methodPrompt = discord.Embed.from_dict(recipeMenuEmbeds.methodPrompt)
servesPrompt = discord.Embed.from_dict(recipeMenuEmbeds.servesPrompt)


async def optionsMenu(bot, ctx, newRecipe, check):
    await ctx.author.send(embed=mainRecipeMenu)

    msg: Message = await bot.wait_for("message", check=check)

    args = (bot, ctx, newRecipe, check)
    optionDict = {
        "1": lambda: supplyTitle(*args),
        "2": lambda: supplyIngredients(*args),
        "3": lambda: supplyCookTime(*args),
        "4": lambda: supplyMethod(*args),
        "5": lambda: supplyServes(*args),
        "6": lambda: exitMenu(ctx)
    }

    responder = optionDict.get(msg.content, lambda: ctx.author.message("Please choose either option 1 or option 2"))
    await responder()


async def supplyTitle(bot, ctx, newRecipe, check):
    await ctx.author.send(embed=recipeTitlePrompt)
    msg: Message = await bot.wait_for("message", check=check)

    newRecipe.setTitle(msg.content)
    await ctx.author.send(f"Recipe title is {newRecipe.title}!")
    await optionsMenu(bot, ctx, newRecipe, check)


async def supplyIngredients(bot, ctx, newRecipe, check):
    await ctx.author.send(embed=ingredientsPrompt)
    msg: Message = await bot.wait_for("message", check=check)

    newRecipe.setIngredient(msg.content)
    await ctx.author.send(f"Ingredient is {newRecipe.ingredients}!")
    await optionsMenu(bot, ctx, newRecipe, check)


async def supplyCookTime(bot, ctx, newRecipe, check):
    await ctx.author.send(embed=cookTimePrompt)
    msg: Message = await bot.wait_for("message", check=check)

    newRecipe.setCookTime(msg.content)
    await ctx.author.send(f"Cooking time is {newRecipe.cookTime}!")
    await optionsMenu(bot, ctx, newRecipe, check)


async def supplyMethod(bot, ctx, newRecipe, check):
    await ctx.author.send(embed=methodPrompt)
    msg: Message = await bot.wait_for("message", check=check)

    newRecipe.setMethod(msg.content)
    await ctx.author.send(f"Method is {newRecipe.method}!")
    await optionsMenu(bot, ctx, newRecipe, check)


async def supplyServes(bot, ctx, newRecipe, check):
    await ctx.author.send(embed=servesPrompt)
    msg: Message = await bot.wait_for("message", check=check)

    newRecipe.setServes(msg.content)
    await ctx.author.send(f"This recipe serves {newRecipe.serves}!")
    await optionsMenu(bot, ctx, newRecipe, check)


async def exitMenu(ctx):
    await ctx.author.send("Exiting Recipe Creation.")
