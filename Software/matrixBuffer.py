# framebuffer is an instance of frameBuf
def setByteArray(framebuffer, allCharacters):
    yMax = len(allCharacters)
    if yMax == 0:
        return
    for y in range(yMax):
        for x in range(len(allCharacters[y])):
            framebuffer.pixel(x, y, allCharacters[y][x])


if __name__ == "__main__":
    None
