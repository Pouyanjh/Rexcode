import requests, json

spotheader = {
    'Content-Type': 'application/json',
    '$API': 'Zex/Jp+cqy3poc/YnNuV7AKrjQYwhg==',
    '$LEVEL': '-1'
}


def licencecreate(course, name):
    body = {
        "course": str(course),
        "name": str(name),
        "watermark": {"texts": [{"text": "rexcode.ir"}]},
        "test": True

    }
    print(body)

    response = requests.post(
        'https://panel.spotplayer.ir/license/edit/',
        data=json.dumps(body),
        headers=spotheader
    )

    return response