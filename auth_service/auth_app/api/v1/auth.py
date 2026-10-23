from flask_jwt_extended.exceptions import JWTDecodeError, InvalidTokenError

@app.route('/tokens/validate', methods=['GET'])
def validate_token():
    try:
        verify_jwt_in_request()
        return send_result(message='Token valid')
    except JWTDecodeError as e:
        current_app.logger.error(f"JWT Decode Error: {e}")
        return jsonify({"message": str(e)}), 401
    except Exception as e:
        current_app.logger.error(f"Unexpected Error: {e}")
        return jsonify({"message": str(e)}), 500