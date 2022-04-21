import graphene
from graphene import ObjectType, Schema, relay
from graphene_django import DjangoObjectType, DjangoListField 
from api.models import News
from api.models import FakeNews
from api.models import DataText
from api.documents import newsSearch


from graphene_elastic import (
    ElasticsearchObjectType,
    ElasticsearchConnectionField,
)
from graphene_elastic.filter_backends import (
    FilteringFilterBackend,
    SearchFilterBackend,
    HighlightFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
)
from graphene_elastic.constants import (
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_TERM,
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_EXCLUDE,
    LOOKUP_QUERY_IN,
)

import spacy
import pandas as pd
import numpy as np
import random
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from textblob import Blobber
from textblob_fr import PatternTagger, PatternAnalyzer
from spacy.lang.fr.stop_words import STOP_WORDS as fr_stop
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from time import time





# Object type definition
class Searchnews(ElasticsearchObjectType):

    class Meta(object):
        document = newsSearch
        interfaces = [relay.Node]
        filter_backends = [
            FilteringFilterBackend,
            SearchFilterBackend,
            HighlightFilterBackend,
            OrderingFilterBackend,
            DefaultOrderingFilterBackend,
        ]

        # For `FilteringFilterBackend` backend
        filter_fields = {
            
            'title': {
                'field': 'title.raw',
                # Available lookups
                'lookups': [
                    LOOKUP_FILTER_TERM,
                    LOOKUP_FILTER_TERMS,
                    LOOKUP_FILTER_PREFIX,
                    LOOKUP_FILTER_WILDCARD,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_EXCLUDE,
                ],
                # Default lookup
                'default_lookup': LOOKUP_FILTER_TERM,
            },

           'details': {
                'field': 'details.raw',
                # Available lookups
                'lookups': [
                    LOOKUP_FILTER_TERM,
                    LOOKUP_FILTER_TERMS,
                    LOOKUP_FILTER_PREFIX,
                    LOOKUP_FILTER_WILDCARD,
                    LOOKUP_QUERY_IN,
                    LOOKUP_QUERY_EXCLUDE,
                ],
                # Default lookup
                'default_lookup': LOOKUP_FILTER_TERM,
            },
            'id': 'id',


            
            
        }

        # For `SearchFilterBackend` backend
        search_fields = {
            'title': {'boost': 4},
            'details': {'boost': 2},
            
        }

        # For `OrderingFilterBackend` backend
        ordering_fields = {
            
            # 'title': 'title.raw',

            
            'id': 'id',
        }

        # For `DefaultOrderingFilterBackend` backend
        ordering_defaults = (
            '-id',  # Field name in the Elasticsearch document
            #'title.raw',  # Field name in the Elasticsearch document
        )

        # For `HighlightFilterBackend` backend
        highlight_fields = {
            'title': {
                'enabled': True,
                'options': {
                    'pre_tags': ["<b>"],
                    'post_tags': ["</b>"],
                }
            },
            'details': {
                'options': {
                    'fragment_size': 50,
                    'number_of_fragments': 3
                }
            },
            
        }


class DataType(DjangoObjectType):
    class Meta:
        model = DataText
        fields = "__all__" 


class NewsType(DjangoObjectType):
    class Meta:
        model = News
        fields = "__all__"   #we can chose all field by using this fields = "__all__" or ("id","title","details","date")


class FakeNewsType(DjangoObjectType):
    class Meta:
        model = FakeNews
        fields = "__all__"   #we can chose all field by using this fields = "__all__" or ("id","title","details","date")



#now we create a query 
class Query(graphene.ObjectType):
    all_news = graphene.List(NewsType)
    all_fake_news = graphene.List(FakeNewsType)
    news = graphene.Field(NewsType, news_id=graphene.Int(required=True))
    fake_news = graphene.Field(FakeNewsType, fake_news_id=graphene.Int(required=True))
    all_post_documents = ElasticsearchConnectionField(Searchnews)



    def resolve_all_news(self, info, **kwargs):
        return News.objects.all()

    def resolve_all_fake_news(self, info, **kwargs):
        return FakeNews.objects.all()

    def resolve_news(self, info, news_id):
        return News.objects.get(pk=news_id)

    def resolve_fake_news(self, info, fake_news_id):
        return FakeNews.objects.get(pk=fake_news_id)

class NewsInput(graphene.InputObjectType):
    #id = graphene.ID()
    title = graphene.String()
    details = graphene.String()
    #date = graphene.String()


class DataInput(graphene.InputObjectType):
    
    text = graphene.String()
    



class CreateNews(graphene.Mutation):
    class Arguments:
        News_data = NewsInput(required=True)

    News = graphene.Field(NewsType)

    @staticmethod
    def mutate(root, info, News_data):
        News_instance = News( 
            #id=News_data.id,
            title=News_data.title,
            details=News_data.details,
            #date=News_data.date
        )
        News_instance.save()
        return CreateNews(News=News_instance)


class UpdateNews(graphene.Mutation):
    class Arguments:
        News_data = NewsInput(required=True)
        id = graphene.ID()

    News = graphene.Field(NewsType)

    @staticmethod
    def mutate(root, info, News_data, id):

        News_instance = News.objects.get(pk=id)

        if News_instance:
            #News_instance.id = News_data.id
            News_instance.title = News_data.title
            News_instance.details = News_data.details
            #News_instance.date = News_data.date
            News_instance.save()

            return UpdateNews(News=News_instance)
        return UpdateNews(News=None)



class DeleteNews(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        

    News = graphene.Field(NewsType)

    @staticmethod
    def mutate(root, info, id):
        News_instance = News.objects.get(pk=id)
        News_instance.delete()

        return None


class CreateFakeNews(graphene.Mutation):
    class Arguments:
        Fake_News_data = NewsInput(required=True)

    Fake_News = graphene.Field(FakeNewsType)

    @staticmethod
    def mutate(root, info, Fake_News_data):
        Fake_News_instance = FakeNews( 
            
            title=Fake_News_data.title,
            details=Fake_News_data.details,
            
        )
        Fake_News_instance.save()
        return CreateFakeNews(Fake_News=Fake_News_instance)


class UpdateFakeNews(graphene.Mutation):
    class Arguments:
        Fake_News_data = NewsInput(required=True)
        id = graphene.ID()

    Fake_News = graphene.Field(FakeNewsType)

    @staticmethod
    def mutate(root, info, Fake_News_data, id):

        Fake_News_instance = FakeNews.objects.get(pk=id)

        if Fake_News_instance:
            #News_instance.id = News_data.id
            Fake_News_instance.title = Fake_News_data.title
            Fake_News_instance.details = Fake_News_data.details
            #News_instance.date = News_data.date
            Fake_News_instance.save()

            return UpdateFakeNews(Fake_News=Fake_News_instance)
        return UpdateFakeNews(Fake_News=None)



class DeleteFakeNews(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        

    Fake_News = graphene.Field(FakeNewsType)

    @staticmethod
    def mutate(root, info, id):
        Fake_News_instance = FakeNews.objects.get(pk=id)
        Fake_News_instance.delete()

        return None


class CleanData(graphene.Mutation):
    data = graphene.Field(DataType)
    class Arguments:
        text_Input = graphene.String()
        
        


    @staticmethod
    def mutate(root, info, text_Input):
        data_instance = DataText(
            text = text_Input
        )
        if data_instance:
            for ch in ['`','«', '_','{','}','[',']','(',')','>','#','+','-','.','!','$','»',',',':','"','”','xa0','/','=','?','&','*','@','€','’','‘','¬','\'','^','%','<']:
                if ch in text_Input:
                    text_Input = text_Input.replace(ch,"")
            data_instance.text = text_Input
                    
            data_instance.save()
            print('success')
            return CleanData(data=data_instance)
            


class AnalyseData(graphene.Mutation):
    data = graphene.Field(DataType)
    class Arguments:
        text_Input = graphene.String()

    @staticmethod
    def mutate(root, info, text_Input):
        tb = Blobber(pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())


        def enter_news():
            news=text_Input
            return news
        news=  enter_news()


        data= pd.DataFrame() 

        def clean_data(text):
            
            for ch in ['·','\ufeff','\u200b','\""','.',',','%','\\','`','«', '_','{','}','[',']','(',')','>','#','+','-','!','$','\'','/','»',':','“','”','xa0','""','1','2','3','4','5','6','7','8','9','0','?','!','’']:
                if ch in text:
                    text = text.replace(ch,"")
                
            return text

        df2=clean_data(news)
        data.loc[0,'text'] = str(df2)
        data['text']  
        data


        # Step - b : Change all the text to lower case. This is required as python interprets 'dog' and 'DOG' differently
        data['text'] = [entry.lower() for entry in data['text']]

        # Step - c : Tokenization : In this each entry in the corpus will be broken into set of words
        data['text']= [word_tokenize(entry) for entry in data['text']]
        data['text']
        final_stopwords_list = list(fr_stop) 
        nlp = spacy.load('fr_core_news_md')     
        ##-----------
        for index,entry in enumerate(data['text']):
            # Declaring Empty List to store the words that follow the rules for this step
            Final_words = []
            # Initializing WordNetLemmatizer()
            word_Lemmatized = WordNetLemmatizer()
            # pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
            for word, tag in pos_tag(entry):
                # Below condition is to check for Stop words and consider only alphabets
                # 
                if word not in final_stopwords_list and word.isalpha():
                    #word_Final = word_Lemmatized.lemmatize(word)
                    word_Final = word
                    #steaming
                    doc = nlp(str(word_Final)) 
                    for token in doc:
                        word_Final =  token.lemma_
                    
                    #word_Final=stemming(word_Final)
                    Final_words.append(word_Final)
            # The final processed set of words for each iteration will be stored in 'text_final'
            data.loc[index,'text_final'] = str(Final_words)
        data['text_final'][0]   # dataframe removed stopword , applied  steaming !
        data['text_final']


        senti_list = []
        for i in data["text_final"]:
            vs = tb(i).sentiment[0]
            if (vs > 0):
                senti_list.append('Positive')
            elif (vs < 0):
                senti_list.append('Negative')
            else:
                senti_list.append('Neutral')  
        
        data["sentiment"]=senti_list

        data_analyse_instance = DataText(
            text = str(data['sentiment'][0])
        )

        return AnalyseData(data=data_analyse_instance)



class DetectNews(graphene.Mutation):
    data = graphene.Field(DataType)
    class Arguments:
        text_Input = graphene.String()

    @staticmethod
    def mutate(root, info, text_Input):
        df=pd.read_json("D:\Autres\Scraping_Project\data.json")
        tittle_1=df['title'][0]
        tittle_=tittle_1
        df.info()

        df['title']=df['title'].astype('str') 
        df['details']=df['details'].astype('str')
        def clean_data(text):
            for ch in ['','\ufeff','\u200b','\""','.',',','%','\\','`','«', '_','{','}','[',']','(',')','>','#','+','-','!','$','\'','/','»',':','“','”','xa0','""','1','2','3','4','5','6','7','8','9','0','?','!','’']:
                if ch in text:
                    text = text.replace(ch,"")         
            return text

        def clean_scraped_data():
            for j in range(0,2867):
                df['title'][j]=clean_data(df['title'][j])
                df['details'][j]=clean_data(df['details'][j])
                #df['date'][j]=clean_data(df['date'][j])
            return df

        df=clean_scraped_data()

        data=  pd.DataFrame()
        data['text'] = df['title'] + " " + df['details']
        foo = [0,1]
        data['label']=0
        for i in range(0,2867):
            data['label'][i]=random.choice(foo)

        no_of_fakes = data.loc[data['label'] == 1].count()[0]
        no_of_trues = data.loc[data['label'] == 0].count()[0]
        

        data['text'].dropna(inplace=True)
        data['text'] = [entry.lower() for entry in data['text']]
        data['text']= [word_tokenize(entry) for entry in data['text']]

        for i in range(0,2867):
            mytxt=""
            mytxt=str(data['text'][i])
        

        final_stopwords_list = list(fr_stop) 
        nlp = spacy.load('fr_core_news_md')     
        for index,entry in enumerate(data['text']):
            # Declaring Empty List to store the words that follow the rules for this step
            Final_words = []
            # Initializing WordNetLemmatizer()
            word_Lemmatized = WordNetLemmatizer()
            # pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
            for word, tag in pos_tag(entry):
                # Below condition is to check for Stop words and consider only alphabets
                # 
                if word not in final_stopwords_list and word.isalpha():
                    #word_Final = word_Lemmatized.lemmatize(word)
                    word_Final = word
                    #steaming
                    doc = nlp(str(word_Final)) 
                    for token in doc:
                        word_Final =  token.lemma_
                    
                    #word_Final=stemming(word_Final)
                    Final_words.append(word_Final)
            # The final processed set of words for each iteration will be stored in 'text_final'
            data.loc[index,'text_final'] = str(Final_words)

        data['text_final']
        Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(data['text_final'],data['label'],test_size=0.2,random_state=42)
        Train_X.shape, Test_X.shape, Train_Y.shape, Test_Y.shape

        Encoder = LabelEncoder()
        Train_Y = Encoder.fit_transform(Train_Y)
        Test_Y = Encoder.fit_transform(Test_Y)
        Tfidf_vect = TfidfVectorizer(max_features=5000)
        Tfidf_vect.fit(data['text_final'])
        Train_X_Tfidf = Tfidf_vect.transform(Train_X)
        Test_X_Tfidf = Tfidf_vect.transform(Test_X)
        

        Naive = naive_bayes.MultinomialNB()
        Naive.fit(Train_X_Tfidf,Train_Y)
        # predict the labels on validation dataset
        predictions_NB = Naive.predict(Test_X_Tfidf)
        # Use accuracy_score function to get the accuracy

        


        SVM = svm.SVC(C=2.0, kernel='linear', degree=3, gamma='auto')
        SVM.fit(Train_X_Tfidf,Train_Y)
        # predict the labels on validation dataset
        predictions_SVM = SVM.predict(Test_X_Tfidf)
        
        

        t0 = time()
        model = GaussianNB()
        model.fit(Train_X_Tfidf.toarray(), Train_Y)
        
        t0 = time()
        score_train = model.score(Train_X_Tfidf.toarray(), Train_Y)
        
        t0 = time()
        score_test = model.score(Train_X_Tfidf.toarray(), Train_Y)
        

        def enter_news():
            news = text_Input
            return news
        news=  enter_news()

        data3= pd.DataFrame() 

        def clean_data(text):
            
            for ch in ['·','\ufeff','\u200b','\""','.',',','%','\\','`','«', '_','{','}','[',']','(',')','>','#','+','-','!','$','\'','/','»',':','“','”','xa0','""','1','2','3','4','5','6','7','8','9','0','?','!','’']:
                if ch in text:
                    text = text.replace(ch,"")
                
            return text

        df2=clean_data(news)
        data3.loc[0,'text'] = str(df2)
        data3['text']  
        data3
        # Step - b : Change all the text to lower case. This is required as python interprets 'dog' and 'DOG' differently
        data3['text'] = [entry.lower() for entry in data3['text']]

        # Step - c : Tokenization : In this each entry in the corpus will be broken into set of words
        data3['text']= [word_tokenize(entry) for entry in data3['text']]
        final_stopwords_list = list(fr_stop) 
        nlp = spacy.load('fr_core_news_md')     
        for index,entry in enumerate(data3['text']):
            # Declaring Empty List to store the words that follow the rules for this step
            Final_words = []
            # Initializing WordNetLemmatizer()
            word_Lemmatized = WordNetLemmatizer()
            # pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
            for word, tag in pos_tag(entry):
                # Below condition is to check for Stop words and consider only alphabets
                # 
                if word not in final_stopwords_list and word.isalpha():
                    #word_Final = word_Lemmatized.lemmatize(word)
                    word_Final = word
                    #steaming
                    doc = nlp(str(word_Final)) 
                    for token in doc:
                        word_Final =  token.lemma_
                    
                    #word_Final=stemming(word_Final)
                    Final_words.append(word_Final)
            # The final processed set of words for each iteration will be stored in 'text_final'
            data3.loc[index,'text_final'] = str(Final_words)

        data3['text_final'][0]
        news_p= Tfidf_vect.transform(data3['text_final'])
        predictions_news_p = Naive.predict(news_p)

        resultat = "******  Naive Bayes  :    "
        #print(" **************************  Naive Bayes  : ")
        if predictions_news_p==1:
            
            resultat=resultat+"Real"
        else :
            resultat=resultat+"Fake"
        #print(" **************************  SVM : ")
        predictions_nes= SVM.predict(news_p)

        resultat=resultat+ " ||     ******  SVM : "
        if predictions_nes==1:
            
            resultat=resultat+"Real"
        else :
            resultat=resultat+"Fake"

        News_Analyse_instance = DataText(
            text = resultat
        )

        return DetectNews(data=News_Analyse_instance)

        









class Mutation(graphene.ObjectType):
    detect_news = DetectNews.Field()
    analyse_data = AnalyseData.Field()
    clean_data = CleanData.Field()
    create_News = CreateNews.Field()
    create_Fake_News = CreateFakeNews.Field()
    update_News = UpdateNews.Field()
    update_fake_news = UpdateFakeNews.Field()
    delete_News = DeleteNews.Field()
    delete_fake_news = DeleteFakeNews.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)


