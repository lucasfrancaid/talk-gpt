# TalkGPT
A back-end and front-end implementation to talk to ChatGPT via mobile app, browser, CLI or API.

## A Short Story
I created this project to improve my English using ChatGPT. 
I had the idea to create a mobile application that would allow me talk with ChatGPT using `audio` and `voice`, and I did it (_in few hours_). 
I used it for a while and was able to improve my English, at least a little. 
Now, I've just opened up this project for contributions and added some features, such as using the CLI with specific prompts that direct ChatGPT's behavior to the desired topic (_e.g. ChatGPT acting as an English Teacher_) or even without specific prompts, allowing you to ask anything.

**NOTE**: I decided to build the `text-to-speech` and `speech-to-text` functions on the back-end because it's easier to handle in Python due to the _Open Source_ libraries. Furthermore, it's difficult to deal in `React Native` because of the Expo (_I can be wrong_).

## To Do
Some improvements are necessary to have a better and fluid experience.

### [Back-end](./backend/)
* Add sent_at in messages
* Add a NoSQL Database as Repository
* Create Dockerfile and Docker Compose to automate the infrastructure
* Add authentication to isolate conversations by authenticated user, creating a historic
* Create websocket for the chat? Instead of HTTP requests
* Improve Text to Speech with voice options
* Improve Speech to Text with auto correction, add comma, full stop, etc

### [Front-end](./frontend/)
* Add streaming by response from AI, not downloading all the audio then playing it, but downloading and playing audio as chunks
* Improve User Experience and User Interface
* Add SignUp and SignIn screens
* Add dotenv configuration

## Contributing
I would really appreciate it if you could contribute to this project. Either on the back-end or front-end, you can contribute with something in our [To do list](#to-do).  
If you have nice skills of UI/UX don't hesitate to contribute as well, I'm not good at all.

## Author
Created by **Lucas França**:
* Website: https://lucasfrancaid.com.br
* LinkedIn: https://linkedin.com/in/lucasfrancaid
