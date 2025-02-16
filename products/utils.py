

def set_attributes(instance, data, exclude=[]):
    for key in data:
        if key in exclude:
            continue
        value = data.get(key)
        if value is not None:
            setattr(instance, key, value)
            

            
            
    