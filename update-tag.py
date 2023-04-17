import requests
import json

user = ""
token = ""

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json"
}
apiUrl = "https://api.github.com/user/repos"
response = requests.get(apiUrl, headers=headers)

if response.status_code == 200:
    repos = json.loads(response.text)
    for repo in repos:
        repo_name = repo["name"]
        print(f"Repository: {repo_name}")
        try:
            tagsUrl = f"https://api.github.com/repos/{user}/{repo_name}/git/refs/tags?ref=refs/heads/main"
            response = requests.get(tagsUrl, headers)
            response.raise_for_status()
            tag = json.loads(response.text)

            position = -1
            latest_tag = tag[position]["ref"].split("/")[-1]
            suffix = "-"
            while suffix in latest_tag:
                position = position - 1
                latest_tag = tag[position]["ref"].split("/")[-1]

            sha = tag[position]['object']['sha']
            print(f"SHA: {sha}")
            print(f"Latest tag: {latest_tag}")

            major, minor, patch = latest_tag.split(".")

            if (int(major) < 1):
                major = 1
            else:
                major = str(int(major) + 1)

            minor = 0
            patch = 0
            new_tag = f"{major}.{minor}.{patch}"
            print(f"New tag: {new_tag}")

            tag_data = {
                "tag": new_tag,
                "message": "New tag created",
                "object": sha,
                "type": "commit"
            }

            ref_data = {
                "ref": f"refs/tags/{new_tag}",
                "sha": sha
            }

            tag_url = f"https://api.github.com/repos/{user}/{repo_name}/git/tags"
            tag_response = requests.post(tag_url, headers=headers, data=json.dumps(tag_data))
            tag_response.raise_for_status()

            ref_url = f"https://api.github.com/repos/{user}/{repo_name}/git/refs"
            ref_response = requests.post(ref_url, headers=headers, data=json.dumps(ref_data))
            ref_response.raise_for_status()

            print(f'New tag {new_tag} created for repository {repo_name}')
            print("------------------------------------------------------------------")

        except:
            print(f"Something went wrong whit repository {repo_name}")
            print("------------------------------------------------------------------")

elif response.status_code == 401:
    print("Error: Unauthorized - check your access token")
elif response.status_code == 404:
    print("Error: Resource not found - check the API endpoint")
else:
    print(f"Error: {response.status_code}")
