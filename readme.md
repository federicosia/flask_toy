## How to run

This software can be launched in two ways, by installing all the dependecies needed on the current machine or using Docker. Starting with the first approch:

1. Install Python 3.12 and MongoDB 7.0 (other versions were not tested, but you can try using other versions at your risk)
2. Start MongoDB's service
3. Open the terminal and position yourself in project's root directory
4. Create a virtual environment by:
    1. Running ```pip install virtualenv```
    2. Create a directory were all depedencies and utility scripts are stored by launching the command ``` python -m venv <environment_name>```
    3. Position yourself in **Scripts** inside the created directory and launch the script ```Activate.ps1``` (in Powershell), ```Activate.bat``` (in CMD) or ```activate``` (Linux/MacOS). You should be in the virtual environment.
5. Launch the command  ```pip install -r requirements.txt``` to install all the dependecies needed
6. Launch the command ```flask --app .\source\app run``` to start the application in localhost!

The recommended approach though is by using Docker:

1. Install Docker
2. Position yourself the root directory and launch the command ```docker compose up -d```, two containers will start, one for the Flask application and the other one with MongoDB instance. 

After command has done running, you can interact with the software with localhost using the browser, like it was installed on your local machine!

> [!NOTE] 
> In the directory **doc** are present a Swagger and a Postman's collection.
> At the endpoint **/openapi** you can view, in browser, the Swagger (remember to start
> the application first!).