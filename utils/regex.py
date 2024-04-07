isValidName = r"^[a-zA-Z0-9_ ]{1,32}$"

isObjectId = r"^[0-9a-fA-F]{24}$"
isUsername = r"^[a-zA-Z0-9_]{3,32}$"
isEmail = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
isPassword = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
isJWT = r"^[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+$"
