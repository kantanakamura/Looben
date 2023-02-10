from .models import Users


def for_earning_post_likes(author):
    author.contributed_points += 1
    author.save()
    
    
def for_losing_post_likes(author):
    author.contributed_points -= 1
    author.save()


def for_getting_best_answer(user):
    user.contributed_points += 3
    user.save()
    
    
def for_creating_post(author):
    author.contributed_points += 1
    author.save()
    
    
def for_creating_question(user):
    user.contributed_points += 0.3
    user.save()
    
    
def for_creating_review(user):
    user.contributed_points += 0.3
    user.save()
    

def for_getting_follower(user):
    user.contributed_points += 0.5
    user.save()
    

def for_losing_follower(user):
    user.contributed_points -= 0.5
    user.save()