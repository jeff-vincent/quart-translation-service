from quart import Quart, request
import aiohttp

app = Quart(__name__)

DETECT_BASE_URL = 'https://google-translate1.p.rapidapi.com/language/translate/v2/detect'
TRANSLATE_BASE_URL = 'https://google-translate1.p.rapidapi.com/language/translate/v2'
HEADERS = {
    'x-rapidapi-host': "google-translate1.p.rapidapi.com",
    'x-rapidapi-key': "YOUR-VERY-OWN-RAPID-API-KEY",
    'content-type': "application/x-www-form-urlencoded"
    }

@app.route('/')
async def health_check():
    return 'Translation Service is up.'

@app.route('/detect', methods=['POST'])
async def detect():
    # parse args
    form = await request.form
    text = form['text']

    # url encode text
    long_list_of_words = text.split(' ')
    url_encoded_text = f"{'%20'.join(long_list_of_words)}"

    params = {
        'q': url_encoded_text
    }

    # make the request
    async with aiohttp.ClientSession() as session:
        async with session.post(DETECT_BASE_URL, 
        headers=HEADERS, params=params) as resp:
            print(resp)
            data = await resp.json()

    return data


@app.route('/translate', methods=['POST'])
async def translate():
    # parse args
    form = await request.form
    text = form['text']
    target = form['target']

    # url encode text
    long_list_of_words = text.split(' ')
    url_encoded_text = f"{'%20'.join(long_list_of_words)}"

    params = {
        'q': url_encoded_text,
        'target': target
    }

    # make the request
    async with aiohttp.ClientSession() as session:
        async with session.post(TRANSLATE_BASE_URL, 
        headers=HEADERS, params=params) as resp:
            print(resp)
            data = await resp.json()

    return data


if __name__ == '__main__':
    app.run(debug=True)