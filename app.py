import gspread
from google.oauth2.service_account import Credentials
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# מזהה הגיליון שלך:
SPREADSHEET_ID = "1hndqlzttaMkJAnfm7WbmpToG2LhBsol3EZMgHOrBC1Q"
SHEET_NAME = "coupons"  # ודאי שזה שם הגיליון שלך

app = Flask(__name__)
CORS(app)

# התחברות לחשבון השירות
creds = Credentials.from_service_account_file(
    "/etc/secrets/credentials.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)

@app.route("/")
def home():
    return "🎉 Coupon API is running and ready to go!"


@app.route("/coupons", methods=["GET"])
def get_coupons():
    data = sheet.get_all_records()
    return jsonify(data)

@app.route("/coupons", methods=["POST"])
def add_coupon():
    new_coupon = request.json
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheet.append_row([
        new_coupon["name"],
        new_coupon["discountPercent"],
        new_coupon["amount"],
        ",".join(new_coupon["stores"]),
        new_coupon["code"],
        new_coupon["expiry"],
        new_coupon["owner"],
        new_coupon["owner"],
        now
    ])
    return jsonify({"status": "success"})

@app.route("/coupons/<int:row_index>", methods=["PUT"])
def update_coupon(row_index):
    updated_coupon = request.json
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sheet.update(f"A{row_index+2}:I{row_index+2}", [[
        updated_coupon["name"],
        updated_coupon["discountPercent"],
        updated_coupon["amount"],
        ",".join(updated_coupon["stores"]),
        updated_coupon["code"],
        updated_coupon["expiry"],
        updated_coupon["owner"],
        updated_coupon["owner"],
        now
    ]])
    return jsonify({"status": "updated"})


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # ← Render מגדיר את PORT כמשתנה סביבה
    app.run(host='0.0.0.0', port=port)

