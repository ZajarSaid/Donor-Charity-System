from users.models import CustomUser, Charithy
from Activity.models import Venue, Event, Comment
from django.shortcuts import get_object_or_404



def run():

  # taking all events with their corresponding id's
  comments = Comment.objects.all()
  for comment in comments:
    print(comment.author)
    print(comment.post)
    print(comment.body)
    



  
  e_names = []

  # assign members of event from custom users
  
  
  # for event in events:
  #    for member in event.members.all:
  #     print(member.username)
  #     print(member.status)
    
    # event.members.add(Kevo)
    # print(event.members.all)

  
 
  # members_id = []

  # for event in events:
  #   MEMBERS = event.members.add(Ceo)
    

  
  # event_members = [members for event.members.all in events]

  

  




  

















    #description = 'For all kind of contracts'
    #Category.objects.create(name='Contracts', description= description)
    #g = Category.objects.values()
    # f_name = 'John'
    # m_name = 'John'
    # l_name = 'John'
    # age = 23
    #print (g)
    # User = Charithy.objects.create(first_name=f_name, middle_name=m_name, last_name=l_name, age=age)
    # Result = Charithy.objects.values().filter(age=25)
    
    # Result = Charithy.objects.all()
    # r2=Charithy.objects.select_related('created_by').values()
    # # Result.delete()
    # # print(Result)
    # for r in Result:
      
    #   print(r.created_by)
    # User.save()
    # Venues = Venue.objects.all()




        
        


  #  api_url = 'https://api.covid19api.com/countries'
   # response = requests.get(api_url)

   # if response.status_code == 200:
     #   if response.text:  # Check if response has data
      #      try:
       #         api_data = response.json()
        #        # Process the JSON data here
         #       for region in api_data:
          #          print (region)
           # except ValueError as e:
            #    print(f"Error parsing JSON: {e}")
        #else:
         #   print("Empty response received from the API.")
    #else:
     #   print(f"Failed to fetch data from API. Status code: {response.status_code}")




