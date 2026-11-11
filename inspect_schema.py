import requests

token = 'PusyzNtSvSHFlLIGi1yzLLmA4Fl_5kLFHQ8t51-59MH'
query = """
query {
  __type(name: "PostTypeFacebook") {
    enumValues {
      name
      description
    }
  }
}
"""
r = requests.post('https://api.buffer.com/graphql', headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}, json={'query': query})
values = r.json().get('data', {}).get('__type', {}).get('enumValues', [])
for v in values:
    print(v['name'])
