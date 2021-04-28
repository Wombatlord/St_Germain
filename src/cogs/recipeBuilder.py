from __future__ import annotations

from typing import Optional

import discord
from discord import Message
from discord.ext import commands
from discord.ext.commands import Context

from config import recipeMenuEmbeds
from src.models.recipe import menus
from src.models.recipe.recipe import Recipe, Ingredient
from src.adaptors.repositories.recipeRepository import PostgresRecipeRepository as Repository
from src.models.recipe.menus import registerEmbed, NodeConfig


class RecipeBuilderCog(commands.Cog):
    mainRecipeMenu = discord.Embed.from_dict(recipeMenuEmbeds.mainRecipeMenu)
    recipeTitlePrompt = discord.Embed.from_dict(recipeMenuEmbeds.recipeTitlePrompt)
    ingredientsPrompt = discord.Embed.from_dict(recipeMenuEmbeds.ingredientsPrompt)
    cookTimePrompt = discord.Embed.from_dict(recipeMenuEmbeds.cookTimePrompt)
    methodPrompt = discord.Embed.from_dict(recipeMenuEmbeds.methodPrompt)
    servesPrompt = discord.Embed.from_dict(recipeMenuEmbeds.servesPrompt)
    howManyIngredientsPrompt = discord.Embed.from_dict(recipeMenuEmbeds.howManyIngredientsPrompt)

    def __init__(self, bot):
        self.bot = bot
        self._recipe: Optional[Recipe] = None
        self._ingredient: Optional[Ingredient] = None

    @commands.command()
    async def newRecipe(self, ctx: Context) -> None:
        authorID: int = ctx.author.id
        self._recipe: Recipe = Recipe(author=ctx.author.name,
                                      title="",
                                      ingredients=[],
                                      cookTime="",
                                      method=[],
                                      serves=4)

        ingredientList = []

        def check(message) -> bool:
            print(authorID)
            print(message.author.id)
            return isinstance(message.channel, discord.channel.DMChannel) and message.author.id == authorID

        registerEmbed(self.recipeTitlePrompt, identifier="title_input")
        menuConfig = {
            "1": NodeConfig(self.recipeTitlePrompt, self.titleInputHandler, check, menus.rootNode),
            "2": NodeConfig(self.ingredientsPrompt, self.ingredientsInputHandler, check, menus.rootNode),
            "3": NodeConfig(self.cookTimePrompt, self.cookTimeInputHandler, check, menus.rootNode),
            "4": NodeConfig(self.methodPrompt, self.methodInputHandler, check, menus.rootNode),
            "5": NodeConfig(self.servesPrompt, self.servesInputHandler, check, menus.rootNode),
            "6": "exit",
            "7": NodeConfig(self.howManyIngredientsPrompt, self.addIngredientsInputHandler, check, menus.rootNode)
        }
        fullConfig = {
            "check": check,
            "prompt": self.mainRecipeMenu,
            "config": menuConfig
        }
        menus.configure(fullConfig)

        await menus.rootNode(self.bot, ctx)
        Repository.save(self._recipe)
        # Repository.saveMethod(self._recipe)

        self.clean()

    @commands.command()
    async def recipeID(self, ctx, recipeID):
        requestedRecipe = Repository.getByID(recipeID)
        print(requestedRecipe)
        recipeDict = {
            "author": requestedRecipe.author,
            "title": requestedRecipe.title,
            "ingredients": requestedRecipe.ingredients,
            "recipeMethod": requestedRecipe.method,
            "serves": requestedRecipe.serves,
        }
        await ctx.author.send(recipeDict)

    def clean(self):
        self._recipe = None

    async def titleInputHandler(self, bot_, context, message):
        self._recipe.setTitle(message.content)
        await context.author.send(f"Recipe title is {self._recipe.title}!")

    async def ingredientsInputHandler(self, bot_, context, message):
        self._recipe.setIngredient(message.content)
        await context.author.send(f"Ingredient is {self._recipe.ingredients}!")

    async def addIngredientsInputHandler(self, bot_, context, message):
        def check(message) -> bool:
            authorID = context.author.id
            print(authorID)
            print(message.author.id)
            return isinstance(message.channel, discord.channel.DMChannel) and message.author.id == authorID

        for each in range(int(message.content)):
            """
            Maybe like this?
            """
            self._ingredient: Ingredient = Ingredient(ingredient="",
                                                      quantity="")

            await context.author.send(f"{str(each + 1)}: Please enter an ingredient.")
            msg: Message = await bot_.wait_for("message", check=check)
            self._ingredient.ingredient = msg.content

            await context.author.send(f"{str(each + 1)}: Please enter a total quantity.")
            msg: Message = await bot_.wait_for("message", check=check)
            self._ingredient.quantity = msg.content
            self._recipe.ingredients.append(self._ingredient)
            # print(self._ingredient.ingredient)
            # print(self._ingredient.quantity)
            print(self._ingredient)

        for each in self._recipe.ingredients:
            await context.author.send(each)

    async def cookTimeInputHandler(self, bot_, context, message):
        self._recipe.setCookTime(message.content)
        await context.author.send(f"Cook time is {self._recipe.cookTime}!")

    async def methodInputHandler(self, bot_, context, message):
        self._recipe.setMethod(message.content)
        await context.author.send(f"Recipe method is {self._recipe.method}!")

    async def servesInputHandler(self, bot_, context, message):
        self._recipe.setServes(message.content)
        await context.author.send(f"This recipe serves {self._recipe.serves}!")


def setup(bot):
    cog = RecipeBuilderCog(bot)

    bot.add_cog(cog)
