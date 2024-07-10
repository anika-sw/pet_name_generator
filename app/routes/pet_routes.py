from flask import Blueprint, jsonify, request, abort, make_response
from ..db import db
from ..models.pet import Pet
from openai import OpenAI

client = OpenAI()

bp = Blueprint("pets", __name__, url_prefix="/pets")

@bp.post("")
def add_pets():

    request_body = request.get_json()
    try: 
        new_pet = Pet(
            name = generate_pet_name(request_body),
            animal_type = request_body["animal type"],
            personality = request_body["personality"],
            color = request_body["coloring"]
        )

        db.session.add(new_pet)
        db.session.commit()

        return make_response("New pet created", 201)
    
    except KeyError as e:
        abort(make_response({"message": f"missing required value: {e}"}, 400))

# helper function
def generate_pet_name(new_pet):
    prompt = f"I am creating a library of various pets and I need help naming them! \
        I have one pet that is a {new_pet['coloring']} {new_pet['animal type']} \
        with a {new_pet['personality']} personalitly. Please generate \
        a name that would suit this special animal!"

    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "user", "content": prompt}
        ]
    )

    return(completion.choices[0].message.content)