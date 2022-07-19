def arxiveTemplate(src = list):
    auth = ""
    for i in src[4]:
        auth = i + ", "
    auth = auth[0:-2]
    src[2][0] = src[2][0].replace('\n','')
    text = f"""
    📄 {src[0][6:]} \n {src[1]}\n\n 🔵 Abstract:{src[2][0][9:]}\n \n 📌 {src[5]}\n 👤 {auth} \n\n ----\n @UTPhysicsArticles
    """
    text = u"{0}".format(text)
    return text