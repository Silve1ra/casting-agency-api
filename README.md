<h4 align="center">
  🚀 Casting Agency API
</h4>

<p align="center">
  
  <a href="https://github.com/Silve1ra/casting-agency-api/commits/main">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Silve1ra/casting-agency-api">
  </a>

  <a href="https://github.com/Silve1ra/casting-agency-api/issues">
    <img alt="Repository issues" src="https://img.shields.io/github/issues/Silve1ra/casting-agency-api">
  </a>

  <img alt="License" src="https://img.shields.io/badge/license-MIT-brightgreen">
</p>

This project is a casting agency to operate movies and actors. 
All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 


## 💻 Getting Started

### Live demo
url: https://casting-api-silve1ra.herokuapp.com/

documentation: https://casting-api-silve1ra.herokuapp.com/docs

### 🏡 Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines.

To run the application run the following commands: 
```
export FLASK_APP=app
export FLASK_ENV=development
flask run
```
or (Windows 10 PowerShell):
```
$env:FLASK_APP='app'
$env:FLASK_ENV='development'
flask run
```

The application is run on `http://127.0.0.1:5000/` by default.

---

### ✔ Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
python test_app.py
```


### 🎯 Endpoints
There are complete information about endpoints in the documentation, please refer there [Docs](https://casting-api-silve1ra.herokuapp.com/docs "Documentation")


### ⛔ Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Unprocessable 
- 500: Internal Server Error

---

## 🤔 How to Contribute

- Clone the project: `git clone git@github.com:Silve1ra/casting-agency-api.git`;
- Create your branch with your feature: `git checkout -b my-feature`;
- Commit your feature: `git commit -m 'feat: My new feature'`;
- Push to your branch: `git push -u origin my-feature`.

After the merge of your pull request is done, you can delete your branch.

## :memo: License

This project is under the MIT license. See the [LICENSE](LICENSE.md) file for more details.


## 🍸 Acknowledgements 
The awesome Udacity Nanodegree helping me to be an extraordinary full stack developer! 

---

Made with ♥ by <tr>
    <td align="center"><a href="https://github.com/silve1ra"><b>Felipe Silveira</b></a><br /></td>
<tr>
