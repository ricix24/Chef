import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Initialize the Google API
google_api_key = st.secrets["GOOGLE_API_KEY"]
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=google_api_key)

# Define prompts and responses
menu = {
    "Appetizers": {"Spring Rolls": 50, "Garlic Bread": 80},
    "Main Courses": {"Grilled Chicken": 150, "Pasta Alfredo": 120},
    "Desserts": {"Chocolate Cake": 40, "Ice Cream": 45},
}

events = [
    {"name": "Folk Lore Show", "date": "Every Friday at 7 PM"},
    {"name": "Cooking Class", "date": "Every Saturday at 5 PM"},
]

offers = [
    {"description": "10% off on all orders above $50", "validity": "Till 31st December"}
]

# Define a template for handling inquiries
template = """
You are a customer support bot for "The Chef Story". You should be friendly and helpful.

{context}

User: {user_input}
Bot: 
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "user_input"]
)

# Streamlit interface
st.title("The Chef Story - Customer Support Bot")

# Initialize session state for conversation
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_input("You: ", "")

def get_menu():
    menu_text = "Here's our menu:\n"
    for category, items in menu.items():
        menu_text += f"\n{category}:\n"
        for item, price in items.items():
            menu_text += f" - {item}: ₹{price:.2f}\n"
    return menu_text

def get_events():
    events_text = "Here are our upcoming events:\n"
    for event in events:
        events_text += f" - {event['name']} on {event['date']}\n"
    return events_text

def get_offers():
    offers_text = "Current offers:\n"
    for offer in offers:
        offers_text += f" - {offer['description']} (valid till {offer['validity']})\n"
    return offers_text

def handle_inquiry(user_input):
    if "menu" in user_input.lower():
        return get_menu()
    elif "price" in user_input.lower():
        return get_menu()  # Assuming menu function includes prices
    elif "special" in user_input.lower():
        return "Today's special is Grilled Salmon for $15.99."
    elif "vegan" in user_input.lower() or "vegetarian" in user_input.lower():
        return "We offer several vegan/vegetarian options, including Vegan Burger and Vegetable Stir Fry."
    elif "combo" in user_input.lower():
        return "Our combo meals start at $10.99."
    elif "dessert" in user_input.lower():
        return get_menu()  # Assuming menu function includes desserts
    elif "best-selling" in user_input.lower():
        return "Our best-selling dishes are Grilled Chicken and Pasta Alfredo."
    elif "kid" in user_input.lower():
        return "Yes, we offer kids' meals including Chicken Nuggets and Mini Burgers."
    elif "customize" in user_input.lower():
        return "Yes, you can customize your order. Please specify your preferences."
    elif "drink" in user_input.lower():
        return "We offer a variety of drinks including soda, juices, and cocktails."
    elif "happy hour" in user_input.lower():
        return "Our happy hour is from 5 PM to 7 PM with special discounts on drinks."
    elif "weekend offer" in user_input.lower():
        return "We have special weekend offers with 20% off on all family meals."
    elif "family meal" in user_input.lower():
        return "Our family meal packages start at $29.99."
    elif "low-calorie" in user_input.lower():
        return "We offer several low-calorie options like Grilled Chicken Salad and Quinoa Bowl."
    elif "tour" in user_input.lower():
        return "Sure, we can arrange a tour of our facility. Please visit our reception."
    elif "food festival" in user_input.lower():
        return "Yes, we have an upcoming food festival on the first weekend of next month."
    elif "cooking class" in user_input.lower():
        return "We host cooking classes every Saturday at 5 PM."
    elif "schedule" in user_input.lower():
        return get_events()
    elif "loyalty program" in user_input.lower():
        return "Yes, we have a loyalty program for frequent visitors. Please ask our staff for details."
    elif "book table" in user_input.lower():
        return "You can book a table for an event online through our website."
    elif "theme night" in user_input.lower():
        return "Yes, we have themed nights every Wednesday."
    elif "duration" in user_input.lower():
        return "The Folk Lore show lasts for about 1 hour."
    elif "kid-friendly" in user_input.lower():
        return "Yes, our shows are kid-friendly."
    elif "participate" in user_input.lower():
        return "Yes, you can participate in our shows and events. Please ask our staff for details."
    elif "play area" in user_input.lower():
        return "Yes, we have a kid's play area."
    elif "pre-order" in user_input.lower():
        return "Yes, you can pre-order meals for a specific time. Please visit our website."
    elif "discount" in user_input.lower():
        return "Yes, we offer discounts for large group bookings. Please contact our staff for details."
    elif "wheelchair accessible" in user_input.lower():
        return "Yes, our restaurant is wheelchair accessible."
    elif "digital payment" in user_input.lower():
        return "Yes, we accept digital payments like Apple Pay and Google Pay."
    elif "reset password" in user_input.lower():
        return "You can reset your password on our website by clicking 'Forgot Password'."
    elif "track delivery" in user_input.lower():
        return "Yes, you can track your delivery order online through our website."
    elif "gift card" in user_input.lower():
        return "Yes, we offer online gift cards. Please visit our website."
    elif "change delivery address" in user_input.lower():
        return "You can change your delivery address on our website under 'My Account'."
    elif "cancel order" in user_input.lower():
        return "Yes, you can cancel your order online through our website."
    elif "delete account" in user_input.lower():
        return "You can delete your account on our website under 'Account Settings'."
    elif "online chat support" in user_input.lower():
        return "Yes, we have an online chat support available on our website."
    elif "social media" in user_input.lower():
        return "You can contact us through our social media channels listed on our website."
    elif "customer reviews" in user_input.lower():
        return "Yes, you can see customer reviews on our website."
    elif "update profile" in user_input.lower():
        return "You can update your profile information on our website under 'My Account'."
    else:
        context = "You are interacting with a customer on the website of 'The Chef Story'."
        prompt_text = prompt.format(context=context, user_input=user_input)
        answers = llm.invoke(prompt_text)
        return answers.content

if user_input:
    bot_response = handle_inquiry(user_input)
    st.session_state.conversation.append((user_input, bot_response))
    user_input = ""


# Display the most recent conversation
if st.session_state.conversation:
    user, bot = st.session_state.conversation[-1]
    st.text_area("User: ", value=user, height=50, max_chars=None, key="user")
    st.text_area("Bot: ", value=bot, height=50, max_chars=None, key="bot")
    
# # Display the conversation
# for i, (user, bot) in enumerate(st.session_state.conversation):
#     st.text_area(f"User {i+1}: ", value=user, height=50, max_chars=None, key=f"user_{i}")
#     st.text_area(f"Bot {i+1}: ", value=bot, height=50, max_chars=None, key=f"bot_{i}")
