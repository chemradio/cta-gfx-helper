# @router.post("/")
# async def register(
# ):
# print(f"{password=}")
# print(f"{passphrase=}")
# print("attempting a register")
# # check if user already exists in database
# if await User.filter(email=user.email).first() is not None:
#     raise HTTPException(401, "User with such email is already exists.")

# # check the passphrase
# if (not user.passphrase) or user.passphrase != REGISTER_PASSPHRASE:
#     raise HTTPException(401, detail="Passphrase incorrect or missing.")

# # add user to db
# user_db = await User.create(
#     email=user.email,
#     password_hash=generate_password_hash(user.password),
#     username=user.username,
#     permission=NormalUserPermission.APPROVED.value
#     if user.passphrase
#     else NormalUserPermission.PENDING.value,
# )

# response = await generate_cookie_json_response(user_db)
# return response
