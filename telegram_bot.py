import json
import requests
import urllib
import datetime
import logging
from requests.models import DEFAULT_REDIRECT_LIMIT
import time

# Logging configuration
logging.basicConfig(
    filename="telegram_bot.log", level=logging.INFO, format="%(asctime)s %(message)s"
)
TOKEN = "<YOUR_TELEGRAM_BOT_TOKEN>"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
USERNAME_BOT = "<YOUR_TELEGRAM_BOT_USERNAME>"
DISCORD_CHANNEL_LINK = "<YOUR_DISCORD_CHANNEL_LINK>"
CLIST_USERNAME = "<YOUR_CLIST_USERNAME>"
CLIST_API_KEY = "<YOUR_CLIST_API_KEY>"
CLUB_WEBSITE = "<YOUR_CLUB_WEBSITE>"
# Modify the API calls to your club website to get the data


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# Commands
def start(chat_id):
    send_message(
        "Hey there, I'm a bot created by Zero Bugs Club, VIT Chennai. Type /help to see what I can do for you.",
        chat_id,
    )


def help(chat_id):
    send_message(
        """
        Commands available:
        /start - Start the bot
        /about - What is Zero Bugs Club?
        /discord - Join our discord channel
        /club_heads - Club Heads
        /contact - Contact the admin
        /faq - FAQs
        /help - To see this message

        Club events:
        /upcoming_events - Upcoming events of the club
        /past_events - Past events of the club

        Contests Details:
        /codeforces - Codeforces Timeline
        /google - Google Timeline
        /codechef - Codechef Timeline
        """,
        chat_id,
    )


def upcoming_events(chat_id):
    send_message(
        "This feature is not yet implemented",
        chat_id,
    )


def about(chat):
    send_message(
        "Zero Bugs Club is a club of VIT students, who are interested in learning about the latest technologies and trends in the field of computer science.\n\nZero Bugs Club is a student run club, and we are always looking for new members to join us.\n\nIf you are interested in joining us, Join our discord channel at "
        + DISCORD_CHANNEL_LINK,
        chat,
    )


def discord(chat):
    send_message(DISCORD_CHANNEL_LINK, chat)


def codechef_contest(chat_id):
    try:
        response = requests.get(
            "https://clist.by/api/v1/json/contest/?username={}&api_key={}&resource__name=codechef.com&limit=5&start__gte=".format(
                CLIST_USERNAME, CLIST_API_KEY
            )
            + datetime.datetime.now().strftime("%Y-%m-%d")
            + "&filtered=true&order_by=start"
        )
        contests = json.loads(response.content.decode("utf8"))["objects"]
        message = "Codechef Timeline for next 5 contests: \n\n"
        send_message(message, chat_id)
        for contest in contests:
            message = ""
            ts = time.strptime(contest["start"], "%Y-%m-%dT%H:%M:%S")
            message += "Event Name: " + contest["event"] + "\n"
            message += (
                "Starts On: "
                + time.strftime("%d/%m/%Y", ts)
                + " at "
                + time.strftime("%H:%M:%S", ts)
                + "\n"
            )
            message += (
                "Duration: "
                + str(datetime.timedelta(seconds=contest["duration"]))
                + " hours\n"
            )
            message += "Link: " + contest["href"] + "\n\n\n"
            send_message(message, chat_id)
    except:
        send_message(
            "Cannot process this request as of now. Please try in few minutes.",
            chat_id,
        )


def google_contest(chat_id):
    try:
        response = requests.get(
            "https://clist.by/api/v1/json/contest/?username={}&api_key={}&resource__name=codingcompetitions.withgoogle.com&limit=5&start__gte=".format(
                CLIST_USERNAME, CLIST_API_KEY
            )
            + datetime.datetime.now().strftime("%Y-%m-%d")
            + "&filtered=true&order_by=start"
        )
        contests = json.loads(response.content.decode("utf8"))["objects"]
        message = "Google Timeline for next 5 contests: \n\n"
        send_message(message, chat_id)
        for contest in contests:
            message = ""
            ts = time.strptime(contest["start"], "%Y-%m-%dT%H:%M:%S")
            message += "Event Name: " + contest["event"] + "\n"
            message += (
                "Starts On: "
                + time.strftime("%d/%m/%Y", ts)
                + " at "
                + time.strftime("%H:%M:%S", ts)
                + "\n"
            )
            message += (
                "Duration: "
                + str(datetime.timedelta(seconds=contest["duration"]))
                + " hours\n"
            )
            message += "Link: " + contest["href"] + "\n\n\n"
            send_message(message, chat_id)
    except:
        send_message(
            "Cannot process this request as of now. Please try in few minutes.",
            chat_id,
        )


def codeforces_contest(chat_id):
    try:
        response = requests.get(
            "https://clist.by/api/v1/json/contest/?username={}&api_key={}&resource__name=codeforces.com&start__gte=".format(
                CLIST_USERNAME, CLIST_API_KEY
            )
            + datetime.datetime.now().strftime("%Y-%m-%d")
            + "&filtered=true&order_by=start"
        )

        contests = json.loads(response.content.decode("utf8"))["objects"]
        message = "Codeforces Timeline for next 5 contests: \n\n"
        send_message(message, chat_id)
        for contest in contests:
            message = ""
            ts = time.strptime(contest["start"], "%Y-%m-%dT%H:%M:%S")
            message += "Name: " + contest["event"] + "\n"
            message += (
                "Starts On: "
                + time.strftime("%d/%m/%Y", ts)
                + " at "
                + time.strftime("%H:%M:%S", ts)
                + "\n"
            )
            message += (
                "Duration: "
                + str(datetime.timedelta(seconds=contest["duration"]))
                + " hours\n"
            )
            message += "Link: " + contest["href"] + "\n\n\n"
            send_message(message, chat_id)
    except:
        send_message(
            "Cannot process this request as of now. Please try in few minutes.",
            chat_id,
        )


def contact(chat):
    send_message(
        "You can contact the admin at @vishalteotia",
        chat,
    )


def faq(chat):
    """
    Frequently asked questions about the club.
    """
    send_message(
        "1. What is Zero Bugs Club?\n\n"
        + "2. How can I join Zero Bugs Club?\n\n"
        + "3. What are the benefits of joining Zero Bugs Club?\n\n"
        + "4. How can I get involved in the club?\n\n"
        + "5. What skills are required to join Zero Bugs Club?\n\n"
        + "6. What are the rules of the club?\n\n"
        + "7. How to contact the admin?\n\n"
        + " Type /answer/<question number> to get the answer to the question.\n Like /answer/1",
        chat,
    )


def answer(chat, question):
    if question == "1":
        send_message(
            "What is Zero Bugs Club? \n\nZero Bugs Club is a techincal club of VIT, Chennai. We are a student run club, mainly focusing on learning about the latest frameworks and technologies in the field of computer science. We use our knowledge to help other students in their studies. We also help students in their projects. We help them develop real world applications to put in use with hundreds/thousands of user. We are always looking for new members to join us.",
            chat,
        )
    elif question == "2":
        send_message(
            "How can I join Zero Bugs Club?\n\nWe have regular recruitment drives, and we are always looking for new members to join us. You can get updates of recruitments on our discord server "
            + DISCORD_CHANNEL_LINK,
            chat,
        )
    elif question == "3":
        send_message(
            "What are the benefits of joining Zero Bugs Club?\n\n1. You will get experienced developers to collaborate with you on your projects.\n"
            + "2. You will get mentorship from the club members.\n"
            + "3. You will get a chance to interact with the club members.\n"
            + "4. You will get exposure to the latest frameworks and technologies in the field of computer science.\n"
            + "5. You will get exposure to real world applications.\n"
            + "And more is there to come.",
            chat,
        )
    elif question == "4":
        send_message(
            "How can I get involved in the club?\n\nYou can join us by sending us a message on our discord channel."
            + DISCORD_CHANNEL_LINK,
            chat,
        )
    elif question == "5":
        send_message(
            "What skills are required to join Zero Bugs Club?\n\nWe don't have any specific skills required to join us. The only requirement is that you are a student of VIT, Chennai and want to learn about the latest frameworks and technologies while working on real world applications.",
            chat,
        )
    elif question == "6":
        send_message(
            "What are the rules of the club?\n\nRespect is the key to success. Respect the club members and the club itself.",
            chat,
        )
    elif question == "7":
        send_message(
            "How to contact the admin?\n\nYou can contact the admin at @vishalteotia",
            chat,
        )
    else:
        send_message(
            "Invalid question number. Please type /faq to get the list of questions.",
            chat,
        )


def answers(text, chat):
    ques_num = text.split("/")[-1]
    answer(chat, ques_num)


def club_heads(chat):
    response = requests.get(CLUB_WEBSITE + "/get_admin_names")
    message = "Club Heads: \n\n"
    for head in json.loads(response.content.decode("utf8")):
        message += (
            head["fields"]["user_first_name"]
            + " "
            + head["fields"]["user_last_name"]
            + "\n"
        )
        message += "Post: " + head["fields"]["user_post"] + "\n"
        if (
            head["fields"]["user_insta"] != None
            and head["fields"]["user_insta"] != ""
            and head["fields"]["user_insta"] != "None"
        ):
            message += "Insta: " + head["fields"]["user_insta"] + "\n"
        if (
            head["fields"]["user_github"] != None
            and head["fields"]["user_github"] != ""
            and head["fields"]["user_github"] != "None"
        ):
            message += "Github: " + head["fields"]["user_github"] + "\n"
        if (
            head["fields"]["user_linkedin"] != None
            and head["fields"]["user_linkedin"] != ""
            and head["fields"]["user_linkedin"] != "None"
        ):
            message += "LinkedIn: " + head["fields"]["user_linkedin"] + "\n"
        message += "\n"
    send_message(message, chat)


def upcoming_events(chat):
    response = requests.get(CLUB_WEBSITE + "/get_upcoming_events")
    message = "Upcoming Events: \n\n"
    events = json.loads(response.content.decode("utf8"))
    if events:
        for event in events:
            ts = time.strptime(
                event["fields"]["event_start_date"], "%Y-%m-%dT%H:%M:%SZ"
            )
            message += "Name: " + event["fields"]["event_name"] + "\n"
            message += (
                "Starts On: "
                + time.strftime("%d/%m/%Y", ts)
                + " at "
                + time.strftime("%H:%M:%S", ts)
                + "\n\n"
            )
        message += "For more details, visit our website: " + CLUB_WEBSITE
        send_message(message, chat)
    else:
        send_message("No upcoming events. We are planning one soon.", chat)


def past_events(chat):
    response = requests.get(CLUB_WEBSITE + "/get_past_events")
    message = "Past Events: \n\n"
    events = json.loads(response.content.decode("utf8"))
    if events:
        for event in events:
            ts = time.strptime(
                event["fields"]["event_start_date"], "%Y-%m-%dT%H:%M:%SZ"
            )
            # message += "<image src={}>".format(event["fields"]["event_image"])
            message += "Name: " + event["fields"]["event_name"] + "\n"
            message += (
                "Held On: "
                + time.strftime("%d/%m/%Y", ts)
                + " at "
                + time.strftime("%H:%M:%S", ts)
                + "\n\n"
            )
        message += "For more details, visit our website: " + CLUB_WEBSITE
        send_message(message, chat)
    else:
        send_message("No past events.", chat)


def echo_all(updates):
    for update in updates["result"]:
        if update.get("message") != None:
            if update.get("message", {}).get("text") != None:
                text = update["message"]["text"]
                chat = update["message"]["chat"]["id"]
                if text == "/start":
                    start(chat)
                elif text == "/help":
                    help(chat)
                elif text == "/about":
                    about(chat)
                elif text == "/discord":
                    discord(chat)
                elif text == "/contact":
                    contact(chat)
                elif text == "/upcoming_events":
                    upcoming_events(chat)
                elif text == "/google":
                    google_contest(chat)
                elif text == "/codeforces":
                    codeforces_contest(chat)
                elif text == "/codechef":
                    codechef_contest(chat)
                elif text == "/faq":
                    faq(chat)
                elif text.startswith("/answer/"):
                    answers(text, chat)
                elif text == "/club_heads":
                    club_heads(chat)
                elif text == "/upcoming_events":
                    upcoming_events(chat)
                elif text == "/past_events":
                    past_events(chat)
                else:
                    send_message(
                        "I don't understand you. Type /help to see what I can do for you.",
                        chat,
                    )


def send_message(text, chat_id):
    tot = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(tot, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if updates is not None:
            if len(updates["result"]) > 0:
                last_update_id = get_last_update_id(updates) + 1
                echo_all(updates)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
