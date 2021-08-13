# MovieSuggestionBot
A simple bot made using AWS Amazon Lex to suggest some good movies to its users.

### What is Amazon Lex?

![Amazon Lex](https://github.com/Apeksh742/MovieRecommendationBot/blob/main/images/lexBot.png?raw=true)

> Amazon Lex is an AWS service for building conversational interfaces for applications using voice and text. Amazon Lex provides the deep functionality and flexibility of natural language understanding (NLU) and automatic speech recognition (ASR) so you can build highly engaging user experiences with lifelike, conversational interactions, and create new categories of products.

### Useful Resources: 
These are some of the useful resources to help you get started creating your first bot

1. [Amazon Lex](https://docs.aws.amazon.com/lex/latest/dg/what-is.html)
2. [Programming Model](https://docs.aws.amazon.com/lex/latest/dg/programming-model.html)
3. [Managing conversations](https://docs.aws.amazon.com/lexv2/latest/dg/using-conversations.html)
4. [Using Lambda Functions](https://docs.aws.amazon.com/lex/latest/dg/using-lambda.html)
5. [Testing a bot using the console](https://docs.aws.amazon.com/lexv2/latest/dg/build-test.html)
6. [Examples of Amazon Lex Bots](https://docs.aws.amazon.com/lex/latest/dg/additional-exercises.html)
7. [Deploying Amazon Lex Bots](https://docs.aws.amazon.com/lex/latest/dg/examples.html)

### Usage
To use this code in your lamda function, you have to do few things:
1. Register and get your api key from [here](https://developers.themoviedb.org/3/getting-started/introduction) to get list of movies.\
   ```Note:``` Give **Application URL** = "NA" if you don't have one when they ask for your app details.
2. Set **api_key** as an environmental variable in your lambda function.
3. These are some things you can customize:\
    i) **category** : Slot variable to take input from user\
   ii) **WelcomeIntent** : Intent for greeting user\
  iii) **RecommendMovie** : Intent for suggesting movies
  
## Source of Movie Dataset API:

### [The Movie Database (TMDb)](https://www.themoviedb.org/)


## Amazon Lex Console configuration of my bot: 
![Amazon Lex Configuration 1](https://github.com/Apeksh742/MovieRecommendationBot/blob/main/images/LexSS1.png?raw=true)

![Amazon Lex Configuration 2](https://github.com/Apeksh742/MovieRecommendationBot/blob/main/images/LexSS2.png?raw=true)

### Testing Bot From Amazon Lex console: 

![Amazon Lex Bot Working](https://github.com/Apeksh742/MovieRecommendationBot/blob/main/images/chatBot.png?raw=true)

![Amazon Lex Bot Working 2](https://github.com/Apeksh742/MovieRecommendationBot/blob/main/images/chatBot2.png?raw=true)

### Testing Bot in Slack:

![Lex in Slack](https://github.com/Apeksh742/MovieRecommendationBot/blob/main/images/slackIntegration1.png?raw=true)
