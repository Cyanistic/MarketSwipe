# Python Backend (Flask + SQLite)
## Initial Setup
<details> 

<summary>macOS/Linux</summary>

> 
> 1. Create a virtual environment
> ```
> python -m venv .venv
> ``` 
> 2. Activate the environment
> ```
> source .venv/bin/activate
> ``` 
> 3. Install python dependencies
> ```
> pip install -r requirements.txt
> ```
> Once all python dependencies are installed you can move on to the [running](#running) section

</details>

<details> 
<summary>Windows</summary>

> 1. Create a virtual environment
> ```
> py -3 -m venv .venv
> ``` 
> 2. Activate the environment
> ```
> .venv\Scripts\activate
> ``` 
> 3. Install python dependencies
> ```
> pip install -r requirements.txt
> ```
> Once all python dependencies are installed you can move on to the [running](#running) section

</details>  

## Running

<details> 
<summary>macOS/Linux</summary>

> 
> 1. Activate your virtual environment. This must be done every time you exit the shell.
> ```
> source .venv/bin/activate
> ``` 
> 2. Run the startup command
> ```
> flask --app main run
> ```
> 3. (Optional) Deactivate your virtual environment
> ```
> deactivate
> ```

</details>

<details> 
<summary>Windows</summary>

> 
> 1. Activate your virtual environment. This must be done every time you exit the shell.
> ```
>  .venv\Scripts\activate
> ``` 
> 2. Run the startup command
> ```
> flask --app main run
> ```
> 3. (Optional) Deactivate your virtual environment
> ```
> deactivate
> ```

</details>  
