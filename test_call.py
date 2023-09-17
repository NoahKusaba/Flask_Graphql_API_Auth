import requests 

#Testing Output Successfuly 
body = """
{
  allBooks{
    edges{
      node{
        title
        description
        author{
          username
        }
      }
    }
  }
}
"""


token = requests.get("http://127.0.0.1:5000/token").json()['AUTH-HEADER']
breakpoint()
headers ={ 'AUTH-HEADER': token }

response = requests.get("http://127.0.0.1:5000/graphql-Auth",json={"query": body}, headers = headers)

breakpoint()