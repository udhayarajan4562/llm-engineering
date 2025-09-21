import requests
from bs4 import BeautifulSoup
from IPython.display import display, Markdown
import ollama

# Define headers for requests
headers = {"User-Agent": "Mozilla/5.0"}

class Website:
    def __init__(self, url):
        """
        Create a Website object from the given URL using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        self.title = soup.title.string if soup.title else "No title found"

        # Remove irrelevant tags (scripts, styles, images, inputs)
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()

        # Get cleaned text
        self.text = soup.body.get_text(separator="\n", strip=True)

# System prompt for the model
system_prompt = (
    "You are an assistant that analyzes the contents of a website "
    "and provides a short summary, ignoring text that might be navigation related. "
    "Respond in markdown."
)

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}\n"
    user_prompt += "The contents of this website is as follows; "
    user_prompt += "please provide a short summary of this website in markdown. "
    user_prompt += "If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

def summarize(url):
    website = Website(url)
    response = ollama.chat(
        model="deepseek-r1:1.5b",  # Make sure you have this model installed in ollama
        messages=messages_for(website)
    )
    return response["message"]["content"]

def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))

# Example usage
if __name__ == "__main__":
    display_summary("https://cnn.com")
