# SpeakGPT
A back-end and front-end implementation to speak with ChatGPT via mobile app, browser, CLI or API.

## To Do
Some improvements are necessary to have a better and fluid experience.

### [Back-end](./backend/)
* Add `.env` file for configuration
* Improve setup documentation
* Improve CLI using [Click](https://click.palletsprojects.com/en/8.1.x/)
* Add a NoSQL Database as Repository
* Create Dockerfile and Docker Compose to automate the infrastructure
* Add authentication to isolate conversations by authenticated user, creating a historic
* Create websocket for the chat? Instead of HTTP requests
* Improve Text to Speech with voice options
* Improve Speech to Text with auto correction, adding semi collons, etc

### [Front-end](./frontend/)
* Add streaming by response from AI, not download all the audio and then play it, but downloading and playing audio in the same time
* Improve User Experience and User Interface
* Add SignUp and SignIn screens
* Add dotenv configuration

## Author
Created by **Lucas França**:
* Website: https://lucasfrancaid.com.br
* LinkedIn: https://linkedin.com/in/lucasfrancaid
