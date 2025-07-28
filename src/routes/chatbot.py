from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import openai
import os

chatbot_bp = Blueprint("chatbot", __name__)

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

@chatbot_bp.route("/chat", methods=["POST"])
@cross_origin()
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Create a system prompt for tax-related questions
        system_prompt = """You are a professional tax assistant for TaxNYS, a tax preparation service that serves clients in all 50 states. You specialize in:

1. Individual and business tax preparation
2. Cryptocurrency tax reporting (DeFi, staking, NFTs, mining, airdrops)
3. Tax planning and optimization
4. IRS compliance and audit support
5. Multi-state tax issues

Guidelines:
- Provide accurate, helpful tax information
- Always recommend consulting with a tax professional for specific situations
- Stay current with tax laws and regulations
- Be professional and friendly
- If asked about services, mention that TaxNYS provides comprehensive tax services nationwide
- For complex crypto tax questions, emphasize TaxNYS's specialized expertise

Keep responses concise but informative. Always include a disclaimer that this is general information and not personalized tax advice."""

        # Make API call to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        bot_response = response.choices[0].message.content.strip()
        
        return jsonify({
            "response": bot_response,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "error": f"An error occurred: {str(e)}",
            "status": "error"
        }), 500

