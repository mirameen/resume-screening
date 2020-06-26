Steps to run the resume screening app :-

1. You need to have nodejs and mongodb community server installed in your PC/laptop

2. Extract the code files from the zip or Download or Clone it from github link :- https://github.com/mirameen/resume-screening

3. Now we have to start the mongodb server and rasa server.

Note :- I have included a very primitive chatbot in this app, but you can replace it with any rasa chatbot developed by you for your specific needs.

4. Install rasa in your PC/laptop and run the following command in the chatbot folder to start the rasa server :- rasa run -m models --enable-api --cors "*" --debug

5. Start the mongodb server by typing the following command in your terminal :- ./mongod

6. Next run the following command to start the website :- node app.js

7. Open the browser and go to the url :- http://localhost:3000/ to view the website.


Note :- Input for skills should be given with a comma as separator between each skill, while adding a new job description.  