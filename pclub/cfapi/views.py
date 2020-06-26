import requests
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def cfapi_view(request, *args, **kwrags):
    """
        Codeforces API view

        Gets the data of the user using CF API and
        prepares statistics form it.
    """
    user = request.user.cf_username
    wrong_tag_count = dict()
    all_tag_count = dict()
    all_verdicts = dict()
    total = 0
    max_tag = max_wrong_tag = None
    response = requests.get('https://codeforces.com/api/user.status',
                            params={'handle': user, 'from': 1, 'count': 1000})

    response = response.json()
    if response['status'] == 'OK':
        all_results = response['result']

        for result in all_results:
            total += 1

            if result['verdict'] in all_verdicts:
                all_verdicts[result['verdict']] += 1
            else:
                all_verdicts[result['verdict']] = 1

            tags = result['problem']['tags']
            for tag in tags:
                if tag in all_tag_count:
                    all_tag_count[tag] += 1
                else:
                    all_tag_count[tag] = 1

                if result['verdict'] != 'OK':
                    if tag in wrong_tag_count:
                        wrong_tag_count[tag] += 1
                    else:
                        wrong_tag_count[tag] = 1

        try:
            max_tag = max(all_tag_count, key=all_tag_count.get)
        except Exception as identifier:
            max_tag = None

        try:
            max_wrong_tag = max(wrong_tag_count, key=wrong_tag_count.get)
        except Exception as identifier:
            max_wrong_tag = None

    try:
        correct = all_verdicts['OK']
    except Exception as identifier:
        correct = None

    try:
        status = response['status']
    except Exception as identifier:
        status = None

    context = {'status': status, 'correct': correct, 'total': total,
               'max_tag': max_tag, 'max_wrong_tag': max_wrong_tag,
               'all_verdicts': json.dumps(all_verdicts),
               'all_tags': json.dumps(all_tag_count)}

    return render(request, 'cfapi/cfapi.html', context)


@login_required
def github_api_view(request, *args, **kwrags):
    """
        Github API view

        Gets the data of the user using Github users API 
        and prepares statistics form it.
    """

    user = request.user.github_username
    all_languages = dict()
    max_language = None
    status = False
    repos = 0

    a = 'https://api.github.com/users/' + user + '/repos'

    response = requests.get('https://api.github.com/users/' + user + '/repos')
    response = response.json()

    try:
        response['message']
    except Exception as identifier:
        status = True

    if status:
        for repository in response:
            repos += 1
            language_url = repository['languages_url']
            languages_response = requests.get(language_url)
            languages_response = languages_response.json()

            for language in languages_response:
                if language in all_languages:
                    all_languages[language] += languages_response[language]
                else:
                    all_languages[language] = languages_response[language]

        try:
            max_language = max(all_languages, key=all_languages.get)
        except Exception as identifier:
            max_language = None

    context = {'status': status, 'repos': repos, 'max_language': max_language,
               'all_languages': json.dumps(all_languages)}
        
    return render(request, 'cfapi/githubapi.html', context)
