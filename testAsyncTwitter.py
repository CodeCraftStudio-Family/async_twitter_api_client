import anyio
import json
import os
from asyncTwitter.asyncAccount import AsyncAccount
from asyncTwitter.asyncScraper import AsyncScraper
from asyncTwitter.asyncSearch import AsyncSearch


config = json.load(open("config.json"))


async def testSearch():
    search = AsyncSearch(debug=True)
    await search.asyncAuthenticate(
        cookies="C:/Users/a/Documents/Git/infiniteMoneyTwitterBot/cookies/obJellyfin.cookies"
    )
    results = await search.asyncSearch(
        queries=[{"query": "kanye west", "category": "Top"}],
        limit=100,
        out="data/search_results",
    )
    results = results[0]
    print(f"Found {len(results)}")


async def testAccount():
    twitter = AsyncAccount(debug=True, twoCaptchaApiKey=config.get("2CaptchaKey"))

    # cookies = {
    #    "ct0": "b6e7f4a7c7b0f8d3b6e7f4a7c7b0f8d329t3i4320t9u432t902t430932ty4902u3t923tu329tu32t9u",
    #    "auth_token": "egfwiopjgew90pgj4w9gugh89u0f",
    # }
    
    if os.path.exists("cookies/testing.cookies.cookies"):
        kwargs = {
            "cookies": "cookies/testing.cookies.cookies",
        }
    else:
        kwargs = {
            "email": "sbillingsley316@yahoo.com",
            "password": "5682szvzcg",
            "username": "SamanthaB117",
        }

    if await twitter.asyncAuthenticate(
        proxies="http://127.0.0.1:9090",
        #httpxSocks=True,
        **kwargs,
    ):
        twitter.save_cookies(fname="cookies/testing.cookies", toFile=True)
    else:
        print("Failed to authenticate.")
        exit()

    results1 = await twitter.asyncLike(tweet_id="1783497801906696316")

    if "this account is temporarily locked." in str(results1):
        print("Account is locked. Unlocking...")
    else:
        print("Account is not locked.")
        #exit()

    results2 = await twitter.asyncVotePoll(
        card_uri='card://1787309739010850816',
        tweet_id='1787309739354833192',
        selected_choice='2'
    )
    
    print(results2)

    #results = await twitter.unlockViaArkoseCaptcha()

    #print(results)

    # results = await twitter.asyncTweet(text="A test tweet from the asyncTwitter module!")
    # scheduleTweetResults = await twitter.asyncScheduleTweet(
    #    text="A test tweet from the asyncTwitter module!",
    #    date="2021-08-01 08:21",
    # )

    # print(scheduleTweetResults)

async def testScraper():
    twitter = AsyncScraper(debug=True)
    await twitter.asyncAuthenticate(
        cookies="cookies/testing.cookies.cookies",
        proxies="http://127.0.0.1:9090",
        httpxSocks=False
    )
    
    screenNameToJSON = await twitter.asyncUsers(screen_names=["obJellyfin"])
    
    restId = screenNameToJSON[0].get("data", {}).get("user", {}).get('result', {}).get("rest_id")
    
    if not restId:
        print("Failed to get restId.")
        exit()
    
    results = await twitter.asyncFollowers(
        user_ids=[restId], limit=10
    )
    
    print(f"Found {len(results)} followers.")
    
if __name__ == "__main__":
    # run(testSearch)
    anyio.run(testAccount)
    anyio.run(testScraper)
