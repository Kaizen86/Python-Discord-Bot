from discord import File

def isWholeWordInString(sentence,searchterm):
    try:
        x = sentence.index(searchterm)
        return True
    except: return False

async def main(globaldata):
    message = globaldata["message"]
    userData = globaldata["userData"]
    core_files_foldername = globaldata["core_files_foldername"]

    #react to certain phrases
    msg_lowercase = message.content.lower()
    if isWholeWordInString(msg_lowercase, "meep"):
        await message.channel.send("Meep")
        userData.set_user_data(message.author.id,"meeps",int(userData.get_user_data(message.author.id,"meeps"))+1)

    if isWholeWordInString(msg_lowercase, "wheatley") and isWholeWordInString(msg_lowercase, "moron"): #message must have the words "wheatley" and "moron" to count.
        await message.channel.send("I AM NOT A MORON!")

    if isWholeWordInString(msg_lowercase, "the more you know"):
        await message.channel.send(file=File(core_files_foldername+"/images/moreyouknow.gif", filename="img.png"))
