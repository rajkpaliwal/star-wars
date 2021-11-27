from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
import math 
import os

def Home(request):
	if os.path.exists('characters_data.json'):
		with open('characters_data.json', 'r') as file:
			all_chars_data = json.load(file)
			file.close()
	else:
		all_chars_data = []

		total_characters = requests.get('https://swapi.dev/api/people/').json()['count']
		pages = math.ceil(total_characters/10)

		for page in range(1, pages+1):
			character_data = requests.get('https://swapi.dev/api/people/?page='+str(page)).json()['results']
			all_chars_data.extend(character_data)

		json_object = json.dumps(all_chars_data, indent=4) # Added indent to make json file human readable
		with open("characters_data.json", "w") as file:
			file.write(json_object)
			file.close()

	return render(request, 'index.html', {'characters_data':all_chars_data})

def Graph(request):
	if os.path.exists('characters_data.json'):
		with open('characters_data.json', 'r') as jsonfile:
			all_chars_data = json.load(jsonfile)
			jsonfile.close()

			all_chars_data[:] = [d for d in all_chars_data if d.get('height') != "unknown" and d.get('gender') in ["male","female"]]

			data = []
			for record in all_chars_data:
				temprecord = {'name':record['name'], 'height':int(record['height']), 'gender':record['gender']}
				data.append(temprecord)

		return render(request, 'graph.html', {'data':data})
	else:
		return redirect('/')