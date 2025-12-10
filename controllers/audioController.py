from flask import Blueprint, request, jsonify, send_file
from gtts import gTTS
from models.database import Session
from models.models import Shipment
from pathlib import Path

audio_bp = Blueprint("audio", __name__)

@audio_bp.route("/api/save_audio", methods=["GET"])
def save_audio():
    shipment_id = request.args.get("shipment_id")
    if shipment_id is None:
        return {"error": "shipment_id parameter missing"}, 400
    shipment_id = int(shipment_id)

    audio_folder = Path(r"C:\Users\USER098\Documents\GitHub\MobileApplicationsLessions\static\audio")
    audio_folder.mkdir(parents=True, exist_ok=True)  # tworzy folder jeśli nie istnieje

    with Session() as session:
        shipment = session.query(Shipment).filter_by(id=shipment_id).first()
        if not shipment:
            return {"error": "Shipment not found"}, 404

        text_to_read = f"{shipment.message_target}"

        # nazwa pliku
        file_name = f"shipment_audio.mp3"
        file_path = audio_folder / file_name

        # zapis pliku na dysku
        tts = gTTS(text=text_to_read, lang='pl')
        tts.save(str(file_path))

    # zwracamy link do pliku, żeby frontend mógł go odtworzyć
    return jsonify({"audio_url": f"/static/audio/{file_name}"})
