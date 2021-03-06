## github-orgs-api
---

For calculating score of all members of any github organisation and top contributors of all repositories.

[![view original](https://img.shields.io/badge/upstream-view%20source%20repo-orange.svg)](https://github.com/GDGVIT/gdginfo-backend.git) [![docs](https://img.shields.io/badge/docs-view%20API%20documentation-brightgreen.svg)](https://codechefvit.github.io/github-orgs-api/) [![deployment](https://img.shields.io/badge/deployment-go%20to%20API%20endpoint-yellow.svg)](https://cc-leaderboard.herokuapp.com/)

<br/>

### Some features

- [X] GitHub Graph API
- [X] Interchangable organization leaderboard
- [X] Top contributors for organizations
- [X] Repository specific metadata for organizations
- [X] Pluggable caching layer 
- [X] Automatic Scheduled cache update
- [X] Manual cache update

<br/>

### Getting Started

You can use this application easily just by changing the following credentials..

* Redis server url (optional)
* Name of the organization
* Github api key

This project uses `.env`. To configure, simply make a file named *.env* in the root of your project and add the following lines to it.

```
# GitHub token
TOKEN=<Your github token, under developer settings on GitHub>

# organization handle on GitHub 
ORGANIZATION=<Name of the organization as specified in GitHub>

# redis URI
REDIS_URL=<your redis url>
```

<br/>

### How to use

Clone the repository and add the above credentials.

```bash
git clone https://github.com/CodeChefVIT/github-orgs-api.git
cd github-orgs-api
pip install -r requirements.txt
## Create .env (see sample above) 
```

<br/>

### Ways to run

*	**Regular mode**: run this if you do not want a caching layer in your application. Will drastically increase response time but save the cost of having a caching service

```
python api_server.py
```

* **Caching mode**: run this if you want a caching layer in your application. Will drastically decrease response latency.

```
python api_server.py --with-cache
```
<br/>

### How it works

**Algorithm**: It uses github api and fetches the information about members, all the repositories in that organization, 
members contribution in those repository.
The application scrolls through all the repositories that belong to this organization.
and using that it calculates contribution a particular individual based on his contribution to that repository.


| Action | Weightage |
|:------:|:---------:|
| stargazers count | 10 |
| watchers count | 10 |
| forks count | 15 |
| contributions | 40 |

<br/>

```python
d[contributors['login']] += project[1] * 10 + project[2] * 5 +project[3] * 15 + contributors['contributions'] * 40
```
<br/>

**Caching**: When the `--with-cache` flag is provided, all responses are served from a cache. This cache is updated daily. This significantly decreases response latency since github api provides only 10 requests per minute. 


<br/>

### Limitations

* Only 30 repositories can be fetched from the API at one time.
* Only 10 requests can be made to the API per minute.

<br/>

### Mitigation

* Pluggable caching layer
* Cron cache seed 
* Manual cache seed ( because heroku dynos go to sleep after 30 minutes of inactivity )

### Built With

* [GithubApi](https://developer.github.com/v3/) 

### Built by
* [GDGVIT](https://www.gdgvitvellore.com)
* [CodeChef-VIT](http://www.codechefvit.com)

### Contributors

* Shubham Bhardwaj
* Apurva Nitanjay
* Angad Sharma

#### References
See [FAQs](https://github.com/CodeChefVIT/github-orgs-api/wiki/FAQs-and-references)
