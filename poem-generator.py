from dotenv import load_dotenv
import os
import requests
import streamlit as st

load_dotenv()
st.title(':shamrock: :green[Leprechaun name generator] :shamrock:')

def generate_image(model, name, fav_food, fav_drink, fav_movie, fav_sport):
    account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    api_token = os.environ["CLOUDFLARE_API_TOKEN"]
    headers = {
        "Authorization": f"Bearer {api_token}",
    }
    url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
    prompt = f"""You are a celebrity artist known for making pictures of celebrities as leprechauns. 
    Generate an image of {name} as a leprechaun who is eating {fav_food} and drinking {fav_drink} with equipment from {fav_sport}
    """
    response = requests.post(
        url,
        headers=headers,
        json={"prompt": prompt},
    )
    st.image(response.content, caption=f"Personalized leprechaun image for {name}")
with st.form("poem_generator"):
    # All models at https://developers.cloudflare.com/workers-ai/models/
    model = st.selectbox(
        ":green[Choose your text generation model]",
        options=(
            "@cf/meta/llama-2-7b-chat-fp16",
            "@cf/meta/llama-2-7b-chat-int8",
            "@cf/mistral/mistral-7b-instruct-v0.1",
            "@cf/tiiuae/falcon-7b-instruct",
            "@hf/thebloke/llama-2-13b-chat-awq",
            "@hf/thebloke/llamaguard-7b-awq",
            "@hf/thebloke/mistral-7b-instruct-v0.1-awq",
            "@hf/thebloke/neural-chat-7b-v3-1-awq",
            "@cf/openchat/openchat-3.5-0106",
            "@hf/thebloke/openhermes-2.5-mistral-7b-awq",
            "@cf/microsoft/phi-2",
            "@cf/qwen/qwen1.5-0.5b-chat",
            "@cf/qwen/qwen1.5-1.8b-chat",
            "@cf/qwen/qwen1.5-14b-chat-awq",
            "@cf/qwen/qwen1.5-7b-chat-awq",
            "@cf/defog/sqlcoder-7b-2",
            "@cf/tinyllama/tinyllama-1.1b-chat-v1.0",
            "@hf/thebloke/zephyr-7b-beta-awq"
        ),
    )
    name = st.text_input(":green[What is your name?]")
    fav_food = st.text_input(":green[What is your favorite food?]")
    fav_drink = st.text_input(":green[What is your favorite drink?]")
    fav_movie = st.text_input(":green[What is your favorite movie?]")
    fav_sport = st.text_input(":green[What is your favorite sport?]")
    prompt = f"""You are a professional at naming leprechauns. Some examples include:
    Silly names: Dandy Tiddlywink, Charm McLuck, Clover McTwinkle, Clover O'Clever, Paddy Shamrock, Ginger Fancypants, Pipping O'Rainbow, Tricky Shenanigan
    Whimsical names: Alby, Apple, Aodh, Baloobas, Bajaxed, Bailey, Biddy, Big Nose
    Lucky names: A combination of the first initial of your first name and the month you were born
    Other names: Padraig, Rónán, The burner/ The Ravager, Rezihp 
    Give {name} a leprechaun name based on their interests: 
    {fav_food}, {fav_drink}, {fav_movie}, {fav_sport}
    Return only the name and no other text.
    """
    submitted = st.form_submit_button("Generate")
    if submitted:
        account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
        api_token = os.environ["CLOUDFLARE_API_TOKEN"]
        headers = {
            "Authorization": f"Bearer {api_token}",
        }
        with st.spinner("Generating..."):
            url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
            response = requests.post(
                url,
                headers={"Authorization": f"Bearer {api_token}"},
                json={
                    "messages": [
                        {"role": "system", "content": "You are a friendly assistant"},
                        {"role": "user", "content": prompt}
                    ]
                }
            )   
            json = response.json()
            result = json["result"]
            st.write(result['response'])
            generate_image("@cf/lykon/dreamshaper-8-lcm", name, fav_food, fav_drink, fav_movie, fav_sport)

st.write("Made with Cloudflare AI")