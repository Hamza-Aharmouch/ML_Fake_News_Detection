import graphene

from graphene_django import DjangoObjectType, DjangoListField 
from api.models import FakeNews



class FakeNewsType(DjangoObjectType):
    class Meta:
        model = FakeNews
        fields = "__all__"   #we can chose all field by using this fields = "__all__" or ("id","title","details","date")


#now we create a query 
class Query(graphene.ObjectType):
    all_fake_news = graphene.List(FakeNewsType)
    fake_news = graphene.Field(FakeNewsType, fake_news_id=graphene.Int(required=True))

    def resolve_all_fake_news(self, info, **kwargs):
        return News.objects.all()

    def resolve_fake_news(self, info, fake_news_id):
        return News.objects.get(pk=fake_news_id)

class FakeNewsInput(graphene.InputObjectType):
    #id = graphene.ID()
    title = graphene.String()
    details = graphene.String()
    #date = graphene.String()



class CreateFakeNews(graphene.Mutation):
    class Arguments:
        Fake_News_data = FakeNewsInput(required=True)

    Fake_News = graphene.Field(FakeNewsType)

    @staticmethod
    def mutate(root, info, Fake_News_data):
        Fake_News_instance = Fake_News( 
            #id=News_data.id,
            title=Fake_News_data.title,
            details=Fake_News_data.details,
            #date=News_data.date
        )
        Fake_News_instance.save()
        return CreateFakeNews(Fake_News=Fake_News_instance)


class UpdateFakeNews(graphene.Mutation):
    class Arguments:
        Fake_News_data = FakeNewsInput(required=True)
        id = graphene.ID()

    Fake_News = graphene.Field(FakeNewsType)

    @staticmethod
    def mutate(root, info, Fake_News_data, id):

        Fake_News_instance = News.objects.get(pk=id)

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


class Mutation(graphene.ObjectType):
    create_Fake_News = CreateFakeNews.Field()
    update_Fake_News = UpdateFakeNews.Field()
    delete_Fake_News = DeleteFakeNews.Field()


schemaF = graphene.Schema(query=Query, mutation=Mutation)