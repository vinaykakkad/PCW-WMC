import json
import requests

from django.shortcuts import render
from django.core.paginator import Paginator

from account.models import Account
# Create your views here.


def profiles_list_view(request, *args, **kwargs):
    accounts = Account.objects.filter(is_superuser=False).order_by('pk')

    paginator = Paginator(accounts, 10)
    page = request.GET.get('page')
    accounts = paginator.get_page(page)

    context = {'page_object': accounts, 'last_page': paginator.num_pages}
    return render(request, 'profiles/profiles_list.html', context)


def home_profile_view(request, *args, **kwargs):
    username = request.GET.get('username')
    user = Account.objects.get(username=username)
    
    context = {'user': user}
    return render(request, 'profiles/home_profile.html', context)    


def codeforces_api_view(request, *args, **kwargs):
    """
        Codeforces API view

        Gets the data of the user using CF API and
        prepares statistics form it.
    """
    username = request.GET.get('username')
    user = Account.objects.get(username=username)
    cf_username = user.cf_username
    wrong_tag_count = dict()
    all_tag_count = dict()
    all_verdicts = dict()
    total = 0
    max_tag = max_wrong_tag = None
    response = requests.get('https://codeforces.com/api/user.status',
                            params={'handle': cf_username, 'from': 1, 'count': 1000})

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
               'all_tags': json.dumps(all_tag_count), 'user': user}

    return render(request, 'profiles/cfapi.html', context)



def github_api_view(request, *args, **kwargs):
    """
        Github API view

        Gets the data of the user using Github users API 
        and prepares statistics form it.
    """

    username = request.GET.get('username')
    user = Account.objects.get(username=username)
    github_username = user.github_username
    all_languages = dict()
    max_language = None
    status = False
    repos = 0


    response = requests.get('https://api.github.com/users/' + github_username + '/repos')
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
               'all_languages': json.dumps(all_languages), 'user': user}
        
    return render(request, 'profiles/githubapi.html', context)
