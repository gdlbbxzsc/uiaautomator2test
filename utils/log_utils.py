is_debug_print = True


def logd(content):
    if not is_debug_print:
        return
        pass
    print(content)
    pass


def loge(content):
    print(content)
    pass
