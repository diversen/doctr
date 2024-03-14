import asyncio
import aiohttp
import os
import tempfile
from bs4 import BeautifulSoup
import json
import os
import logging

from doctr.datasets import VOCABS  # Ensure this is available in your environment


async def save_words_safe(words, json_file):
    """
    Save the words to the json_file safely by writing to a temporary file
    and then renaming it to the original file name.
    """
    # Create a temporary file in the same directory as the original file
    dir_name = os.path.dirname(json_file)
    with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8", dir=dir_name, suffix=".tmp") as tmp_file:
        json.dump(words, tmp_file, ensure_ascii=False, indent=4)
        temp_file_name = tmp_file.name

    # Replace the original file with the temporary file
    os.replace(temp_file_name, json_file)

async def fetch_page(session, lang="da"):
    """
    Asynchronously fetch a random Wikipedia page.
    """
    logging.debug(f"Fetching random Wikipedia page in {lang}...")
    random_url = f"https://{lang}.wikipedia.org/wiki/Special:Random"
    async with session.get(random_url) as response:
        return await response.text()

async def get_random_words(session, lang="da", vocab=None):
    """
    Extract words from a random Wikipedia page.
    """
    page_content = await fetch_page(session, lang)
    soup = BeautifulSoup(page_content, "html.parser")
    article_text = soup.find_all("p")
    p_content = [tag.get_text().replace("\n", "").strip() for tag in article_text]
    words = " ".join(p_content).split(" ")
    
    if vocab:
        vocab_ = VOCABS[vocab]
        words = [word for word in words if all(char in vocab_ for char in word)]

    words = [word for word in words if word]

    # remove words over 32 chars
    words = [word for word in words if len(word) <= 32]

    return words

async def generate_word_list(json_file, max_words, vocab, lang, concurrent_requests=5, save_every_n_tasks=5):
    """
    Generate words from Wikipedia and save them to a json file,
    using asynchronous requests to fetch multiple pages concurrently.
    Save the progress to the file after every 'save_every_n_tasks' tasks are completed.
    """
    if not os.path.exists(json_file):
        await save_words_safe([], json_file)

    with open(json_file, "r", encoding="utf-8") as f:
        words = json.load(f)

    print(f"Fetching {max_words} words from Wikipedia in {lang}...")

    async with aiohttp.ClientSession() as session:
        tasks = []
        completed_tasks = 0  # Keep track of completed tasks to know when to save
        while len(words) < max_words:
            for _ in range(concurrent_requests - len(tasks)):
                if len(words) >= max_words:
                    break  # Stop creating new tasks if we have enough words
                task = asyncio.create_task(get_random_words(session, lang, vocab))
                tasks.append(task)

            done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                tasks.remove(task)
                words.extend(task.result())
                words = sorted(set(words))  # Unique words, sorted
                completed_tasks += 1

                if completed_tasks >= save_every_n_tasks:
                    # Save progress to the file safely
                    await save_words_safe(words, json_file)
                    logging.info(f"Saved {len(words)} words to {json_file}.")
                    completed_tasks = 0  # Reset the counter

                if len(words) >= max_words:
                    break  # Break if max words is reached

    # Final save to ensure all progress is stored
    words = words[:max_words]  # Ensure we don't exceed max_words
    await save_words_safe(words, json_file)
    logging.info(f"Final save: {len(words)} words to {json_file}.")
