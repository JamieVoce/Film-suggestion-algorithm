from film_data_csv_reader import reading_csv
import binary_search

import profiler #This profiles the system so I can check if anything is too innefficient

#likes_to_update: list[int] = [0,2,3,4,5,6]
likes_to_update: list[int] = [x for x in range(500,600)]
likes_to_save: list[int] = [like_to_update for like_to_update in likes_to_update]
#A second list is made so films already used to calculate score do not need to be checked again 


@profiler.profile
def suggestion_alorithm(list_of_film_data):
    data_of_index: list[str] = [iterator for like in likes_to_update for iterator in list_of_film_data[like].get_data()]
    for like in likes_to_update:
        #Films watched checked here and not in selecting film so films can be set to watched after the program is closed
        if list_of_film_data[like].watched == False:
            list_of_film_data[like].set_watched()
            
    #This is unneceary on repeated runs^ there will only be one like so why bother sorting the films by id? Instead .get_(data) on the list used for binary sort! 
    likes_to_update.clear()
    for each_film in list_of_film_data: #Compare each film with the data of the films the user likes
        each_film.set_score(data_of_index)
    return list_of_film_data

  
def selecting_film(list_of_film_classes):
    like = input("\nWhat film do you like?").lower()
    #Binary Search
    list_of_film_classes.sort(key=lambda x: x.title) #Sort by title so binary search can be performed
    finding_film = binary_search.BinarySearch(list_of_film_classes, like, len(list_of_film_classes)-1)
    list_of_film_classes.sort(key=lambda x: x.id) #Sort by ID so the films are ready to get the data
    if finding_film != None:
        likes_to_update.append(finding_film)
        max_likes(finding_film, list_of_film_classes)  
    

def max_likes(finding_film, list_of_film_classes): #The system only keeps track of the last 100 films the user likes inbetween sessions
    if len(likes_to_save) >= 100:
        list_of_film_classes[likes_to_save[0]].set_not_watched()
        likes_to_save.pop(0)
    likes_to_save.append(finding_film)
   
def main():
    list_of_film_classes = reading_csv() # 0.1 seconds roughly
    while 1:
        list_of_film_classes = suggestion_alorithm(list_of_film_classes) #Uses the same variable as previously as to not use multiple variables for the same data
        list_of_film_classes.sort(key=lambda x: x.score, reverse=True) #Efficient sorting algorithm
        for x in range(10):
            print(list_of_film_classes[x].title + "\t" + str(list_of_film_classes[x].score)) #Faster to concatenate strings than to use ','
        
        selecting_film(list_of_film_classes)
        
main()