def link_class_classifier(value, classes):
    if value > 0:
        retVal = classes[0]
    elif value < 0:
        retVal = classes[1]
    else:
        retVal = classes[2]

    return retVal