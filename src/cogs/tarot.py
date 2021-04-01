import io
from typing import List

import random
import discord
from discord.ext import commands
from discord.ext.commands import Context
from src.backend import requests, formatting, predicates

from src.images.imageManipulators import combineImageListHorizontal, convertImage

SPACER: str = '\n' + '__ ' * 22
COMBINED_IMAGE_PATH: str = r"C:\Users\Owner\PycharmProjects\StGermain\images\combined.jpg"
SUITS: List[str] = [
    "Wands",
    "Cups",
    "Swords",
    "Pentacles",
]
CARD_NUMBERS: List[str] = [
    "One",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
]
CARD_COURTS: List[str] = [
    "Ace",
    "King",
    "Queen",
    "Knight",
    "Page",
]
INVALID_MESSAGE: str = "Please check your input. Search is case sensitive.\n" \
                       "Images should be searched by complete name.\n" \
                       "Major Arcana: Wheel Of Fortune\n" \
                       "Minor Arcana: Knight of Swords\n"
testID = 815785251879649311


async def checkInvalid(ctx: Context, cardName):
    """
    Responds to the discord user with an error message if they provide
    a search term that is too generic
    @param ctx:
    @param cardName:
    @return:
    """
    numbersOf = list(map(lambda s: f"{s} of", CARD_NUMBERS))
    courtsOf = list(map(lambda s: f"{s} of", CARD_COURTS))
    invalidTerms = CARD_NUMBERS + numbersOf + CARD_COURTS + courtsOf + SUITS + [""]
    if cardName in invalidTerms:
        await formatting.sendDelimited(ctx, INVALID_MESSAGE)
        return False

    # Single letter input is invalid
    if len(cardName) == 1:
        await formatting.sendDelimited(ctx, INVALID_MESSAGE)
        return False

    return True


class Tarot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CARD_LIMIT = 7

    async def checkInvalid(self, ctx: Context, cardName):
        """
        Responds to the discord user with an error message if they provide
        a search term that is too generic
        @param ctx:
        @param cardName:
        @return:
        """
        numbersOf = list(map(lambda s: f"{s} of", CARD_NUMBERS))
        courtsOf = list(map(lambda s: f"{s} of", CARD_COURTS))
        invalidTerms = CARD_NUMBERS + numbersOf + CARD_COURTS + courtsOf + SUITS + [""]
        if cardName in invalidTerms:
            await formatting.sendDelimited(ctx, INVALID_MESSAGE)
            return False

        # Single letter input is invalid
        if len(cardName) == 1:
            await formatting.sendDelimited(ctx, INVALID_MESSAGE)
            return False

        return True

    @commands.command()
    @predicates.inChannels(testID)
    async def meaning(self, ctx, *, message=''):
        """
            Responds to the user with the meanings of the provided car
            @param ctx:
            @param message:
            @return:
            """
        searchTerm = message
        fullDeck = await requests.getFullDeck()

        if not await checkInvalid(ctx, message) or fullDeck is None:
            return

        meanings = {}
        for card in fullDeck["cards"]:
            if searchTerm in card["name"]:
                meanings = {
                    'up': card['meaning_up'],
                    'rev': card['meaning_rev'],
                }

        if not meanings:
            await formatting.sendDelimited(ctx, INVALID_MESSAGE)
        else:
            await formatting.sendDelimited(ctx, f"Upright: {meanings.get('up', '')}")
            await formatting.sendDelimited(ctx, f"Reversed: {meanings.get('rev', '')}")

    @commands.command()
    async def image(self, ctx: Context, message: str):
        """
        Responds to the discord user with the image associated to a card
        @param ctx:
        @param message:
        @return:
        """
        global INVALID_MESSAGE
        cardName = message
        fullDeck = await requests.getFullDeck()

        if not await checkInvalid(ctx, message) or fullDeck is None:
            return

        desiredCard = None
        for card in fullDeck["cards"]:
            if cardName in card["name"]:
                desiredCard = card

        if desiredCard is None:
            await formatting.sendDelimited(ctx, INVALID_MESSAGE)
            return

        rawImage = await requests.downloadCardImage(desiredCard)
        if rawImage is None:
            await ctx.send("Please check input.")
            return

        cardImage = io.BytesIO(rawImage)
        await ctx.send(file=discord.File(cardImage, f"{cardName}.jpg"))

    @commands.command()
    async def describe(self, ctx: Context, message: str) -> None:
        """
        Retrieves the description of a card by its name.
        Single search terms will return all cards containing that term in the name.
        EG. Searching "Knight" will retrieve ALL Knights.
        Searching a suit (Swords, Cups, Wands, Pentacles) will retrieve all cards in the suit.
        """
        cardName = message
        thisInvalidMessage = INVALID_MESSAGE + "Single Term: Knight / Ace / Devil etc."
        if cardName == '':
            await formatting.sendDelimited(ctx, thisInvalidMessage)
            return

        fullDeck = await requests.getFullDeck()
        if fullDeck is None:
            return

        cardsFound = False
        for card in fullDeck["cards"]:
            if cardName in card["name"]:
                await formatting.sendDelimited(ctx, card['desc'])
                cardsFound = True

        if not cardsFound:
            await formatting.sendDelimited(ctx, thisInvalidMessage)

    @commands.command()
    async def tarot(self, ctx: Context, numberOfCards):
        """
        Retrieves random cards as JSON.
        If API response is OK, creates a variable to hold the username and prepares cards.
        Card orientation is represented as 0 or 1 (card meanings are tied to orientation)
        Sends either the card name, or card name + * to represent a reversed card.
        """
        numberOfCards = int(numberOfCards)
        if numberOfCards > self.CARD_LIMIT or numberOfCards <= 0:
            numberOfCards = self.CARD_LIMIT

        cards = await requests.getRandomCards(numberOfCards)

        await ctx.send(f"Very well {str(ctx.author)}{SPACER}")
        images = []

        # Determines card orientation and posts message in sequence.
        for card in cards["cards"]:
            await formatting.sendDelimited(
                ctx,
                await self.getCardMessage(card, orientation=random.randint(0, 1)),
                delimiters=("```", "***")
            )
            image = await requests.downloadCardImage(card)
            images.append(await convertImage(image))

        finalSpread = await combineImageListHorizontal(images)
        finalSpread.save(COMBINED_IMAGE_PATH)

        # Sends the final combined image.
        await ctx.send(
            file=discord.File(COMBINED_IMAGE_PATH, "spread.jpg")
        )

    async def getCardMessage(self, card: dict, orientation) -> str:
        """
        Given a card and a orientation (of value 1 or 0) this will return a formatted
        message as a string
        @param card:
        @param orientation:
        @return:
        """
        meaning = card['meaning_up'] if orientation == 0 else card['meaning_rev']
        revTag = "" if orientation == 0 else "[Rev.]"
        message = "{}{}:\n\n{}{}".format(
            revTag,
            card["name"],
            meaning,
            SPACER,
        )
        return message
