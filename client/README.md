# HTML + CSS + JS Frontend 
## Initial Setup
<details> 

<summary>MacOS/Linux</summary>

> 
> 1. Create a Virtual Environment
> ```
> fnm env | Out-String | Invoke-Expression
> ``` 
> 2. Navigate to Project's Front-end Folder
> ```
> cd client
> ``` 
> 3. Install Dependencies
> ```
> npm install
> npm install react-router-dom
> ```
> Once all information is installed you can move on to the [running](#running) section

</details>

<details> 
<summary>Windows</summary>

> 
> 1. Create a Virtual Environment
> ```
> fnm env | Out-String | Invoke-Expression
> ``` 
> 2. Navigate to Project's Front-end Folder
> ```
> cd client
> ``` 
> 3. Install Dependencies
> ```
> npm install
> npm install react-router-dom
> ```
> Once all information is installed you can move on to the [running](#running) section

</details>  

## Running

<details> 
<summary>macOS/Linux</summary>

> 
> 1. Activate Your Local Host
> ```
> npm run dev
> ``` 
> 2. (Optional) Stop Local Host
> ```
> Ctrl + C
> Type "Y" at Stop Batch Prompt
> ```

</details>

<details> 
<summary>Windows</summary>

> 
> 1. Activate Your Local Host
> ```
> npm run dev
> ``` 
> 2. (Optional) Stop Local Host
> ```
> Ctrl + C
> Type "Y" at Stop Batch Prompt
> ```

</details>  

## Troubleshooting
If you get an error when attempting to run `npm run dev`, you are most likely missing dependencies. To resolve delete the `.vite\deps` folder under the `node_modules` folder, and run again the commands in steps 1-3 of the Initial Setup section.
