"""
 This code demonstrates an implementation of the Lex Code Hook Interface
 in order to serve a bot which recommends movies to its users in a category.

 For complete guide and better understanding of Amazon Lex Bots and how they works,
 visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html.
"""

import os
import urllib3
import json

""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """

def get_slots(intent_request):
    return intent_request['currentIntent']['slots']
    
def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message, response_card):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message,
            'responseCard': response_card
        }
    }
    
def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response

def closeWithResponseCard(session_attributes, fulfillment_state, message, response_card):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message,
            'responseCard': response_card
        }
    }
    return response    


def closeWelcomeIntent(session_attributes, fulfillment_state, message, response_card):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message,
            'responseCard': response_card
        }
    }
    return response
    
def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }
    
""" --- Build a responseCard with a title, subtitle, and an optional set of options which should be displayed as buttons --- """    

def build_response_card(title, subtitle, options):
    buttons = None
    if options is not None:
        buttons = []
        for i in range(min(5, len(options))):
            buttons.append(options[i])

    return {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': [{
            'title': title,
            'subTitle': subtitle,
            'buttons': buttons
        }]
    }
    
""" --- Build a responseCard with a movie name as title, rating as a subtitle, and moviePoster with an attached URL to its provider --- """ 

def build_response_card_for_movies(movies, movieLinks, moviePosters,ratings):
    responseCards = []
    for i in range(0,min(10,len(movies))):
        responseCards.append(
            {
            'title': movies[i],
            'subTitle': 'Average Voting: {}'.format(ratings[i]),
            'imageUrl': moviePosters[i],
            'attachmentLinkUrl': movieLinks[i]
           }
            )
            
    return {
        'contentType': 'application/vnd.amazonaws.card.generic',
        'version': 1,
        'genericAttachments': responseCards
    }

""" --- Build a list of potential options for a given slot, to be used in responseCard generation --- """  

def build_options(slot):
    if slot == 'category':
        return [
            {'text': 'Top Rated', 'value': '1'},
            {'text': 'Most Popular', 'value': '2'},
            {'text': 'Newly Released', 'value': '3'},
            {'text': 'Trending Today', 'value': '4'}
        ]
        
""" --- Build a list of intents availaible, to be used in responseCard generation --- """  

def build_intent_suggestions(intentName):
    """
    Build a list of intents availaible, to be used in responseCard generation.
    """
    if intentName == 'Welcome':
        return [
            {'text': 'Recommend Movies', 'value': 'suggest some movies'},
            
        ]

""" --- Validate and build a response for Amazon Lex --- """ 

def build_validation_result(is_valid, violated_slot, message_content):
    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }
    
def validate_choosen_category(category):
    if category not in ["1","2","3","4"]:
        return build_validation_result(False, 'category', 'Choose from given categories')
    return build_validation_result(True, None, None)
    
    
def get_movie(intent_request):
    """
    Performs dialog management and fulfillment for getting validated slots.

    Beyond fulfillment, the implementation for this intent demonstrates the following:
    1) Use of elicitSlot in slot validation and re-prompting
    2) Use of confirmIntent to support the confirmation of inferred slot values, when confirmation is required
    on the bot model and the inferred slot values fully specify the intent.
    """
    category = get_slots(intent_request)["category"]
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)
        validation_result = validate_choosen_category(category)
        
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            slots['category'] = None
            return elicit_slot(
                output_session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message'],
                build_response_card(
                    'Choose a {}'.format(validation_result['violatedSlot']),
                    validation_result['message']['content'],
                    build_options(validation_result['violatedSlot'])
                )
            )
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        return delegate(output_session_attributes, slots)
        
          
    if category == "1":
        movies = get_top_rated(category)[0]
        movieId =get_top_rated(category)[1]
        moviePosters =get_top_rated(category)[2]
        ratings = get_top_rated(category)[3]
        movieLinks = get_movie_provider(movieId)
       
        return closeWithResponseCard(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Top Rated Movies in our list are:'},
                  build_response_card_for_movies(movies,movieLinks,moviePosters,ratings)
                  )
                  
    elif category == "2":
        movies = get_popular(category)[0]
        movieId =get_popular(category)[1]
        moviePosters =get_popular(category)[2]
        ratings =get_popular(category)[3]
        movieLinks = get_movie_provider(movieId)
        
        return closeWithResponseCard(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Most Popular Movies in our list are:'},
                  build_response_card_for_movies(movies,movieLinks,moviePosters,ratings)
                  )
                  
    elif category == "3":
        movies = get_newly_released(category)[0]
        movieId =get_newly_released(category)[1]
        moviePosters =get_newly_released(category)[2]
        ratings =get_newly_released(category)[3]
        movieLinks = get_movie_provider(movieId)
        
        return closeWithResponseCard(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Newly Released Movies are:'},
                  build_response_card_for_movies(movies,movieLinks,moviePosters,ratings)
                  )
                  
    elif category == "4":
        movies = get_trending_today(category)[0]
        movieId =get_trending_today(category)[1]
        moviePosters =get_trending_today(category)[2]
        ratings =get_trending_today(category)[3]
        movieLinks = get_movie_provider(movieId)
        
        return closeWithResponseCard(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Movies Trending Today are: '},
                  build_response_card_for_movies(movies,movieLinks,moviePosters,ratings)
                  )
    else:
        return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': "Sorry, I can't help with that"})

""" --- Below are a bunch of functions to help in get movies according to a category chosen by user --- """ 
    
def get_top_rated(category):
    '''
    api_key = Environmental Variable set in Lambda function
    '''
    api_key=os.environ.get('api_key')
    http = urllib3.PoolManager()
    r = http.request('GET', "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US&page=1".format("top_rated",api_key))
    response=json.loads(r.data.decode('utf-8'))
    result=response['results']
    movieList = []
    movieId =[]
    moviePosters = []
    vote_average = []
    for movie in result:
        movieList.append(movie['title'])
        movieId.append(movie['id'])
        moviePosters.append("https://image.tmdb.org/t/p/original"+movie['poster_path'])
        vote_average.append(movie['vote_average'])
    return [movieList,movieId,moviePosters,vote_average]

def get_newly_released(category):
    '''
    api_key = Environmental Variable set in Lambda function
    '''
    api_key=os.environ.get('api_key')
    http = urllib3.PoolManager()
    r = http.request('GET', "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US&page=1".format("now_playing",api_key))
    response=json.loads(r.data.decode('utf-8'))
    result=response['results']
    movieList = []
    movieId =[]
    moviePosters = []
    vote_average = []
    for movie in result:
        movieList.append(movie['title'])
        movieId.append(movie['id'])
        moviePosters.append("https://image.tmdb.org/t/p/original"+movie['poster_path'])
        vote_average.append(movie['vote_average'])
    return [movieList,movieId,moviePosters,vote_average]
    
def get_popular(category):
    '''
    api_key = Environmental Variable set in Lambda function
    '''
    api_key=os.environ.get('api_key')
    http = urllib3.PoolManager()
    r = http.request('GET', "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US&page=1".format("top_rated",api_key))
    response=json.loads(r.data.decode('utf-8'))
    result=response['results']
    movieList = []
    movieId =[]
    moviePosters = []
    vote_average = []
    for movie in result:
        movieList.append(movie['title'])
        movieId.append(movie['id'])
        moviePosters.append("https://image.tmdb.org/t/p/original"+movie['poster_path'])
        vote_average.append(movie['vote_average'])
    return [movieList,movieId,moviePosters,vote_average]

def get_trending_today(category):
    '''
    api_key = Environmental Variable set in Lambda function
    '''
    api_key=os.environ.get('api_key')
    http = urllib3.PoolManager()
    r = http.request('GET', "https://api.themoviedb.org/3/trending/{}/day?api_key={}".format("movie",api_key))
    response=json.loads(r.data.decode('utf-8'))
    result=response['results']
    movieList = []
    movieId =[]
    moviePosters = []
    vote_average = []
    for movie in result:
        movieList.append(movie['title'])
        movieId.append(movie['id'])
        moviePosters.append("https://image.tmdb.org/t/p/original"+movie['poster_path'])
        vote_average.append(movie['vote_average'])
    return [movieList,movieId,moviePosters,vote_average]
    
def get_movie_provider(movieId):
    '''
    api_key = Environmental Variable set in Lambda function
    '''
    api_key=os.environ.get('api_key')
    http = urllib3.PoolManager()
    movieProviders = []
    moviePosters = []
    for id in movieId:
        r = http.request('GET', "https://api.themoviedb.org/3/movie/{}/watch/providers?api_key={}".format(id,api_key))
        response=json.loads(r.data.decode('utf-8'))
        result=response['results']
        if "US" in result:
            link = result["US"]["link"]
            movieProviders.append(link)
        else:
            link = "https://cutt.ly/5QGm4jF"
            movieProviders.append(link)
    return movieProviders
    

""" --- Intents --- """
    
def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'RecommendMovie':
        return get_movie(intent_request)
    if intent_name == 'Welcome':
        return closeWelcomeIntent(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Hi, how can i help you?'},
                  build_response_card(
                      "I can help you with",
                      "choose an option",
                      build_intent_suggestions(intent_name)
                  )
                  )

    raise Exception('Intent with name ' + intent_name + ' not supported')

""" --- Main handler --- """

def lambda_handler(event, context):
    return dispatch(event)
