import asyncio
import logging

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from doctr.datasets import VOCABS  # Ensure this is available in your environment
from word_image_synth.database import DatabaseManager


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

    # remove words less than 2 chars
    words = [word for word in words if len(word) >= 2]

    return words


async def generate_word_list(output_dir, max_words, vocab, lang, concurrent_requests=5):
    """
    Generate words from Wikipedia and save them to an SQLite database,
    using asynchronous requests to fetch multiple pages concurrently.
    Words are saved to the database after each finished task.
    """
    db = DatabaseManager(output_dir)

    # Check the current count of words for the specified language
    current_count = await db.get_word_count(lang)
    if current_count >= max_words:
        logging.info(
            f"The database already contains {current_count} words for the language '{lang}', "
            f"which meets or exceeds the max_words limit of {max_words}. No additional words will be fetched."
        )
        return

    async with ClientSession() as session:
        tasks = set()  # Using a set to manage tasks
        words = set()  # To store unique words

        while current_count < max_words:
            # Only create new tasks if below the concurrent request limit and target word count has not been reached
            while len(tasks) < concurrent_requests and current_count < max_words:
                task = asyncio.create_task(get_random_words(session, lang, vocab))
                tasks.add(task)

            done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                tasks.remove(task)
                new_words = task.result()
                words.update(new_words)

                # Save words after each task completion
                await db.save_words_to_db(words, lang)
                words.clear()  # Clear the set after saving
                logging.info(f"Saved {len(new_words)} words to database. Progress is now updated.")

                # Update current_count to ensure it reflects the latest number of words in the database for the specified language
                current_count = await db.get_word_count(lang)
                if current_count >= max_words:
                    break  # Exit if the target word count is reached or exceeded

        # In case there are any words left unsaved due to an early loop exit
        if words:
            await db.save_words_to_db(words, lang)
            logging.info("Final save: Saved remaining words.")

    # select all labels from the database
    labels = db.get_labels()

    # 