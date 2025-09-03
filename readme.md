# CWSE-TEST
This repository its a prove of concept of an security automation. The application in this repository
is going to monitor an telegram group trying to find a keyword on messages and image media. If the keyword
was found in the message, some information about the sender, message, media is going to be stored on postgreSQL.

## How to run (docker)
Requirements:
- Telegram api credentials
- Telegram Phone
- Telegram group with your account as member (Better to create one for the PoC)
- Docker

### Set up credentials
First of all, you need api_id, api_hash and phone from telegram, you can get this information
on [official website](https://my.telegram.org/) by creating an app.
- https://core.telegram.org/api/obtaining_api_id

### Populate .env file
After get the information, you need to fill the [.env](.env) file with the information.
Here is a table of environment variables, the required variables you need to put in the [environent file](.env)

| Key          | Configuration                                          | Required | Example                       |
| ------------ | ------------------------------------------------------ | -------- | ----------------------------- |
| TL_API_ID    | App api_id                                             | ✅       | 12345678                      |
| TL_API_HASH  | App api_hash                                           | ✅       | asdasdn2346sdbf23487yhsdbf347 |
| PHONE        | Phone of telegram account                              | ✅       | +5511999999999                |
| GROUP_ID     | Group id you want to monitor                           | ✅       | -1234356                      |
| KEYWORD      | The word you want to search                            | ✅       | cloudflare                    |
| LOG_LEVEL    | Level of logs                                          | ❌       | INFO,WARNING,ERROR,DEBUG      |
| SESSION_FILE | Session file, if you want to map a volume on container | ❌       | /app/session/example.session  |

**Important, if you dont know the group ID, you can set the LOG_LEVEL to debug and run at first time with the
GROUP_ID variable setted to ""**

### Run the docker compose to setup the final step
After set up the .env (environment file) run the following commando is going to build
the docker image using the docker compose file and run in a interactive mode so you can
enter you telegram phone. (This is really necessary due telegram security reasons)*[I think if I had used a BotFather this step should not be necessary]*

> docker compose run --build --rm -it cwse-test

### Configure your session
After you run the docker compose command, the app is going to ask you the phone,
so you have to input the phone like this example: `+5511999999999`
Then you will receive a message from telegram with a code, insert the code when
the app asks

### Now is time to test
Send a message on telegram group configured with the word configured on .env file.
Send a image with the word configured on .env file.
The expected message should be something like this: `[WARNING] ⚠️ >>ALERT<< the word 'cloudflare' was found on text: cloudflare`

![group](img/group.jpeg)
![log](img/log.jpeg)


## REF
- https://docs.telethon.dev/en/stable/modules/client.html
- https://tesseract-ocr.github.io/
