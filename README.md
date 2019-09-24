# TG Userbot

A modular telegram Python UserBot running on python3 with a mongoDB coupled with Redis backend.

## Disclaimer

First of all you should know this bot is a major work in progress. It is based on [Paperplane](), but without all of the things that people hate about it. There is no "sudoers" and no one will have control of your bot except you, not even me. If you choose to use this bot now, be prepared to pull changes frequently as I continue to fix broken english, pull or change things that don't make sense, or add new things.

## Getting started

Getting started is pretty easy, but a few commands currently rely on API access through a few different services, so be ready to sign up for some free accounts.

#### Step one

Clone this repo using `git clone https://github.com/watzon/tg_userbot.git` and enter the newly created `tg_userbot` directory. Go ahead and open the directory in your favorite text editor, we're going to be doing some typing.

#### Step two

Copy `sample_config.env` to `config.env`. This file WILL NOT be checked into version control, so if you're hosting your bot remotely you'll need to think about that. Normal environment variables are also supported, but `config.env` makes things a little easier for local development at least.

Now open `config.env` in your text editor and remove the first two lines. If these aren't removed your file will not be loaded. For now the only variables we're going to change are the first two, `API_KEY` and `API_HASH`. Using your Telegram account information (ie. your phone number) login to https://my.telegram.org and click on the link that says API Development Tools. The `API_KEY` in your `config.env` will be the `App api_id` and the  `API_HASH` will be the `APP api_hash`.

#### Step three

This bot includes logging for a lot of things, but to implement logging you need a chat for it to send logs to. Ideally this chat should NOT be a public chat with other people in it, or they will be getting spammed with logs (including some potentially semi sensitive information such as error logs).

You will need to get the chat id for the config file. The easiest way to do so would be to add [@RawDataBot](https://t.me/RawDataBot) to your group. Upon being added it will output a JSON formatted message which will include the information about the current "chat". Take the chat id and add it to your config file using the `BOTLOG_CHATID` environment variable.

To enable logging, set the `BOTLOG` environment variable to `True`.

#### Step four

Now we need to setup database access. This is not, strictly speaking, mandatory. Your bot will run without a database connection, but there are certain functions that won't work.

Currently this bot is setup to work with [MongoDB Atlas](https://cloud.mongodb.com), but I don't see any reason why it wouldn't work with any MongoDB database. If you want to use Atlas you'll need to make an account at [cloud.mongodb.com](https://cloud.mongodb.com). It's free, don't worry.

Follow the instructions to create a cluster. In the `Network Access` area make sure to add your IP address to the list. Alternatively you can also do `0.0.0.0/0` to allow connections from all IP addresses. You'll also need a new user with the access level of Atlas Admin.

If you've done the setup correctly under the "Clusters" tab you should see your newly created cluster. Under your cluster click `CONNECT`->`Connect Your Application` pick Python 3.6 or later as the driver and version, copy the connection string, and paste it in your config file as the `MONGO_DB_URI`.

#### Step five

Now it's time to generate a session with Telegram. This will allow us to maintain access to the Telegram API across restarts. First make sure all of the requirements are installed by running 

```
pip3 install -r ./requirements.txt --user
```

Once deps are installed we can generate a session file

```
python3 ./generate_session_file.py
```

It will ask for your phone number, and then the code you get from Telegram. If you do everything right it should generate a `userbot.session` file in your project's root directory. Now for a couple warnings:

1. DO NOT under any circumstances check `userbot.session` into version control or put it anywhere where someone else can get their hands on it.
2. See 1

#### Step six

We're almost done. Techincally your bot should work now, but there are some niceties that won't work until you provide an API key. You can skip this if you don't plan on using any of those. Don't worry, they're all free.

1. The `.screencap` command currently relies on the ScreenShotLayer API. You can get a free API key from [their website](https://screenshotlayer.com/) and provide it via the `SCREENSHOT_LAYER_ACCESS_KEY` environment variable.
2. The `.weather` command relies on the OpenWeatherMap API. You can get an API key via [their website](https://openweathermap.org/) and plug it in using the `OPEN_WEATHER_MAP_APPID` environment variable.
3. The YouTube related commands such as `.yt`, `.ytdl`, and `.ytmp3` rely on access to the YouTube API. You can get an API key for it from the [Google Cloud Console](https://console.cloud.google.com). Insert the API key into the `YOUTUBE_API_KEY` environment variable.
4. If you want last.fm integration you'll need access to [their API](https://www.last.fm/api/account/create) as well. Your account information needs to be supplied using the variables that start with `LASTFM`.
5. For currency conversions wwe currently rely on the CurrencyConverterAPI. You can get a free API key from [here](https://free.currencyconverterapi.com/) and plug it in to the `CURRENCY_API` environment variable.


#### Step seven

There are currently some commands that allow uploading to Google Drive. They are forked functionality and haven't been personally tested by me yet, but should you wish to try:

Get a Google Drive API key from the [Google Cloud Console](https://console.cloud.google.com). When creating credentials you'll be asked a few questions.

Which API are you using? - Google Drive API
Where will you be calling the API from? - Other UI
What data will you be accessing? - User data

Click `What credentials do I need`.

Choose a name for your client.

On the next screen it should list your credentials in a table. Click the edit button.

Set Authorized JavaScript origins and Authorized Redirect URIs to **http://localhost:8080** and hit Save.

Click the download button on the right side of the table to download a JSON file containing your credentials. Copy that file to your project root and rename it to `client_secrets.json`.

Now back in your project folder run `python3 generate_drive_session.py`.

#### Step eight

Should you wish to use Docker you should be able to do so quite easily. First make sure you have docker installed, then in the project root run `docker build . -t userbot`, where `userbot`. To run it use `docker run userbot`.

If you don't want to use docker you can just run `./init/start.sh` from the project root.

## Getting help

I am `@watzon` on Telegram, but don't PM me without permission unless you like being blocked swiftly. Feel free to report issues here or mention me in [@pythonofftopic](https://t.me/pythonofftopic).